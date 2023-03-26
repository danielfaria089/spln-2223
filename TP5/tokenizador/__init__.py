#!/usr/bin/env python3

'''
Tokenizador de textos
'''

__version__ = '0.1'

import os
import re
from .utils import *

list_poems=[]

def quebrasPagina(text):
    '''0. Quebra de páginas'''

    regex_par = r"([a-z0-9,;-])\n\n([a-z0-9])"
    return re.sub(regex_par, r"\1\n\2", text)

def separaPontuacao(text,abrevs):
    '''1. Separar pontuação das palavras
    
    Realizar tratamento das abreviaturas
    '''

    for key in abrevs:
        abrev=abrevs[key]
        regex_abrev = r""+abrev
        text=re.sub(regex_abrev, r"<"+abrev.replace(".","")+r">", text)

    return text


def marcarCapitulos(text):
    '''2. Marcar capitulos'''

    regex_cap = r".*(CAP[ÍI]TULO \w+).*"
    return re.sub(regex_cap, r"\n# \1.", text)

def juntarFrases(text):
    '''4. Juntar linhas da mesma frase | 5. Uma frase por linha
    '''

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

    return linhas.join("\n")

def guarda_poemas(text):
    '''6. Guardar poemas'''
    matches=re.findall(r"<poema>(.*)</poema>", text)
    for match in matches:
        list_poems.append(match.group(1))

def abbreviations(lang):
    '''Read abbreviations from file'''

    # get the current directory
    dirname = os.path.abspath(__file__)
    # remove the file name from the path
    dirname = dirname[:dirname.rfind('/')]
    abrevFile = dirname+'/conf/abrev.txt'

    abrevs={}

    with open(abrevFile, "r") as f:
        txt=f.read()
        list_langs=txt.split("#")
        for lang_txt in list_langs:
            lang_txt=lang_txt.strip()
            split=lang_txt.split("\n")
            abrevs[split[0]]=split[1:]
    
    return abrevs

def main():
    vars=parse_args()
    text=read_inputFile()

    text=quebrasPagina(text)
    text=separaPontuacao(text)
    text=marcarCapitulos(text)
    text=juntarFrases(text)
    if(vars['poems']):
        guarda_poemas(text)

    write_outputFile(text)
    
if __name__ == "__main__":
    main()