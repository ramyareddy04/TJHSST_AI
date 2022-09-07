import sys; args = sys.argv[1:]
idx = int(args[0])-40

myRegexLst = [
    r"/^[xo.]{64}$/i",
    r"/^[xo]*\.[xo]*$/i",
    r"/((^(x+o*)?)\.|\.(o*x+)?$)/i",
    r"/^.(..)*$/s",
    r"/^(0|1[10])([10]{2})*$/s",
    r"/\w*(a[eiou]|e[aiou]|i[aeou]|o[aeiu]|u[aeio])\w*/i", 
    r"/^(1?0)*1*$/", 
    r"/^([bc]*a[bc]*|[bc]+a?[bc]*)$/",
    r"/^([bc]+|(([bc]*a[bc]*){2})+)$/",
    r"/^(2[20]*|(2[20]*)?((1[02]*){2})+)$/",
    ]

if idx < len(myRegexLst):
  print(myRegexLst[idx])
  
# Ramya Reddy, 2, 2023