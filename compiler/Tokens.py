from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    STRING = 0
    INT = 1
    FLOAT = 2
    LPAREN = 3
    RPAREN = 4
    BUILTIN = 5
    LCURLY = 6
    RCURLY = 7
    LBRACKET = 8
    RBRACKET = 9
    PERIOD = 10
    HASHTAG = 11
    DQUOTE = 12
    SQUOTE = 13
    BACKSLASH = 14
    FORSLASH = 15
    OR = 16
    AND = 17
    EQUAL = 18
    FN = 19
    COMMA = 20
    PLUS = 21
    MINUS = 22
    MULTIPLY = 23
    DIVIDE = 24
    DASH = 25
    ISEQUAL = 26
    NOTEQUAL = 27
    ARRAY = 28
    EXCLAMATION = 29
    SEMI = 30


@dataclass
class Token:
    type: TokenType
    value: any = None

    def __repr__(self):
        return f"{self.type.name}" + (f":{self.value}" if self.value is not None else "")
