import sys

predefined_symbols = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576
}

destinations = {
    "": "000",
    '0': "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111",
}

computations = {
    '0': "0101010",
    "": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}

jumps = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP" : "111"
}

def c_instruction(file1, line):
    line = line.rstrip()
    indexOfEqual = line.find("=")
    indexOfSemicolon = line.find(";")
    if indexOfSemicolon == -1:
        jump = "000"
    else:
        jump = jumps[line[indexOfSemicolon+1:]]
        line = line[:indexOfSemicolon]
    
    instruction = "111" + computations[line[indexOfEqual+1:]] + destinations[line[:indexOfEqual]] + jump
    file1.write(instruction  + '\n')

 
filename = sys.argv[1]

assembly = open(filename, 'r')
lines = assembly.readlines()
 
file1 = open('output.hack', 'w')

instruction_counter = 0

variable_counter = 16


for line in lines:
    if line.strip() and not line[0:2] == "//":
        line = line.replace(" ", "")
        line = line.replace('\n', "")
        line = line.replace('\r', "")
        comment = line.find("//")
        if comment != -1:
            line = line[:comment]
        if line[0] == '(':
            label = line[1:-1]
            predefined_symbols[label] = instruction_counter
            instruction_counter -= 1
        instruction_counter += 1
        



for line in lines:
    if line.strip() and not line[0:2] == "//":
        line = line.replace(" ", "")
        line = line.replace('\n', "")
        line = line.replace('\r', "")
        comment = line.find("//")
        if comment != -1:
            line = line[:comment]
        print(line)
        if line[0] == '@':
            line = line[1:]
            if line.isdigit():
                bin_ = '{0:016b}'.format(int(line))
                file1.write(bin_ + '\n')
            else:
                if line in predefined_symbols:
                    bin_ = '{0:016b}'.format(int(predefined_symbols[line]))
                    file1.write(bin_ + '\n')
                else:
                    predefined_symbols[line] = variable_counter
                    variable_counter += 1
                    bin_ = '{0:016b}'.format(int(predefined_symbols[line]))
                    file1.write(bin_ + '\n')
            
        elif line[0] != '(':
            c_instruction(file1, line)
    
 

file1.close()
assembly.close()
 


