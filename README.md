# Implementačná dokumentácia k 1. úlohe do IPP 2023/2024

**Meno a priezvisko:** Filip Botlo  
**Login:** xbotlo01

## 1 Implementácia

IPP parser je implementovaný v programovacom jazyku Python. Používa štandardné knižnice na manipuláciu so reťazcami, regulárne výrazy a prácu s XML. Implementácia sa skladá z niekoľkých tried, ktoré spolupracujú na načítaní a spracovaní kódu v jazyku IPPcode24.

### 1.1 Spracovanie kódu

IPP parser začína analýzou vstupných argumentov. Ak je prítomný argument `-help`, parser vypíše nápovedu. Samotné spracovanie kódu prebieha vo funkcii `parse()`. Parser číta vstupné riadky a postupne ich spracováva. Pre každý riadok vstupu sa vytvára inštancia triedy `Instruction`, ktorá reprezentuje jednotlivé inštrukcie programu. Na základe opcode inštrukcie sa volá vhodná metóda pre spracovanie danej inštrukcie. Funkcia `parse()` využíva funkciu `parse_instruction()`, ktorá je zodpovedná za spracovanie jednotlivých inštrukcií.

### 1.2 Spracovanie inštrukcií

Pri spracovaní inštrukcie sa kontroluje syntax a validita argumentov. Na základe opcode inštrukcie sa určuje, aké typy argumentov očakáva a ako sú spracované. Metódy pre spracovanie inštrukcií sú definované v rámci triedy `IPPParser`. Napríklad, metóda `handle_defvar_pops()` sa stará o spracovanie inštrukcií s opcode `DEFVAR` a `POPS`. Pre inštrukciu `DEFVAR` kontroluje, či argument má správny formát a typ.

### 1.3 Generovanie XML

Po spracovaní všetkých inštrukcií sa vytvára XML reprezentácia programu. Trieda `XMLVisitor` sa stará o prevod inštrukcií na XML elementy. Každá inštrukcia sa prevedie na element `<instruction>`, ktorý obsahuje informácie o poradí, opcode a argumenty inštrukcie.


