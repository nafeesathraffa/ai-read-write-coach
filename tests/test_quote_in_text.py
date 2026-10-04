from app.services.evidence import quote_in_text

def test_quote_matches_exactly():
    text = "I went to the store. Then I came home and cooked dinner."
    quote = "went to the store"
    assert quote_in_text(text, quote)

def test_quote_matches_ignoring_case():
    text = "I went to the store. Then I came home and cooked dinner."
    quote = "WENT TO THE STORE"
    assert quote_in_text(text, quote)

def test_quote_elipse_check():
    text = "I went to the store. Then I came home and cooked dinner."
    quote = "went to the store ... came home"
    assert quote_in_text(text, quote)

def test_quote_order_check():
    text = "I went to the store. Then I came home and cooked dinner."
    quote = "came home ... went to the store"
    assert not quote_in_text(text, quote)

def test_quote_sentence_check():
    text = "I went to the store. Then I came home and cooked dinner."
    quote = "I love pineapple"
    assert not quote_in_text(text, quote)  

def test_quote_empty_check():
    text = "I went to the store. Then I came home and cooked dinner."
    quote = ""
    assert not quote_in_text(text, quote)           

def test_quote_leading_ellipses():
    text = "I went to the store. Then I came home and cooked dinner."
    quote = "...came home"
    assert not quote_in_text(text, quote)  

def test_quote_curly_apostrophe():
    text = "it’s fine"
    quote = "it's fine"
    assert quote_in_text(text, quote)     

   