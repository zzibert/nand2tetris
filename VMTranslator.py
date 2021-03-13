import sys
import os


# PARSER

# filename = sys.argv[1]


# CONTSTRUCTOR
# vm_file = open(filename, 'r')



# output_name = filename.split('.')

# assembly = open(output_name[0] + ".asm", 'w')



# sys_file = open("Sys.vm", 'r')

# lines = sys_file.readlines




# SET SP TO 256
def set_sp():
    machine_code = "@256" + "\n" + "D=A" + "\n" + "@0" + "\n" + "M=D" + "\n"
    assembly.write(machine_code)

def call_sys_init():
    handle_call("Sys.init0")


def pop():
    return decrement_sp() + "@0" + "\n" + "A=M" + "\n" + "D=M" + "\n"

def push():
    return "@0" + "\n" + "A=M" + "\n" + "M=D" + "\n" + increment_sp()

def increment_sp():
    return "@0" + "\n" + "M=M+1" + "\n"

def decrement_sp():
    return "@0" + "\n" + "M=M-1" + "\n"

def sub():
    return pop() + decrement_sp() + "A=M" + "\n" + "D=M-D" + "\n" + push()

def neg():
    return pop() + "D=-M" + "\n" + push()

def bit_wise_not():
    return pop() + "D=!M" + "\n" + push()

def bit_wise_and():
    return pop() + decrement_sp() + "A=M" + "\n" + "D=D&M" + "\n" + push()

def bit_wise_or():
    return pop() + decrement_sp() + "A=M" + "\n" + "D=D|M" + "\n" + push()

def handle_bit_wise_and():
    machine_code = bit_wise_and()
    assembly.write(machine_code)

def handle_bit_wise_not():
    machine_code = bit_wise_not()
    assembly.write(machine_code)

def handle_bit_wise_or():
    machine_code = bit_wise_or()
    assembly.write(machine_code)

def handle_add():
    machine_code = pop() + decrement_sp() + "A=M" + "\n" + "D=D+M" + "\n" + push()
    assembly.write(machine_code)

def handle_sub():
    machine_code = sub()
    assembly.write(machine_code)

def handle_neg():
    machine_code = neg()
    assembly.write(machine_code)

def handle_eq():
    x_minus_y = pop() + decrement_sp() + "A=M" + "\n" + "D=M-D" + "\n" + "@13" + "\n" + "M=D" + "\n"
    y_minus_x = "@0" + "\n" + "A=M+1" + "\n" + "D=M" + "\n" + "A=A-1" + "\n" + "D=D-M" + "\n" + "@13" + "\n" + "D=D|M" + "\n" + "D=!D" + "\n" + "@0" + "\n" + "A=M" + "\n" + "M=D" + "\n" + increment_sp()
    machine_code = x_minus_y + y_minus_x
    assembly.write(machine_code)

def handle_lt(label):
    machine_code = pop() + decrement_sp() + "A=M" + "\n" + "D=M-D" + "\n" + "@TRUE_" + str(label) + "\n" + "D; JLT" + "\n" + "(FALSE_" + str(label) + ")" + "\n" + "D=0" + "\n" + "@RETURN_" + str(label) + "\n" + "0; JMP" + "\n" + "(TRUE_" + str(label) + ")" + "\n" + "D=-1" + "\n" + "(RETURN_" + str(label) + ")" + "\n" + push()
    assembly.write(machine_code)

def handle_gt(label):
    machine_code = pop() + decrement_sp() + "A=M" + "\n" + "D=M-D" + "\n" + "@TRUE_" + str(label) + "\n" + "D; JGT" + "\n" + "(FALSE_" + str(label) + ")" + "\n" + "D=0" + "\n" + "@RETURN_" + str(label) + "\n" + "0; JMP" + "\n" + "(TRUE_" + str(label) + ")" + "\n" + "D=-1" + "\n" + "(RETURN_" + str(label) + ")" + "\n" + push()
    assembly.write(machine_code)

def handle_label(label):
    machine_code = "(" + label + ")" + "\n"
    assembly.write(machine_code)

def handle_goto(label):
    machine_code = "@" + label + "\n" + "0; JMP" + "\n"
    assembly.write(machine_code)

def handle_if_goto(label):
    machine_code = pop() + "@" + label + "\n" + "D; JNE" + "\n"
    assembly.write(machine_code)

def handle_return():
    frame = "@1" + "\n" + "D=M" + "\n" + "@13" +"\n" + "M=D" + "\n"
    return_address = "@5" + "\n" + "A=D-A" + "\n" + "D=M" "\n" + "@14" + "\n" + "M=D" + "\n"
    reposition_the_return_value = "@0" + "\n" + "A=M-1" + "\n" + "D=M" + "\n" + "@2" + "\n" + "A=M" + "\n" + "M=D" + "\n"
    reposition_sp = "@2" + "\n" + "D=M" + "\n" + "@0" + "\n" + "M=D+1" + "\n"
    that = "@13" + "\n" + "D=M-1" + "\n" + "A=D" + "\n" + "D=M" + "\n" + "@4" + "\n" + "M=D" + "\n"
    this = "@13" + "\n" + "D=M" + "\n" + "@2" + "\n" + "D=D-A" +  "\n" + "A=D" + "\n" + "D=M" + "\n" + "@3" + "\n" + "M=D" + "\n"
    arg = "@13" + "\n" + "D=M" + "\n" + "@3" + "\n" + "D=D-A" + "\n" + "A=D" + "\n" + "D=M" + "\n" + "@2" + "\n" + "M=D" + "\n"
    lcl = "@13" + "\n" + "D=M" + "\n" + "@4" + "\n" + "D=D-A" + "\n" + "A=D" + "\n" + "D=M" + "\n" + "@1" + "\n" + "M=D" + "\n"
    goto = "@14" + "\n" + "D=M" + "\n" + "A=D" + "\n" + "0; JMP" + "\n"

    machine_code = frame + return_address + reposition_the_return_value + reposition_sp + that + this + arg + lcl + goto

    assembly.write(machine_code)

def handle_function(function_and_number):
    function = function_and_number[:-1]
    number_of_arguments = int(function_and_number[-1])
    
    machine_code = "(" + function + ")" + "\n"
    for i in range(number_of_arguments):
        machine_code += push_constant(0)
    
    assembly.write(machine_code)


def handle_call(function_and_number):
    global return_counter

    function = function_and_number[:-1]
    number_of_arguments = int(function_and_number[-1])

    return_address = "return_" + function + "_" + str(return_counter)

    return_counter += 1


    push_return_address = "@" + return_address + "\n" + "D=A" + "\n" + push()
    push_local = "@1" + "\n" + "D=M" + "\n" + push()
    push_arg = "@2" + "\n" + "D=M" + "\n" + push()
    push_this = "@3" + "\n" + "D=M" + "\n" + push()
    push_that = "@4" + "\n" + "D=M" + "\n" + push()
    reposition_argument = "@" + str(number_of_arguments) + "\n" + "D=A" + "\n" + "@5" + "\n" + "D=D+A" + "\n" + "@0" + "\n" "D=M-D" + "\n" + "@2" + "\n" + "M=D" + "\n"
    reposition_local = "@0" + "\n" + "D=M" + "\n" + "@1" + "\n" + "M=D" + "\n"
    goto_function = "@" + function + "\n" + "0; JMP" + "\n"
    declare_label = "(" + return_address + ")" + "\n"
    machine_code = push_return_address + push_local + push_arg + push_this + push_that + reposition_argument + reposition_local + goto_function + declare_label
    assembly.write(machine_code)
    
def push_constant(number):
    return "@" + str(number) + "\n" + "D=A" + "\n" + "@0" + "\n" + "A=M" + "\n" + "M=D" + "\n" + increment_sp()

def pop_to_memory_segment(index, number):
    return "@" + number + "\n" + "D=A" + "\n" + "@" + str(index) + "\n" + "D=D+M" + "\n" + "@14" + "\n" + "M=D" + "\n" + pop() + "@14" + "\n" + "A=M" + "\n" "M=D" + "\n"

def push_from_memory_segment(index, number):
    return "@" + number + "\n" + "D=A" + "\n" + "@" + str(index) + "\n" + "A=D+M" + "\n" + "D=M" + "\n" + push()

def pop_local(number):
    return pop_to_memory_segment(1, number)

def pop_argument(number):
    return pop_to_memory_segment(2, number)

def pop_this(number):
    return pop_to_memory_segment(3, number)

def pop_that(number):
    return pop_to_memory_segment(4, number)

def pop_temp(number):
    return pop() + "@" + str(int(number)+5) + "\n" + "M=D" + "\n"

def pop_pointer(number):
    return pop() + "@" + str(int(number)+3) + "\n" + "M=D" + "\n"

def pop_static(number, filename):
    return pop() + "@" + filename + "." + str(number) + "\n" + "M=D" + "\n"

def handle_pop(line, filename):
    machine_code = ""
    if line[0:5] == "local":
        machine_code = pop_local(line[5:])
    elif line[0:8] == "argument":
        machine_code = pop_argument(line[8:])
    elif line[0:4] == "this":
        machine_code = pop_this(line[4:])
    elif line[0:4] == "that":
        machine_code = pop_that(line[4:])
    elif line[0:4] == "temp":
        machine_code = pop_temp(line[4:])
    elif line[0:7] == "pointer":
        machine_code = pop_pointer(line[7:])
    elif line[0:6] == "static":
        machine_code = pop_static(line[6:], filename)
    assembly.write(machine_code)

def push_local(number):
    return push_from_memory_segment(1, number)

def push_argument(number):
    return push_from_memory_segment(2, number)

def push_this(number):
    return push_from_memory_segment(3, number)

def push_that(number):
    return push_from_memory_segment(4, number)

def push_temp(number):
    return "@" + str(int(number)+5) + "\n" + "D=M" + "\n" + push()

def push_pointer(number):
    return "@" + str(int(number)+3) + "\n" + "D=M" + "\n" + push()

def push_static(number, filename):
    return "@" + filename + "." + str(number) + "\n" + "D=M" + "\n" + push()

def handle_push(line, filename):
    machine_code = ""
    if line[0:8] == "constant":
        machine_code = push_constant(line[8:])
    elif line[0:5] == "local":
        machine_code = push_local(line[5:])
    elif line[0:8] == "argument":
        machine_code = push_argument(line[8:])
    elif line[0:4] == "this":
        machine_code = push_this(line[4:])
    elif line[0:4] == "that":
        machine_code = push_that(line[4:])
    elif line[0:4] == "temp":
        machine_code = push_temp(line[4:])
    elif line[0:7] == "pointer":
        machine_code = push_pointer(line[7:])
    elif line[0:6] == "static":
        machine_code = push_static(line[6:], filename)
    
    assembly.write(machine_code)

# MAIN PROGRAM



def read_file(vm_file, assembly, filename):
    global label_counter
    global return_counter

    lines = vm_file.readlines()
    for line in lines:
        if line.strip() and not line[0:2] == "//":
            line = line.replace(" ", "")
            line = line.replace('\n', "")
            line = line.replace('\r', "")
            comment = line.find("//")
            if comment != -1:
                line = line[:comment]
            if line[0:3] == "add":
                handle_add()
            elif line[0:4] == "push":
                handle_push(line[4:], filename)
            elif line[0:3] == "pop":
                handle_pop(line[3:], filename)
            elif line[0:2] == "eq":
                handle_eq()
            elif line[0:2] == "lt":
                label_counter += 1
                handle_lt(label_counter)
            elif line[0:2] == "gt":
                label_counter += 1
                handle_gt(label_counter)
            elif line[0:3] == "sub":
                handle_sub()
            elif line[0:3] == "neg":
                handle_neg()
            elif line[0:3] == "and":
                handle_bit_wise_and()
            elif line[0:2] == "or":
                handle_bit_wise_or()
            elif line[0:3] == "not":
                handle_bit_wise_not()
            elif line[0:5] == "label":
                handle_label(line[5:])
            elif line[0:4] == "goto":
                handle_goto(line[4:])
            elif line[0:7] == "if-goto":
                handle_if_goto(line[7:])
            elif line[0:6] == "return":
                handle_return()
            elif line[0:8] == "function":
                handle_function(line[8:])
            elif line[0:4] == "call":
                handle_call(line[4:])
    vm_file.close()

argument = sys.argv[1]

label_counter = 0

return_counter = 1

if os.path.isdir(argument):
    assembly = open(argument + "/" + argument + ".asm", 'w')
    set_sp()
    call_sys_init()
    for filename in os.listdir(argument):
        name_and_suffix = filename.split(".")
        suffix = name_and_suffix[1]

        if suffix == "vm":
            vm_file = open(argument + "/" + filename, 'r')
            read_file(vm_file, assembly, filename)

    assembly.close()
else:
    name_and_suffix = argument.split(".")
    filename = name_and_suffix[0]
    assembly = open(filename + ".asm", 'w')
    set_sp()
    vm_file = open(argument, 'r')
    read_file(vm_file, assembly, filename)
    assembly.close()

# filename = directory_name.split("/")[-1]

# assembly = open(directory_name + "/" + filename + ".asm", 'w')



# set_sp()

# sys_init_exists = Path(directory_name + "/Sys.vm")
# if sys_init_exists.is_file():
#     call_sys_init()

# for filename in os.listdir(directory_name):
#     name_and_suffix = filename.split(".")
#     suffix = name_and_suffix[1]

#     if suffix == "vm":
#         vm_file = open(directory_name + "/" + filename, 'r')
#         read_file(vm_file, assembly, filename)

# assembly.close()

# CODE WRITER