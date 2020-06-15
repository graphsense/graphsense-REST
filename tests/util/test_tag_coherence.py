from gsrest.util.tag_coherence import compute_tag_coherence


def test_compute_tag_coherence(client, auth, monkeypatch):
    tags = []
    assert compute_tag_coherence(tags) is None

    def toTags(labels):
        return [{'label': label} for label in labels]

    tags = toTags(['foo'])
    assert compute_tag_coherence(tags) == 1

    tags = toTags(['foo', 'foo'])
    assert compute_tag_coherence(tags) == 1

    tags = toTags(['foo', 'foo', 'foo'])
    assert compute_tag_coherence(tags) == 1

    tags = toTags(['foo', 'bar'])
    assert compute_tag_coherence(tags) == 0

    tags = toTags(['foo', 'bar', '42'])
    assert compute_tag_coherence(tags) == 0

    tags = toTags(['foo', 'foobar'])
    assert round(compute_tag_coherence(tags), 3) == 0.667

    tags = toTags(['tide', 'diet'])
    assert round(compute_tag_coherence(tags), 3) == 0.375

    tags = toTags(['foo', 'foo', 'bar'])
    assert compute_tag_coherence(tags) == 0.5

    tags = toTags(['foo', 'foo', 'foo', 'bar'])
    assert compute_tag_coherence(tags) == 0.75

    tags = toTags(['foo', 'foo', 'foo', 'foo', 'bar'])
    assert round(compute_tag_coherence(tags), 3) == 0.857

    tags = toTags(['tide', 'tide', 'diet'])
    assert round(compute_tag_coherence(tags), 3) \
        == 0.688
