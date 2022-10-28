data=[]

filesList= ["Stack.py", "TwoPDA.py", "JSTransitionFun.py", "CSSTransitionFun.py", "HTMLTransitionFun.py", "HTMLParser.py"]

for file in filesList:
    fp = open("../htmlParser/"+file)
    dataTemp= fp.readlines()
    data+=dataTemp[4:]
    data+=['\n']
    fp.close()

fp = open("tempConf.py")
dataTemp= fp.readlines()
data+=dataTemp
data+=['\n']
fp.close()

with open ('detector.py', 'w') as fp:
    for line in data:
        fp.write(line)
