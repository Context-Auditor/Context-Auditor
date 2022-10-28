from TwoPDA import TwoPDA
from JSTransitionFun import *
from CSSTransitionFun import *
from HTMLTransitionFun import *
import urllib
import sys
from urllib.parse import unquote_plus

class HTMLParser:

    def __init__(self):
        self.parser = TwoPDA(HTMLTransitionFun.states, {}, HTMLTransitionFun.tf, 'Data', {}, {}, "")
        self.generalizeCSSTF(CSSTransitionFun.CSSTF)
        self.generalizeJSTF(JSTransitionFun.JSTF)
        self.JSparser = TwoPDA(JSTransitionFun.jsStates, {}, self.JSTF, 'Script_Start', {}, {}, "")
        self.CSSparser = TwoPDA(CSSTransitionFun.cssStates, {}, self.CSSTF, 'CSS_Start', {}, {}, "")
        self.current_parser = self.parser

    def return_index(self):
        return self.current_parser.return_index()

    def returnUniqueStates(self, TF):
        states = list()
        for key in TF.keys():
            (state, character, tops) = key
            if not state in states:
                states.append(state)
        return states

    def generalizeJSTF(self, TF):
        states = self.returnUniqueStates(TF)
        self.JSTF = dict(TF)

        forbiddenstates = ["Single_Line_Comment", "Multi_Line_Comment", "RelationalExpressionG",
                           "RelationalExpressionGG", "Tag_Skip", 'Syntax_Error', "Tag_open_JS",
                           "CSS_Tag_Skip"]  ### cover this states later
        for state in states:
            if not state in forbiddenstates:
                self.JSTF[(state, '<', 'any')] = ("Tag_Skip", "R", "PUSH", "<")

    def generalizeCSSTF(self, TF):
        states = self.returnUniqueStates(CSSTransitionFun.CSSTF)
        self.CSSTF = dict(CSSTransitionFun.CSSTF)

        forbiddenstates = ['Syntax_Error']  ### cover this states later
        for state in states:
            if not state in forbiddenstates:
                self.CSSTF[(state, '<', 'any')] = ("CSS_Tag_Skip", "R", "PUSH", "<")

    def testCSSFileStates(self, cssfile):
        with open(cssfile, 'r') as myfile:
            CSSString = myfile.read()
        self.CSSparser.restart(CSSString)
        print ("Testing css file to verify states")
        self.CSSparser.states_at_Malicious_substring(CSSString)
        self.CSSparser.transfer_back_to_Start_Script()

    def testJSFileStates(self, jsfile):
        with open(jsfile, 'r') as myfile:
            JSString = myfile.read()
        self.JSparser.restart(JSString)
        print ("Testing js file to verify states")
        self.JSparser.states_at_Malicious_substring(JSString)
        self.JSparser.transfer_back_to_Start_Script()

    def findXSSAttackOneReq(self, Mal, MalQueryParams, state_tr):
        st = ''
        for key in MalQueryParams.keys():
            malString = unquote_plus(MalQueryParams[key])
            offset = Mal.find(malString)
            count = 0
            if offset != -1:
                done = False
                index = 0
                context = "HTML"
                submal = Mal
                lastIndex = 0
                self.current_parser = self.parser
                preContex = "HTML"
                while not done:
                    preContex = context
                    context, index = self.current_parser.state_before_mal_substr(submal, offset)
                    if (context == "OK"):
                        states = self.current_parser.states_at_Malicious_substring(malString)
                        if (states == -2):
                            print("found for param : " + key + " and value: " + malString + '\n')
                            return "language transition detected"
                        if (states != -2 and states != -1):
                            preState = states[0]
                            for state in states:
                                if (state == "Syntax_Error"):
                                    rt = "Syntax Error inside " + preContex + " found for param : " + key + " and value: " + malString + '\n'
                                    return st
                                    break
                                else:
                                    if (state != preState):
                                        st = "An injection inside " + preContex + " found for param : " + key + " and value: " + malString + '\n'
                                        return st
                                        break
                                preState = state
                        submalTemp = submal[offset + len(malString):]
                        if (submalTemp.find(malString) > -1 and count < 5):
                            offset = offset + len(malString) + submalTemp.find(malString)
                            count += 1
                        else:
                            done = True
                    if context != "OK":
                        if context == "JS":
                            self.current_parser = self.JSparser
                        if context == "CSS":
                            self.current_parser = self.CSSparser
                        if context == "HTML":
                            self.current_parser = self.parser
                        submal = Mal[lastIndex + index:]
                        lastIndex += index
                        offset = submal.find(malString)
                        self.current_parser.restart(submal)
                    if offset == -1 or index == len(submal) - 1:
                        done = True
        return st

    def findXSSAttackIndexes(self, key, start, end, HTML):
        st = ''
        malString = HTML[start:end]
        offset = start
        if offset != -1:
            done = False
            index = 0
            context = "HTML"
            submal = HTML
            lastIndex = 0
            self.current_parser = self.parser
            preContex = "HTML"
            while not done:
                preContex = context
                context, index = self.current_parser.state_before_mal_substr(submal, offset)
                if (context == "OK"):
                    states = self.current_parser.states_at_Malicious_index(offset, malString)
                    if (states == -2):
                        return "language transition detected"
                    if (states != -2 and states != -1):
                        preState = states[0]
                        for state in states:
                            if (state == "Syntax_Error"):
                                st = "Syntax Error inside " + preContex + " found for param : " + key + " and value: " + malString + '\n'
                                return st
                            else:
                                if (state != preState):
                                    st = "An injection inside " + preContex + " found for param : " + key + " and value: " + malString + '\n'
                                    return st
                            preState = state
                    return st

                if context != "OK":
                    if context == "JS":
                        self.current_parser = self.JSparser
                    if context == "CSS":
                        self.current_parser = self.CSSparser
                    if context == "HTML":
                        self.current_parser = self.parser
                    submal = HTML[lastIndex + index:]
                    lastIndex += index
                    offset = start - lastIndex

                    self.current_parser.restart(submal)
                if offset == -1:
                    done = True
        return st

        def findXSSAttackOneReqNginx(self,Mal,MalQueryParams):
    	#return 404
            st='11111'+str(len(Mal))
            for key in MalQueryParams.keys():
                st+= MalQueryParams[key]
                #************** INJECTIONS INSIDE JAVASCRIPT************************
                malString = urllib.unquote_plus(urllib.unquote_plus(MalQueryParams[key]))
                MalScriptStartIndex = Mal.find("<script>")
                MalScriptEndIndex = Mal.find("</script>")
                MalParameterIndex = Mal.find(malString)
                if(MalScriptStartIndex<MalParameterIndex<MalScriptEndIndex):

                    MalScript = Mal[MalScriptStartIndex + 8:MalScriptEndIndex - 1]
                    print "CHECKING INJECTION INSIDE JAVASCRIPT "
                    print MalScript
                    self.JSparser.restart(MalScript)
                    expectedState = self.JSparser.states_at_Malicious_substring(malString)
                    if (expectedState != -1):
                        # return 404
                        #return 300
                        print "We Found parsing states for desired input as: " + MalQueryParams[key] + " is: " + expectedState

                        # print self.parser.html
                        # malString=urllib.unquote(urllib.unquote(MalQueryParams[key]))
                        preState=expectedState[0]
                        for state in expectedState:
                            st+=state
                            if (state != preState):
                                print '!' * 78 + "INJECTION INSIDE SCRIPT DETECETED" + '!' * 78
                                return (404,'fgfgdg')
                                break
                            preState=state
    		    #return 200

                # return (200 , st)

                else:
                    # return 404
                    print "CHECKING HTML INJECTION"
                    self.parser.restart(Mal)
                    malString = urllib.unquote_plus(urllib.unquote_plus(MalQueryParams[key]))
                    expectedState=self.parser.states_at_Malicious_substring(malString)

                    st+="yes"
                    st+=malString
                    st+=Mal
                    if(expectedState!=-1):
                        st+="With MAl"

                        # print "We Found parsing states for desired input as: " + MalQueryParams[key] + " is: " + expectedState

                        preState=expectedState[0]

                        for state in expectedState:
                            st+=state
                            if (state != preState):
                                print '!' * 78 + "INJECTION INSIDE HTML DETECETED" + '!' * 78
                                return (404,state)
                                # return (404,'INJECTION INSIDE HTML DETECETED')
                                break
                            preState=state
            print "done"
            return (200 , st)
