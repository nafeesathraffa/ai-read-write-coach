from app.services.evidence import normalize

def test_normalize_text():
  assert normalize("Hello, World!") == "hello, world!"
  assert normalize("  Hello   World  ") == "hello world"
  assert normalize("it’s") == "it's"
  assert normalize("a    b\n\tc") == "a b c"
  assert normalize("wait — what") == "wait - what"
  assert normalize("wait…") == "wait..."