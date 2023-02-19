# ZEP -> E*
# E -> EC
#    | ER
# EC -> num pals pos CORPO
# CORPO -> area LINGUAS
# LINGUAS -> pt pals
#          | en pals
#          | es pals
# ER -> pals VID
# VID -> Vid.- pals

#<text top="73" left="521" width="54" height="10" font="18">ocabulario</text> Esta linha indica que vai começar uma nova página

#Todas as linhas têm o mesmo formato <text top=?? left=?? width=?? height=?? font=??>TEXTO</text>


import re

texto=open("medicina.xml").read()

#Remover xml header e footer, entre outros
def removeHeaderFooter(texto):
    #Marcar o início de uma nova página
    texto = re.sub(r'<text.*?>ocabulario.*</text>',r'###',texto,flags=re.MULTILINE)

    texto = re.sub(r'.*\n###\n.*\n',r'', texto,flags=re.MULTILINE)
    return texto

#Remover non-text
def removeNonText(texto):
    texto = re.sub(r'^\s*<(?!text).*>\n',r'',texto,flags=re.MULTILINE)
    return texto

#Remover linhas em branco
def removeBlankLines(texto):
    texto = re.sub(r'<.*?>\s+<\/text>\n',r'',texto,flags=re.MULTILINE)
    return texto

#Remover <i>, </i>, <b>, </b>
def removeTags(texto):
    texto = re.sub(r'</?(i|b)>',r'',texto,flags=re.MULTILINE)
    return texto

#Marcar palavra a traduzir
def markWord(texto):
    texto = re.sub(r'<text.*font="(?:10|3)">\s*(\d+)\s*((\S+ ?)+).*</text>',r'###C \1 \2',texto,flags=re.MULTILINE)
    texto = re.sub(r'<text.*font="(?:10|3)">\s*((?:\S+ ?)+).*</text>',r'###R \1',texto,flags=re.MULTILINE)
    return texto

def markArea(texto):
    #Como a área vem sempre em font 6 depois da palavra a traduzir, basta procurar por essa font
    texto = re.sub(r'<text.*font="6">\s*((\w+ *)+).*',r'%\1',texto,flags=re.MULTILINE)
    return texto

def markLinguas(texto):
    texto = re.sub(r'<text.*?>\s*(es|pt|en|la)\s*.*</text>',r'&\1',texto,flags=re.MULTILINE)
    return texto

def markSIN(texto):
    texto = re.sub(r'<text.*?>\s*SIN\.- (.*)</text>',r'SIN \1',texto,flags=re.MULTILINE)
    return texto

def markVID(texto):
    texto = re.sub(r'<text.*?>\s*Vid\.- (.*)</text>',r'VID \1',texto,flags=re.MULTILINE)
    return texto

def markNota(texto):
    texto = re.sub(r'<text.*?>\s*Nota\.- (.*)</text>',r'NOTA \1',texto,flags=re.MULTILINE)
    return texto

def remainingText(texto):
    texto = re.sub(r'<text.*?>(.*)</text>',r'\1',texto,flags=re.MULTILINE)
    return texto

#Remove o texto a começar a página
texto=removeHeaderFooter(texto)

#Remove linhas com tags que não são texto
texto=removeNonText(texto)

#Remove tags italico e bold
texto=removeTags(texto)

#Remove linhas em branco
texto=removeBlankLines(texto)

#Marca palavra a traduzir
texto=markWord(texto)

#Marca área de estudo da palavra
texto=markArea(texto)

#Marca línguas
texto=markLinguas(texto)

#Marca SIN
texto=markSIN(texto)

#Marca VID
texto=markVID(texto)

#Marca Nota
texto=markNota(texto)

#Escrever o resto do texto
texto=remainingText(texto)

#De ###C até % é uma palavra a traduzir (incluindo qualquer ###R que houver no meio)
#De ###R, se não houver um ###C, até % é uma palavra a traduzir
dicionario={}


palavra=""
entrada={}


for line in texto.splitlines():
    if line.startswith("###C"):
        if(entrada is not {}):
            dicionario[palavra]=entrada
            entrada={}
        else:
            palavra=re.match(r'###C (\d+) ((?:\S+ ?)+)',line).group(2)
    elif line.startswith("###R"):
        if(entrada is not {} and palavra==entrada['palavra']):
            dicionario[palavra]=entrada
            entrada={}
        else:
            palavra="".join((re.match(r'###R ((?:\S+ ?)+)',line).group(1),palavra))
    elif line.startswith("%"):
        if(entrada is not {}):
            entrada['palavra']=palavra
            entrada['areas']=re.match(r'%(.*)',line).group(1).split()
    elif line.startswith("&"):
        lingua=re.match(r'&(\w+)',line).group(1)

    #If the line is the last one, add the entry to the dictionary
    elif line == "\n":
        dicionario[palavra]=entrada
        break



with open("output.xml","w") as f:
    f.write(texto)