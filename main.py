import compiler.Lexer
import sys
import os
from compiler.Tokens import TokenType

ENDLABEL = "\tMOV R7, #1\n\tSWI 0\n"
funcs = {"_putnumb{}\n": {"num": 0, "code": ["\tMOV R7, #4\n", "\tMOV R0, #1\n", "\tMOV R2, #1000 @ MAX NUM LEN 1000\n", "\tLDR R1, ={}\n", "\tSWI 0\n"]
                         }, "_start{}\n": {"num": 0, "code": ["\tB {}"]}}
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
                    advance()
                elif char.type == TokenType.SQUOTE:
                    advance()
                    if len(char.value) <= 4:
                        sections[".text\n"].append(f"{name}:\n\t.ascii \"{char.value}\"\n")
                    else:
                        print("CharError: Length greater than 4")
                        exit(1)
                elif char.type == TokenType.INT:
                    sections[".text\n"].append(f"{name}:\n\t.ascii \"{char.value}\"\n")
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
        elif char.value == "putnumb":
            advance()
            if char.type != TokenType.LPAREN:
                print("ParenthesesError: Expected left parentheses")
                exit(1)
            advance()
            # Don't know why this works, it just does, leave it
            funcs["_putnumb{}\n"]["code"] = ["\tMOV R7, #4\n", "\tMOV R0, #1\n", "\tMOV R2, #1000 @ MAX NUM LEN 1000\n", "\tLDR R1, ={}\n", "\tSWI 0\n"]
            sections["_putnumb{}\n".format(funcs["_putnumb{}\n"]["num"])] = funcs["_putnumb{}\n"]["code"]
            if char.value in var and type(var[char.value]) == int:
                sections["_putnumb{}\n".format(funcs["_putnumb{}\n"]["num"])][3] = sections["_putnumb{}\n".format(funcs["_putnumb{}\n"]["num"])][3].format(char.value)
            elif char.type == TokenType.INT:
                sections["_putnumb{}\n".format(funcs["_putnumb{}\n"]["num"])][3] = sections["_putnumb{}\n".format(funcs["_putnumb{}\n"]["num"])][3].format(f"\"{char.value}\"")
            else:
                print("TypeError: putnumb's argument must be a whole number")
            funcs["_putnumb{}\n"]["num"] += 1
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
rfile = open(f"{filename}.s", "r")
for i in sections.keys():
    file.write(i)
    for e in sections[i]:
        file.write(e)
