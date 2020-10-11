import compiler.Lexer
import sys
import os
from compiler.Tokens import TokenType
from strchar import Char

# NOTE TO REMEMBER: R6 WILL BE USED FOR getchar FUNCTION

ENDLABEL = "\tMOV R7, #1\n\tSWI 0\n"
funcs = {"_putnumb{}\n": {"num": 0, "code": ["\tMOV R7, #4\n", "\tMOV R0, #1\n", "\tMOV R2, #1000 @ MAX NUM LEN 1000\n", "\tLDR R1, ={}\n", "\tSWI 0\n"]
                         }, "_putstr{}\n": {"num": 0, "code": ["\tMOV R7, #4\n", "\tMOV R0, #1\n", "\tMOV R2, #10000 @ MAX NUM LEN 10000\n", "\tLDR R1, ={}\n", "\tSWI 0\n"]},
         "_putchar{}\n": {"num": 0, "code": ["\tMOV R7, #4\n", "\tMOV R0, #1\n", "\tMOV R2, #1000 @ MAX NUM LEN 10000\n", "\tLDR R1, ={}\n", "\tSWI 0\n"]},
         "_getstr{}\n": {"num": 0, "code": ["\tMOV R7, #3\n", "\tMOV R0, #0\n", "\tMOV R2, #10000 @ MAX NUM LEN 10000\n", "\tLDR R1, ={}\n", "\tSWI 0\n"]}}
var = {}
sections = {".text\n": [], ".global _start\n": ["_start:\n", ENDLABEL]}

# Argument variables
filename, tocompile, keepasm, supress = "a", sys.argv[1] if len(sys.argv) >= 2 else input("File name: "), False, False
i = 2
while i < len(sys.argv[2:]):
    if sys.argv[i] == "-o":
        i += 1
        filename = sys.argv[i]
    elif sys.argv[i] == "-a":
        keepasm = True
    i += 1

tocompile = open(tocompile)
tokens = compiler.Lexer.Lexer(tocompile.read()).generate_tokens()
tocompile.close()
text = iter(tokens)
char = next(text)


def advance():
    global text, char
    try:
        char = next(text)
    except StopIteration:
        char = None


inmain = False
# Execute immediately
while char is not None:
    if char.type == TokenType.BUILTIN:
        if char.value == "auto":
            advance()
            name = char.value
            advance()
            if char.type == TokenType.SEMI:
                sections[".text\n"].append(f"{name}:\n\t.ascii\"0\"")
            elif char.type == TokenType.EQUAL:
                advance()
                if char.type == TokenType.DQUOTE:
                    advance()
                    sections[".text\n"].append(f"{name}:\n\t.ascii \"{char.value}\"\n")
                    var[name] = char.value
                    advance()
                elif char.type == TokenType.SQUOTE:
                    advance()
                    if len(char.value) >= 4:
                        sections[".text\n"].append(Char(f"{name}:\n\t.ascii \"{char.value}\"\n"))
                        var[name] = Char(char.value)
                    else:
                        print("CharError: Length greater than 4")
                        exit(1)
                    advance()
                elif char.type == TokenType.INT:
                    sections[".text\n"].append(f"{name}:\n\t.ascii \"{char.value}\\n\"\n")
                    var[name] = int(char.value)
                advance()
                if char.type != TokenType.SEMI:
                    print("SemicolonMissingError: No end of line")
                    exit(1)
        elif char.value == "main":
            inmain = True
            advance()
            if char.type != TokenType.LPAREN:
                print("ParenthesesError: Expected left parentheses")
                exit(1)
            advance()
            if char.type != TokenType.RPAREN:
                print("ParenthesesError: Expected right parentheses")
                exit(1)
            advance()
            if char.type != TokenType.LCURLY:
                print("BracketError: Expected left curly bracket")
                exit(1)
        elif inmain:
            if char.value == "putnumb":
                advance()
                if char.type != TokenType.LPAREN:
                    print("ParenthesesError: Expected left parentheses")
                    exit(1)
                advance()
                # Don't know why this works, it just does, leave it
                funcs["_putnumb{}\n"]["code"] = ["\tMOV R7, #4\n", "\tMOV R0, #1\n", "\tMOV R2, #1000 @ MAX NUM LEN 1000\n",
                                                 "\tLDR R1, ={}\n", "\tSWI 0\n"]
                sections["_putnumb{}\n".format(funcs["_putnumb{}\n"]["num"])] = funcs["_putnumb{}\n"]["code"]
                if char.value in var and type(var[char.value]) == int:
                    sections["_putnumb{}\n".format(funcs["_putnumb{}\n"]["num"])][3] = \
                    sections["_putnumb{}\n".format(funcs["_putnumb{}\n"]["num"])][3].format(char.value)
                elif char.type == TokenType.INT:
                    sections["_putnumb{}\n".format(funcs["_putnumb{}\n"]["num"])][3] = \
                    sections["_putnumb{}\n".format(funcs["_putnumb{}\n"]["num"])][3].format(f"\"{char.value}\"")
                elif char.type == TokenType.AND:
                    advance()
                    sections["_putnumb{}\n".format(funcs["_putnumb{}\n"]["num"])][3] = \
                    sections["_putnumb{}\n".format(funcs["_putnumb{}\n"]["num"])][3].format(f"{char.value}").replace("LDR",
                                                                                                                     "ADR")
                else:
                    print("TypeError: putnumb's argument must be a whole number")
                    exit(1)
                funcs["_putnumb{}\n"]["num"] += 1
                advance()
                if char.type != TokenType.RPAREN:
                    print("ParenthesesError: Expected right parentheses")
                    exit(1)
                advance()
                if char.type != TokenType.SEMI:
                    print("SemicolonMissingError: No end of line")
                    exit(1)
            elif char.value == "putstr":
                advance()
                if char.type != TokenType.LPAREN:
                    print("ParenthesesError: Expected left parentheses")
                    exit(1)
                advance()
                # Don't know why this works, it just does, leave it
                funcs["_putstr{}\n"]["code"] = ["\tMOV R7, #4\n", "\tMOV R0, #1\n", "\tMOV R2, #1000 @ MAX NUM LEN 10000\n",
                                                "\tLDR R1, ={}\n", "\tSWI 0\n"]
                sections["_putstr{}\n".format(funcs["_putstr{}\n"]["num"])] = funcs["_putstr{}\n"]["code"]
                if char.value in var and type(var[char.value]) == str:
                    sections["_putstr{}\n".format(funcs["_putstr{}\n"]["num"])][3] = \
                    sections["_putstr{}\n".format(funcs["_putstr{}\n"]["num"])][3].format(char.value)
                elif char.type == TokenType.DQUOTE:
                    advance()
                    sections["_putstr{}\n".format(funcs["_putstr{}\n"]["num"])][3] = \
                    sections["_putstr{}\n".format(funcs["_putstr{}\n"]["num"])][3].format(f"\"{char.value}\"")
                    advance()
                else:
                    print("TypeError: putstr's argument must be a string with \"")
                    exit(1)
                funcs["_putstr{}\n"]["num"] += 1
                advance()
                if char.type != TokenType.RPAREN:
                    print("ParenthesesError: Expected right parentheses")
                    exit(1)
                advance()
                if char.type != TokenType.SEMI:
                    print("SemicolonMissingError: No end of line")
                    exit(1)
            elif char.value == "putchar":
                advance()
                if char.type != TokenType.LPAREN:
                    print("ParenthesesError: Expected left parentheses")
                    exit(1)
                advance()
                # Don't know why this works, it just does, leave it
                funcs["_putchar{}\n"]["code"] = ["\tMOV R7, #4\n", "\tMOV R0, #1\n",
                                                 "\tMOV R2, #10000 @ MAX NUM LEN 10000\n", "\tLDR R1, ={}\n", "\tSWI 0\n"]
                sections["_putchar{}\n".format(funcs["_putchar{}\n"]["num"])] = funcs["_putchar{}\n"]["code"]
                if char.value in var and type(var[char.value]) == Char:
                    sections["_putchar{}\n".format(funcs["_putchar{}\n"]["num"])][3] = \
                        sections["_putchar{}\n".format(funcs["_putchar{}\n"]["num"])][3].format(char.value)
                elif char.type == TokenType.SQUOTE:
                    advance()
                    sections["_putchar{}\n".format(funcs["_putchar{}\n"]["num"])][3] = \
                        sections["_putchar{}\n".format(funcs["_putchar{}\n"]["num"])][3].format(f"\"{char.value}\"")
                    advance()
                else:
                    print("TypeError: putchar's argument must be a char with '")
                    exit(1)
                funcs["_putchar{}\n"]["num"] += 1
                advance()
                if char.type != TokenType.RPAREN:
                    print("ParenthesesError: Expected right parentheses")
                    exit(1)
                advance()
                if char.type != TokenType.SEMI:
                    print("SemicolonMissingError: No end of line")
                    exit(1)
            elif char.value == "getstr":
                advance()
                if char.type != TokenType.LPAREN:
                    print("ParenthesesError: Expected left parentheses")
                    exit(1)
                advance()
                funcs["_getstr{}\n"]["code"] = ["\tMOV R7, #3\n", "\tMOV R0, #0\n", "\tMOV R2, #10000 @ MAX NUM LEN 10000\n"
                                                                                    "", "\tLDR R1, ={}\n", "\tSWI 0\n"]
                sections["_getstr{}\n".format(funcs["_getstr{}\n"]["num"])] = funcs["_getstr{}\n"]["code"]
                if char.value in var and type(var[char.value]) == str:
                    sections["_getstr{}\n".format(funcs["_getstr{}\n"]["num"])][3] = \
                        sections["_getstr{}\n".format(funcs["_getstr{}\n"]["num"])][3].format(char.value)
                else:
                    print("TypeError: getstr's argument must be a string with \"")
                    exit(1)
                funcs["_getstr{}\n"]["num"] += 1
                advance()
                if char.type != TokenType.RPAREN:
                    print("ParenthesesError: Expected right parentheses")
                    exit(1)
                advance()
                if char.type != TokenType.SEMI:
                    print("SemicolonMissingError: No end of line")
                    exit(1)
    elif char.type == TokenType.RCURLY and inmain:
        inmain = False
    advance()

open(f"{filename}.s", "w")
file = open(f"{filename}.s", "a+")
for i in sections.keys():
    file.write(i)
    for e in sections[i]:
        file.write(e)
file.close()
