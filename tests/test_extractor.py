# tests/test_extractor.py
from feature_extractor.extractor import extract_all
def test_extract():
    feats = extract_all("https://example.com")
    assert "url_length" in feats
