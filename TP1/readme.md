# TPC 1
## Ficheiros Importantes
* [Dicionario em XML](medicina.xml)
* [Ficheiro de texto marcado](output.txt)
* [Conversor do TXT para JSON legível](main.py)
* [Dicionario em JSON](final.json)

## Método de Trabalho
1. Comecei por fazer a conversão do ficheiro PDF para XML, usando o pdf2xml.
2. Com o ficheiro XML, com a utilização de várias substituições e maracações, consegui obter um ficheiro de texto marcado, para ser utilizado na conversão para dicionário.
3. A partir do ficheiro de texto marcado, foi possível fazer a conversão para uma estrutura de dados organizada (dict) em python, usando o ficheiro main.py. Esta estrutura de dados foi guardada num ficheiro JSON.
