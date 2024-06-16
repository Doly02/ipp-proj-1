#
#  Project:        First project for the course Principles of Programming Languages and OOP
#  File Name:      parser.py
#  Author:         Tomas Dolak
#  Date:           12.2.2024
#  Description:    First project for the course Principles of Programming Languages and OOP,
#                  parse.py converts IPPcode24 input to .XML output.

# Importing libraries
import re
import sys
from Xml import Xml
from Instruction import Instruction

from Xml import MISSING_OR_INVALID_HEADER
from Xml import UNKNOWN_OR_INVALID_INSTRUCTION
from Xml import LEXICAL_OR_SYNTACTIC_ERROR

# Main program
"""
Main function of the program
:return: 0 if the program was successful, 10 if the program was not successful
"""
if not Instruction.ArgumentCheck(len(sys.argv), sys.argv):
    sys.exit(1)


# Variables 
headerOnceFound = False  
HeaderFound = False  
Empty = True

try:
    # Read the input file
    for line in sys.stdin:
        if line:
            Empty = False

            line = Instruction.RemoveComments(line)

            # Remove An End OF Line Character
            line = line.rstrip('\n')
            
            # Header Twice In Source Code 
            if headerOnceFound:
                if re.fullmatch(r".IPPcode24\s*", line):
                    sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                    
            if not HeaderFound:
                if re.fullmatch(r".IPPcode24\s*", line):
                    xmlGenerator = Xml()
                    headerOnceFound = True
                    HeaderFound = True
                    continue
                elif re.match(r"\s*#", line) or line == "":
                    continue 
                else:
                    sys.exit(MISSING_OR_INVALID_HEADER)
                    
            # Split the line into tokens
            if line.strip():
                # Split the line into tokens
                tokens = line.split(' ')
                # Convert the line to upper case -> Used for INSTRUCTIONS Without Operators And Operands (E.g. RETURN, BREAK)
                upperCaseLine = line.upper()
                command = tokens[0]
                command = command.upper()                
                
                # -------------------------------------------------------------- 
                #   DATA-STACK INSTRUCTIONS
                # --------------------------------------------------------------
                if command == "PUSHS":
                    # PUSHS ⟨symb⟩
                    if len(tokens) == 2:
                        if Instruction.ConstantCheck(tokens[1]) or Instruction.VariableCheck(tokens[1]):
                            xmlGenerator.PrintInstruction(command, [tokens[1]])
                        else:
                            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                    else:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        
                elif command == "POPS":
                    # POPS ⟨var⟩
                    if len(tokens) == 2:
                        if Instruction.VariableCheck(tokens[1]):
                            xmlGenerator.PrintInstruction(command, [tokens[1]])
                        else:
                            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                    else:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                    
                elif command == "MOVE":
                    # MOVE ⟨var⟩ ⟨symbol⟩
                    if len(tokens) != 3:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        
                    if not Instruction.VariableCheck(tokens[1]): # ⟨var⟩
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                    if Instruction.VariableCheck(tokens[2]) or Instruction.ConstantCheck(tokens[2]): # ⟨symbol⟩
                        xmlGenerator.PrintInstruction(command, [tokens[1],tokens[2]])
                    else:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                
                # -------------------------------------------------------------- 
                #   FRAME-STACK INSTRUCTIONS & FUNCTION CALLS
                # --------------------------------------------------------------
                elif command == "CREATEFRAME":
                    # Allowed White Characters After The Command 
                    if re.fullmatch(r"CREATEFRAME\s*", upperCaseLine):
                        xmlGenerator.PrintInstruction(command, [])
                    else:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                                                    
                elif command == "PUSHFRAME": 
                    # Allowed White Characters After The Command 
                    if re.fullmatch(r"PUSHFRAME\s*", upperCaseLine):
                        xmlGenerator.PrintInstruction(command, [])
                    else:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                            
                elif command == "POPFRAME":
                    # Allowed White Characters After The Command 
                    if re.fullmatch(r"POPFRAME\s*", upperCaseLine):
                        xmlGenerator.PrintInstruction(command, [])
                    else:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)

                elif command == "DEFVAR":
                    # DEFVAR ⟨var⟩
                    if len(tokens) == 2:
                        if Instruction.VariableCheck(tokens[1]):
                            xmlGenerator.PrintDeclaration(command, [tokens[1]])
                        else:
                            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)                            
                    else:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)   
                        
                elif command == "CALL":
                    # CALL ⟨label⟩
                    if len(tokens) == 2:
                        if not Instruction.LabelCheck(tokens[1]):
                            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        else:
                            xmlGenerator.PrintJump(command, [tokens[1]])
                    else:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)  
                    
                elif command == "RETURN":
                    # Allowed White Characters After The Command 
                    if re.fullmatch(r"RETURN\s*", upperCaseLine):
                        xmlGenerator.PrintInstruction(command, [])
                    else:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
            
                # -------------------------------------------------------------- 
                #   ARITHMETIC INSTRUCTIONS
                # --------------------------------------------------------------
                #SUB ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩
                elif command == "SUB" or command == "ADD":
                    if len(tokens) == 4:
                        if not Instruction.VariableCheck(tokens[1]):
                            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        if not Instruction.VariableCheck(tokens[2]) and not Instruction.ConstantCheck(tokens[2]):
                            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        if not Instruction.VariableCheck(tokens[3]) and not Instruction.ConstantCheck(tokens[3]):
                            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        xmlGenerator.PrintArithmetic(command, tokens[1:])
                    else:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                    
                elif command == "MUL" or command == "IDIV":
                    if len(tokens) == 4:
                        if not Instruction.VariableCheck(tokens[1]):
                            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        if not Instruction.VariableCheck(tokens[2]) and not Instruction.ConstantCheck(tokens[2]):
                            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        if not Instruction.VariableCheck(tokens[3]) and not Instruction.ConstantCheck(tokens[3]):
                            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        xmlGenerator.PrintArithmetic(command, tokens[1:])
                    else:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                    
                elif command == "GT" or command == "LT" or command == "EQ":
                    if len(tokens) == 4:
                        # TODO Check if [var] Is Bool Type?
                        if not Instruction.VariableCheck(tokens[1]):
                            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        if not Instruction.VariableCheck(tokens[2]) and not Instruction.ConstantCheck(tokens[2]):
                            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        if not Instruction.VariableCheck(tokens[3]) and not Instruction.ConstantCheck(tokens[3]):
                            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        xmlGenerator.PrintArithmetic(command, tokens[1:])
                    else:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        
                elif command == "NOT":
                    if len(tokens) == 3:
                        if not Instruction.VariableCheck(tokens[1]):
                            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        if not Instruction.VariableCheck(tokens[2]) and not Instruction.ConstantCheck(tokens[2]):
                            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        xmlGenerator.PrintArithmetic(command, tokens[1:])
                    else:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                
                # ADD ⟨var⟩ ⟨symb1⟩ ⟨symb2⟩   
                elif command == "AND" or command == "OR":
                    if len(tokens) == 4:
                        if not Instruction.VariableCheck(tokens[1]):
                            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        if not Instruction.VariableCheck(tokens[2]) and not Instruction.ConstantCheck(tokens[2]):
                            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        if not Instruction.VariableCheck(tokens[3]) and not Instruction.ConstantCheck(tokens[3]):
                                sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)   
                        xmlGenerator.PrintArithmetic(command, tokens[1:])
                    else:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                
                elif command == "INT2CHAR":
                    if len(tokens) == 3:
                        if not Instruction.VariableCheck(tokens[1]):
                            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        if not Instruction.VariableCheck(tokens[2]) and not Instruction.ConstantCheck(tokens[2]):
                            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        xmlGenerator.PrintArithmetic(command, tokens[1:])
                    else:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        
                elif command == "STRI2INT":
                    if len(tokens) == 4:
                        if not Instruction.VariableCheck(tokens[1]):
                            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        if not Instruction.VariableCheck(tokens[2]) and not Instruction.ConstantCheck(tokens[2]):
                            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        if not Instruction.VariableCheck(tokens[3]) and not Instruction.ConstantCheck(tokens[3]):
                            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        xmlGenerator.PrintArithmetic(command, tokens[1:])
                    else:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                
                # -------------------------------------------------------------- 
                #   INPUT-OUTPUT INSTRUCTIONS
                # --------------------------------------------------------------   
                elif command == "WRITE":
                    if len(tokens) == 2:
                        # WRITE [var] -> Check If [var] Is A Constant Or An Variable
                        if Instruction.ConstantCheck(tokens[1]) or Instruction.VariableCheck(tokens[1]):
                            xmlGenerator.PrintWrite(command, tokens[1])
                        else:
                            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                    else:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        
                elif command == "READ":
                    if len(tokens) == 3:    
                        # READ [var] [type] -> Check If [var] Is A Variable
                        if Instruction.VariableCheck(tokens[1]) and Instruction.TypeCheck(tokens[2]):
                            xmlGenerator.PrintRead(command, [tokens[1], tokens[2]])
                        else:
                            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        #TODO Can I Write "READ int@8 int"?
                    else:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)

                # -------------------------------------------------------------- 
                #   STRING PROCESSING INSTRUCTIONS
                # --------------------------------------------------------------
                elif command == "CONCAT":
                    if len(tokens) != 4:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                    #TODO Please Keep In Mind That Is Just Checked If It Is Possible That Argument Is A Variable
                    #TODO Not, If It Is a REAL Variable!  
                    if not Instruction.VariableCheck(tokens[1]):
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                    
                    if not Instruction.VariableCheck(tokens[2]) and not Instruction.ConstantCheck(tokens[2]):
                        #TODO Here Please Check If It Is A String
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                    
                    if not Instruction.VariableCheck(tokens[3]) and not Instruction.ConstantCheck(tokens[3]):
                        #TODO Here Please Check If It Is A String
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                    xmlGenerator.PrintArithmetic(command, tokens[1:])
                    
                elif command == "STRLEN":
                    if len(tokens) != 3:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        
                    if not Instruction.VariableCheck(tokens[1]):
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        
                    if not Instruction.StringCheck(tokens[2]):
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        
                    xmlGenerator.PrintInstruction(command, [tokens[1], tokens[2]])
                                    
                elif command == "GETCHAR":
                    if len(tokens) != 4:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        
                    if not Instruction.VariableCheck(tokens[1]):
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        
                    if not Instruction.ConstantCheck(tokens[2]):
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                    if not Instruction.ConstantCheck(tokens[3]):
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                    xmlGenerator.PrintInstruction(command, [tokens[1], tokens[2], tokens[3]])
                    
                elif command == "SETCHAR":
                    if len(tokens) != 4:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        
                    if not Instruction.VariableCheck(tokens[1]):
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        
                    if not Instruction.ConstantCheck(tokens[2]):
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)

                    if not Instruction.ConstantCheck(tokens[3]):
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)

                    xmlGenerator.PrintInstruction(command, [tokens[1], tokens[2], tokens[3]])
                   
                # --------------------------------------------------------------
                #   TYPE PROCESSING INSTRUCTIONS
                # --------------------------------------------------------------
                elif command == "TYPE":
                    if len(tokens) != 3:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                    if not Instruction.VariableCheck(tokens[1]):
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        
                    if not Instruction.ConstantCheck(tokens[2]):
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                    #TODO: Check [3]?
                    xmlGenerator.PrintInstruction(command, [tokens[1], tokens[2]])

                # --------------------------------------------------------------
                #   FLOW CONTROL INSTRUCTIONS
                # --------------------------------------------------------------
                elif command == "LABEL":
                    if len(tokens) != 2:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        
                    if not Instruction.LabelCheck(tokens[1]):
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                    else:
                        xmlGenerator.PrintJump(command, [tokens[1]]) 
                    
                elif command == "JUMP": #TODO: Check
                    if len(tokens) != 2:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                         
                    # JUMP [label] -> Check If [label] Could Be A Label
                    if False == Instruction.LabelCheck(tokens[1]):
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                    if Instruction.VariableCheck(tokens[1]) or Instruction.ConstantCheck(tokens[1]):
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                    else:
                        xmlGenerator.PrintJump(command, [tokens[1]])
                    
                elif command == "JUMPIFEQ" or command == "JUMPIFNEQ":
                    if len(tokens) != 4:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        
                    if not Instruction.LabelCheck(tokens[1]):
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                    else:
                        if Instruction.ConstantCheck(tokens[2]) or Instruction.VariableCheck(tokens[2]):
                            if Instruction.ConstantCheck(tokens[3]) or Instruction.VariableCheck(tokens[3]):
                                xmlGenerator.PrintJump(command, [tokens[1], tokens[2], tokens[3]])
                            else:
                                sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        else:
                            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                                
                elif command == "EXIT":
                    if len(tokens) != 2:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                    # TODO: Check If The Argument Is A Constant With Its Value Between 0-9
                    if Instruction.ItsNumber(tokens[1]):
                        xmlGenerator.PrintInstruction(command, [tokens[1]])
                    if Instruction.VariableCheck(tokens[1]) or Instruction.ConstantCheck(tokens[1]):
                        exit(LEXICAL_OR_SYNTACTIC_ERROR)
                    if Instruction.LabelCheck(tokens[1]):
                        exit(LEXICAL_OR_SYNTACTIC_ERROR)
                # --------------------------------------------------------------
                #   DEBUG INSTRUCTIONS
                # --------------------------------------------------------------
                elif command == "DPRINT":
                    if len(tokens) != 2:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                        
                    if not Instruction.ConstantCheck(tokens[1]) and not Instruction.VariableCheck(tokens[1]):
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                    else:
                        xmlGenerator.PrintInstruction(command, [tokens[1]])
                    
                elif command == "BREAK":
                    #TODO: Check If There Are Only 0 Or More White Characters After The Command
                    # Allowed White Characters After The Command 
                    if re.fullmatch(r"BREAK\s*", upperCaseLine):
                        xmlGenerator.PrintInstruction(command, [])
                    else:
                        sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
        
                # --------------------------------------------------------------
                #   OTHERS "INSTRUCTIONS"
                # --------------------------------------------------------------
                elif line == "":
                    continue
                
                # Max. Tokens: [command] [arg1] [arg2] [arg3]
                elif len(tokens) > 4:
                    sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
                else:
                    print(command)
                    sys.exit(UNKNOWN_OR_INVALID_INSTRUCTION)
                        
    # Close .XML
    if not Empty:
        xmlGenerator.print_xml()

except EOFError:
    pass
    
if Empty:
    sys.exit(MISSING_OR_INVALID_HEADER)

#TODO: Check If len(tokens) < 4 ???
