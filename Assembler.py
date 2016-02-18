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
    #NOTE: each line must be nonempty
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

def remove_comment_from_line(instruction):
	position = 0
	for char in instruction:
		if char == " " or char == '/': #instructions must be written without spaces or '/' symbols
			break
		else:
			position+=1
	return instruction[:position] #return a substring without any trailing comments just the instruction

def main():
    machine_code_list = [] #a list that will contain lines of machine code in order
    fileObj = open_file()
    for line in fileObj:
        lines = (line.strip() for line in fileObj) #remove space padding before and after instruction
        lines = list(line for line in lines if line) #make sure a line has something on it before adding to list
    fileObj.close()

    #we now have a list composed of lines of Hack assembly with possible comments after instruction
    for instruction in lines:
        instruction = remove_comment_from_line(instruction)
        output = parse_line(instruction)
        if output != "": #ignore lines with comments or address label declarations
            machine_code_list.append(parse_line(instruction))
    write_list_to_hack(machine_code_list)
