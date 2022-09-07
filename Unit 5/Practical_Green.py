import sys
import re
from colorama import init, Back, Fore

init()

pattern = sys.argv[1].split('/')[1:]
flags = 0
for ch in pattern[1]:
    if ch == 'i': flags |= re.I
    elif ch == 'm': flags |= re.M
    elif ch == 's': flags |= re.S
    elif ch == 'u': flags |= re.U
    elif ch == 'l': flags |= re.L
    elif ch=='x': flags |= re.X
print(pattern[0])
cmd = re.compile(pattern[0].encode().decode(), flags)
text = 'While inside they wined and dined, safe from the howling wind.\nAnd she whined, it seemed, for the 100th time, into the ear of her friend,\nWhy indeed should I wind the clocks up, if they all run down in the end?'
text = 'She arrived with the morning vehicle cavalcade'
matches = []
for match in re.finditer(cmd, text): matches.append([match.start(), match.end()])

lastCh = 0
fin = ''
for pair in matches:
    fin += text[lastCh:pair[0]]
    fin += Back.RED + text[pair[0]:pair[1]] + Back.RESET if lastCh == pair[0] and lastCh!=0 else Back.GREEN + text[pair[0]:pair[1]] + Back.RESET
    lastCh = pair[1]
print(fin + text[lastCh:len(text)])