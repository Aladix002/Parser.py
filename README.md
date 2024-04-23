# Implementační dokumentace k 1. úloze do IPP 2023/2024

**Meno a priezvisko:** Filip Botlo  
**Login:** xbotlo01

## 1 Implementace

IPP parser je implementován v programovacím jazyku Python. Používá standardní knihovny na manipulaci s řetězci, regulární výrazy a práci s XML. Implementace se skládá z několika tříd, které spolupracují na načítání a zpracování kódu v jazyku IPPcode24.

### 1.1 Zpracování kódu

IPP parser začíná analýzou vstupních argumentů. Pokud je přítomný argument `-help`, parser vypíše nápovědu. Samotné zpracování kódu probíhá ve funkci `parse()`. Parser čte vstupní řádky a postupně je zpracovává. Pro každý řádek vstupu se vytváří instance třídy `Instruction`, která reprezentuje jednotlivé instrukce programu. Na základě opcode instrukce se volá vhodná metoda pro zpracování dané instrukce. Funkce `parse()` využívá funkci `parse_instruction()`, která je zodpovědná za zpracování jednotlivých instrukcí.

### 1.2 Zpracování instrukcí

Při zpracování instrukce se kontroluje syntax a validita argumentů. Na základě opcode instrukce se určuje, jaké typy argumentů očekává a jak jsou zpracovávány. Metody pro zpracování instrukcí jsou definovány v rámci třídy `IPPParser`. Například, metoda `handle_defvar_pops()` se stará o zpracování instrukcí s opcode `DEFVAR` a `POPS`. Pro instrukci `DEFVAR` kontroluje, zda argument má správný formát a typ.

### 1.3 Generování XML

Po zpracování všech instrukcí se vytváří XML reprezentace programu. Třída `XMLVisitor` se stará o převod instrukcí na XML elementy. Každá instrukce se převede na element `<instruction>`, který obsahuje informace o pořadí, opcode a argumenty instrukce.

