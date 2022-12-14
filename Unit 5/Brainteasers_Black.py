import sys; args = sys.argv[1:]
idx = int(args[0])-60

myRegexLst = [
    r"/^((?!010)\d)*$/",
    r"/^(?!.*010|101)[10]*$/",
    r"/^((10*)*1|(01*)*0)$/",
    r"/\b(?!(\w)+\w*\1\b)\w+/i",
    r"/(?=(\w)+\w*((\w)\w*(\1\w*\3|\3\w*\1)|\1(\w)+\w*\5))\w+/i",
    r"/\b(?=(\w)+(\w*\1){2})(\1|(\w)(?!\w*\4))+\b/i", 
    r"/\b([^aeiou\s]*([aeiou])(?!\w*\2)){5}[^aeiou]*?\b/i", 
    r"/^(?=1*0(1|01*0)*$)(?=(0|10*1)+$).+/", 
    r"/^((1(01*0)*10*)+|0)$/",
    r"/^1(01*0|10*1)*(01*)?$/", 
    ]

if idx < len(myRegexLst):
  print(myRegexLst[idx])
  
# Ramya Reddy, 2, 2023