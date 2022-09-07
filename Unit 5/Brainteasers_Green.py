import sys; args = sys.argv[1:]
idx = int(args[0])-30

myRegexLst = [
    r"/^0$|^10[01]$/",
    r"/^[10]*$/",
    r"/^[10]*0$/",
    r"/\w*[aeiou]\w*[aeiou]\w*/i",
    r"/^0$|^1[10]*0$/", 
    r"/^[10]*110[10]*$/",
    r"/^.{2,4}$/s", 
    r"/^\d{3} *-? *\d{2} *-? *\d{4}$/",
    r"/^.*?d\w*/im",
    r"/^[10]?$|^1[01]*1$|^0[10]*0$/", #
    ]

if idx < len(myRegexLst):
  print(myRegexLst[idx])
  
# Ramya Reddy, 2, 2023