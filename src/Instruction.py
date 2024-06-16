#
#  Project:        First project for the course Principles of Programming Languages and OOP
#  File Name:      Instruction.py
#  Author:         Tomas Dolak
#  Date:           12.2.2024
#  Description:    First project for the course Principles of Programming Languages and OOP,
#                  parse.py converts IPPcode24 input to .XML output.

# Importing libraries
import re
import sys

LEXICAL_OR_SYNTAX_ERROR = 23
MISSING_ARGUMENT = 10

# Function definitions
class Instruction:

    def ItsNumber(string):
        return bool(re.fullmatch(r"^[0-9]$", string))

    def VariableCheck(variable):
        """
        Function checks if the variable is valid
        :param variable: string
        :return: True if the variable is valid, False otherwise
        """
        if re.match(r"(TF|LF|GF)@[-a-zA-Z0-9_$&%?!]+", variable):
            return True
        else:
            return False
    
    def LabelCheck(label):
        if re.match(r"[-a-zA-Z0-9_$&%?!]+$", label):
            return True
        else:
            return False

    def TypeCheck(type):
        """
        Function checks if the type is valid
        :param type: string
        :return: True if the type is valid, False otherwise
        """
        if re.match(r"(int|bool|string)", type):
            return True
        else:
            return False
        
    def ConstantCheck(variable):
        """
        Function checks if the variable is constant
        :param variable: string
        :return: True if the variable is valid, False otherwise
        """
        if re.match(r"nil@nil$", variable):
            return True
        elif re.match(r"bool@(true|false)$", variable):
            return True
        elif re.match(r"int@([-+]?[0-9]+)$", variable):         # Decimal
            return True
        elif re.match(r"int@([-+]?0[oO][0-7]+)$", variable):         # Octal
            return True
        elif re.match(r"int@([-+]?0[xX][0-9a-fA-F]+)$", variable):   # Hexadecimal
            return True
        elif re.match(r"^string@", variable):
            # Ověření, že všechna zpětná lomítka jsou následována třemi číslicemi
            if re.match(r"^string@((\\[0-9]{3})|[^\\#])*$", variable):
                return True
            else:
                sys.exit(LEXICAL_OR_SYNTAX_ERROR)
        elif re.match(r"^int@$", variable):     # Edge Case Empty Int
            sys.exit(LEXICAL_OR_SYNTAX_ERROR)
        elif re.match(r"^bool@$", variable):    # Edge Case Empty Bool
            sys.exit(LEXICAL_OR_SYNTAX_ERROR)
        return False

    def StringCheck(variable):
        """
        Function checks if the variable is string
        :param variable: string
        :return: True if the variable is valid, False otherwise
        """
        if re.match(r"string@.*", variable):
            return True
        else:
            return False
        
    def ArgumentCheck(argc,argv):
        """
        Function checks if the number of arguments is correct
        :param argc: int
        :param argv: list
        :return: True if the number of arguments is correct, False otherwise
        """
        if argc > 1:
            if argc == 2 and argv[1] == "--help":
                print("Usage: python3.8 parse.py <input_file>")
                sys.exit(0) 
            else:
                #TODO Check CORRECT Return Value
                sys.exit(MISSING_ARGUMENT)
        else:
            return True

    def ValidUnicode(value):
        try:
            _ = chr(value) 
            return True  
        except ValueError:  # Catch Exception If Value Is Not Valid
            return False
        
    # Removes Comments
    def RemoveComments(line):
        """
        Function removes comments from the line
        :param line: string
        :return: string without comments
        """
        comment_start = line.find('#')
        if comment_start != -1:
            return line[:comment_start].rstrip()
        else:
            return line

