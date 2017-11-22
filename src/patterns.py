NON_MATH_OPEN = r"\[\{"
NON_MATH_CLOSE = r"\}\]"
COMMENT_OPEN = r"/\*"
COMMENT_CLOSE = r"\*/"
# ~^{text} --> \widetile{text} (~ over the text)
TILDE_OVER = r"~\^"
# -^{text} --> \overline{text}
OVERLINE = r"\-\^"
RUS_WORD = "([ ]?[-\(]*[а-яА-ЯёЁ]+[\-:!\.,\)]*[ ]?)"
RANGE = r"\s*(.*?)\s*\.\.\s*(.*?)\s*"
# __div_operand__ = r"\s*((?>(?!\]\]|/)+|(?R))*)\s*"
__div_operand__ = "\s*((?>[^\[\]/]+|(?R))*)\s*"
DIVISION = r"\[\["+__div_operand__+r"/"+__div_operand__+r"\]\]"

