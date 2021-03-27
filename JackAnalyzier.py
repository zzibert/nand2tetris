import sys
import os

middle_of_string = False

ignore_line = False


# JACK ANALYZER
def jack_analyzer(filename):

    # create an jackTokenizer from the input file
    tokenizer = jack_tokenizer(filename)


    # Create an output file called xxx.xml and prepare it for writing
    # name_and_suffix = filename.split(".")
    # output = name_and_suffix[0]
    # output_file = open(output + ".xml", 'w')

    # Use the Compilation Engine to compile the input JackTokenizer into the output file
    # compilation_engine(output_file, tokenizer)

# JACK TOKENIZER
def jack_tokenizer(filename):
    name_and_suffix = filename.split(".")
    output = name_and_suffix[0]
    output_file = open( "test.xml", 'w')

    tab_counter = 1

    input_file = open(filename, 'r')
    output_file.write("<tokens>\n")
    lines = input_file.readlines()

    global ignore_line

    for line in lines:
        line = line.strip()
        if line[0:3] == "/**":
            ignore_line = True
        if not line[0:2] == "//" and not ignore_line:
            line = line.replace('\n', "")
            line = line.replace('\r', "")
            comment = line.find("//")
            if comment != -1:
                line = line[:comment]
            tokens = token_maker(line)

            for token in tokens:
                token = tokenTypeMaker(token)
                tabs = tab_counter * '\t'
                output_file.write(token)
        if line[-2:] == "*/":
            ignore_line = False

    output_file.write("</tokens>\n")

def token_maker(line):
    line = line.replace('(', ' ( ')
    line = line.replace(')', ' ) ')
    line = line.replace('{', ' { ')
    line = line.replace('}', ' } ')
    line = line.replace('[', ' [ ')
    line = line.replace(']', ' ] ')
    line = line.replace(';', ' ; ')
    line = line.replace('+', ' + ')
    line = line.replace('*', ' * ')
    line = line.replace('=', ' = ')
    line = line.replace('.', ' . ')
    line = line.replace(',', ' , ')
    line = line.replace('-', ' - ')
    line = line.replace('~', ' ~ ')
    tokens = line.split(" ")
    while("" in tokens): 
        tokens.remove("")
    return tokens

def tokenTypeMaker(token):
    global middle_of_string

    if (token == "if" or token == "class" 
                     or token == "method"
                     or token == "function"
                     or token == "constructor"
                     or token == "int"
                     or token == "boolean"
                     or token == "char"
                     or token == "void"
                     or token == "var"
                     or token == "static"
                     or token == "field"
                     or token == "let"
                     or token == "do"
                     or token == "else"
                     or token == "while"
                     or token == "return"
                     or token == "true"
                     or token == "false"
                     or token == "null"
                     or token == "this"):
        return handleKeyword(token)
    elif (token == '{' or token == '}'
                      or token == '('
                      or token == ')'
                      or token == '['
                      or token == ']'
                      or token == '.'
                      or token == ','
                      or token == ';'
                      or token == '+'
                      or token == '-'
                      or token == '*'
                      or token == '/'
                      or token == '='
                      or token == '|'
                      or token == '.'
                      or token == ','
                      or token == '~'):
        return handleSymbol(token)
    elif (token == '<'or token == '>' or token == '&'):
        return handleEqual(token)
    elif token.isdecimal():
        return handleIntVal(token)
    elif token[0] == '"' and token[-1] == '"' and not middle_of_string:
        return handleStringValWhole(token)
    elif token[0] == '"' and not middle_of_string:
        middle_of_string = True
        return handleStringValBeginning(token)
    elif token[0] == '"' and middle_of_string:
        middle_of_string = False
        return handleStringValEnd(token)
    elif middle_of_string:
        return handleStringVal(token)
    else:
        return handleIdentifier(token)


def handleKeyword(token):
    return "<keyword> " + token + " </keyword>\n"

def handleSymbol(token):
    return "<symbol> " + token + " </symbol>\n"

def handleEqual(token):
    symbol = ""
    if token == "<":
        symbol = "&lt;"
    elif token == ">":
        symbol = "&gt;"
    elif token == "&":
        symbol = "&amp;"
    
    return handleSymbol(symbol)

def handleIdentifier(token):
    return "<identifier> " + token + " </identifier>\n"

def handleIntVal(token):
    return "<integerConstant> " + token + " </integerConstant>\n"

def handleStringValWhole(token):
    return "<stringConstant> " + token[1:-1] + " </stringConstant>\n"

def handleStringValBeginning(token):
    return "<stringConstant> " + token[1:] + " "

def handleStringValEnd(token):
    return token[:-1] + " </stringConstant>\n"

def handleStringVal(token):
    return token + " "

            


# COMPILATION ENGINE

filename = sys.argv[1]

jack_tokenizer(filename)