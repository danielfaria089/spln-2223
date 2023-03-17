#!/usr/bin/env python3

import sys
import fileinput
import re

text=""

for line in fileinput.input():
    text+=line



# 0. Quebras de página
# 1. Separar pontuação das palavras
# 2. Marcar capitulos

regex_cap = r".*(CAP[ÍI]TULO \w+).*"
text=re.sub(regex_cap, r"\n# \1", text)


# 3. Separar paragrafos de linhas pequenas

regex_par = r"([a-z0-9,;-])\n\n([a-z0-9])"
text=re.sub(regex_par, r"\1\n\2", text)

# 4. Juntar linhas da mesma frase
# 5. Uma frase por linha
# 6. Poema

def guarda_poema(poema):
    pass

print(text)