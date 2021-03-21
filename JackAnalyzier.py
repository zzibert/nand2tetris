import sys
import os


# JACK ANALYZER
def jack_analyzer(filename):

    # create an jackTokenizer from the input file
    tokenizer = jack_tokenizer(filename)


    # Create an output file called xxx.xml and prepare it for writing
    name_and_suffix = filename.split(".")
    output = name_and_suffix[0]
    output_file = open(output + ".xml", 'w')

    # Use the Compilation Engine to compile the input JackTokenizer into the output file
    compilation_engine(output_file, tokenizer)

# JACK TOKENIZER


# COMPILATION ENGINE