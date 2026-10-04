import re
import unicodedata

def normalize(text):
  text = unicodedata.normalize('NFKC', text)
  text = text.casefold()
  text = text.replace("’", "'").replace("‘", "'")
  text = text.replace("“", '"').replace("”", '"')
  text = text.replace("—", "-").replace("–", "-")
  text = re.sub(r"\s+", " ", text).strip()
  return text

def quote_in_text(text, quote):
  normalized_text = normalize(text)
  normalized_quote = normalize(quote)
  if normalized_quote == "":
    return False
  if '...' in normalized_quote:
    pieces = normalized_quote.split("...")
    pieces = [piece.strip() for piece in pieces]
    if any(piece == "" for piece in pieces):
      return False
    position = 0
    for piece in pieces:
        position = normalized_text.find(piece, position)
        if position == -1:
            return False
        position += len(piece)
    return True
  if normalized_quote in normalized_text:
    return True

  