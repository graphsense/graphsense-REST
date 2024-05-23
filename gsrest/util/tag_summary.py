from collections import Counter
import re
from openapi_server.models.tag_summary import TagSummary
from openapi_server.models.tag_cloud_entry import TagCloudEntry

filter_words = {
    w: True for w in ["to", "in", "the", "by", "of", "at", ""]
}

def map_concept_to_broad_concept(concept) -> str:
    if concept == "exchange":
        return concept
    else:   
        return "entity"

def normalizeWord(istr: str) -> str:
    return re.sub(r'[^0-9a-zA-Z_ ]+', '', istr.strip().lower())

def skipTag(t) -> bool:
    return t.label == "dark web" and t.confidence == "web_crawl" and t.category == None

async def get_tag_summary(get_tags_page_fn, label_words_max_items = 30, label_max_items = 30):
    nextpage="start"
    tags_count = 0
    total_words = 0
    actor_counter = Counter()
    label_word_counter = Counter()
    full_label_counter = Counter()
    concepts_counter = Counter()

    while nextpage is not None:
        if nextpage == "start":
            nextpage = None

        # get tags
        tags = await get_tags_page_fn(page=nextpage)
        tags_count += len(tags.address_tags)

        for t in tags.address_tags:
           if not skipTag(t):

            # compute words
            norm_words = [normalizeWord(w) for w in t.label.split(" ")]
            filtered_words = [w for w in norm_words if w not in filter_words]
            total_words += len(filtered_words)

            # add words
            label_word_counter.update(Counter(filtered_words))

            # add labels
            full_label_counter.update([normalizeWord(t.label)])
            
            # add actor
            if t.actor:
                actor_counter.update([t.actor])
            
            if t.category and not t.concepts:
                concepts_counter.update([t.category])

            elif t.concepts:
                concepts_counter.update(t.concepts)

        nextpage = tags.next_page

    # get most common actor
    p_actor = None
    actor_mc = actor_counter.most_common(1)
    if len(actor_mc) > 0:
        p_actor = actor_mc[0][0]

    # get best label
    best_label = None
    if len(full_label_counter) > 0:
        best_label = full_label_counter.most_common(1)[0][0].capitalize()

    # get broad category
    broad_category = None
    if len(concepts_counter) > 0:
        broad_category = map_concept_to_broad_concept(concepts_counter.most_common(1)[0][0])
    
    return TagSummary(broad_category=broad_category
                      , tag_count=tags_count
                      , best_actor=p_actor
                      , best_label=best_label
                      , label_words_tag_cloud={word: TagCloudEntry(cnt=cnt, weighted=cnt / total_words) for word, cnt in label_word_counter.most_common(label_words_max_items)}
                      , label_tag_cloud={word: TagCloudEntry(cnt=cnt, weighted=cnt / tags_count) for word, cnt in full_label_counter.most_common(label_max_items)}
                      , concept_tag_cloud={word: TagCloudEntry(cnt=cnt, weighted=cnt / tags_count) for word, cnt in concepts_counter.most_common()}
                      , actors_tag_cloud={word: TagCloudEntry(cnt=cnt, weighted=cnt / tags_count) for word, cnt in actor_counter.most_common()})