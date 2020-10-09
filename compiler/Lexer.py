from compiler.Tokens import TokenType, Token

WHITESPACE = " \t\n"

mainfuncs = ["for",
             "while",
             "if",
             "elif",
             "else",
             "fn"]

types = ["int",
         "float",
         "string",
         "char",
         "array",
         "object"]

DIGITS = "0123456789"


class Lexer:
    def __init__(self, text):
        self.text = iter(text)
        self.advance()

    def advance(self):
        try:
            self.current_char = next(self.text)
        except StopIteration:
            self.current_char = None

    def generate_tokens(self):
        while self.current_char != None:
            if self.current_char in WHITESPACE:
                self.advance()
            elif self.current_char == "'":
                self.advance()
                yield Token(TokenType.SQUOTE)
                yield Token(TokenType.STRING, self.generate_string(False))
                if self.current_char == "'":
                    yield Token(TokenType.SQUOTE)
                else:
                    print("CharError: Expected end of string")
                    exit(1)
                self.advance()
            elif self.current_char == "|":
                self.advance()
                yield TokenType(TokenType.OR)
            elif self.current_char == '"':
                self.advance()
                yield Token(TokenType.DQUOTE)
                yield Token(TokenType.STRING, self.generate_string(True))
                if self.current_char == "\"":
                    yield Token(TokenType.DQUOTE)
                else:
                    print("StringError: Expected end of string")
                    exit(1)
                self.advance()
            elif self.current_char == "&":
                self.advance()
                yield Token(TokenType.AND)
            elif self.current_char == "(":
                self.advance()
                yield Token(TokenType.LPAREN)
            elif self.current_char == ")":
                self.advance()
                yield Token(TokenType.RPAREN)
            elif self.current_char == "=":
                self.advance()
                if self.current_char == "=":
                    yield Token(TokenType.ISEQUAL)
                else:
                    yield Token(TokenType.EQUAL)
                self.advance()
            elif self.current_char == "\\":
                self.advance()
                yield Token(TokenType.BACKSLASH)
            elif self.current_char == "/":
                self.advance()
                if self.current_char == "/":
                    self.generate_message_newline()
                elif self.current_char == "*":
                    self.generate_message()
                else:
                    yield Token(TokenType.FORSLASH)
            elif self.current_char == "//":
                self.advance()
                if self.current_char == "/":
                    self.generate_message_newline()
                else:
                    self.generate_message()
            elif self.current_char == ".":
                self.advance()
                yield Token(TokenType.PERIOD)
            elif self.current_char == "[":
                self.advance()
                yield Token(TokenType.LBRACKET)
            elif self.current_char == "]":
                self.advance()
                yield Token(TokenType.RBRACKET)
            elif self.current_char == "{":
                self.advance()
                yield Token(TokenType.LCURLY)
            elif self.current_char == "}":
                self.advance()
                yield Token(TokenType.RCURLY)
            elif self.current_char == ",":
                self.advance()
                yield Token(TokenType.COMMA)
            elif self.current_char == "+":
                self.advance()
                yield Token(TokenType.PLUS)
            elif self.current_char == "!":
                self.advance()
                if self.current_char == "=":
                    yield Token(TokenType.NOTEQUAL)
                    self.advance()
                elif self.current_char == "/":
                    yield Token(TokenType.NOTIN)
                    self.advance()
                else:
                    yield Token(TokenType.EXCLAMATION)
            elif self.current_char in DIGITS:
                a = self.generate_float(eadvan=" ")
                if a:
                    try:
                        yield Token(TokenType.INT, int(a))
                    except ValueError:
                        yield Token(TokenType.FLOAT, float(a))
            elif self.current_char == ";":
                self.advance()
                yield Token(TokenType.SEMI)
            else:
                token = Token(TokenType.BUILTIN, self.generate_function())
                if token.value in types:
                    self.advance()
                    if token.value == "int":
                        yield Token(TokenType.INT, self.generate_function() + " " + self.generate_int())
                    elif token.value == "float":
                        yield Token(TokenType.FLOAT, self.generate_function() + " " + self.generate_float())
                    elif token.value == "string":
                        yield Token(TokenType.STRING, self.generate_function() + " " + self.generate_string(
                            True if self.current_char == "\'" else False))
                        # Strings are returning ''. Look into that and make some frigging comments!
                else:
                    yield token

    def generate_string(self, is_dquote):
        string = ""
        if is_dquote is True:
            while self.current_char is not None and self.current_char != "\"":
                if self.current_char == "\\":
                    self.advance()
                    if self.current_char == "t":
                        string += "\t"
                    elif self.current_char == "b":
                        string += "\b"
                    elif self.current_char == "n":
                        string += "\n"
                    else:
                        string += self.current_char
                    self.advance()
                else:
                    string += self.current_char
                    self.advance()
        else:
            while self.current_char is not None and self.current_char != "'":
                if self.current_char == "\\":
                    self.advance()
                    string += self.current_char
                    self.advance()
                else:
                    string += self.current_char
                    self.advance()
        return string

    def generate_function(self):
        func = ""
        while self.current_char is not None and self.current_char not in WHITESPACE + "(),&|./;":
            func += self.current_char
            self.advance()
        return func

    def generate_int(self, eadvan=""):
        num = ""
        if eadvan:
            pass
        else:
            self.advance()
        while self.current_char is not None and self.current_char in DIGITS:
            num += self.current_char
            self.advance()
        return num

    def generate_float(self, eadvan=""):
        num = ""
        period_count = 0
        if eadvan:
            pass
        else:
            self.advance()
        while self.current_char is not None and self.current_char in DIGITS + ".":
            if self.current_char == ".":
                period_count += 1
            if period_count > 1:
                raise Exception("Greater than one period in the float point")
            num += self.current_char
            self.advance()
        return num

    def generate_message(self):
        while self.current_char is not None:
            self.advance()
            if self.current_char == "*":
                self.advance()
                if self.current_char == "/":
                    break
        self.advance()

    def generate_message_newline(self):
        while self.current_char is not None and self.current_char != "\n":
            self.advance()
        self.advance()
