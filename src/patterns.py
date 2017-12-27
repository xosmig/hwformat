COMMENT_OPEN = r"/\*"
COMMENT_CLOSE = r"\*/"
RUS_WORD = "([ ]?[-\(]*[а-яА-ЯёЁ]+[\-:!\.,\)]*[ ]?)"
RANGE = r"\s*(.*?)\s*\.\.\s*(.*?)\s*"
# __div_operand__ = r"\s*((?>(?!\]\]|/)+|(?R))*)\s*"
__div_operand__ = "\s*((?>[^\[\]/]+|(?R))*)\s*"
DIVISION = r"\[\["+__div_operand__+r"/"+__div_operand__+r"\]\]"
DIVISION_BIG = r"\[\[!"+__div_operand__+r"/"+__div_operand__+r"\]\]"

