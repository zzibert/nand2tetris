import sys
import os


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
    output_file = open(output + ".xml", 'w')

    input_file = open(filename, 'r')
    lines = input_file.readlines()

    for line in lines:
        if line.strip() and not line[0:2] == "//":
            line = line.replace('\n', "")
            line = line.replace('\r', "")
            comment = line.find("//")
            if comment != -1:
                line = line[:comment]
            tokens = token_maker(line)

            for token in tokens:
                token = tokenTypeMaker(token)
                output_file.write(token + '\n')

def token_maker(line):
    line = line.replace('(', ' ( ')
    line = line.replace(')', ' ) ')
    line = line.replace('{', ' { ')
    line = line.replace('}', ' } ')
    line = line.replace(';', ' ; ')
    line = line.replace('+', ' + ')
    line = line.replace('*', ' * ')
    line = line.replace('=', ' = ')
    tokens = line.split(" ")
    while("" in tokens): 
        tokens.remove("")
    return tokens

def tokenTypeMaker(token):
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
                      or token == '&'
                      or token == '|'
                      or token == '<'
                      or token == '>'
                      or token == '='
                      or token == '~'):
        return handleSymbol(token)
    elif token.isdecimal():
        return handleIntVal(token)
    elif token[0] == '"':
        return handleStringVal(token)
    else:
        return handleIdentifier(token)


def handleKeyword(token):
    return "<keyword> " + token + " </keyword>"

def handleSymbol(token):
    return "<symbol> " + token + " </symbol>"

def handleIdentifier(token):
    return "<identifier> " + token + " </identifier>"

def handleIntVal(token):
    return "<integerConstant> " + token + " </integerConstant>"

def handleStringVal(token):
    return "<stringConstant> " + token[1:-1] + " </stringConstant>" 

            


# COMPILATION ENGINE

filename = sys.argv[1]

jack_tokenizer(filename)