import sys
import re

d = []
with open("./"+sys.argv[1],"r") as f:
	for line in f: d.append(line.strip())

myRegexList = [
    re.compile(r"\b((?=\w*a)(?=\w*e)(?=\w*i)(?=\w*o)(?=\w*u))\w+", re.I),
    re.compile(r"\b(((?![aeiou])[a-z])*[aeiou]){5}((?![aeiou])[a-z])*\b", re.I),
    re.compile(r"\b(?=(\w)+)\1((?!\1)\w)*\1\b", re.I),
    re.compile(r"\b(?=(\w)(\w)(\w))\w*\3\2\1\b", re.I),
    re.compile(r"\b(?!\w*b\w*b)(?!\w*t\w*t)\w*(bt|tb)\w*", re.I),
    re.compile(r"(\w)\1+", re.I), 
    re.compile(r"(\w)(\w*\1){1,}", re.I),
    re.compile(r"(\w\w)(\w*\1){1,}", re.I),
    re.compile(r"((?![aeiou])[a-z])", re.I),
    re.compile(r"\b(?!\w*(\w)(\w*\1){2})\w+", re.I),
    ]

for i in range(len(myRegexList)):
    matches = []
    if i == 0:
        minV = 100
        for word in d:
            if re.search(myRegexList[i], word):
               if len(word) < minV:
                   minV = len(word)
                   matches = [word]
               elif len(word) == minV: matches.append(word)
    elif i in [1, 2, 9]:
        max = 0
        for word in d:
            if re.search(myRegexList[i], word):
                if len(word) > max:
                    max = len(word)
                    matches = [word]
                elif len(word) == max: matches.append(word)
    elif i in [5,6,7]:
        max = 0
        for word in d:
            for ch in range(len(word)):
                if re.search(myRegexList[i], word[ch:]):
                    if i == 5: 
                        temp = re.search(myRegexList[i], word[ch:]).span()
                        temp2 = temp[1]-temp[0]
                    elif i == 6: temp2 = len(re.findall(re.compile((word[ch]).encode().decode(), re.I), word[ch:]))
                    else: temp2 = 2*len(re.findall(re.compile((word[ch:ch+2]).encode().decode(), re.I), word[ch:]))
                    if temp2 > max:
                        max = temp2
                        matches = [word]
                    elif word not in matches and temp2 == max: matches.append(word)
    elif i == 8:
        max = 0
        for word in d:
            if re.search(myRegexList[i], word):
                if len(re.findall(myRegexList[i], word)) > max:
                    max = len(re.findall(myRegexList[i], word))
                    matches = [word]
                elif len(re.findall(myRegexList[i], word)) == max: matches.append(word)
    else:
        for word in d: 
            if re.search(myRegexList[i], word): matches.append(word)

    print("#{} {}\n{} total matches".format(i+1, myRegexList[i], len(matches)))
    for i in range(min(5, len(matches))): print(matches[i].lower())
    print()