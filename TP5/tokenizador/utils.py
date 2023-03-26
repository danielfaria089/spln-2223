import argparse
import sys

vars={
    'inputFile': 'stdin',
    'outputFile': 'stdout',
    'language': 'pt',
    'poems': True
}


def read_inputFile():
    '''Read text from input file or from stdin if input file is not specified'''
    text=""
    if vars['inputFile'] == 'stdin':
        for line in sys.stdin:
            text+=line
    else:
        with open(vars['inputFile'], 'r') as f:
            return f.read()
        
    return text

def write_outputFile(text):
    '''Write text to output file or to stdout if output file is not specified'''
    if vars['outputFile'] == 'stdout':
        print(text)
    else:
        with open(vars['outputFile'], 'w') as f:
            f.write(text)

def write_poems(list_poems):
    '''Write poems to output file or to stdout if output file is not specified'''
    if vars['outputFile'] == 'stdout':
        for poem in list_poems:
            print(poem)
    else:
        with open(vars['outputFile'], 'w') as f:
            for poem in list_poems:
                f.write(poem)
                f.write("\n\n")

def parse_args():
    '''Parse arguments from command line'''
    parser=argparse.ArgumentParser(
        prog='tokenizador',
        description='Tokenizer for text file',
        epilog='Work done in the context of the course (SPLN) of the Master in Informatics Engineering of the University of Minho (UMinho).')
    
    parser.add_argument('-i', '--input', help='input file', default='stdin')
    parser.add_argument('-o', '--output', help='output file', default='stdout')
    parser.add_argument('-l', '--language', help='language of the text', default='pt')
    parser.add_argument('-p', '--poems', help='keep poems', action='store_true')

    args=parser.parse_args()
    vars['inputFile']=args.input
    vars['outputFile']=args.output
    vars['language']=args.language
    vars['poems']=args.poems
    
    return vars