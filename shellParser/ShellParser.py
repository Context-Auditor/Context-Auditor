#! /usr/bin/python2.7
from ShellTransitionFun import*
from TwoPDA import *
import os
import urllib


class ShellParser:
    def __init__(self):
        self.parser=TwoPDA(ShellTransitionFun.shellStates, {}, ShellTransitionFun.SHTF, 'SH_Start', {}, {}, "")
def main():
    import sys
    shellParser=ShellParser()
    if (len(sys.argv)>2):
        command=sys.argv[1]
        #print ("commmand is " + command + '\n')
        userInput=sys.argv[2]
        #print ("user data is: "+ userInput + '\n')
        commandInjection=False
        if(urllib.unquote_plus(userInput) in command):
            shellParser.parser.restart(command)
            #print ("decoded user data is: "+ urllib.unquote_plus(userInput) + '\n')
            stateTransitions=shellParser.parser.states_at_Malicious_substring(urllib.unquote_plus(userInput))
            #print("Decoded url is:\n")
            #print(urllib.unquote_plus(userInput))
            #print (stateTransitions)
            if(len(stateTransitions)>1):
                preState=stateTransitions[0]
                i=0
                #commandInjection=False
                while(i<len(stateTransitions)-1):
                    i=i+1
                    state=stateTransitions[i]
                    if(preState!=state):
                        commandInjection=True
                        break
                    preState=state
            if(commandInjection):
                #print("Command injection found")
                #sys.stdout.write("0")
                print(0)
		#os._exit(0)
            else:
                #print("Safe Command")
                #sys.stdout.write("1")
		#os._exit(1)
                print(1)


if __name__ == "__main__":
	main()
