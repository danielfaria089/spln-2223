#!/usr/bin/env python3

import sys
import fileinput
import re

text=""

for line in fileinput.input():
    text+=line



# 0. Quebras de página

regex_par = r"([a-z0-9,;-])\n\n([a-z0-9])"
text=re.sub(regex_par, r"\1\n\2", text)

# 1. Separar pontuação das palavras

regex_sr=r"Sr\."
text=re.sub(regex_sr, r"<Sr>", text)

regex_sra=r"Sra\."
text=re.sub(regex_sra, r"<Sra>", text)

regex_undo=r"<(Sra?)>"


# 2. Marcar capitulos

regex_cap = r".*(CAP[ÍI]TULO \w+).*"
text=re.sub(regex_cap, r"\n# \1.", text)


# 3. Separar paragrafos de linhas pequenas

#???

# 4. Juntar linhas da mesma frase

regex_frase = r"(#.*?\n|\n?–.*[.!?]*\n|[^.!?]*(?:\n[^.!?]*)*[.!?]+)"
matches = re.findall(regex_frase, text)
linhas = []
for match in matches:
    if match == "":
        pass
    elif match[0] == "#":
        linhas.append(match.strip().replace("\n", " ").strip())
    else:
        linha=match.strip().replace("\n", " ").strip()
        if(linha[0].islower()):
            linhas[-1]+=" "+linha
        else:
            linhas.append(linha)

# 5. Uma frase por linha

for linha in linhas:
    linha=re.sub(regex_undo, r"\1", linha)
    #pass
    print(linha)

# 6. Poema

def guarda_poema(poema):
    pass