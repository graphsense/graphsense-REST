from collections import Counter, defaultdict
import re
from openapi_server.models.tag_summary import TagSummary
from openapi_server.models.tag_cloud_entry import TagCloudEntry
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


filter_words = {w: True for w in ["to", "in", "the", "by", "of", "at", ""]}


def map_concept_to_broad_concept(concept) -> str:
    if concept == "exchange":
        return concept
    else:
        return "entity"


def normalizeWord(istr: str) -> str:
    return re.sub(r'[^0-9a-zA-Z_ ]+', ' ', istr.strip().lower())


def skipTag(t) -> bool:
    return (t.label == "dark web" and t.confidence == "web_crawl"
            and t.category is None)


def calcTagCloud(wctr: wCounter, at_most=None) -> Dict[str, TagCloudEntry]:
    total_weight = wctr.get_total(weighted=True)
    return {
        word: TagCloudEntry(cnt=wctr.get(word), weighted=cnt / total_weight)
        for word, cnt in wctr.most_common(n=at_most, weighted=True)
    }


async def get_tag_summary(get_tags_page_fn,
                          label_words_max_items=30,
                          label_max_items=30):
    nextpage = "start"
    tags_count = 0
    total_words = 0
    actor_counter = wCounter()
    label_word_counter = wCounter()
    full_label_counter = wCounter()
    concepts_counter = wCounter()
    actor_lables = defaultdict(wCounter)

    while nextpage is not None:
        if nextpage == "start":
            nextpage = None

        # get tags
        tags = await get_tags_page_fn(page=nextpage)

        for t in tags.address_tags:
            if not skipTag(t):

                conf = t.confidence_level or 1

                tags_count += 1

                # compute words
                norm_words = [normalizeWord(w) for w in normalizeWord(t.label).split(" ")]
                filtered_words = [
                    w for w in norm_words if w not in filter_words
                ]
                total_words += len(filtered_words)

                # add words
                label_word_counter.update(Counter(filtered_words))

                # add labels
                full_label_counter.add(normalizeWord(t.label), conf)

                # add actor
                if t.actor:
                    actor_lables[t.actor].add(t.actor, weight=conf)
                    actor_counter.add(t.actor, weight=conf)

                if t.category and not t.concepts:
                    concepts_counter.add(t.category, weight=conf)

                elif t.concepts:
                    for x in t.concepts:
                        concepts_counter.add(x, weight=conf)

        nextpage = tags.next_page

    # get most common actor (weighted by tag confidence)
    # get best label (within actor if actor is specified)
    p_actor = None
    best_label = None
    actor_mc = actor_counter.most_common(1, weighted=True)
    if len(actor_mc) > 0:
        p_actor = actor_mc[0][0]
        best_label = actor_lables[p_actor].most_common(1, weighted=True)[0][0].capitalize()
    else:
        if len(full_label_counter) > 0:
            best_label = full_label_counter.most_common(
                1, weighted=True)[0][0].capitalize()

    # get broad category
    broad_category = "user"
    if len(concepts_counter) > 0:
        broad_category = map_concept_to_broad_concept(
            concepts_counter.most_common(1, weighted=True)[0][0])

    return TagSummary(
        broad_category=broad_category,
        tag_count=tags_count,
        best_actor=p_actor,
        best_label=best_label,
        label_words_tag_cloud=calcTagCloud(label_word_counter,
                                           at_most=label_words_max_items),
        label_tag_cloud=calcTagCloud(full_label_counter),
        concept_tag_cloud=calcTagCloud(concepts_counter),
        actors_tag_cloud=calcTagCloud(actor_counter),
    )
