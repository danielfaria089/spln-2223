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


import json
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

#Separar por tags

lines=texto.splitlines()

linhas=[]
j=0
i=0

while i < len(lines):
    line=lines[i]
    if line.startswith("###C"):
        linhas.append(line.strip())
        i+=1
    elif line.startswith("###R"):
        linhas.append(line.strip())
        i+=1
    elif line.startswith("%"):
        linhas.append(line.strip())
        i+=1
    elif line.startswith("&"):
        linhas.append(line.strip())
        i+=1
    elif line.startswith("SIN"):
        linhas.append(line.strip())
        i+=1
    elif line.startswith("VID"):
        linhas.append(line.strip())
        i+=1
    elif line.startswith("NOTA"):
        linhas.append(line.strip())
        i+=1
    else:
        linhas[-1]+=" "+line.strip()
        i+=1

i=0
j=0
palavra=""
palavras=[]

while i < len(linhas):
    linha=linhas[i]
    if linha.startswith("###C"):
        for j in range(i+1,len(linhas)):
            if linhas[j].startswith("###R"):
                linha+=" "+linhas[j]
            else:
                i=j
                break
        
        linha=re.sub(r'###\w ',"",linha)
        linha=re.sub(r'(?<=\d)\s+(?=\d)','',linha,flags=re.MULTILINE)
        match=re.search(r'(\d+) +((?:[A-Za-zÀ-ÖØ-öø-ÿ0-9\-]+ ?)+)',linha)
        num=match.group(1)
        palavra=match.group(2)
        palavras.append({"num":num,"palavra":palavra})
    
    elif linha.startswith("###R"):
        if(linhas[i-1].startswith("###C")):
            print("Erro")
        for j in range(i+1,len(linhas)):
            if linhas[j].startswith("###R"):
                linha+=" "+linhas[j]
            else:
                i=j
                break
        linha=re.sub(r'###\w ',"",linha)
        palavras.append({"palavra":linha,"num":None})
    elif linha.startswith("&"):
        matches=re.findall(r'(?:&(\w{2})|;) ?(.*?)( ;| \[|$)',linha)
        if('traducao' not in palavras[-1]):
            palavras[-1]["traducao"]={}
        lingua=matches[0][0]
        palavras[-1]["traducao"][lingua]=[]
        for match in matches:
            if(match[1] is not None):
                traducao=match[1]
                palavras[-1]["traducao"][lingua].append(traducao)
        i+=1
    elif linha.startswith("%"):
        linha=re.sub(r'%',"",linha)
        palavras[-1]["areas"]=linha.split()
        i+=1
    elif linha.startswith("SIN"):
        linha=re.sub(r'SIN ',"",linha)
        palavras[-1]["sinonimos"]=[x.strip() for x in linha.split(";")]
        i+=1
    elif linha.startswith("VID"):
        linha=re.sub(r'VID ',"",linha)
        palavras[-1]["vid"]=linha
        i+=1
    elif linha.startswith("NOTA"):
        linha=re.sub(r'NOTA ',"",linha)
        palavras[-1]["nota"]=linha
        i+=1
    else:
        i+=1
    
with open("output.txt","w") as f:
    f.write(texto)


#Passar lista para dict, onde key é o número da palavra
palavras={palavra["num"]:palavra for palavra in palavras if palavra["num"] is not None}

#Colocar o campo palavra no dict traducao
for key in palavras:
    palavra=palavras[key]
    if "traducao" in palavra:
        palavra["traducao"]["ga"]=[palavra["palavra"]]
    if "sinonimos" in palavra:
        palavra["traducao"]["ga"].extend(palavra["sinonimos"])
    del palavra["palavra"]
    del palavra["num"]  
    
    
with open("final.json","w") as file:
    json.dump(palavras,file,indent=4,ensure_ascii=False)
