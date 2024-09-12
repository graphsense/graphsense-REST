from collections import Counter, defaultdict
import re
from openapi_server.models.tag_summary import TagSummary
from openapi_server.models.tag_cloud_entry import TagCloudEntry
from openapi_server.models.label_summary import LabelSummary
from typing import Dict


class wCounter:

    def __init__(self):
        self.wctr = Counter()
        self.ctr = Counter()

    def add(self, item, weight=1):
        self.ctr.update({item: 1})
        self.wctr.update({item: weight})

    def update(self, items):
        self.ctr.update(items)
        self.wctr.update(items)

    def getcntr(self, weighted=False):
        return self.wctr if weighted else self.ctr

    def get_total(self, weighted=False):
        return sum(dict(self.getcntr(weighted)).values())

    def get(self, item, weighted=False):
        return self.getcntr(weighted)[item]

    def most_common(self, n=None, weighted=False):
        return self.getcntr(weighted).most_common(n)

    def __len__(self):
        return len(self.ctr)


filter_words = {
    w: True
    for w in ["to", "in", "the", "by", "of", "at", "", "vault"]
}


def map_concept_to_broad_concept(concept) -> str:
    if concept == "exchange":
        return concept
    else:
        return "entity"


def remove_mulit_spaces(istr: str) -> str:
    return re.sub(' +', ' ', istr)


def normalizeWord(istr: str) -> str:
    return remove_mulit_spaces(
        re.sub(r'[^0-9a-zA-Z_ ]+', ' ',
               istr.strip().lower()))


def skipTag(t) -> bool:
    return False
    # return (t.label == "dark web" and t.confidence == "web_crawl"
    #         and t.category is None)


def calcTagCloud(wctr: wCounter, at_most=None) -> Dict[str, TagCloudEntry]:
    total_weight = wctr.get_total(weighted=True)
    return {
        word: TagCloudEntry(cnt=wctr.get(word), weighted=cnt / total_weight)
        for word, cnt in wctr.most_common(n=at_most, weighted=True)
    }


async def get_tag_summary(get_tags_page_fn,
                          label_words_max_items=30,
                          label_max_items=30,
                          additional_tags=[]):
    nextpage = "start"
    tags_count = 0
    total_words = 0
    actor_counter = wCounter()
    label_word_counter = wCounter()
    full_label_counter = wCounter()
    concepts_counter = wCounter()
    actor_lables = defaultdict(wCounter)
    label_summary = defaultdict(
        lambda: {
            "cnt": 0,
            "lbl": None,
            "src": set(),
            "sumConfidence": 0,
            "creators": set(),
            "concepts": set(),
            "lastmod": 0,
            "inherited": True
        })

    def add_tag_data(t, tags_count, total_words):
        if not skipTag(t):

            conf = t.confidence_level or 0.1

            tags_count += 1

            # compute words
            norm_words = [
                normalizeWord(w) for w in normalizeWord(t.label).split(" ")
            ]
            filtered_words = [w for w in norm_words if w not in filter_words]
            total_words += len(filtered_words)

            # add words
            label_word_counter.update(Counter(filtered_words))

            # add labels
            nlabel = normalizeWord(t.label)
            ls = label_summary[nlabel]
            full_label_counter.add(nlabel, conf)

            # add actor
            if t.actor:
                actor_lables[t.actor].add(t.actor, weight=conf)
                actor_counter.add(t.actor, weight=conf)

            if t.category and not t.concepts:
                concepts_counter.add(t.category, weight=conf)

                ls["concepts"].add(t.category)

            elif t.concepts:
                for x in t.concepts:
                    concepts_counter.add(x, weight=conf)

                    ls["concepts"].add(x)

            ls["cnt"] += 1
            ls["lbl"] = t.label
            ls["src"].add(t.source)
            ls["creators"].add(t.tagpack_creator)
            ls["sumConfidence"] += conf
            ls["lastmod"] = max(ls["lastmod"], t.lastmod)
            ls["inherited"] = t.inherited_from == "cluster" and (
                ls["inherited"])

        return tags_count, total_words

    for t in additional_tags:
        tags_count, total_words = add_tag_data(t, tags_count, total_words)

    while nextpage is not None:
        if nextpage == "start":
            nextpage = None

        # get tags
        tags = await get_tags_page_fn(page=nextpage)

        for t in tags.address_tags:
            tags_count, total_words = add_tag_data(t, tags_count, total_words)

        nextpage = tags.next_page

    # get most common actor (weighted by tag confidence)
    # get best label (within actor if actor is specified)
    p_actor = None
    best_label = None
    actor_mc = actor_counter.most_common(1, weighted=True)
    if len(actor_mc) > 0:
        p_actor = actor_mc[0][0]
        best_label = actor_lables[p_actor].most_common(
            1, weighted=True)[0][0].capitalize()
    else:
        if len(full_label_counter) > 0:
            best_label = full_label_counter.most_common(
                1, weighted=True)[0][0].capitalize()

    # get broad category
    broad_category = "user"
    if len(concepts_counter) > 0:
        broad_category = map_concept_to_broad_concept(
            concepts_counter.most_common(1, weighted=True)[0][0])

    # create a relevance score, prefer items where similar labels exist.
    sw_full_label_counter = wCounter()
    data = full_label_counter.most_common(weighted=True)
    for lbl, v in data:
        multiplier = sum([
            occurances
            for word, occurances in label_word_counter.most_common()
            if word in lbl and occurances > 1
        ])
        n = (1 + multiplier / total_words)
        sw_full_label_counter.add(lbl, v * n)

    ltc = calcTagCloud(sw_full_label_counter)

    return TagSummary(
        broad_category=broad_category,
        tag_count=tags_count,
        best_actor=p_actor,
        best_label=best_label,
        # label_tag_cloud=calcTagCloud(full_label_counter),
        concept_tag_cloud=calcTagCloud(concepts_counter),
        label_summary={
            key: LabelSummary(
                label=value["lbl"],
                count=value["cnt"],
                confidence=value["sumConfidence"] / (value["cnt"] * 100),
                relevance=ltc[key].weighted,
                creators=list(value["creators"]),
                sources=list(value["src"]),
                concepts=list(value['concepts']),
                lastmod=value["lastmod"],
                inherited_from="cluster" if value["inherited"] else None)
            for (key, value) in label_summary.items()
        })
