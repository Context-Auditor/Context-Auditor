from Stack import Stack



import time
import sys

class TwoPDA:

    def __init__(self, states, alphabet, _function, start_state, accept_states, reject_states, JavaScript):
        EOF = chr(0)
        ASCII_upper = list()
        for i in range(65, 90):
            ASCII_upper.append(chr(i))
        ASCII_lower = list()
        for i in range(97, 122):
            ASCII_lower.append(chr(i))
        ASCII_alpha = ASCII_upper + ASCII_lower

        self.WHITESPACES = [' ', '\t', '\b']
        self.LINEBREAKS = ['\n']
        self.stack = Stack()
        self.stack.push("$$$")
        self.states = states;
        self.alphabet = alphabet;
        self.transition_function = _function;
        self.start_state = start_state;
        self.accept_states = accept_states;
        self.reject_states = reject_states;
        self.current_state = start_state;
        self.direction = 'R'
        self.current_char = ''
        self.js = JavaScript
        self.index = -1
        self.returnState_after_Character_Reference_in_data = ''
        self.JSList = list(JavaScript)
        self.lastUpdate = time.clock()

    def transition_to_new_state(self, input_value):
        timet = time.time()
        if (timet - self.lastUpdate > 5):
            print("Current State:  " + self.current_state + "  " + str(self.index))
            # print(self.stack.items)
            # print(("loop detected"))
            if (self.current_state == 'ASI'):
                self.current_state = 'Syntax_Error'
            else:
                self.current_state = 'ASI'
                # print(("loop detected"))
                # print(self.js[self.index - 250:self.index + 5])
        input_value = self.Automatic_Semicolon_Insertion(input_value)
        if ((self.current_state, input_value, self.stack.peek()) in self.transition_function.keys()):
            (new_state, direction, action, topOfStack) = self.transition_function[
                (self.current_state, input_value, self.stack.peek())]

        elif ((self.current_state, 'else', self.stack.peek()) in self.transition_function.keys()):
            (new_state, direction, action, topOfStack) = self.transition_function[
                (self.current_state, 'else', self.stack.peek())]

        elif ((self.current_state, input_value, 'any') in self.transition_function.keys()):
            (new_state, direction, action, topOfStack) = self.transition_function[
                (self.current_state, input_value, 'any')]
        elif (not (self.current_state, 'else', 'any') in self.transition_function.keys()):
            self.current_state = 'Syntax_Error'
            (new_state, direction, action, topOfStack) = self.transition_function[
                (self.current_state, 'else', 'any')]
        else:
            (new_state, direction, action, topOfStack) = self.transition_function[
                (self.current_state, 'else', 'any')]

        self.current_state = new_state
        self.direction = direction
        if action == 'PUSH':
            self.stack.push(topOfStack)
        elif action == 'POP':
            self.stack.pop()
        elif action == 'CHANGE':
            self.stack.pop()
            self.stack.push(topOfStack)

    def Automatic_Semicolon_Insertion(self, input):
        if (self.current_state == 'ASI'):
            if (input in [')', '}']):
                self.current_state = 'Syntax_Error'
                return input
            self.index = self.index - 1
            if (self.stack.peek() == 'NIN'):
                self.stack.pop()
                self.index = self.index - 1
            chr = self.js[self.index]
            if (chr in self.LINEBREAKS or chr in self.WHITESPACES or chr in [')', '}']):
                print('yes')
                self.js = self.js[:self.index] + ';' + self.js[self.index:]
                print(self.js[0:self.index + 10])
                chr = self.js[self.index]
                self.current_state = 'After_Assignment'
                return chr
            return chr
        else:
            return input

    def return_index(self):
        return self.index

    def state_before_mal_substr(self, html, offset):
        self.restart(html)
        end = offset
        self.index = -1
        self.direction = "R"
        while self.index < end:
            if self.direction == 'R':
                self.lastUpdate = time.time()
                self.index = self.index + 1

            self.current_char = html[self.index]
            self.transition_to_new_state(self.current_char)
            if (self.current_state == "Transition_Back_To_HTML"):
                return ("HTML", self.index + 1)
            if (self.current_state == "Transition_Back_To_HTML_Syntax"):
                return ("HTML", self.index)
            if self.current_state == "Transition_To_JS":
                return ("JS", self.index + 1)
            if self.current_state == "Transition_To_CSS":
                return ("CSS", self.index + 1)
        return ("OK", self.index + 1)

    def transfer_back_to_Start_Script(self):
        while (self.current_state != self.start_state):
            state_edges = []
            for element in self.transition_function.keys():
                if (element[0] == self.current_state and (element[2] == top or element[2] == "any")):
                    state_edges.append(element)
            found = False
            for (state, input_value, topElement) in state_edges:
                (new_state, direction, action, topOfStack) = self.transition_function[
                    (state, input_value, topElement)]
                if (action == "POP"):
                    found = True
                    self.transition_to_new_state(input_value)
                    break

            if ((self.current_state == self.start_state and self.stack.peek() == "$$$") or self.current_state == "Syntax_Error"):
                return
            if (found):
                continue
            else:
                for (state, input_value, topElement) in state_edges:
                    (new_state, direction, action, topOfStack) = self.transition_function[
                        (state, input_value, topElement)]
                    if (action == "CHANGE"):
                        found = True
                        self.transition_to_new_state(input_value)
                        break
            if (found):
                continue


            else:
                for (state, input_value, topElement) in state_edges:
                    (new_state, direction, action, topOfStack) = self.transition_function[
                        (state, input_value, topElement)]
                    if (state != new_state):
                        found = True
                        self.transition_to_new_state(input_value)
                        break

    def in_accept_state(self):
        return self.current_state in self.accept_states;

    def in_reject_state(self):
        return self.current_state in self.reject_states;

    def state_at_substring(self, substr):
        if (not substr in self.js):
            return -1
        while (self.index != self.js.index(substr) and self.index < len(self.js)):
            if (self.direction == 'R'):
                self.index = self.index + 1
                self.lastUpdate = time.time()
            self.current_char = self.JSList[self.index]
            self.transition_to_new_state(self.current_char)
        return self.current_state

    def states_at_Malicious_substring(self, substr):
        if (not substr in self.js):
            return -1
        outputList = list()
        end = len(substr)
        if (self.current_state == "Script_Start"):
            flag = False
        else:
            flag = True
        while (self.index < self.js.index(substr) + end - 1 and self.index < len(self.js) - 1):
            if (self.direction == 'R'):
                self.lastUpdate = time.time()
                self.index = self.index + 1
                if (self.start_state == "Script_Start" and self.index > self.js.index(substr)):
                    outputList.append(self.current_state)
                    flag = True
            self.current_char = self.JSList[self.index]
            self.transition_to_new_state(self.current_char)
            if (self.current_state in ["Transition_Back_To_HTML", "Transition_To_JS", "Transition_To_CSS",
                                       "Transition_Back_To_HTML_Syntax"]):  ##change of language happended here
                return -2
            if (flag == True and self.index >= self.js.index(substr) and self.direction == 'R'):
                outputList.append(self.current_state)
        if (len(outputList) == 0):
            return -1
        else:
            return outputList

    def states_at_Malicious_index(self, start, substring):
        print(self.js)
        if (not substring in self.js):
            return -1
        outputList = list()
        end = len(substring)
        if (self.current_state == "Script_Start"):
            flag = False
        else:
            flag = True
        while (self.index < start + end - 1 and self.index < len(self.js) - 1):
            if (self.direction == 'R'):
                self.lastUpdate = time.time()
                self.index = self.index + 1
                if (self.start_state == "Script_Start" and self.index > start):
                    outputList.append(self.current_state)
                    flag = True
            self.current_char = self.JSList[self.index]
            self.transition_to_new_state(self.current_char)
            if (self.current_state in ["Transition_Back_To_HTML", "Transition_To_JS", "Transition_To_CSS",
                                       "Transition_Back_To_HTML_Syntax"]):  ##change of language happended here
                return -2
            if (flag == True and self.index >= start and self.direction == 'R'):
                outputList.append(self.current_state)
        if (len(outputList) == 0):
            return -1
        else:
            return outputList

    def restart(self, JS):
        self.stack.empty()
        self.stack.push("$$$")
        self.js = JS
        self.current_state = self.start_state
        self.direction = 'R'
        self.current_char = ''
        self.index = -1
        self.returnState_after_Character_Reference_in_data = ''
        self.JSList = list(JS)
        self.outPutList = list()
