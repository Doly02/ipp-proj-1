#
#  Project:        First project for the course Principles of Programming Languages and OOP
#  File Name:      Xml.py
#  Author:         Tomas Dolak
#  Date:           12.2.2024
#  Description:    First project for the course Principles of Programming Languages and OOP,
#                  parse.py converts IPPcode24 input to .XML output.

# Libraries
import xml.etree.ElementTree as ET
from xml.dom import minidom
import sys

# Macros
MISSING_OR_INVALID_HEADER = 21
UNKNOWN_OR_INVALID_INSTRUCTION = 22
LEXICAL_OR_SYNTACTIC_ERROR = 23
CORRECT = 0


class Xml:
    def __init__(self):
        self.root = ET.Element("program", language="IPPcode24")
        self.tree = ET.ElementTree(self.root)
        self.__order = 1
    
    
        
    def PrintInstruction(self, instruction, args):
        """ Prints Instructions Use For: DATA-STACK INSTRUCTIONS, FRAME-STACK INSTRUCTIONS,
            STRING PROCESSING INSTRUCTIONS, TYPE PROCESSING INSTRUCTIONS, DEBUG INSTRUCTIONS,
            And Instructions Without Arguments (CREATEFRAME, PUSHFRAME, POPFRAME, RETURN, BREAK)           
        Args:
            instruction (str): Operation Code Of Instruction
            args (tuple): String With Instructions Parameters

        Returns:
            none: If Failed, Exits The Program With Error Code 23
        """
        if (instruction == "GETCHAR"):
            retVal = self.GetCharCheck(instruction,args)
            if (retVal == False):
                sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
        if (instruction == "SETCHAR"):
            retVal = self.SetCharChecker(instruction,args)
            if (retVal == False):
                sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)    
    
        instruction_element = ET.SubElement(self.root, "instruction", order=str(self.__order), opcode=instruction)
        # Edge Cases For Instructions With Arguments
        if len(args) > 3:
            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
        if not args:
            # Filter Possible Instructions Without Arguments
            if instruction not in ["CREATEFRAME", "PUSHFRAME", "POPFRAME", "RETURN", "BREAK"]:
                sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)  # Ukončení programu s chybou
            else:
                # Trick With Space To Avoid Empty Tags
                instruction_element.text = ''
        else:
            for index, argument in enumerate(args, start=1):
                # Set Type & Value Of The Argument 
                argument_type = self.ReturnType(argument)
                argument_value = self.ReturnValue(argument)
                ET.SubElement(instruction_element, f"arg{index}", type=argument_type).text = argument_value
        self.__order += 1
    
     
            
    def ReturnType(self,argument):
        """Returns The Data Type Of The Argument

        Args:
            argument (str): Argument of Instruction

        Returns:
            str: If Constant The Data Type, If Variable Then "var", If Failed, Exits The Program With Error Code 23
        """
        type = argument.split('@', 1)
        if type[0] == "int" or type[0] == "bool" or type[0] == "string" or type[0] == "nil":
            return type[0]
        elif type[0] == "GF" or type[0] == "LF" or type[0] == "TF":
            return "var"
        else:
            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
    
    
    
    def ReturnValue(self, argument):
        """
        Returns the Value of The Given Argument.

        Args:
            argument (str): The Input Argument to Process.

        Returns:
            str: The processed value of the argument. If Failed Then Exits The Program With Error Code 23
        """
        splittedArg = argument.split('@', 1)
        if splittedArg[0] == "int" or splittedArg[0] == "bool" or splittedArg[0] == "string" or splittedArg[0] == "nil":
            # If The Argument Is String, We Need To Update It (Change &lt and &gt to < and >)
            return splittedArg[1]
        elif splittedArg[0] == "GF" or splittedArg[0] == "LF" or splittedArg[0] == "TF":
            return argument
        else:
            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
    
    
        
    def PrintJump(self, instruction, args):
        """Creates XML Element For JUMP, JUMPIFEQ, JUMPIFNEQ And CALL Instructions.

        Args:
            instruction (str): Operation Code Of Instruction
            args (tuple): String With Instructions Parameters
        """
        if not args:
            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR) 
        else:
            instruction_element = ET.SubElement(self.root, "instruction", order=str(self.__order), opcode=instruction.upper())
            if instruction in ["CALL", "LABEL","JUMP"]:
                # Pro CALL a LABEL se očekává pouze jeden argument typu label
                ET.SubElement(instruction_element, "arg1", type="label").text = args[0]
            elif instruction in ["JUMPIFEQ", "JUMPIFNEQ"]:
                # Pro JUMPIFEQ a JUMPIFNEQ se očekává první argument typu label a další argumenty
                for index, argument in enumerate(args, start=1):
                    arg_type = "label" if index == 1 else self.ReturnType(argument)  # První argument je vždy typu label
                    arg_value = argument if index == 1 else self.ReturnValue(argument)
                    ET.SubElement(instruction_element, f"arg{index}", type=arg_type).text = arg_value
        self.__order += 1
    
    
    def PrintRead(self, instruction, args):
        """Creates XML Element For PRINT Instruction.

        Args:
            instruction (str): Operation Code Of Instruction
            args (tuple): String With Instructions Parameters
        """
        if not args or len(args) < 2:
            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR) 
        else:
            instruction_element = ET.SubElement(self.root, "instruction", order=str(self.__order), opcode=instruction.upper())
            # Předpokládáme, že první argument je proměnná a druhý je typ
            ET.SubElement(instruction_element, "arg1", type="var").text = args[0]
            ET.SubElement(instruction_element, "arg2", type="type").text = args[1]
        self.__order += 1


    def PrintArithmetic(self, instruction, args):
        """Creates XML Element For Arithmetic & Logic Instructions.

        Args:
            instruction (str): Operation Code Of Instruction
            args (tuple): String With Instructions Parameters
        """
        # Check If Operands That Will Be ADD or SUB Are Not Strings
        correct = False
        correct = self.CheckAritmehticOperarands(instruction, args)            
        if (correct == False):
            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
              
        instruction_element = ET.SubElement(self.root, "instruction", order=str(self.__order), opcode=instruction.upper())
        if instruction == "NOT": #TODO: Check Other Arithmetic Instructions! (2 Operands), Maybe Check Var/Const In Possible
            if len(args) != 2:
                sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)
        for index, argument in enumerate(args, start=1):
            argument_type = self.ReturnType(argument)
            argument_value = self.ReturnValue(argument)
            ET.SubElement(instruction_element, f"arg{index}", type=argument_type).text = argument_value
        self.__order += 1


    def PrintWrite(self, instruction, args):
        """Creates XML Element For WRITE Instruction.

        Args:
            instruction (str): Operation Code Of Instruction
            args (tuple): String With Instructions Parameters
        """
        instruction_element = ET.SubElement(self.root, "instruction", order=str(self.__order), opcode=instruction.upper())

        arg_type = self.ReturnType(args)
        arg_value = self.ReturnValue(args)
        # Pro typy "bool", "int", "string" použijeme přímo hodnoty
        if arg_type == "bool" or arg_type == "int" or arg_type == "string" or arg_type == "nil":
            ET.SubElement(instruction_element, "arg1", type=arg_type).text = arg_value
        # Pro typy "GF", "LF", "TF" se očekává, že celý argument bude v 'args'
        elif arg_type == "var":
            ET.SubElement(instruction_element, "arg1", type="var").text = args
        else:
            sys.exit(LEXICAL_OR_SYNTACTIC_ERROR)  # Neznámý nebo neplatný typ
        self.__order += 1


    def PrintDeclaration(self, instruction, args):
        """Creates XML Element For Variable Declaration (Instruction DEFVAR).

        Args:
            instruction (str): Operation Code Of Instruction
            args (tuple): String With Instructions Parameters
        """
        instruction_element = ET.SubElement(self.root, "instruction", order=str(self.__order), opcode=instruction.upper())
        for argument in args:
            argument_type = self.ReturnType(argument)
            argument_value = self.ReturnValue(argument)
            ET.SubElement(instruction_element, "arg1", type=argument_type).text = argument_value
        self.__order += 1

            
    def print_xml(self):
        """Prints XML Tree To Standard Output.
        """
        rough_string = ET.tostring(self.root, encoding="unicode", method="xml")
        # Použití minidom pro hezké formátování
        reparsed = minidom.parseString(rough_string)
        # Výpis s XML deklarací a odsazením
        print(reparsed.toprettyxml(indent="    ", encoding="UTF-8").decode("UTF-8"))
        sys.exit(CORRECT)
            
    def CheckAritmehticOperarands(self, instruction, args):
        if (instruction == "ADD" or instruction == "SUB" or instruction == "MUL" or instruction == "IDIV"):
            checkOperand1 = self.ReturnType(args[1])
            checkOperand2 = self.ReturnType(args[2])
            if (checkOperand1 == "int" and checkOperand2 == "int"):
                correct = True
            elif (checkOperand1 == "var" or checkOperand2 == "var"):
                
                if (checkOperand1 == "var" and checkOperand2 == "var"):
                    correct = True
                    
                elif (checkOperand1 == "var" and checkOperand2 == "int"):
                    correct = True
                    
                elif (checkOperand1 == "int" and checkOperand2 == "var"):
                    correct = True
                    
        elif (instruction == "LT" or instruction == "GT" or instruction == "EQ"):
            checkOperand1 = self.ReturnType(args[1])
            checkOperand2 = self.ReturnType(args[2])
            if (checkOperand1 == checkOperand2):
                correct = True
            elif (checkOperand1 == "var" or checkOperand2 == "var"):
                correct = True
                    
        elif (instruction == "AND" or instruction == "OR"):
            checkOperand1 = self.ReturnType(args[1])
            checkOperand2 = self.ReturnType(args[2])
            if (checkOperand1 == "bool" and checkOperand2 == "bool"):
                correct = True
            elif (checkOperand1 == "var" or checkOperand2 == "var"):
                if (checkOperand1 == "var" and checkOperand2 == "var"):
                    correct = True
                    
                elif (checkOperand1 == "var" and checkOperand2 == "bool"):
                    correct = True
                    
                elif (checkOperand1 == "bool" and checkOperand2 == "var"):
                    correct = True
                    
        elif (instruction == "NOT"):
            checkOperand1 = self.ReturnType(args[1])
            if (checkOperand1 == "bool"):
                correct = True
            elif (checkOperand1 == "var"):
                correct = True
                
        elif (instruction == "STRI2INT"):
            checkOperand1 = self.ReturnType(args[1])
            checkOperand2 = self.ReturnType(args[2])
            if (checkOperand1 == "string" and checkOperand2 == "int"):
                correct = True
            elif (checkOperand1 == "var" or checkOperand2 == "var"):
                if (checkOperand1 == "var" and checkOperand2 == "var"):
                    correct = True
                    
                elif (checkOperand1 == "var" and checkOperand2 == "int"):
                    correct = True
                    
                elif (checkOperand1 == "string" and checkOperand2 == "var"):
                    correct = True
        elif (instruction == "INT2CHAR"):
            checkOperand1 = self.ReturnType(args[0])
            checkOperand2 = self.ReturnType(args[1])
            if (checkOperand1 == "var" and checkOperand2 == "int"):
                correct = True
            elif (checkOperand1 == "var" and checkOperand2 == "var"):
                correct = True
        elif (instruction == "CONCAT"):
            checkOperand1 = self.ReturnType(args[1])
            checkOperand2 = self.ReturnType(args[2])
            if (checkOperand1 == "string" and checkOperand2 == "string"):
                correct = True
            elif (checkOperand1 == "var" or checkOperand2 == "var"):
                if (checkOperand1 == "var" and checkOperand2 == "var"):
                    correct = True
                    
                elif (checkOperand1 == "var" and checkOperand2 == "string"):
                    correct = True
                    
                elif (checkOperand1 == "string" and checkOperand2 == "var"):
                    correct = True
                    
    def GetCharCheck(self,instruction,args):
        if (instruction == "GETCHAR"):
            operand1 = self.ReturnType(args[0])
            operand2 = self.ReturnType(args[1])
            operand3 = self.ReturnType(args[2])
            if (operand1 == "var"):
                if (operand2 == "string" or operand2 == "var"):
                    if (operand3 == "int" or operand3 == "var"):
                        return True
        return False
    
    def SetCharChecker(self,instruction,args):
        if (instruction == "SETCHAR"):
            operand1 = self.ReturnType(args[0])
            operand2 = self.ReturnType(args[1])
            operand3 = self.ReturnType(args[2])       
            if (operand1 == "var"):
                if (operand2 == "int" or operand2 == "var"):
                    if (operand3 == "string" or operand3 == "var"):
                        return True
        return False