"""
Title: PM_A_instruction_to_machine_language
Author: Denny Hood
Class: CS 271
Description: This module has a function to convert an A instruction into machine
code.
"""
#dictionary of addresses for reserved words
reserved_symbol_table={"R0":0,"R1":1,"R2": 2,"R3": 3,"R4": 4,"R5": 5,"R6": 6,
                       "R7": 7,"R8": 8,"R9": 9,"R10": 10,"R11": 11,"R12": 12,
                       "R13": 13,"R14": 14,"R15": 15,"SP":0,"LCL":1,"ARG":2,
                       "THIS":3,"THAT":4,"SCREEN":16384,"KBD":24576}
#dictionary of addresses for user defined symbols
user_symbol_table={}

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

def convert_to_16bit_string(value):
    """Author: Denny Hood
       pad output with 0(s) on left to make 16 bit string"""
    return '{0:016b}'.format(value)
        
def generate_A_instruction(symbol):
    """Author: Denny Hood
       this function is designed to generate an A instruction (in machine code)
       as a 16 bit binary string using the syntax in the HACK assembly language.
       This function will check to see if the symbol is a literal, reserved or
       user defined symbol. A literal will return its value in binary. A reserved
       symbol will return the value in binary according to it's assigned address.
       Finally, if user defined symbol is passed in, the function will check
       if it is already in the user defined symbol dictionary and will return the
       value otherwise, it will add the symbol to the dictionary with its
       value calculated sequentially starting at address 16 and will return the
       new key's value as a 16bit binary string."""
    #check to see if symbol is an integer
    if symbol.isdigit():
        return convert_to_16bit_string(int(symbol))
    
    #take symbol and compare to reserved_symbol_table
    elif is_in_dictionary(symbol,reserved_symbol_table) == True:
        return convert_to_16bit_string(reserved_symbol_table[symbol])
    
    else: #we need to check if symbol is already in user table
        if is_in_dictionary(symbol,user_symbol_table) == True:
            return convert_to_16bit_string(user_symbol_table[symbol])
        
        else: #symbol is not in table, need to add to user_symbol_table dictionary
            #calculate address of next available memory
            nextMemoryLocation = (len(user_symbol_table)+16)
            #nextMemoryLocation = 16 + number of items in user_symbol_table
            user_symbol_table[symbol] = nextMemoryLocation  
            return convert_to_16bit_string(user_symbol_table[symbol])
