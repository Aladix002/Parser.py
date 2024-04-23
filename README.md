Implementačná dokumentácia k 1. úlohe do
IPP 2023/2024
Meno a priezvisko: Filip Botlo
Login: xbotlo01
1
Implementácia
IPP parser je implementovaný v programovacom jazyku Python. Použı́va štandardné
knižnice na manipuláciu so ret’azcami, regulárne výrazy a prácu s XML. Implementácia
sa skladá z niekol’kých tried, ktoré spolupracujú na načı́tanı́ a spracovanı́ kódu v jazyku
IPPcode24.
1.1
Spracovanie kódu
IPP parser začı́na analýzou vstupných argumentov. Ak je prı́tomný argument -help”,
parser vypı́še nápovedu. Samotné spracovanie kódu prebieha vo funkcii parse().
Parser čı́ta vstupné riadky a postupne ich spracováva. Pre každý riadok vstupu sa
vytvára inštancia triedy Instruction, ktorá reprezentuje jednotlivé inštrukcie prog-
ramu. Na základe opcode inštrukcie sa volá vhodná metóda pre spracovanie danej
inštrukcie.
Funkcia parse() využı́va funkciu parse instruction(), ktorá je zodpo-
vedná za spracovanie jednotlivých inštrukciı́.
1.2
Spracovanie inštrukciı́
Pri spracovanı́ inštrukcie sa kontroluje syntax a validita argumentov. Na základe opcode
inštrukcie sa určuje, aké typy argumentov očakáva a ako sú spracovávané. Metódy pre
spracovanie inštrukciı́ sú definované v rámci triedy IPPParser.
Naprı́klad, metóda handle defvar pops() sa stará o spracovanie inštrukciı́ s
opcode DEFVAR a POPS. Pre inštrukciu DEFVAR kontroluje, či argument má správny
formát a typ.
1.3
Generovanie XML
Po spracovanı́ všetkých inštrukciı́ sa vytvára XML reprezentácia programu. Trieda
XMLVisitor sa stará o prevod inštrukciı́ na XML elementy. Každá inštrukcia sa pre-
vedie na element <instruction>, ktorý obsahuje informácie o poradı́, opcode a
argumenty inštrukcie.
