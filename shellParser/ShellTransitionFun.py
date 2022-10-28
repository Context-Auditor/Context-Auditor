
"""
    Shell Parsing State Machine Module -- Formulates bahs(1) Parsing in form of a two-way push down automata
    @author Faezeh Kalantari (faezeh.kalantari@asu.edu)
    @date March 24, 2019
"""

class ShellTransitionFun():
    shellStates={ 'SH_Start'

    }

    Blank = [' ', '\t']
    NewLine = ['\n', '\r', '\f', '\r\n']

    EOF = chr(0)
    ASCII_upper = list()

    for i in range(65, 91):
        ASCII_upper.append(chr(i))

    ASCII_lower = list()
    for i in range(97, 123):
        ASCII_lower.append(chr(i))
    # NonSpecialChars=
    ASCII_alpha = ASCII_upper + ASCII_lower
    Digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    CSS_Alpha_Digits = ASCII_alpha  + Digits
    NonSpecialChars = CSS_Alpha_Digits+ {'.'}
    SHTF=dict()

    #*********************************  SH_Start State Rules    ***********************************
    for char in Blank:
        SHTF[('SH_Start', char, '$$$')] = ('SH_Start', 'R', 'READ', '')
        SHTF[('SH_Start', char, 'NEC')] = ('After_Command', 'R', 'POP', 'NEC')
        ## FOR
        SHTF[('SH_Start', char, 'FOR')] = ('For_Expr', 'R', 'READ', '')
        ## FUNCTION
        SHTF[('SH_Start', char, 'FUNCTION')] = ('Fun_Expr', 'R', 'READ', '')


    for char in NewLine:
        SHTF[('SH_Start', char, '$$$')] = ('End_Command', 'R', 'READ', '')
        SHTF[('SH_Start', char, 'NEC')] = ('End_Command', 'R', 'POP', 'NEC')
        SHTF[('SH_Start', char, 'any')] = ('End_Command', 'R', 'READ', '')


    # sequence of characters considering as a word
    for char in NonSpecialChars:
        SHTF[('SH_Start', char, '$$$')] = ('SH_Start', 'R', 'PUSH', 'NEC') ##Nonempty Command
        SHTF[('SH_Start', char, 'NEC')] = ('SH_Start', 'R', 'READ', '')

    # Arithmetic Evaluation
    SHTF[('SH_Start', '!', 'any')] = ('Arithmetic_Eval', 'R', 'PUSH', '!')

    # Command Substitution
    SHTF[('SH_Start', '`', 'any')] = ('Command_Substitution', 'R', 'PUSH', '`')
    SHTF[('SH_Start', '`', 'NEC')] = ('Command_Substitution', 'R', 'CHANGE', '`')

    SHTF[('SH_Start', '$', 'any')] = ('Command_Substitution', 'R', 'PUSH', '$')
    SHTF[('SH_Start', '$', 'NEC')] = ('Command_Substitution', 'R', 'CHANGE', '$')

    # Key words
    SHTF[('SH_Start', 'f', '$$$')] = ('SH_Start', 'R', 'PUSH', 'F')
    ## FI
    SHTF[('SH_Start', 'i', 'F')] = ('SH_Start', 'R', 'CHANGE', 'FI')
    SHTF[('SH_Start', 'else', 'F')] = ('SH_Start', 'L', 'CHANGE', 'NEC')
    ## FOR
    SHTF[('SH_Start', 'o', 'F')] = ('SH_Start', 'R', 'CHANGE', 'FO')
    SHTF[('SH_Start', 'r', 'FO')] = ('SH_Start', 'R', 'CHANGE', 'FOR')
    SHTF[('SH_Start', 'else', 'FO')] = ('SH_Start', 'L', 'CHANGE', 'NEC')
    SHTF[('SH_Start', 'else', 'FOR')] = ('SH_Start', 'L', 'CHANGE', 'NEC')
    SHTF[('SH_Start', '(', 'FOR')] = ('For_Expr', 'R', 'CHANGE', 'FOR(')
    ## Function
    SHTF[('SH_Start', 'u', 'F')] = ('SH_Start', 'R', 'CHANGE', 'FU')
    SHTF[('SH_Start', 'n', 'FU')] = ('SH_Start', 'R', 'CHANGE', 'FUN')
    SHTF[('SH_Start', 'else', 'FU')] = ('SH_Start', 'L', 'CHANGE', 'NEC')
    SHTF[('SH_Start', 'c', 'FUN')] = ('SH_Start', 'R', 'CHANGE', 'FUNC')
    SHTF[('SH_Start', 'else', 'FUN')] = ('SH_Start', 'L', 'CHANGE', 'NEC')
    SHTF[('SH_Start', 't', 'FUNC')] = ('SH_Start', 'R', 'CHANGE', 'FUNCT')
    SHTF[('SH_Start', 'else', 'FUNC')] = ('SH_Start', 'L', 'CHANGE', 'NEC')
    SHTF[('SH_Start', 'i', 'FUNCT')] = ('SH_Start', 'R', 'CHANGE', 'FUNCTI')
    SHTF[('SH_Start', 'else', 'FUNCT')] = ('SH_Start', 'L', 'CHANGE', 'NEC')
    SHTF[('SH_Start', 'o', 'FUNCTI')] = ('SH_Start', 'R', 'CHANGE', 'FUNCTIO')
    SHTF[('SH_Start', 'else', 'FUNCTI')] = ('SH_Start', 'L', 'CHANGE', 'NEC')
    SHTF[('SH_Start', 'n', 'FUNCTIO')] = ('SH_Start', 'R', 'CHANGE', 'FUNCTION')
    SHTF[('SH_Start', 'else', 'FUNCTIO')] = ('SH_Start', 'L', 'CHANGE', 'NEC')




    #*********************************  After_Command Rules    ***********************************
    for char in Blank:
        SHTF[('After_Command', char, '$$$')] = ('After_Command', 'R', 'READ', '')
        SHTF[('After_Command', char, 'NEC')] = ('After_Command', 'R', 'POP', 'NEC')
    for char in NewLine:
        SHTF[('After_Command', char, '$$$')] = ('End_Command', 'R', 'READ', '')
        SHTF[('After_Command', char, 'NEC')] = ('End_Command', 'L', 'POP', 'NEC')
        SHTF[('After_Command', char, 'any')] = ('End_Command', 'R', 'READ', '')

    # sequence of characters considering as a word
    for char in NonSpecialChars:
        SHTF[('After_Command', char , '$$$')] = ('After_Command', 'R', 'PUSH', 'NEC') ##Nonempty Command
        SHTF[('After_Command', char , 'NEC')] = ('After_Command', 'R', 'READ', '')

    # Control Operators
    SHTF[('After_Command', ';', '$$$')] = ('Control_Operator', 'R', 'PUSH', ';')
    SHTF[('After_Command', ';', 'NEC')] = ('Control_Operator', 'R', 'CHANGE', ';')
    SHTF[('After_Command', '|', '$$$')] = ('Control_Operator', 'R', 'PUSH', '|')
    SHTF[('After_Command', '|', 'NEC')] = ('Control_Operator', 'R', 'CHANGE', '|')
    SHTF[('After_Command', '&', '$$$')] = ('Control_Operator', 'R', 'PUSH', '&')
    SHTF[('After_Command', '&', 'NEC')] = ('Control_Operator', 'R', 'CHANGE', '&')
    SHTF[('After_Command', '(', '$$$')] = ('Control_Operator', 'R', 'PUSH', '(')
    SHTF[('After_Command', '(', 'NEC')] = ('Control_Operator', 'R', 'CHANGE', '(')
    SHTF[('After_Command', ')', '(')] = ('Control_Operator', 'R', 'POP', '(')
    SHTF[('After_Command', ')', '((')] = ('Control_Operator', 'R', 'CHANGE', '(')

    ### TODO Could we have ) here???

    ## Redirection
    SHTF[('After_Command', '>', '$$$')] = ('Redirection', 'R', 'PUSH', '>')
    SHTF[('After_Command', '>', 'NEC')] = ('Redirection', 'R', 'CHANGE', '>')
    SHTF[('After_Command', '<', '$$$')] = ('Redirection', 'R', 'PUSH', '<')
    SHTF[('After_Command', '<', 'NEC')] = ('Redirection', 'R', 'CHANGE', '<')




    #*********************************  After_Command Rules    ***********************************

    for char in NewLine:
        SHTF[('After_Command', char, 'any')] = ('End_Command', 'R', 'READ', '')
    SHTF[('Redirection', '<', '<')] = ('Redirection', 'R', 'CHANGE', 'WW')
    SHTF[('Redirection', '&', '<')] = ('Redirection', 'R', 'CHANGE', 'WW')
    SHTF[('Redirection', '>', '<')] = ('Redirection', 'R', 'CHANGE', 'WW')
    SHTF[('Redirection', '>', '>')] = ('Redirection', 'R', 'CHANGE', 'WW')
    SHTF[('Redirection', '&', '>')] = ('Redirection', 'R', 'CHANGE', 'WW')


    for char in NonSpecialChars:
        SHTF[('Redirection', char , 'WW')] = ('Redirection', 'R', 'CHANGE', 'RW')
        SHTF[('Redirection', char , '<')] = ('Redirection', 'R', 'CHANGE', 'RW')
        SHTF[('Redirection', char , '>')] = ('Redirection', 'R', 'CHANGE', 'RW')
        SHTF[('Redirection', char , 'RW')] = ('Redirection', 'R', 'READ', '')
        # Pipeline
        SHTF[('Control_Operator', char, '|')] = ('SH_Start', 'R', 'POP', '|')
        # List
        SHTF[('Control_Operator', char, '(')] = ('SH_Start', 'R', 'READ', '')
        SHTF[('Control_Operator', char, '((')] = ('SH_Start', 'R', 'READ', '')


    #*********************************  Control_Operator Rules    ***********************************
    SHTF[('Control_Operator', '<', '&')] = ('Redirection', 'R', 'CHANGE', 'WW')
    SHTF[('Control_Operator', '>', '&')] = ('Redirection', 'R', 'CHANGE', 'WW')

    # AND List
    SHTF[('Control_Operator', '&', '&')] = ('SH_Start', 'R', 'POP', '&')
    # Or List
    SHTF[('Control_Operator', '|', '|')] = ('SH_Start', 'R', 'POP', '|')
    # Pipeline
    SHTF[('Control_Operator', '&', '|')] = ('SH_Start', 'R', 'POP', '|')

    # List
    SHTF[('Control_Operator', '(', '(')] = ('Control_Operator', 'R', 'CHANGE', '((')
    SHTF[('Control_Operator', ')', '(')] = ('After_Command', 'R', 'POP', '')


    #*********************************  Arithmetic_Eval Rules    ***********************************
    for char in NonSpecialChars:
        SHTF[('Arithmetic_Eval', char , '!')] = ('SH_Start', 'L', 'CHANGE', 'NEC')


    #*********************************  For_Expr Rules    ***********************************
