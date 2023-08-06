from demo_it_analyze.nlp.ner import Entity, compute_ner


def test_ner_success():
    output = compute_ner("Cristiano Ronaldo non gioca nel Palermo")
    expected = [
        Entity(text="Cristiano Ronaldo", start=0, end=2, label="PER"),
        Entity(text="Palermo", start=5, end=6, label="LOC"),
    ]
    assert output == expected


def test_ner_empty():
    output = compute_ner("domani andiamo al lago")
    expected = []
    assert output == expected
