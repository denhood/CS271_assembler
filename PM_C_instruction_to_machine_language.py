"""
Title: PM_C_instruction_to_machine_language
Author: Denny Hood
Class: CS 271
Description:
"""
comp_a_0_dict = {"0":"101010","1":"111111","-1":"111010","D":"001100","A":"110000",
                 "!D":"001101","!A":"110001","-D":"001111","-A":"110011","D+1":"011111",
                 "A+1":"110111","D-1":"001110","A-1":"110010","D+A":"000010","A+D":"000010",
                 "D-A":"010011","A-D":"000111","D&A":"000000","D|A":"010101"}
comp_a_1_dict = {"M":"110000","!M":"110001","-M":"110011","M+1":"110111",
                 "M-1":"110010","D+M":"000010","D-M":"010011","M-D":"000111",
                 "D&M":"000000","D|M":"010101"}
dest_dict     = {"":"000","M":"001","D":"010","MD":"011","A":"100","AM":"101","AD":"110","AMD":"111"}
jump_dict     = {"":"000","JGT":"001","JEQ":"010","JGE":"011","JLT":"100","JNE":"101","JLE":"110",
                 "JMP":"111"}

def is_in_dictionary(symbol,dictionary):
    """Author: Denny Hood
       this function takes in two parameters a string for symbol and a python
       dictionary for dictionary. The function will compare the symbol string
       to the keys of the dictionary one at a time and if it finds a match, it
       will return True."""
    inDictionary = False
    #compare symbol to keys in reserved_symbol_table
    for key in dictionary:
        #check to see if symbol is in dictionary
        if str(key) == symbol:
            inDictionary = True
            break
    return inDictionary
def is_assignment(instruction):
    """Author: Denny Hood
       this function determines if a C instruction is an assignment"""
    for char in instruction:
        if char == "=":
            return True
        #else instruction doesn't have = sign
    return False

def is_jump(instruction):
    """Author: Denny Hood
       this function determines if a C instruction is a jump statement"""
    for char in instruction:
        if char == ";":
            return True
        #else instruction doesn't have ; sign
    return False

def convert_comp_to_bin(compIn): #compIn will the right side of '=' symbol
    """Author: Denny Hood"""
    #function will return a 7 digit binary string
    #first, we need to determine if a=0 or a=1
    #look through compIn for 'M' for a=1 instruction
    for char in compIn:
        if char == 'M':
            #we may have an a=1 instruction
            #now look in comp_when_a_1 dictionary
            for a1key in comp_a_1_dict:
                if compIn == a1key:
                    return '1' + comp_a_1_dict[a1key] #a=1
    #look through compIn for 'A' for a=0 instruction
    for char in compIn:
        if char == 'A' or char == 'D' or char == '0' or char == '1':
            #we may have an a=0 instruction
            #now look in comp_when_a_0 dictionary
            for a0key in comp_a_0_dict:
                if compIn == a0key:
                    return '0' + comp_a_0_dict[a0key] #a=0
    #else, we don't have a valid comp string
    return "COMPERR"

def convert_dest_to_bin(destIn):
    """Author: Denny Hood"""
    #destination is left side of '=' symbol
    for destKey in dest_dict: 
        if destIn == destKey:#compare destIn to keys in dest dictionary
            return dest_dict[destKey] #return binary string in dictionary
    return 'DER' #error checking

def convert_jump_to_bin(jumpIn):
    """Author: Denny Hood"""
    #jump mnemonic is right side of ';' symbol
    for jumpMnemonic in jump_dict:
        if jumpIn == jumpMnemonic:
            return jump_dict[jumpMnemonic]
    return 'JER' #error checking

def separate_argument(argumentIn): #argumentIn is a string
    """Author: Denny Hood"""
    #function will return a list of two substrings: the left side of argumentIn and the right side
    #where left side of list is dest and right side is comp
    position = 0
    returnList = []
    for char in argumentIn:
        if char == '=' or char == ';': #stop the loop
            break
        else:
            position+=1
    returnList.append(argumentIn[0:position])
    returnList.append(argumentIn[(position+1):len(argumentIn)])
    return returnList


def generate_C_instruction(arithmetic_operation):
    """Author: Denny Hood
       This function takes in a string as arithmetic_operation and parse it and
       return a 16bit binary string."""
    argumentList=[] #clear argumentList
    #determine if assignment or jump
    if is_assignment(arithmetic_operation) == True:
        #if arithmetic_operation is assignment, we need to convert to 16bit C instruction ending with "000"
        #parse assignment into parts:
        argumentList = separate_argument(arithmetic_operation) #left and Right Arguments are a list where argumentList[0]=dest and argrumentList[1]=comp
        return("111"+convert_comp_to_bin(argumentList[1])+convert_dest_to_bin(argumentList[0])+"000") #ignore jump bits
        
    elif is_jump(arithmetic_operation) == True:
        #if arithmetic_operation is jump, we need to convert to 16bit C instruction with "000" in positions 10-12 (destination)
        #parse jump into compare bits and jump mnemonic
        argumentList = separate_argument(arithmetic_operation) #left and Right Arguments are a list where argumentList[0]=comp and argumentList[1]=jump mnemonic
        return("111"+convert_comp_to_bin(argumentList[0])+"000"+convert_jump_to_bin(argumentList[1])) #ignore dest bits
    else:
        print("invalid instruction!")
        return 0
