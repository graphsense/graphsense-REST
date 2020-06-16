from gsrest.util.tag_coherence import compute_tag_coherence


def test_compute_tag_coherence():
    tags = []
    assert compute_tag_coherence(tags) is None

    def to_tags(labels):
        return [{'label': label} for label in labels]

    tags = to_tags(['foo'])
    assert compute_tag_coherence(tags) == 1

    tags = to_tags(['foo', 'foo'])
    assert compute_tag_coherence(tags) == 1

    tags = to_tags(['foo', 'foo', 'foo'])
    assert compute_tag_coherence(tags) == 1

    tags = to_tags(['foo', 'bar'])
    assert compute_tag_coherence(tags) == 0

    tags = to_tags(['foo', 'bar', '42'])
    assert compute_tag_coherence(tags) == 0

    tags = to_tags(['foo', 'foobar'])
    assert round(compute_tag_coherence(tags), 3) == 0.667

    tags = to_tags(['tide', 'diet'])
    assert round(compute_tag_coherence(tags), 3) == 0.375

    tags = to_tags(['foo', 'foo', 'bar'])
    assert compute_tag_coherence(tags) == 0.5

    tags = to_tags(['foo', 'foo', 'foo', 'bar'])
    assert compute_tag_coherence(tags) == 0.75

    tags = to_tags(['foo', 'foo', 'foo', 'foo', 'bar'])
    assert round(compute_tag_coherence(tags), 3) == 0.857

    tags = to_tags(['tide', 'tide', 'diet'])
    assert round(compute_tag_coherence(tags), 3) == 0.688
