# Autor: Filip Botlo
# Login: xbotlo01
# Dátum: 12.3.2024
# Popis: Skript v jazyku Python na analýzu a manipuláciu s XML a inštrukciami jazyka IPPcode24
import sys
import re
import xml.etree.ElementTree as ET

# Funkcia special_chars(s) slúži na nahradenie špeciálnych XML znakov v reťazci s
def special_chars(s):
    s = s.replace('&', "&amp;")
    s = s.replace('>', "&gt;")
    s = s.replace('<', "&lt;")
    s = s.replace('"', "&quot;")
    s = s.replace("'", "&apos;")
    return s

# Trieda XMLVisitor slúži na prechádzanie inštrukcií a ich prevod do XML formátu, pôvodne snaha o návrhový typ návštevník
class XMLVisitor:
    def __init__(self):
        self.xml_program = ET.Element("program")
        self.xml_program.set("language", "IPPcode24")
        self.order_count = 0
        
    def visit_instruction(self, instruction):
        instruction_elem = ET.Element("instruction")
        instruction_elem.set("order", str(instruction.order))
        instruction_elem.set("opcode", instruction.opcode)
        self.xml_program.append(instruction_elem)
        for arg in instruction.args:
            arg_elem = ET.SubElement(instruction_elem, "arg")
            arg_elem.text = special_chars(arg["value"])
            arg_elem.set("type", arg["type"])

    def to_xml(self):
        xml_tree = ET.ElementTree(self.xml_program)
        return xml_tree

# Trieda Instruction reprezentuje jednu inštrukciu v programe s jej poradím a opcode.
class Instruction:
    def __init__(self, order, opcode):
        self.order = order
        self.opcode = opcode
        self.args = []

    def add_argument(self, arg, arg_type):
        self.args.append({"value": arg, "type": arg_type})
        
# Trieda XMLProgram uchováva zoznam inštrukcií a zoznam návestí (labels).
class XMLProgram:
    def __init__(self):
        self.instructions = []
        self.labels_array = []

    def add_instruction(self, instruction):
        self.instructions.append(instruction)

    def add_label(self, label):
        self.labels_array.append(label)

class IPPParser:
    # Funkcia na inicializáciu parsera.
    def __init__(self):
        # Inicializácia premenných pre sledovanie stavu spracovania, pôvodne mali byť súČasťou STATP
        self.loc = 0
        self.comments = 0
        self.has_content = False
        self.order_count = 0
        self.jumps = 0
        self.labels = 0
        self.program = XMLProgram()
        
    # Funkcia na spracovanie jednej inštrukcie.
    def parse_instruction(self, line):
        self.loc += 1
        line = line.strip()
        self.comments += line.count("#")
        line = re.sub("#.*", "", line).rstrip()

        if not line:
            return

        if not self.has_content:
            self.has_content = True

        if ".IPPcode24" in line:
            sys.exit(23)
            
        # Rozdelenie riadku na časti podľa medzier.
        instruction_parts = line.split()
        opcode = instruction_parts[0].upper()
        self.order_count += 1

        # Vytvorenie inštancie inštrukcie.
        instruction = Instruction(self.order_count, opcode)

        # Rozdeľovanie spracovania podľa opcode.
        if opcode in ["CREATEFRAME", "PUSHFRAME", "POPFRAME", "RETURN", "BREAK"]:
            self.handle_frame_instructions(instruction, instruction_parts)
        elif opcode in ["DEFVAR", "POPS"]:
            self.handle_defvar_pops(instruction, instruction_parts)
        elif opcode in ["CALL", "LABEL", "JUMP"]:
            self.handle_call_label_jump(instruction, instruction_parts)
        elif opcode == "PUSHS":
            self.handle_pushs(instruction, instruction_parts)
        elif opcode == "EXIT":
            self.handle_exit(instruction, instruction_parts)
        elif opcode == "DPRINT":
            self.handle_dprint(instruction, instruction_parts)
        elif opcode == "WRITE":
            self.handle_write(instruction, instruction_parts)
        elif opcode in ["MOVE", "INT2CHAR", "STRLEN", "TYPE", "NOT"]:
            self.handle_unary_instructions(instruction, instruction_parts)
        elif opcode in ["ADD", "SUB", "MUL", "IDIV"]:
            self.handle_arithmetic_operation(instruction, instruction_parts)
        elif opcode in ["LT", "GT", "EQ", "AND", "OR", "STRI2INT", "CONCAT", "GETCHAR", "SETCHAR"]:
            self.handle_binary_operations(instruction, instruction_parts)
        elif opcode == "READ":
            self.handle_read(instruction, instruction_parts)
        elif opcode in ["JUMPIFEQ", "JUMPIFNEQ"]:
            self.handle_jumpifeq_jumpifneq(instruction, instruction_parts)
        else:
            sys.exit(23)
            
        # Pridanie spracovanej inštrukcie do zoznamu inštrukcií.
        self.program.add_instruction(instruction)

    # Nasledujúce funkcie spracúvajú inštrukcie s argumentmi a ich lexikálnu a syntaktickú správnosť
    def handle_frame_instructions(self, instruction, instruction_parts):
        if len(instruction_parts) != 1:
            sys.exit(23)
        if instruction.opcode == "RETURN":
            self.jumps += 1

    def handle_defvar_pops(self, instruction, instruction_parts):
        if len(instruction_parts) != 2:
            sys.exit(23)
        if not re.match('^(GF|LF|TF)@[A-Za-z_$&%*!?-][A-Za-z0-9_$&%*!?-]*$', instruction_parts[1]):
            sys.exit(23)
        instruction.add_argument(instruction_parts[1], "var")

    def handle_call_label_jump(self, instruction, instruction_parts):
        if len(instruction_parts) != 2:
            sys.exit(23)
        if not re.match('^[A-Za-z_$&%*!?-][A-Za-z0-9_$&%*!?-]*$', instruction_parts[1]):
            sys.exit(23)
        if instruction.opcode == "LABEL":
            if instruction_parts[1] not in self.program.labels_array:
                self.program.add_label(instruction_parts[1])
                self.labels += 1
        else:
            self.jumps += 1
        instruction.add_argument(instruction_parts[1], "label")

    def handle_pushs(self, instruction, instruction_parts):
        if len(instruction_parts) != 2:
            sys.exit(23)
        if "@" not in instruction_parts[1]:
            sys.exit(23)
        arg_type, arg_value = instruction_parts[1].split('@', 1)
        if arg_type in ["int", "nil", "bool", "string"]:
            instruction.add_argument(arg_value, arg_type)
        elif arg_type not in ["int", "nil", "bool", "string"]:
            instruction.add_argument(instruction_parts[1], "var")
        if arg_type == "int":
            if not re.match(r'^-?(0[xX][\da-fA-F]+|0[oO][0-7]+|\d+)$', arg_value):  
                sys.exit(23)

    def handle_exit(self, instruction, instruction_parts):
        if len(instruction_parts) != 2:
            sys.exit(23)
        if "@" not in instruction_parts[1]:
            sys.exit(23)
        arg_type, arg_value = instruction_parts[1].split('@', 1)
        if arg_type not in ["int", "nil", "bool"]:
            sys.exit(23)
        instruction.add_argument(arg_value, arg_type)

    def handle_dprint(self, instruction, instruction_parts):
        if len(instruction_parts) != 2:
            sys.exit(23)
        if "@" not in instruction_parts[1]:
            sys.exit(23)
        arg_type, arg_value = instruction_parts[1].split('@', 1)
        if arg_type not in ["int", "nil", "bool", "string"]:
            sys.exit(23)
        instruction.add_argument(arg_value, arg_type)

    # Pri testovaní WRITE sa vyskytovali problémy, tak som tu nakoniec vypísal regul=erne výrazy pre jednotlivé symboly
    def handle_write(self, instruction, instruction_parts):
        if len(instruction_parts) != 2:
            sys.exit(23)
        arg_value = instruction_parts[1]
        if "@" not in arg_value:
            sys.exit(23)
        symb_type, _ = arg_value.split("@", 1)
        patterns = {
            "int": r"^int@([+-]?(0o[0-7]+|0x[0-9a-fA-F]+|[0-9]+))$",
            "bool": r"^bool@(true|false)$",
            "string": r"^string@((?![#\s\\])[^\x00-\x1F\x7F]|\\[0-2][0-9]{2}|\\03[0-5]|\\09[2])*$",
            "GF": r"^(GF|LF|TF)@[_\-$&%*!?a-zA-Z][_\-\$&%*!?a-zA-Z0-9]*$",
            "LF": r"^(GF|LF|TF)@[_\-$&%*!?a-zA-Z][_\-\$&%*!?a-zA-Z0-9]*$",
            "TF": r"^(GF|LF|TF)@[_\-$&%*!?a-zA-Z][_\-\$&%*!?a-zA-Z0-9]*$",
            "nil": r"^nil@nil$",
        }
        pattern = patterns.get(symb_type)
        if not pattern:
            sys.exit(23)
        if not re.match(pattern, arg_value):
            sys.exit(23)
        if symb_type in ["int", "nil", "bool", "string"]:
            instruction.add_argument(_, symb_type)
        else:
            instruction.add_argument(arg_value, "var")

    def handle_unary_instructions(self, instruction, instruction_parts):
        if len(instruction_parts) != 3:
            sys.exit(23)
        if not re.match('^(GF|LF|TF)@[A-Za-z_$&%*!?-][A-Za-z0-9_$&%*!?-]*$', instruction_parts[1]):
            sys.exit(23)
        instruction.add_argument(instruction_parts[1], "var")
        if "@" not in instruction_parts[2]:
            sys.exit(23)
        arg_type, arg_value = instruction_parts[2].split('@', 1)
        if arg_type not in ["int", "nil", "bool", "string"]:
            instruction.add_argument(instruction_parts[2], "var")
        else:
            instruction.add_argument(arg_value, arg_type)

    def handle_arithmetic_operation(self, instruction, instruction_parts):
        if len(instruction_parts) != 4:
            sys.exit(23)
        if not re.match('^(GF|LF|TF)@[A-Za-z_$&%*!?-][A-Za-z0-9_$&%*!?-]*$', instruction_parts[1]):
            sys.exit(23)
        instruction.add_argument(instruction_parts[1], "var")
        if "@" not in instruction_parts[2]:
            sys.exit(23)
        arg_type2, arg_value2 = instruction_parts[2].split('@', 1)
        if arg_type2 not in ["int", "nil", "bool", "string"]:
            instruction.add_argument(instruction_parts[2], "var")
        else:
            instruction.add_argument(arg_value2, arg_type2)
        if "@" not in instruction_parts[3]:
            sys.exit(23)
        arg_type3, arg_value3 = instruction_parts[3].split('@', 1)
        if arg_type3 not in ["int", "nil", "bool", "string"]:
            instruction.add_argument(instruction_parts[3], "var")
        else:
            instruction.add_argument(arg_value3, arg_type3)

    def handle_binary_operations(self, instruction, instruction_parts):
        if len(instruction_parts) != 4:
            sys.exit(23)
        if not re.match('^(GF|LF|TF)@[A-Za-z_$&%*!?-][A-Za-z0-9_$&%*!?-]*$', instruction_parts[1]):
            sys.exit(23)
        instruction.add_argument(instruction_parts[1], "var")
        if ("@" not in instruction_parts[2]) or ("@" not in instruction_parts[3]):
            sys.exit(23)
        arg3_type, arg3_value = instruction_parts[2].split('@', 1)
        arg4_type, arg4_value = instruction_parts[3].split('@', 1)
        if arg3_type not in ["int", "nil", "bool", "string"]:
            instruction.add_argument(instruction_parts[2], "var")
        else:
            instruction.add_argument(arg3_value, arg3_type)
        if arg4_type not in ["int", "nil", "bool", "string"]:
            instruction.add_argument(instruction_parts[3], "var")
        else:
            instruction.add_argument(arg4_value, arg4_type)

    def handle_read(self, instruction, instruction_parts):
        if len(instruction_parts) != 3:
            sys.exit(23)
        if not re.match('^(GF|LF|TF)@[A-Za-z_$&%*!?-][A-Za-z0-9_$&%*!?-]*$', instruction_parts[1]):
            sys.exit(23)
        if instruction_parts[2] not in ["int", "bool", "string"]:
            sys.exit(23)
        instruction.add_argument(instruction_parts[1], "var")
        instruction.add_argument(instruction_parts[2], "type")

    def handle_jumpifeq_jumpifneq(self, instruction, instruction_parts):
        if len(instruction_parts) != 4 or ("@" in instruction_parts[1]):
            sys.exit(23)
        self.jumps += 1
        if "@" in instruction_parts[1]:
            sys.exit(23)
        instruction.add_argument(instruction_parts[1], "label")
        arg_types = []
        for i in range(2, 4):
            if "@" not in instruction_parts[i]:
                sys.exit(23)
            arg_type, arg_value = instruction_parts[i].split('@', 1)
            if arg_type not in ["int", "nil", "bool", "string"]:
                instruction.add_argument(instruction_parts[i], "var")
            else:
                instruction.add_argument(arg_value, arg_type)
            arg_types.append(arg_type)

    # Trieda reprezentujúca parser pre jazyk IPPcode24.
    def parse(self):
        try:
            # Preskakuje komentáre a prázdne riadky na začiatku vstupu.
            line = input().strip()
            while line.startswith("#") or not line:
                line = input().strip()

            if not line.startswith(".IPPcode24"):
                sys.exit(21)

            self.has_content = True

            while True:
                line = input().strip()
                count = line.count("#")
                self.comments += count

                if not line:
                    continue

                self.parse_instruction(line)

        except EOFError:
            if not self.has_content:
                sys.exit(21)
                
     # Metóda na výpis XML reprezentácie parsovaného kódu.
    def output_xml(self):
        print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
        print("<program language=\"IPPcode24\">")
        for instruction in self.program.instructions:
            # Výpis každej inštrukcie s jej argumentami.
            print(f"  <instruction order=\"{instruction.order}\" opcode=\"{instruction.opcode}\">")
            for i, arg in enumerate(instruction.args, start=1):
                print(f"    <arg{str(i)} type=\"{arg['type']}\">{special_chars(arg['value'])}</arg{str(i)}>")
            print("  </instruction>")
        print("</program>")


if __name__ == "__main__":
    # Spracovanie vstupných argumentov skriptu.
    arguments = sys.argv[1:]
    if "--help" in arguments:
        if len(arguments) > 1:
            sys.exit(10)
        print("Skript načíta kód v jazyku IPPcode24 zo vstupu, skontroluje jeho lexikálnu a syntaktickú správnosť a vypíše XML reprezentáciu programu.")
        print("  --help - zobrazí túto nápovedu")
        sys.exit(0)

    parser = IPPParser()   
    parser.parse()
    parser.output_xml()




