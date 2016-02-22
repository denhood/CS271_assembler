"""
Title: Assembler
Authors: Denny Hood, Harold Smith
Class: CS 271
Description:The main program of the assembler.

NOTE:missing address labels stored in memory
"""

import PM_A_instruction_to_machine_language as A_inst
import PM_C_instruction_to_machine_language as C_inst

def open_file():
    fileName = input("Input filename: ")
    if fileName[len(fileName)-4:len(fileName)] == '.asm':
        try:
            filePtr = open(fileName,"r") #we don't want to modify .asm file
            return filePtr
        except IOError:
            print ("Error: ",fileName," does not exist.")
            return -1
    else:
        print("Error: ",fileName," does not appear to be a '.asm' file.")
        return -2

def parse_line(lineIn):
    #determine if lineIn is an address label, a instruction, c instruction or a comment
    #return value is 16bit machine code
    if len(lineIn) > 0:#NOTE: each line must be nonempty
        if lineIn[0] == '(': #we have an address label
            #print("label")
            return ""
        elif lineIn[0] == '@': #we have an a instruction
            #print("ainst", A_inst.generate_A_instruction(lineIn[1:])) #ignore @ symbol
            return A_inst.generate_A_instruction(lineIn[1:])
        elif lineIn[0] == '/' and lineIn[1] == '/': #we have a comment
            #print("comment")
            return ""
        else: # we may have a c instruction
            #print("cinst", C_inst.generate_C_instruction(lineIn))
            return C_inst.generate_C_instruction(lineIn)
    
def write_list_to_hack(listIn):
    outputFileName = input("enter output name withhout extension: ")
    try:
        outputFileName+=".hack" #add .hack extension
        filePtr = open(outputFileName, "w")
        for line in listIn:
            filePtr.write(line)
            filePtr.write("\n")
        filePtr.close()
        print('file successfully written')
    except IOError:
        print("Error: could not write to ",outputFileName)
        return -1

def remove_comment_from_line(fileIn):
    line_list = []
    for line in fileIn:
        line = line.strip() #remove space padding before and after instruction
        if line != "": #make sure a line has something on it before adding to list
            if line[0] != '/':
                tmp_list = line.partition(' ')
                tmp_line = tmp_list[0]
                if tmp_line[len(tmp_line)-1] == '\t': #check to see is a tab was left
                    tmp_line = tmp_line[:len(tmp_line)-1]
                line_list.append(tmp_line)
    return line_list

def add_labels_to_dictionary(command_list, symbol_dict):
    for line in command_list:
        if line[0] == '(':
            ProgCount = command_list.index(line)
            symbol_dict[line[1:len(line)-1]]=ProgCount
            command_list.remove(line)

def main():
    machine_code_list = [] #a list that will contain lines of machine code in order
    fileObj = open_file()
    #read in file ignoring comments
    line_list = remove_comment_from_line(fileObj) #line list should just be a list of address labels or commands
    fileObj.close()
    #we now have a list composed of lines of Hack assembly without comments after instruction
    add_labels_to_dictionary(line_list, A_inst.user_symbol_table)
    
    for instruction in line_list:
        output = parse_line(instruction)
        if output != "": #ignore lines with comments or address label declarations
            machine_code_list.append(parse_line(instruction))
    write_list_to_hack(machine_code_list)
