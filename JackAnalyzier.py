import sys
import os
import gc

middle_of_string = False

ignore_line = False

middle_of_statements_stack = []

def lookup_from_stack():
    length = len(middle_of_statements_stack)
    if len(middle_of_statements_stack) > 0:
        return middle_of_statements_stack[length-1]
    else:
        "empty"

def pop_from_stack():
    middle_of_statements_stack.pop()

def push_to_stack(element):
    middle_of_statements_stack.append(element)



# JACK ANALYZER
def jack_analyzer(filename):

    # create an jackTokenizer from the input file
    tokenizer = jack_tokenizer(filename)


    # Create an output file called xxx.xml and prepare it for writing
    name_and_suffix = filename.split(".")
    output = name_and_suffix[0]
    output_file = open("test.xml", 'w')

    # Use the Compilation Engine to compile the input JackTokenizer into the output file
    compilation_engine(output_file, tokenizer)

# JACK TOKENIZER
def jack_tokenizer(filename):
    # name_and_suffix = filename.split(".")
    # output = name_and_suffix[0]
    # output_file = open( "test.xml", 'w')

    tab_counter = 1
    tokenizer = []

    input_file = open(filename, 'r')
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
                # token = tokenTypeMaker(token)
                tabs = tab_counter * "  "
                # output_file.write(token + '\n')
                tokenizer.append(token)

        if line[-2:] == "*/":
            ignore_line = False

    return tokenizer

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
    elif token[0] == '"' or token[-1] == '"' and middle_of_string:
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

def compilation_engine(output_file, tokenizer):
    if tokenizer[0] == "class":
        output_file.write("<class>\n")
        compileClass(tokenizer, output_file, 1)
        output_file.write("</class>\n")

# def parseStatement():

# def parseWhileStatement():

# def parseIfStatement():

def parseStatementSequence(tokens, output_file, tabs):
    if tokens[0] == "static" or tokens[0] == "field":
        end_of_class_var_dec = tokens.index(';')
        output_file.write(tabs * "  " + "<classVarDec>\n")
        compileClassVarDec(tokens[:end_of_class_var_dec+1], output_file, tabs+1)
        output_file.write(tabs * "  " + "</classVarDec>\n")
        parseStatementSequence(tokens[end_of_class_var_dec+1:], output_file, tabs)

    elif tokens[0] == "function" or tokens[0] == "constructor" or tokens[0] == "method":
        end_of_subroutine_dec = tokens.index(';')
        output_file.write(tabs * "  " + "<subroutineDec>\n")
        compileSubroutineDec(tokens, output_file, tabs+1)
        # parseStatementSequence(tokens[end_of_subroutine_dec+1:], output_file, tabs)



# def parseExpression():

def compileClass(tokens, output_file, tabs):
    output_file.write(tabs * "  " + handleKeyword(tokens[0])) # class keyword
    output_file.write(tabs * "  " + handleIdentifier(tokens[1])) # class Name
    output_file.write(tabs * "  " + handleSymbol(tokens[2])) # {
    parseStatementSequence(tokens[3:-1], output_file, tabs)
    output_file.write(tabs * "  " + handleSymbol(tokens[-1])) # }


def compileClassVarDec(tokens, output_file, tabs):
    for token in tokens:
        output_file.write(tabs * "  " + tokenTypeMaker(token))

def compileSubroutineDec(tokens, output_file, tabs):
    # output_file.write(tabs * "  " + handleKeyword(tokens[0])) # static or field keyword
    # output_file.write(tabs * "  " + handleKeyword(tokens[1])) # type
    # output_file.write(tabs * "  " + handleIdentifier(tokens[2])) # subroutine name
    # output_file.write(tabs * "  " + handleSymbol(tokens[3])) # (
    
    beginning_of_subroutine_dec = tokens.index('(')
    compileTerm(tokens[:(beginning_of_subroutine_dec+1)], output_file, tabs)
    end_of_subroutine_dec = tokens.index(')')
    output_file.write(tabs * "  " + "<parameterList>\n")
    compileParameterList(tokens[(beginning_of_subroutine_dec+1):end_of_subroutine_dec], output_file, tabs)
    output_file.write(tabs * "  " + "</parameterList>\n")
    output_file.write(tabs * "  " + handleSymbol(tokens[end_of_subroutine_dec])) # )
    output_file.write(tabs * "  " + "<subroutineBody>\n")
    compileSubroutineBody(tokens[1+end_of_subroutine_dec:], output_file, tabs+1)



def compileParameterList(tokens, output_file, tabs):
  for token in tokens:
    output_file.write((tabs+1) * "  " + tokenTypeMaker(token))

def compileSubroutineBody(tokens, output_file, tabs):
  if tokens[0] == "{":
    output_file.write(tabs * "  " + handleSymbol(tokens[0])) # {
    compileSubroutineBody(tokens[1:], output_file, tabs)
  elif tokens[0] == "var":
    end_of_var_dec = tokens.index(';')
    output_file.write(tabs * "  " + "<varDec>\n")
    compileVarDec(tokens[:end_of_var_dec+1], output_file, tabs)
    output_file.write(tabs * "  " + "</varDec>\n")
    compileSubroutineBody(tokens[end_of_var_dec+1:], output_file, tabs)

  elif tokens[0] == "}":
    output_file.write(tabs * "  " + handleSymbol(tokens[0])) # }
    parseStatementSequence(tokens[1:], output_file, tabs-2)

  else:
    output_file.write(tabs * "  " + "<statements>\n")
    compileStatements(tokens, output_file, tabs+1)

def compileVarDec(tokens, output_file, tabs):
  for token in tokens:
    output_file.write((tabs+1) * "  " + tokenTypeMaker(token))

def compileStatements(tokens, output_file, tabs):

    if len(tokens) < 1:
        output_file.write((tabs-1) * "  " + "</subroutineBody>\n")
        output_file.write((tabs-2) * "  " + "</subroutineDec>\n")
        return

        
    elif tokens[0] == "let":
        end_of_let_dec = tokens.index(';')
        output_file.write(tabs * "  " + "<letStatement>\n")
        compileLet(tokens[:end_of_let_dec+1], output_file, tabs+1)
        output_file.write(tabs * "  " + "</letStatement>\n")
        compileStatements(tokens[end_of_let_dec+1:], output_file, tabs)

    elif tokens[0] == "do":
        end_of_do_dec = tokens.index(';')
        output_file.write(tabs * "  " + "<doStatement>\n")
        compileDo(tokens[:end_of_do_dec+1], output_file, tabs+1)
        output_file.write(tabs * "  " + "</doStatement>\n")
        compileStatements(tokens[end_of_do_dec+1:], output_file, tabs)

    elif tokens[0] == "return":
        end_of_return_dec = tokens.index(';')
        output_file.write(tabs * "  " + "<returnStatement>\n")
        compileReturn(tokens[:end_of_return_dec+1], output_file, tabs+1)
        output_file.write(tabs * "  " + "</returnStatement>\n")
        compileStatements(tokens[end_of_return_dec+1:], output_file, tabs)


    elif tokens[0] == "if":
        output_file.write(tabs * "  " + "<ifStatement>\n")
        compileIf(tokens, output_file, tabs+1)

    elif tokens[0] == "else":
        output_file.write(tabs * "  " + handleKeyword(tokens[0])) # else keyword
        output_file.write(tabs * "  " + handleSymbol(tokens[1])) # {
        output_file.write(tabs * "  " + "<statements>\n")
        compileStatements(tokens[2:], output_file, tabs)

    elif tokens[0] == "while":
        output_file.write(tabs * "  " + "<whileStatement>\n")
        compileWhile(tokens, output_file, tabs+1)

    elif tokens[0] == "}":
        lookup = lookup_from_stack()
        if lookup == "if" and tokens[1] != "else":
            output_file.write((tabs) * "  " + "</statements>\n")
            output_file.write((tabs) * "  " + handleSymbol(tokens[0])) # }
            output_file.write((tabs-1) * "  " + "</ifStatement>\n")
            pop_from_stack()
        elif lookup == "while":
            output_file.write(tabs * "  " + "</statements>\n")
            output_file.write((tabs) * "  " + handleSymbol(tokens[0])) # }
            output_file.write((tabs-1) * "  " + "</whileStatement>\n")
            pop_from_stack()
        else:
            output_file.write((tabs-1) * "  " + "</statements>\n")
            output_file.write((tabs-1) * "  " + handleSymbol(tokens[0])) # }
        compileStatements(tokens[1:], output_file, tabs-1)

    else:
        output_file.write((tabs-1) * "  " + "</subroutineBody>\n")
        output_file.write((tabs-2) * "  " + "</subroutineDec>\n")
        parseStatementSequence(tokens, output_file, tabs-2)

  # elif tokens[0] == "while":
  #   end_of_if_dec = tokens.index(';')
  #   output_file.write(tabs * "  " + "<ifStatement>\n")
  #   compileDo(tokens[:end_of_if_dec+1], output_file, tabs+1)
  #   output_file.write(tabs * "  " + "</ifStatement>\n")
  #   compileStatements(tokens[end_of_if_dec+1:], output_file, tabs)

def compileDo(tokens, output_file, tabs):
  beginning_of_expression_list = tokens.index('(')
  end_of_expression_list = tokens.index(')')

  for token in tokens[:(beginning_of_expression_list+1)]:
    output_file.write((tabs) * "  " + tokenTypeMaker(token))

  compileExpressionList(tokens[(beginning_of_expression_list+1):end_of_expression_list], output_file, tabs+1)

  for token in tokens[end_of_expression_list:]:
    output_file.write((tabs) * "  " + tokenTypeMaker(token))

def compileLet(tokens, output_file, tabs):
  output_file.write(tabs * "  " + handleKeyword(tokens[0])) # let keyword
  output_file.write(tabs * "  " + handleIdentifier(tokens[1])) # varName
  output_file.write(tabs * "  " + handleSymbol(tokens[2])) # =
  end_of_let_dec = tokens.index(';')
  compileExpression(tokens[3:end_of_let_dec], output_file, tabs+1)
  output_file.write(tabs * "  " + handleSymbol(tokens[end_of_let_dec]))


def compileReturn(tokens, output_file, tabs):
    output_file.write(tabs * "  " + handleKeyword(tokens[0])) # return keyword
    end_of_return_dec = tokens.index(';')
    if len(tokens[1:end_of_return_dec]) > 0:
        compileExpression(tokens[1:end_of_return_dec], output_file, tabs+1)
    output_file.write(tabs * "  " + handleSymbol(tokens[-1])) # ; keyword

def compileIf(tokens, output_file, tabs):

  push_to_stack("if")

  output_file.write(tabs * "  " + handleKeyword(tokens[0])) # if keyword
  output_file.write(tabs * "  " + handleSymbol(tokens[1])) # (
  end_of_expression = tokens.index(')')
  compileExpression(tokens[2:end_of_expression], output_file, tabs+1)
  output_file.write(tabs * "  " + handleSymbol(tokens[end_of_expression])) # )
  output_file.write(tabs * "  " + handleSymbol(tokens[end_of_expression+1])) # {
  output_file.write(tabs * "  " + "<statements>\n")
  compileStatements(tokens[(end_of_expression+2):], output_file, tabs+1)

def compileWhile(tokens, output_file, tabs):

    push_to_stack("while")

    output_file.write(tabs * "  " + handleKeyword(tokens[0])) # while keyword
    output_file.write(tabs * "  " + handleSymbol(tokens[1])) # (
    end_of_expression = tokens.index(')')
    compileExpression(tokens[2:end_of_expression], output_file, tabs+1)
    output_file.write(tabs * "  " + handleSymbol(tokens[end_of_expression])) # )
    output_file.write(tabs * "  " + handleSymbol(tokens[end_of_expression+1])) # {
    output_file.write(tabs * "  " + "<statements>\n")
    compileStatements(tokens[(end_of_expression+2):], output_file, tabs+1)



# def compileExpressionList(tokens, output_file):

def compileTerm(tokens, output_file, tabs):

    for i in range(len(tokens)):
        if middle_of_string:
            output_file.write(tokenTypeMaker(tokens[i]))
        elif tokens[i] == '(':
            output_file.write(tabs * "  " + handleSymbol(tokens[i])) # (
        else:
            output_file.write(tabs * "  " + tokenTypeMaker(tokens[i]))
    # for token in tokens:
    #     if middle_of_string:
    #         output_file.write(tokenTypeMaker(token))
    #     elif token == '(':
    #         output_file.write
    #     else:
    #         output_file.write((tabs) * "  " + tokenTypeMaker(token))

def compileExpression(tokens, output_file, tabs):
  if len(tokens) > 0:
    output_file.write((tabs-1) * "  " + "<expression>\n")
    output_file.write(tabs * "  " + "<term>\n")
    compileTerm(tokens, output_file, tabs+1)
    output_file.write(tabs * "  " + "</term>\n")
    output_file.write((tabs-1) * "  " + "</expression>\n")

def compileExpressionList(tokens, output_file, tabs):
    output_file.write((tabs-1) * "  " + "<expressionList>\n")
    while(True):
        try:
            end_of_expression = tokens.index(',')
            compileExpression(tokens[:end_of_expression], output_file, tabs+1)
            output_file.write(tabs * "  " + handleSymbol(tokens[end_of_expression]))
            tokens = tokens[(end_of_expression+1):]
        except ValueError:
            compileExpression(tokens, output_file, tabs+1)
            break
    output_file.write((tabs-1) * "  " + "</expressionList>\n")

filename = sys.argv[1]

jack_analyzer(filename)