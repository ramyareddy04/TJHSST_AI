import sys
import re

lines = open("./"+sys.argv[1],"r").readlines()

regexes = [
    re.compile(r"(?=^ *((el)?if|while|return))[\w .,''""><()&|!+%/*-]*=[^=]+", re.I),
    re.compile(r"^(?! *((el)?if|while|return))(?=[\w .,''""><()&|!+%/*-]*==)", re.I),
    re.compile(r"(?=^ *((el)?if|else|while|for))(?![\w =.,''""><()&|!+%/*-]*:)", re.I),
    re.compile(r"(?=^ *\d+\w* *= *(.?\d+|\'\'|\"\"|\'(?!(True|False|\'))\w*\'|\"(?!(True|False|\"))\w*\"|True|False))\b"),
    re.compile(r"(?=^ *((?!(\d|print))\w)\w+ *\()", re.I),
    ]

errors = [
    '= has been used instead of == : ',
    '== has been used instead of = : ',
    'Missing colon : ',
    'Variable name begins with digit : ',
    'Function call to undefined function : '
    ]

fin = ''
for idx, text in enumerate(lines):
    if '\n' in text:
        text = text[:-1]
    for idx2, i in enumerate(regexes):
        if re.search(i, text):
            fin += errors[idx2]+' '+str(idx+1)+'\n'
print(fin[:-1])