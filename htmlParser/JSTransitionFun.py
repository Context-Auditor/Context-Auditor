



class JSTransitionFun():
    jsStates = {'Script_Start', 'Punctuators'
                                'Declaration_Statement', 'Declaration_Statement_pre1', 'Declaration_Statement_pre2',
                'Wait_For_Identifier', 'Identifier_Name', 'Wait_For_Assignment', 'Assignment',
                'Double_Quote_Inside_Assignment_Pushed', 'Quote_Skipped'
                                                         'Single_Quote_Inside_Assignment_Pushed',
                }  # we will complete it by code
    WHITESPACES = [' ', '\t', '\b']
    LINEBREAKS = ['\n']
    JSPunctuators = [
        '{', '(', ')', '[', ']',
        '.', '...', '<>', '<=', '>=', '==', '!=', '===', '!==', '+', '-', '*', '%', '**', '++', '--', '<<',
        '>>', '>>>', '&', '|', '^', '!', '~', '&&', '||', '?', ':', '=', '+=', '-=', '*=', '%=', '**=',
        '<<=', '>>=', '>>>=', '&=', '|=', '^=', '=>'
    ]
    JSSTRPunctuators = [
        '{', '(', ')', '[', ']',
        '.', '|'
    ]
    popsignes = ['=', '<', '-', '+S', '++S', '!=', '!==', '||', '==', '===', '<=', '<<=', '>', '>=', '+', 'TYPEOF',
                 'THROW', 'INSTANCEOF', 'DELETE', 'FUN.IN']

    JSOperators = ['+', '-', '*', '%']
    EOF = chr(0)
    ASCII_upper = list()

    for i in range(65, 91):
        ASCII_upper.append(chr(i))

    ASCII_lower = list()
    for i in range(97, 123):
        ASCII_lower.append(chr(i))
    Source_Char_Without_Non_Terminator = []
    ASCII_alpha = ASCII_upper + ASCII_lower
    Digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    JS_Alpha = ASCII_alpha + ['$', '_']
    JS_Alpha_Digits = ASCII_alpha + ['$', '_'] + Digits
    Source_Char = JS_Alpha_Digits
    for char in Source_Char:
        if char not in LINEBREAKS:
            Source_Char_Without_Non_Terminator.append(char)
    Identifier_Part = JS_Alpha

    Identifier_List = {
        '$IVAR', '$I{I', '$IFOR(VARI', '$IBP{I', '$IBP{IBE', '$IBP[I', '$IFOR(LETI', '$IFOR(LETIL',
        '$IBL', '$ITRY{}FINALLY{}CATCH(P', '$ITRY{}CATCH(P', '$IB{{', '$IFE', '$IFE(FP', '$IPN'
    }
    ##################################  JavaScript Transition Function ################################
    JSTF = dict()
    # *********************************  Script_Start State Rules    ***********************************
    ### go back to Script_Start
    JSTF[('Script_Start', ';', 'any')] = ('Script_Start', 'R', 'READ', '')
    for char in WHITESPACES:
        JSTF[('Script_Start', char, '$$$')] = ('Script_Start', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('Script_Start', char, '$$$')] = ('Script_Start', 'R', 'READ', '')
    JSTF[('Script_Start', 'else', "$$$")] = ('Specify_Assignment_Type', 'L', 'READ', '')
    # *********************************  Specify_Assignment_Type State Rules    ***********************************
    JSTF[('Specify_Assignment_Type', EOF, '$$$')] = ('Script_Start', 'R', 'READ', '')
    JSTF[('Specify_Assignment_Type', ')', 'FOR(E;E;E')] = ('Iteration_Statement_For', 'L', 'CHANGE', 'FOR(E;E;E')
    # var statement
    JSTF[('Specify_Assignment_Type', 'v', 'any')] = ('Identifier_Or_Function', 'R', 'PUSH', 'V')
    JSTF[('Identifier_Or_Function', 'a', 'V')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'VA')
    JSTF[('Identifier_Or_Function', 'else', 'V')] = ('Identifier_Or_Function', 'L', 'POP', 'V')
    JSTF[('Identifier_Or_Function', 'r', 'VA')] = ('Declaration_Statement', 'R', 'CHANGE', 'VARFIRST')
    JSTF[('Identifier_Or_Function', 'else', 'VA')] = ('Identifier_Or_Function', 'L', 'POP', 'VA')
    # semicolon
    JSTF[('Specify_Assignment_Type', ';', 'any')] = ('Check_For_Empty_Stack', 'L', 'READ', '')
    # null statement
    JSTF[('Specify_Assignment_Type', 'n', 'any')] = ('Identifier_Or_Function', 'R', 'PUSH', 'N')
    JSTF[('Identifier_Or_Function', 'u', 'N')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'NU')
    JSTF[('Identifier_Or_Function', 'else', 'N')] = ('Identifier_Or_Function', 'L', 'POP', 'N')
    JSTF[('Identifier_Or_Function', 'l', 'NU')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'NUL')
    JSTF[('Identifier_Or_Function', 'else', 'NU')] = ('Identifier_Or_Function', 'L', 'POP', 'NUL')
    JSTF[('Identifier_Or_Function', 'l', 'NUL')] = ('NullLiteral', 'R', 'POP', 'NULL')
    JSTF[('Identifier_Or_Function', 'else', 'NUL')] = ('Identifier_Or_Function', 'L', 'POP', 'NUL')
    # false literal
    JSTF[('Specify_Assignment_Type', 'f', 'any')] = ('Identifier_Or_Function', 'R', 'PUSH', 'F')
    JSTF[('Identifier_Or_Function', 'a', 'F')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'FA')
    JSTF[('Identifier_Or_Function', 'else', 'F')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'l', 'FA')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'FAL')
    JSTF[('Identifier_Or_Function', 'else', 'FA')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 's', 'FAL')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'FALS')
    JSTF[('Identifier_Or_Function', 'else', 'FAL')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'e', 'FALS')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'FALSE')
    JSTF[('Identifier_Or_Function', 'else', 'FALS')] = ('Identifier_Or_Function', 'L', 'POP', '')
    for char in WHITESPACES:
        JSTF[('Identifier_Or_Function', char, 'FALSE')] = ('Pre_After_Assignment_No_Line_Terminator', 'R', 'POP', '')
    for char in LINEBREAKS:
        JSTF[('Identifier_Or_Function', char, 'FALSE')] = ('After_Assignment', 'R', 'POP', '')
    JSTF[('Identifier_Or_Function', 'else', 'FALSE')] = ('Identifier_Or_Function', 'L', 'POP', '')
    # True literal
    JSTF[('Specify_Assignment_Type', 't', 'any')] = ('Identifier_Or_Function', 'R', 'PUSH', 'T')
    JSTF[('Identifier_Or_Function', 'r', 'T')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'TR')
    JSTF[('Identifier_Or_Function', 'else', 'T')] = ('Identifier_Or_Function', 'L', 'POP', 'T')
    JSTF[('Identifier_Or_Function', 'u', 'TR')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'TRU')
    JSTF[('Identifier_Or_Function', 'else', 'TR')] = ('Identifier_Or_Function', 'L', 'POP', 'TR')
    JSTF[('Identifier_Or_Function', 'e', 'TRU')] = ('Identifier_Or_Function', 'R', 'POP', 'TRU')
    JSTF[('Identifier_Or_Function', 'else', 'TRU')] = ('Identifier_Or_Function', 'L', 'POP', '')
    # Block Statement
    JSTF[('Specify_Assignment_Type', '{', 'any')] = ('Block_Statement', 'R', 'PUSH', 'B{{')
    JSTF[('Specify_Assignment_Type', '}', 'B{')] = ('Check_For_End_Of_Block', 'L', 'READ', '')
    # IfStatement
    JSTF[('Specify_Assignment_Type', 'i', 'any')] = ('Identifier_Or_Function', 'R', 'PUSH', 'I')
    JSTF[('Identifier_Or_Function', 'f', 'I')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'IF')
    JSTF[('Identifier_Or_Function', 'else', 'I')] = ('Identifier_Or_Function', 'L', 'POP', 'I')
    for char in WHITESPACES:
        JSTF[('Identifier_Or_Function', char, 'IF')] = ('If_Conditional_Statement', 'R', 'READ', 'IF')
    for char in LINEBREAKS:
        JSTF[('Identifier_Or_Function', char, 'IF')] = ('If_Conditional_Statement', 'R', 'READ', 'IF')
    JSTF[('Identifier_Or_Function', '(', 'IF')] = ('If_Conditional_Statement', 'L', 'READ', 'IF')
    JSTF[('Identifier_Or_Function', 'else', 'IF')] = ('Identifier_Or_Function', 'L', 'POP', 'IF')
    # else part
    JSTF[('Specify_Assignment_Type', 'e', 'IF()ELSE')] = ('If_Conditional_Statement_else1', 'R', 'READ', '')
    JSTF[('If_Conditional_Statement_else1', 'l', 'IF()ELSE')] = ('If_Conditional_Statement_else2', 'R', 'READ', '')
    JSTF[('If_Conditional_Statement_else1', 'else', 'IF()ELSE')] = ('Identifier_Or_Function', 'L', 'POP', 'IF()ELSE')
    JSTF[('If_Conditional_Statement_else2', 's', 'IF()ELSE')] = ('If_Conditional_Statement_else3', 'R', 'READ', '')
    JSTF[('If_Conditional_Statement_else2', 'else', 'IF()ELSE')] = ('Identifier_Or_Function', 'L', 'POP', 'IF()ELSE')
    JSTF[('If_Conditional_Statement_else3', 'e', 'IF()ELSE')] = ('If_Conditional_Statement_else4', 'R', 'READ', '')
    JSTF[('If_Conditional_Statement_else3', 'else', 'IF()ELSE')] = ('Identifier_Or_Function', 'L', 'POP', 'IF()ELSE')
    for char in WHITESPACES:
        JSTF[('If_Conditional_Statement_else4', char, 'IF()ELSE')] = (
            'Specify_Assignment_Type', 'R', 'READ', 'IF()ELSE')
    for char in LINEBREAKS:
        JSTF[('If_Conditional_Statement_else4', char, 'IF()ELSE')] = (
            'Specify_Assignment_Type', 'R', 'READ', 'IF()ELSE')
    JSTF[('If_Conditional_Statement_else4', 'else', 'IF()ELSE')] = ('Identifier_Or_Function', 'L', 'POP', 'IF()ELSE')
    # Continue Statement
    JSTF[('Specify_Assignment_Type', 'c', 'any')] = ('Identifier_Or_Function', 'R', 'PUSH', 'C')
    JSTF[('Identifier_Or_Function', 'o', 'C')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'CO')
    JSTF[('Identifier_Or_Function', 'else', 'C')] = ('Identifier_Or_Function', 'L', 'POP', 'C')
    JSTF[('Identifier_Or_Function', 'n', 'CO')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'CON')
    JSTF[('Identifier_Or_Function', 'else', 'CO')] = ('Identifier_Or_Function', 'L', 'POP', 'CO')
    JSTF[('Identifier_Or_Function', 't', 'CON')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'CONT')
    JSTF[('Identifier_Or_Function', 'else', 'CON')] = ('Identifier_Or_Function', 'L', 'POP', 'CON')
    JSTF[('Identifier_Or_Function', 'i', 'CONT')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'CONTI')
    JSTF[('Identifier_Or_Function', 'else', 'CONT')] = ('Identifier_Or_Function', 'L', 'POP', 'CONT')
    JSTF[('Identifier_Or_Function', 'n', 'CONTI')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'CONTIN')
    JSTF[('Identifier_Or_Function', 'else', 'CONTI')] = ('Identifier_Or_Function', 'L', 'POP', 'CONTI')
    JSTF[('Identifier_Or_Function', 'u', 'CONTIN')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'CONTINU')
    JSTF[('Identifier_Or_Function', 'else', 'CONTIN')] = ('Identifier_Or_Function', 'L', 'POP', 'CONTIN')
    JSTF[('Identifier_Or_Function', 'e', 'CONTINU')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'CONTINUE')
    JSTF[('Identifier_Or_Function', 'else', 'CONTINU')] = ('Identifier_Or_Function', 'L', 'POP', 'CONTINU')
    for char in WHITESPACES:
        JSTF[('Identifier_Or_Function', char, 'CONTINUE')] = (
            'No_Line_Terminator_Wait_For_Semicolon_Or_Identifier', 'R', 'CHANGE', 'DEBUGGER')
    for char in LINEBREAKS:
        JSTF[('Identifier_Or_Function', char, 'CONTINUE')] = ('Wait_For_Semicolon', 'R', 'CHANGE', 'DEBUGGER')
    JSTF[('Identifier_Or_Function', ';', 'CONTINUE')] = ('Wait_For_Semicolon', 'L', 'CHANGE', 'DEBUGGER')
    JSTF[('Identifier_Or_Function', 'else', 'CONTINUE')] = ('Identifier_Or_Function', 'L', 'POP', 'CONTINUE')
    # Break Statement
    JSTF[('Specify_Assignment_Type', 'b', 'any')] = ('Identifier_Or_Function', 'R', 'PUSH', 'B')
    JSTF[('Identifier_Or_Function', 'r', 'B')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'BR')
    JSTF[('Identifier_Or_Function', 'else', 'B')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'e', 'BR')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'BRE')
    JSTF[('Identifier_Or_Function', 'else', 'BR')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'a', 'BRE')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'BREA')
    JSTF[('Identifier_Or_Function', 'else', 'BRE')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'k', 'BREA')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'BREAK')
    JSTF[('Identifier_Or_Function', 'else', 'BREA')] = ('Identifier_Or_Function', 'L', 'POP', '')
    for char in WHITESPACES:
        JSTF[('Identifier_Or_Function', char, 'BREAK')] = (
            'No_Line_Terminator_Wait_For_Semicolon_Or_Identifier', 'R', 'CHANGE', 'DEBUGGER')
    for char in LINEBREAKS:
        JSTF[('Identifier_Or_Function', char, 'BREAK')] = ('Wait_For_Semicolon', 'R', 'CHANGE', 'DEBUGGER')
    JSTF[('Identifier_Or_Function', ';', 'BREAK')] = ('Wait_For_Semicolon', 'L', 'CHANGE', 'DEBUGGER')
    JSTF[('Identifier_Or_Function', 'else', 'BREAK')] = ('Identifier_Or_Function', 'L', 'POP', '')
    # return Statement
    JSTF[('Specify_Assignment_Type', 'r', 'any')] = ('Identifier_Or_Function', 'R', 'PUSH', 'R')
    JSTF[('Identifier_Or_Function', 'e', 'R')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'RE')
    JSTF[('Identifier_Or_Function', 'else', 'R')] = ('Identifier_Or_Function', 'L', 'POP', 'R')
    JSTF[('Identifier_Or_Function', 't', 'RE')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'RET')
    JSTF[('Identifier_Or_Function', 'else', 'RE')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'u', 'RET')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'RETU')
    JSTF[('Identifier_Or_Function', 'else', 'RET')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'r', 'RETU')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'RETUR')
    JSTF[('Identifier_Or_Function', 'else', 'RETU')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'n', 'RETUR')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'RETURN')
    JSTF[('Identifier_Or_Function', 'else', 'RETUR')] = ('Identifier_Or_Function', 'L', 'POP', '')
    for char in WHITESPACES:
        JSTF[('Identifier_Or_Function', char, 'RETURN')] = (
            'No_Line_Terminator_Wait_For_Assignment', 'R', 'CHANGE', 'THROW')
    for char in LINEBREAKS:
        JSTF[('Identifier_Or_Function', char, 'RETURN')] = ('Wait_For_Semicolon', 'R', 'CHANGE', 'DEBUGGER')
    JSTF[('Identifier_Or_Function', '{', 'RETURN')] = ('No_Line_Terminator_Wait_For_Assignment', 'L', 'CHANGE', 'THROW')
    JSTF[('Identifier_Or_Function', 'else', 'RETURN')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', '/', 'RETURN')] = ('RegularExpressionLiteral', 'R', 'CHANGE', 'REL//')
    # with Statement and Iteration_Statement_While
    JSTF[('Specify_Assignment_Type', 'w', 'any')] = ('Identifier_Or_Function', 'R', 'PUSH', 'W')
    JSTF[('Identifier_Or_Function', 'i', 'W')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'WI')
    JSTF[('Identifier_Or_Function', 'else', 'W')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 't', 'WI')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'WIT')
    JSTF[('Identifier_Or_Function', 'else', 'WI')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'h', 'WIT')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'WITH')
    JSTF[('Identifier_Or_Function', 'else', 'WIT')] = ('Identifier_Or_Function', 'L', 'POP', '')
    for char in WHITESPACES:
        JSTF[('Identifier_Or_Function', char, 'WITH')] = ('With_Statement', 'R', 'READ', 'WITH')
    for char in LINEBREAKS:
        JSTF[('Identifier_Or_Function', char, 'WITH')] = ('With_Statement', 'R', 'READ', 'WITH')
    JSTF[('Identifier_Or_Function', '(', 'WITH')] = ('With_Statement', 'L', 'READ', 'WITH')
    JSTF[('Identifier_Or_Function', 'else', 'WITH')] = ('Identifier_Or_Function', 'L', 'POP', '')
    # Iteration_Statement
    # Do Statement
    JSTF[('Specify_Assignment_Type', 'd', 'any')] = ('Identifier_Or_Function', 'R', 'PUSH', 'D')
    JSTF[('Identifier_Or_Function', 'o', 'D')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'DO')
    JSTF[('Identifier_Or_Function', 'else', 'D')] = ('Identifier_Or_Function', 'L', 'POP', '')
    for char in WHITESPACES:
        JSTF[('Identifier_Or_Function', char, 'DO')] = ('Iteration_Statement_Do', 'R', 'READ', 'DO')
    for char in LINEBREAKS:
        JSTF[('Identifier_Or_Function', char, 'DO')] = ('Iteration_Statement_Do', 'R', 'READ', 'DO')
    JSTF[('Identifier_Or_Function', '(', 'DO')] = ('Iteration_Statement_Do', 'L', 'READ', 'DO')
    JSTF[('Identifier_Or_Function', 'else', 'DO')] = ('Identifier_Or_Function', 'L', 'POP', '')
    # While
    JSTF[('Identifier_Or_Function', 'h', 'W')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'WH')
    JSTF[('Identifier_Or_Function', 'i', 'WH')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'WHI')
    JSTF[('Identifier_Or_Function', 'else', 'WH')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'l', 'WHI')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'WHIL')
    JSTF[('Identifier_Or_Function', 'else', 'WHI')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'e', 'WHIL')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'WHILE')
    JSTF[('Identifier_Or_Function', 'else', 'WHIL')] = ('Identifier_Or_Function', 'L', 'POP', '')
    for char in WHITESPACES:
        JSTF[('Identifier_Or_Function', char, 'WHILE')] = ('Iteration_Statement_While', 'R', 'READ', 'WHILE')
    for char in LINEBREAKS:
        JSTF[('Identifier_Or_Function', char, 'WHILE')] = ('Iteration_Statement_While', 'R', 'READ', 'WHILE')
    JSTF[('Identifier_Or_Function', '(', 'WHILE')] = ('Iteration_Statement_While', 'L', 'READ', 'WHILE')
    JSTF[('Identifier_Or_Function', 'else', 'WHILE')] = ('Identifier_Or_Function', 'L', 'POP', '')
    # For
    JSTF[('Identifier_Or_Function', 'o', 'F')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'FO')
    JSTF[('Identifier_Or_Function', 'r', 'FO')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'FOR')
    JSTF[('Identifier_Or_Function', 'else', 'FO')] = ('Identifier_Or_Function', 'L', 'POP', '')
    for char in WHITESPACES:
        JSTF[('Identifier_Or_Function', char, 'FOR')] = ('Iteration_Statement_For', 'R', 'READ', 'FOR')
    for char in LINEBREAKS:
        JSTF[('Identifier_Or_Function', char, 'FOR')] = ('Iteration_Statement_For', 'R', 'READ', 'FOR')
    JSTF[('Identifier_Or_Function', '(', 'FOR')] = ('Iteration_Statement_For', 'L', 'READ', 'FOR')
    JSTF[('Identifier_Or_Function', 'else', 'FOR')] = ('Identifier_Or_Function', 'L', 'POP', '')
    # Switch Statement
    JSTF[('Specify_Assignment_Type', 's', 'any')] = ('Identifier_Or_Function', 'R', 'PUSH', 'S')
    JSTF[('Identifier_Or_Function', 'w', 'S')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'SW')
    JSTF[('Identifier_Or_Function', 'else', 'S')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'i', 'SW')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'SWI')
    JSTF[('Identifier_Or_Function', 'else', 'SW')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 't', 'SWI')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'SWIT')
    JSTF[('Identifier_Or_Function', 'else', 'SWI')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'c', 'SWIT')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'SWITC')
    JSTF[('Identifier_Or_Function', 'else', 'SWIT')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'h', 'SWITC')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'SWITCH')
    JSTF[('Identifier_Or_Function', 'else', 'SWITC')] = ('Identifier_Or_Function', 'L', 'POP', '')
    for char in WHITESPACES:
        JSTF[('Identifier_Or_Function', char, 'SWITCH')] = ('Switch_Statement', 'R', 'READ', 'SWITCH')
    for char in LINEBREAKS:
        JSTF[('Identifier_Or_Function', char, 'SWITCH')] = ('Switch_Statement', 'R', 'READ', 'SWITCH')
    JSTF[('Identifier_Or_Function', 'else', 'SWITCH')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', '(', 'SWITCH')] = ('Switch_Statement', 'L', 'READ', '')
    # Throw Statement
    JSTF[('Identifier_Or_Function', 'h', 'T')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'TH')
    JSTF[('Identifier_Or_Function', 'r', 'TH')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'THR')
    JSTF[('Identifier_Or_Function', 'else', 'TH')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'o', 'THR')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'THRO')
    JSTF[('Identifier_Or_Function', 'else', 'THR')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'w', 'THRO')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'THROW')
    JSTF[('Identifier_Or_Function', 'else', 'THRO')] = ('Identifier_Or_Function', 'L', 'POP', '')
    for char in WHITESPACES:
        JSTF[('Identifier_Or_Function', char, 'THROW')] = (
            'No_Line_Terminator_Wait_For_Assignment', 'R', 'READ', 'THROW')
    for char in LINEBREAKS:
        JSTF[('Identifier_Or_Function', char, 'THROW')] = ('Syntax_Error', 'R', 'READ', '')
    JSTF[('Identifier_Or_Function', 'else', 'THROW')] = ('Identifier_Or_Function', 'L', 'POP', '')
    # Try Statement
    JSTF[('Identifier_Or_Function', 'y', 'TR')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'TRY')
    for char in WHITESPACES:
        JSTF[('Identifier_Or_Function', char, 'TRY')] = ('Try_Statement', 'R', 'READ', 'TRY')
    for char in LINEBREAKS:
        JSTF[('Identifier_Or_Function', char, 'TRY')] = ('Try_Statement', 'R', 'READ', 'TRY')
    JSTF[('Identifier_Or_Function', '{', 'TRY')] = ('Try_Statement', 'L', 'READ', 'TRY')
    JSTF[('Identifier_Or_Function', 'else', 'TRY')] = ('Identifier_Or_Function', 'L', 'POP', '')
    # Debugger Statement
    JSTF[('Identifier_Or_Function', 'e', 'D')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'DE')
    JSTF[('Identifier_Or_Function', 'b', 'DE')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'DEB')
    JSTF[('Identifier_Or_Function', 'else', 'DE')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'u', 'DEB')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'DEBU')
    JSTF[('Identifier_Or_Function', 'else', 'DEB')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'g', 'DEBU')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'DEBUG')
    JSTF[('Identifier_Or_Function', 'else', 'DEBU')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'g', 'DEBUG')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'DEBUGG')
    JSTF[('Identifier_Or_Function', 'else', 'DEBUG')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'e', 'DEBUGG')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'DEBUGGE')
    JSTF[('Identifier_Or_Function', 'else', 'DEBUGG')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'r', 'DEBUGGE')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'DEBUGGER')
    JSTF[('Identifier_Or_Function', 'else', 'DEBUGGE')] = ('Identifier_Or_Function', 'L', 'POP', '')
    for char in WHITESPACES:
        JSTF[('Identifier_Or_Function', char, 'DEBUGGER')] = ('Wait_For_Semicolon', 'R', 'READ', 'DEBUGGER')
    for char in LINEBREAKS:
        JSTF[('Identifier_Or_Function', char, 'DEBUGGER')] = ('Wait_For_Semicolon', 'R', 'READ', 'DEBUGGER')
    JSTF[('Identifier_Or_Function', 'else', 'DEBUGGER')] = ('Identifier_Or_Function', 'L', 'POP', '')

    for char in JS_Alpha:
        if (not char in ['v', 'i', 'n', 't', 'f', 'e', 'c', 'b', 'r', 'w', 'd', 'a', 's']):
            JSTF[('Specify_Assignment_Type', char, 'any')] = ('Identifier_Or_Function', 'L', 'PUSH', '$I')
    for char in WHITESPACES:
        JSTF[('Specify_Assignment_Type', char, 'any')] = ('Specify_Assignment_Type', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('Specify_Assignment_Type', char, 'any')] = ('Specify_Assignment_Type', 'R', 'READ', '')
    JSTF[('Identifier_Or_Function', 'u', 'F')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'FU')
    JSTF[('Identifier_Or_Function', 'else', 'F')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'n', 'FU')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'FUN')
    JSTF[('Identifier_Or_Function', 'else', 'FU')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'c', 'FUN')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'FUNC')
    JSTF[('Identifier_Or_Function', 'else', 'FUN')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 't', 'FUNC')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'FUNCT')
    JSTF[('Identifier_Or_Function', 'else', 'FUNC')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'i', 'FUNCT')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'FUNCTI')
    JSTF[('Identifier_Or_Function', 'else', 'FUNCT')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'o', 'FUNCTI')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'FUNCTIO')
    JSTF[('Identifier_Or_Function', 'else', 'FUNCTI')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'n', 'FUNCTIO')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'FUNCTION')
    JSTF[('Identifier_Or_Function', 'else', 'FUNCTIO')] = ('Identifier_Or_Function', 'L', 'POP', '')
    for char in WHITESPACES:
        JSTF[('Identifier_Or_Function', char, 'FUNCTION')] = ('FunctionDeclaration', 'R', 'CHANGE', 'FD')
    for char in LINEBREAKS:
        JSTF[('Identifier_Or_Function', char, 'FUNCTION')] = ('FunctionDeclaration', 'R', 'CHANGE', 'FD')
    JSTF[('Identifier_Or_Function', '*', 'FUNCTION')] = ('FunctionDeclaration', 'L', 'CHANGE', 'FD')
    JSTF[('Identifier_Or_Function', 'else', 'FUNCTION')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', '(', 'FUNCTION')] = ('FunctionExpression', 'L', 'CHANGE', 'FD')  # 1/30/20
    ## 14.6 AsyncDeclaration
    JSTF[('Specify_Assignment_Type', 'a', 'any')] = ('AsyncDeclaration1', 'R', 'READ', '')
    JSTF[('AsyncDeclaration1', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('AsyncDeclaration1', 's', 'any')] = ('AsyncDeclaration2', 'R', 'READ', '')
    JSTF[('AsyncDeclaration2', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('AsyncDeclaration2', 'y', 'any')] = ('AsyncDeclaration3', 'R', 'READ', '')
    JSTF[('AsyncDeclaration3', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('AsyncDeclaration3', 'n', 'any')] = ('AsyncDeclaration4', 'R', 'READ', '')
    JSTF[('AsyncDeclaration4', 'c', 'any')] = ('AsyncDeclaration5', 'R', 'READ', '')
    JSTF[('AsyncDeclaration4', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    for char in WHITESPACES:
        JSTF[('AsyncDeclaration5', char, 'any')] = ('AsyncDeclaration', 'R', 'READ', '')
    JSTF[('AsyncDeclaration5', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    # Class Declaration
    JSTF[('Continue_Statement1', 'l', 'any')] = ('ClassDeclaration1', 'R', 'READ', '')
    JSTF[('ClassDeclaration1', 'a', 'any')] = ('ClassDeclaration2', 'R', 'READ', '')
    JSTF[('ClassDeclaration1', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('ClassDeclaration2', 's', 'any')] = ('ClassDeclaration3', 'R', 'READ', '')
    JSTF[('ClassDeclaration2', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('ClassDeclaration3', 's', 'any')] = ('ClassDeclaration4', 'R', 'READ', '')
    JSTF[('ClassDeclaration3', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    for char in WHITESPACES:
        JSTF[('ClassDeclaration4', char, 'any')] = ('ClassDeclaration', 'R', 'PUSH', 'CD')
    for char in LINEBREAKS:
        JSTF[('ClassDeclaration4', char, 'any')] = ('ClassDeclaration', 'R', 'PUSH', 'CD')
    JSTF[('ClassDeclaration4', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')

    JSTF[('Specify_Assignment_Type', '/', 'any')] = ('RegularExpressionLiteral', 'R', 'PUSH', 'REL//')
    JSTF[('Specify_Assignment_Type', 'else', 'any')] = ('Wait_For_Assignment', 'L', 'READ', '')
    JSTF[('Specify_Assignment_Type', '}', '{')] = ('ObjectLiteral', 'L', 'READ', '')
    JSTF[('Specify_Assignment_Type', '}', 'any')] = ('Check_For_End_Of_Block', 'L', 'READ', '')
    JSTF[('Specify_Assignment_Type', 'else', '=')] = ('Specify_Assignment_Type', 'L', 'POP', '=')
    JSTF[('Specify_Assignment_Type', ',', '{I')] = ('Specify_Assignment_Type', 'R', 'READ', '')
    ##############################################################################################################################3
    # No_Line_Terminator_Wait_For_Semicolon_Or_Identifier
    for char in WHITESPACES:
        JSTF[('No_Line_Terminator_Wait_For_Semicolon_Or_Identifier', char, 'any')] = (
            'No_Line_Terminator_Wait_For_Semicolon_Or_Identifier', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('No_Line_Terminator_Wait_For_Semicolon_Or_Identifier', char, 'any')] = (
            'Wait_For_Semicolon', 'R', 'READ', '')
    for char in JS_Alpha:
        JSTF[('No_Line_Terminator_Wait_For_Semicolon_Or_Identifier', char, 'any')] = (
            'Identifier_Name', 'L', 'PUSH', '$I')
        JSTF[('No_Line_Terminator_Wait_For_Semicolon_Or_Identifier', char, 'DEBUGGER')] = (
            'Identifier_Name', 'L', 'CHANGE', '$I')

    JSTF[('No_Line_Terminator_Wait_For_Semicolon_Or_Identifier', ';', 'any')] = (
        'Specify_Assignment_Type', 'R', 'READ', '')
    JSTF[('No_Line_Terminator_Wait_For_Semicolon_Or_Identifier', 'else', 'DEBUGGER')] = (
        'No_Line_Terminator_Wait_For_Semicolon_Or_Identifier', 'L', 'POP', '')
    # Wait_For_Semicolon
    for char in WHITESPACES:
        JSTF[('Wait_For_Semicolon', char, 'any')] = ('Wait_For_Semicolon', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('Wait_For_Semicolon', char, 'any')] = ('Wait_For_Semicolon', 'R', 'READ', '')
    JSTF[('Wait_For_Semicolon', ';', 'any')] = ('Check_For_Empty_Stack', 'L', 'READ', '')
    # *********************************  BooleanLiteral State Rules    ***********************************
    for char in WHITESPACES:
        JSTF[('BooleanLiteral', char, 'any')] = ('Pre_After_Assignment_No_Line_Terminator', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('BooleanLiteral', char, 'any')] = ('After_Assignment', 'R', 'READ', '')
    JSTF[('BooleanLiteral', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    # *********************************  NullLiteral_I State Rules    ***********************************
    for char in WHITESPACES:
        JSTF[('NullLiteral', char, 'any')] = ('Pre_After_Assignment_No_Line_Terminator', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('NullLiteral', char, 'any')] = ('After_Assignment', 'R', 'READ', '')

    JSTF[('NullLiteral', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    # *********************************  Block_Statement State Rules    ***********************************
    # State Specific States
    for char in WHITESPACES:
        JSTF[('Block_Statement', char, 'any')] = ('Block_Statement', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('Block_Statement', char, 'any')] = ('Block_Statement', 'R', 'READ', '')
    for char in WHITESPACES:
        JSTF[('Block_Statement', char, 'B{{')] = ('Block_Statement', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('Block_Statement', char, 'B{{')] = ('Block_Statement', 'R', 'READ', '')
    JSTF[('Block_Statement', 'else', 'B{{')] = ('Specify_Assignment_Type', 'L', 'CHANGE', 'B{')
    # Potential_JSON
    JSTF[('Block_Statement', '"', 'B{{')] = ('Double_Quote_Inside_Assignment_Pushed', 'R', 'CHANGE', 'B{JSON')
    JSTF[('Block_Statement', "'", 'B{{')] = ('Single_Quote_Inside_Assignment_Pushed', 'R', 'CHANGE', 'B{JSON')
    JSTF[('Block_Statement', '}', 'any')] = ('Check_For_End_Of_Block', 'L', 'READ', '')
    JSTF[('Block_Statement', 'else', 'any')] = ('Specify_Assignment_Type', 'L', 'READ', '')
    # *********************************  Potential_JSON State Rules    ***********************************
    # State Specific States
    for char in WHITESPACES:
        JSTF[('Potential_JSON', char, 'any')] = ('Potential_JSON', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('Potential_JSON', char, 'any')] = ('Potential_JSON', 'R', 'READ', '')

    JSTF[('Potential_JSON', ':', 'B{JSON_S')] = ('Wait_For_Assignment', 'R', 'READ', '')
    JSTF[('Potential_JSON', 'else', 'B{JSON_S')] = ('After_Assignment', 'L', 'CHANGE', '{I')
    JSTF[('Potential_JSON', '}', 'B{JSON_SV')] = ('After_Assignment', 'R', 'POP', '')
    JSTF[('Potential_JSON', '}', 'B{JSON')] = ('After_Assignment', 'R', 'POP', '')
    JSTF[('Potential_JSON', ",", 'B{JSON_SV')] = ('Potential_JSON', 'R', 'CHANGE', 'B{JSON')
    JSTF[('Potential_JSON', '"', 'B{JSON')] = ('Double_Quote_Inside_Assignment_Pushed', 'R', 'CHANGE', 'B{JSON')
    JSTF[('Potential_JSON', "'", 'B{JSON')] = ('Single_Quote_Inside_Assignment_Pushed', 'R', 'CHANGE', 'B{JSON')
    # LetOrConst
    JSTF[('Block_Statement', 'l', 'any')] = ('Block_Statement_Let1', 'R', 'READ', '')
    JSTF[('Block_Statement_Let1', 'e', 'any')] = ('Block_Statement_Let2', 'R', 'READ', '')
    JSTF[('Block_Statement_Let1', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('Block_Statement_Let2', 't', 'any')] = ('Block_Statement_Let', 'R', 'READ', '')
    JSTF[('Block_Statement_Let2', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    for char in WHITESPACES:
        JSTF[('Block_Statement_Let', char, 'any')] = ('Wait_For_Identifier', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('Block_Statement_Let', char, 'any')] = ('Wait_For_Identifier', 'R', 'READ', '')
    JSTF[('Block_Statement_Let', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    # const
    JSTF[('Block_Statement', 'c', 'any')] = ('Block_Statement_Const1', 'R', 'READ', '')
    JSTF[('Block_Statement_Const1', 'o', 'any')] = ('Block_Statement_Const2', 'R', 'READ', '')
    JSTF[('Block_Statement_Const1', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('Block_Statement_Const2', 'n', 'any')] = ('Block_Statement_Const3', 'R', 'READ', '')
    JSTF[('Block_Statement_Const2', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('Block_Statement_Const3', 's', 'any')] = ('Block_Statement_Const4', 'R', 'READ', '')
    JSTF[('Block_Statement_Const3', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('Block_Statement_Const4', 't', 'any')] = ('Block_Statement_Const', 'R', 'READ', '')
    JSTF[('Block_Statement_Const4', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    for char in WHITESPACES:
        JSTF[('Block_Statement_Const', char, 'any')] = ('Wait_For_Identifier', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('Block_Statement_Const', char, 'any')] = ('Wait_For_Identifier', 'R', 'READ', '')
    JSTF[('Block_Statement_Const', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    # *********************************  Declaration_Statement State Rules    ***********************************
    # State Specific States
    for char in WHITESPACES:
        JSTF[('Declaration_Statement', char, 'any')] = ('Wait_For_Identifier', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('Declaration_Statement', char, 'any')] = ('Wait_For_Identifier', 'R', 'READ', '')
    # *********************************  Wait_For_Identifier State Rules    ***********************************
    # State Specific States
    for char in WHITESPACES:
        JSTF[('Wait_For_Identifier', char, 'any')] = ('Wait_For_Identifier', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('Wait_For_Identifier', char, 'any')] = ('Wait_For_Identifier', 'R', 'READ', '')

    for char in JS_Alpha:
        JSTF[('Wait_For_Identifier', char, 'any')] = ('Identifier_Name', 'L', 'PUSH', '$I')
        JSTF[('Wait_For_Identifier', char, 'VAR,')] = ('Identifier_Name', 'L', 'CHANGE', '$IVAR')
        JSTF[('Wait_For_Identifier', char, 'VARFIRST')] = ('Identifier_Name', 'L', 'CHANGE', '$IVAR')

    JSTF[('Wait_For_Identifier', ';', 'VAR')] = ('Check_For_Empty_Stack', 'L', 'READ', '')
    # *********************************  Identifier_Name State Rules    ***********************************
    # go back to Script_Start
    JSTF[('Identifier_Name', ';', 'any')] = ('Check_For_Empty_Stack', 'L', 'READ', '')
    for char in JS_Alpha_Digits:
        JSTF[('Identifier_Name', char, 'any')] = ('Identifier_Name', 'R', 'READ', '')

    for char in WHITESPACES:
        JSTF[('Identifier_Name', char, 'any')] = ('After_Identifier', 'R', 'READ', '')
        JSTF[('Identifier_Name', char, 'II')] = ('Wait_For_Semicolon', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('Identifier_Name', char, 'any')] = ('After_Identifier', 'R', 'READ', '')
        JSTF[('Identifier_Name', char, 'II')] = ('Wait_For_Semicolon', 'R', 'READ', '')

    JSTF[('Identifier_Name', ',', 'VAR')] = ('Wait_For_Identifier', 'R', 'CHANGE', 'VAR,')
    JSTF[('Identifier_Name', ',', 'FOR(VARI')] = (
        'Wait_For_Identifier', 'R', 'CHANGE', 'FOR(VARIL')  # just case-2 in Iteration_Statement_For
    JSTF[('Identifier_Name', ',', 'FOR(VARIL')] = (
        'Wait_For_Identifier', 'R', 'READ', '')  # just case-2 in Iteration_Statement_For
    JSTF[('Identifier_Name', ',', 'BP{I')] = ('ObjectBindingPattern', 'R', 'CHANGE', 'BP{{')  # ObjectBindingPattern
    JSTF[('Identifier_Name', ',', 'BP[I')] = ('ArrayBindingPattern', 'R', 'CHANGE', 'BP[')  # ArrayBindingPattern
    JSTF[('Identifier_Name', ',', 'BP{IBE')] = (
        'ObjectBindingPattern', 'R', 'CHANGE', 'BP{{')  # end of single name binding for a binding property
    JSTF[('Identifier_Name', '=', '{I')] = ('Wait_For_Assignment', 'R', 'CHANGE', '{IA')
    JSTF[('Identifier_Name', '=', 'BP{I')] = (
        'Wait_For_Assignment', 'R', 'READ', '')  # ObjectBindingPattern with Assignment
    JSTF[('Identifier_Name', '=', 'BP[I')] = (
        'Wait_For_Assignment', 'R', 'READ', '')  # ArrayBindingPattern with Assignment
    JSTF[('Identifier_Name', '=', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', '=')
    JSTF[('Identifier_Name', '=', 'VAR')] = ('Wait_For_Assignment', 'R', 'CHANGE', '=')
    JSTF[('Identifier_Name', '=', 'II')] = ('Syntax_Error', 'R', 'READ', '')
    JSTF[('Identifier_Name', '=', 'FOR(VARI')] = (
        'Wait_For_Assignment', 'R', 'CHANGE', 'FOR(VARIL')  # just case-2 in Iteration_Statement_For
    JSTF[('Identifier_Name', '=', 'BP{IBE')] = ('Wait_For_Assignment', 'R', 'READ', '')
    JSTF[('NullLiteral_I_pre1', 'u', 'any')] = ('NullLiteral_I_pre2', 'R', 'READ', '')
    JSTF[('NullLiteral_I_pre1', 'else', 'any')] = ('Identifier_Name', 'L', 'READ', '')
    JSTF[('NullLiteral_I_pre2', 'l', 'any')] = ('NullLiteral_I_pre3', 'R', 'READ', '')
    JSTF[('NullLiteral_I_pre2', 'else', 'any')] = ('Identifier_Name', 'L', 'READ', '')
    JSTF[('NullLiteral_I_pre3', 'l', 'any')] = ('NullLiteral_I', 'R', 'READ', '')
    JSTF[('NullLiteral_I_pre3', 'else', 'any')] = ('Identifier_Name', 'L', 'READ', '')
    JSTF[('BooleanLiteralF_I_pre1', 'a', 'any')] = ('BooleanLiteralF_I__pre2', 'R', 'READ', '')
    JSTF[('BooleanLiteralF_I_pre1', 'else', 'any')] = ('Identifier_Name', 'L', 'READ', '')
    JSTF[('BooleanLiteralF_I__pre2', 'l', 'any')] = ('BooleanLiteralF_I_pre3', 'R', 'READ', '')
    JSTF[('BooleanLiteralF_I__pre2', 'else', 'any')] = ('Identifier_Name', 'L', 'READ', '')
    JSTF[('BooleanLiteralF_I_pre3', 's', 'any')] = ('BooleanLiteralF_I_4', 'R', 'READ', '')
    JSTF[('BooleanLiteralF_I_pre3', 'else', 'any')] = ('Identifier_Name', 'L', 'READ', '')
    JSTF[('BooleanLiteralF_I_pre4', 'e', 'any')] = ('BooleanLiteral_I', 'R', 'READ', '')
    JSTF[('BooleanLiteralF_I_pre4', 'else', 'any')] = ('Identifier_Name', 'L', 'READ', '')
    # #True keyword
    JSTF[('Identifier_Name', 'else', 'any')] = (
        'After_Identifier', 'L', 'READ', '')
    ## cases 3, 6 and 9 in Assignment Expression
    JSTF[('Identifier_Name', '=', 'FOR(LETI')] = ('Wait_For_Assignment', 'R', 'CHANGE', 'FOR(LETIL')
    JSTF[('Identifier_Name', ',', 'FOR(LETI')] = ('Iteration_Statement_For_Let', 'R', 'CHANGE', 'FOR(LETIL,')
    # Switch Statement
    JSTF[('Identifier_Name', ',', 'BL')] = ('BindingList', 'R', 'CHANGE', 'BL,')
    JSTF[('Identifier_Name', '=', 'BL')] = ('Wait_For_Assignment', 'R', 'READ', '')
    # FunctionExpression
    JSTF[('Identifier_Name', '(', 'FE')] = ('FormalParameters', 'R', 'CHANGE', 'FE((')
    JSTF[('Identifier_Name', '=', 'FE(FP')] = ('Wait_For_Assignment', 'R', 'READ', '')
    JSTF[('Identifier_Name', ')', 'FE(R')] = ('FunctionExpression', 'R', 'CHANGE', 'FE()')
    # SetMethod in MethodDefinition
    JSTF[('Identifier_Name', ')', 'SMD(')] = ('GetMethodWaitForBody', 'R', 'CHANGE', 'FD')
    JSTF[('Identifier_Name', '=', 'SMD(')] = ('Wait_For_Assignment', 'R', 'READ', '')
    # Arrow Parameter
    JSTF[('Identifier_Name', ')', 'APR')] = ('Pre_After_Identifier_Or_Function', 'R', 'POP', 'APR')
    # *********************************  BooleanLiteral_I State Rules    ***********************************
    for char in WHITESPACES:
        JSTF[('BooleanLiteral_I', char, 'any')] = ('Pre_After_Assignment_No_Line_Terminator', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('BooleanLiteral_I', char, 'any')] = ('After_Assignment', 'R', 'READ', '')
    JSTF[('BooleanLiteral_I', char, 'any')] = ('Identifier_Name', 'R', 'READ', '')
    # *********************************  NullLiteral_I State Rules    ***********************************
    for char in WHITESPACES:
        JSTF[('NullLiteral_I', char, 'any')] = ('Pre_After_Assignment_No_Line_Terminator', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('NullLiteral_I', char, 'any')] = ('After_Assignment', 'R', 'READ', '')
    # *********************************  After_Identifier State Rules    ***********************************
    # State Specific States
    for char in WHITESPACES:
        JSTF[('After_Identifier', char, 'any')] = ('After_Identifier', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('After_Identifier', char, 'any')] = ('After_Identifier', 'R', 'READ', '')
    JSTF[('After_Identifier', '=', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH',
                                              '=')  ## This is will fundamentally implement initializer's part for VariableDeclaration (13.3.2)
    JSTF[('After_Identifier', '=', 'VAR')] = ('Wait_For_Assignment', 'R', 'CHANGE',
                                              '=')  ## This is will fundamentally implement initializer's part for VariableDeclaration (13.3.2)
    # ObjectLiteral
    JSTF[('After_Identifier', '=', '{I')] = ('Wait_For_Assignment', 'R', 'CHANGE', '{IA')
    JSTF[('After_Identifier', '=', 'FOR(VARI')] = (
        'Wait_For_Assignment', 'R', 'CHANGE', 'FOR(VARIL')  # just case-2 in Iteration_Statement_For
    JSTF[('After_Identifier', '=', 'FOR(VARIL')] = (
        'Wait_For_Assignment', 'R', 'READ', '')  # just case-2 in Iteration_Statement_For
    JSTF[('After_Identifier', '=', 'BP{IBE')] = (
        'Wait_For_Assignment', 'R', 'READ', '')  # single name binding for a binding property
    JSTF[('After_Identifier', ',', '{I')] = ('ObjectLiteral', 'L', 'CHANGE', '{')
    JSTF[('After_Identifier', '}', '{I')] = ('ObjectLiteral', 'L', 'CHANGE', '{')
    JSTF[('After_Identifier', ',', 'VAR')] = ('Wait_For_Identifier', 'R', 'CHANGE', 'VAR,')
    JSTF[('After_Identifier', ',', 'FOR(VARI')] = (
        'Wait_For_Assignment', 'R', 'CHANGE', 'FOR(VARIL')  # just case-2 in Iteration_Statement_For
    JSTF[('After_Identifier', ',', 'FOR(VARIL')] = (
        'ObjectBindingPattern', 'R', 'CHANGE', 'BP{{')  # just case-2 in Iteration_Statement_For
    JSTF[('After_Identifier', ',', 'BP{IBE')] = (
        'ObjectBindingPattern', 'R', 'CHANGE', 'BP{{')  # end of single name binding for a binding property
    JSTF[('After_Identifier', ';', 'VAR')] = ('Check_For_Empty_Stack', 'L', 'READ', '')
    JSTF[('After_Identifier', ';', 'any')] = ('Check_For_Empty_Stack', 'L', 'READ', '')
    JSTF[('After_Identifier', '}', 'any')] = ('Syntax_Error', 'R', 'READ', '')
    # ObjectLiteral Wait_For_Assignment
    JSTF[('After_Identifier', ':', '{I')] = ('Wait_For_Assignment', 'R', 'CHANGE', '{IA')
    # Iteration_Statement_For case5
    # A single identifier
    JSTF[('After_Identifier', 'i', 'FOR(VARI')] = ('Iteration_Statement_Case6_In1', 'R', 'READ', '')
    # Binding Pattern
    JSTF[('After_Identifier', 'i', 'BP{I')] = ('Iteration_Statement_Case6_In1', 'R', 'READ', '')
    # Binding pattern for object or array FOR(VARBP
    JSTF[('After_Identifier', 'i', 'FOR(VARBP')] = ('Iteration_Statement_Case6_In1', 'R', 'READ', '')
    # cases 3, 6 and 9 of iteration statement
    JSTF[('After_Identifier', 'i', 'FOR(LETI')] = ('Iteration_Statement_Case6_In1', 'R', 'READ', '')

    JSTF[('Iteration_Statement_Case6_In1', 'n', 'any')] = ('Iteration_Statement_Case6_In2', 'R', 'READ', '')
    JSTF[('Iteration_Statement_Case6_In1', 'else', 'any')] = (
        'Syntax_Error', 'R', 'READ', '')
    for char in WHITESPACES:
        JSTF[('Iteration_Statement_Case6_In2', char, 'any')] = ('Wait_For_Assignment', 'R', 'CHANGE', 'FOR(VARFB')

    for char in LINEBREAKS:
        JSTF[('Iteration_Statement_Case6_In2', char, 'any')] = (
            'Wait_For_Assignment', 'R', 'CHANGE', 'FOR(VARFB')
    JSTF[('Iteration_Statement_Case6_In2', 'else', 'any')] = ('Syntax_Error', 'R', 'READ', '')
    # Iteration_Statement_For case8
    # A single Identifier
    JSTF[('After_Identifier', 'o', 'FOR(VARI')] = ('Iteration_Statement_Case6_Of1', 'R', 'READ', '')
    # Binding Pattern
    JSTF[('After_Identifier', 'o', 'BP{I')] = ('Iteration_Statement_Case6_Of1', 'R', 'READ', '')
    # Binding pattern for object or array FOR(VARBP
    JSTF[('After_Identifier', 'o', 'FOR(VARBP')] = ('Iteration_Statement_Case6_Of1', 'R', 'READ', '')
    # cases 3, 6 and 9 of iteration statement
    JSTF[('After_Identifier', 'o', 'FOR(LETI')] = ('Iteration_Statement_Case6_Of1', 'R', 'READ', '')
    JSTF[('Iteration_Statement_Case6_Of1', 'f', 'any')] = ('Iteration_Statement_Case6_Of2', 'R', 'READ', '')
    JSTF[('Iteration_Statement_Case6_Of1', 'else', 'any')] = (
        'Syntax_Error', 'R', 'READ', '')
    for char in WHITESPACES:
        JSTF[('Iteration_Statement_Case6_Of2', char, 'any')] = ('Wait_For_Assignment', 'R', 'CHANGE', 'FOR(VARFB')

    for char in LINEBREAKS:
        JSTF[('Iteration_Statement_Case6_Of2', char, 'any')] = ('Wait_For_Assignment', 'R', 'CHANGE', 'FOR(VARFB')
    JSTF[('Iteration_Statement_Case6_Of2', 'else', 'any')] = (
        'Syntax_Error', 'R', 'READ', '')
    # ObjectBindingPattern
    JSTF[('After_Identifier', ',', 'BP{I')] = ('ObjectBindingPattern', 'R', 'CHANGE', 'BP{{')  # ObjectBindingPattern
    JSTF[('After_Identifier', '=', 'BP{I')] = (
        'Wait_For_Assignment', 'R', 'READ', '')  # ObjectBindingPattern with Assignment
    JSTF[('After_Identifier', '}', 'BP{I')] = ('ObjectBindingPattern', 'L', 'CHANGE', 'BP{')  # ObjectBindingPattern
    # ArrayBindingPattern
    JSTF[('After_Identifier', ',', 'BP[I')] = ('ArrayBindingPattern', 'R', 'CHANGE', 'BP[')  # ObjectBindingPattern
    JSTF[('After_Identifier', '=', 'BP[I')] = (
        'Wait_For_Assignment', 'R', 'READ', '')  # ObjectBindingPattern with Assignment
    JSTF[('After_Identifier', ']', 'BP[I')] = ('ObjectBindingPattern', 'L', 'RAED', '')  # ObjectBindingPattern
    # BindingResetElemet For Array BindingPattern
    JSTF[('After_Identifier', 'else', 'BP[...')] = ('Wait_For_End_Of_ArrayBindingPattern', 'L', 'READ', '')
    # cases 3, 6 and 9 of iteration statement
    JSTF[('After_Identifier', '=', 'FOR(LETI')] = ('Wait_For_Assignment', 'R', 'CHANGE', 'FOR(LETIL')
    JSTF[('After_Identifier', ',', 'FOR(LETI')] = ('Iteration_Statement_For_Let', 'R', 'CHANGE', 'FOR(LETIL,')
    ###
    JSTF[('After_Identifier', 'else', 'FOR(LETI')] = (
        'Wait_For_Assignment', 'L', 'CHANGE', 'FOR(LETIE')  ### THIS WOULD BE AN EXPRESSION
    JSTF[('After_Identifier', '=', 'FOR(LETILBP')] = ('Wait_For_Assignment', 'R', 'CHANGE', 'FOR(LETIL')
    # Switch Statement
    JSTF[('After_Identifier', ',', 'BL')] = ('BindingList', 'R', 'CHANGE', 'BL,')
    JSTF[('After_Identifier', '=', 'BL')] = ('Wait_For_Assignment', 'R', 'READ', '')
    # labeled Statement
    JSTF[('After_Identifier', ':', 'any')] = ('Labeled_Statement', 'R', 'PUSH', 'LS')
    JSTF[('Specify_Assignment_Type', ':', 'any')] = ('Labeled_Statement', 'R', 'PUSH', 'LS')  # 1/29/20
    # Try and Catch Statement
    JSTF[('After_Identifier', 'else', 'TRY{}CATCH(P')] = ('Catch_Statement', 'L', 'READ', '')
    JSTF[('After_Identifier', 'else', 'TRY{}FINALLY{}CATCH(P')] = ('Catch_Statement', 'L', 'READ', '')
    # FunctionExpression
    JSTF[('After_Identifier', '(', 'FE')] = ('FormalParameters', 'R', 'CHANGE', 'FE((')
    JSTF[('After_Identifier', '=', 'FE(FP')] = ('Wait_For_Assignment', 'R', 'READ', '')
    JSTF[('After_Identifier', 'else', 'FE(FP')] = ('FormalParameters', 'L', 'READ', '')
    JSTF[('After_Identifier', ')', 'FE(R')] = ('FunctionExpression', 'R', 'CHANGE', 'FE()')
    # ClassDeclaration
    JSTF[('After_Identifier', 'else', 'CD')] = ('ClassTail', 'L', 'READ', '')
    # PropertyName
    JSTF[('After_Identifier', 'else', 'PN')] = ('After_PropertyName', 'L', 'POP', '')
    # SetMethod in MethodDefinition
    JSTF[('After_Identifier', ')', 'SMD(')] = ('GetMethodWaitForBody', 'R', 'CHANGE', 'FD')
    JSTF[('After_Identifier', '=', 'SMD(')] = ('Wait_For_Assignment', 'R', 'READ', '')
    # Arrow Parameter
    JSTF[('After_Identifier', ')', 'APR')] = ('Pre_After_Identifier_Or_Function', 'R', 'POP', 'APR')
    # AsyncArrowFunction
    JSTF[('After_Identifier', 'else', 'AF')] = ('AsyncArrowFunction', 'L', 'CHANGE', 'AFB')
    # CallExpression . Identifier
    JSTF[('After_Identifier', 'else', 'FUN.IN')] = ('Pre_After_Function_No_Line_Terminator', 'L', 'POP', 'FUN.IN')
    # Member Expression . IdentifierName
    ##JSTF[('After_Identifier', 'else', 'ME.')] = ('Pre_After_Assignment_No_Line_Terminator', 'L', 'POP', 'ME.')
    # SuperProperty: super . Identifier
    JSTF[('After_Identifier', 'else', 'SUP.IN')] = ('Pre_After_Assignment_No_Line_Terminator', 'L', 'POP', 'SUP.IN')
    # ********************************* No_Line_Terminator_Wait_For_Assignment State Rules    ***********************************
    JSTF[('No_Line_Terminator_Wait_For_Assignment', 'else', 'any')] = ('Wait_For_Assignment', 'L', 'READ', '')
    for char in WHITESPACES:
        JSTF[('No_Line_Terminator_Wait_For_Assignment', char, 'any')] = (
            'No_Line_Terminator_Wait_For_Assignment', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('No_Line_Terminator_Wait_For_Assignment', char, 'THROW')] = ('Syntax_Error', 'R', 'READ', '')
    # *********************************  Wait_For_Assignment State Rules    ***********************************
    # go back to Script_Start
    # State Specific States
    for char in WHITESPACES:
        JSTF[('Wait_For_Assignment', char, 'any')] = ('Wait_For_Assignment', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('Wait_For_Assignment', char, 'any')] = ('Wait_For_Assignment', 'R', 'READ', '')

    JSTF[('Wait_For_Assignment', '(', '=')] = ('Wait_For_Assignment', 'L', 'POP', '=')
    JSTF[('Wait_For_Assignment', '[', 'any')] = ('ArrayLiteral', 'R', 'PUSH', '[')
    JSTF[('Wait_For_Assignment', '{', 'any')] = ('ObjectLiteral', 'R', 'PUSH', '{{')
    JSTF[('Wait_For_Assignment', 'else', 'any')] = ('Assignment', 'L', 'READ', '')
    # Unary Expression Prefixes
    JSTF[('Wait_For_Assignment', '+', 'any')] = ('Wait_For_Assignment_Plus', 'R', 'READ', '')
    JSTF[('Wait_For_Assignment_Plus', '+', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', '++S')
    JSTF[('Wait_For_Assignment_Plus', 'else', 'any')] = ('Wait_For_Assignment', 'L', 'PUSH', '+S')
    JSTF[('Wait_For_Assignment', '-', 'any')] = ('Wait_For_Assignment_Minus', 'R', 'READ', '')
    JSTF[('Wait_For_Assignment_Minus', '-', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', '--S')
    JSTF[('Wait_For_Assignment_Minus', 'else', 'any')] = ('Wait_For_Assignment', 'L', 'PUSH', '-S')
    JSTF[('Wait_For_Assignment', '~', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', '~S')
    JSTF[('Wait_For_Assignment', '!', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', '!S')
    JSTF[('Wait_For_Assignment', 'else', '!S')] = ('Wait_For_Assignment', 'L', 'POP', '!S')
    # Unary Expression void prefix
    JSTF[('Wait_For_Assignment', 'v', 'any')] = ('Void_Prefix1', 'R', 'READ', '')
    JSTF[('Void_Prefix1', 'o', 'any')] = ('Void_Prefix2', 'R', 'READ', '')
    JSTF[('Void_Prefix1', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('Void_Prefix2', 'i', 'any')] = ('Void_Prefix3', 'R', 'READ', '')
    JSTF[('Void_Prefix2', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('Void_Prefix3', 'd', 'any')] = ('Void_Prefix', 'R', 'READ', '')
    JSTF[('Void_Prefix3', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    for char in WHITESPACES:
        JSTF[('Void_Prefix', char, 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', 'VOID')
    for char in LINEBREAKS:
        JSTF[('Void_Prefix', char, 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', 'VOID')
    JSTF[('Void_Prefix', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    # Unary Expression delete prefix
    JSTF[('Wait_For_Assignment', 'd', 'any')] = ('Identifier_Or_Function', 'R', 'PUSH', 'D')
    JSTF[('Identifier_Or_Function', 'e', 'D')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'DE')
    JSTF[('Identifier_Or_Function', 'else', 'D')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'l', 'DE')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'DEL')
    JSTF[('Identifier_Or_Function', 'else', 'DE')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'e', 'DEL')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'DELE')
    JSTF[('Identifier_Or_Function', 'else', 'DEL')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 't', 'DELE')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'DELET')
    JSTF[('Identifier_Or_Function', 'else', 'DELE')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'e', 'DELET')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'DELETE')
    JSTF[('Identifier_Or_Function', 'else', 'DELET')] = ('Identifier_Or_Function', 'L', 'POP', '')
    for char in WHITESPACES:
        JSTF[('Identifier_Or_Function', char, 'DELETE')] = ('Wait_For_Assignment', 'R', 'CHANGE', 'DELETE')
    for char in LINEBREAKS:
        JSTF[('Identifier_Or_Function', char, 'DELETE')] = ('Wait_For_Assignment', 'R', 'CHANGE', 'DELETE')
    JSTF[('Identifier_Or_Function', 'else', 'DELETE')] = ('Identifier_Or_Function', 'L', 'POP', '')
    # Unary Expression typeof prefix
    JSTF[('Wait_For_Assignment', 't', 'any')] = ('Identifier_Or_Function', 'R', 'PUSH', 'T')
    JSTF[('Wait_For_Assignment', 't', '=')] = ('Identifier_Or_Function', 'R', 'POP', '=')
    JSTF[('Identifier_Or_Function', 'y', 'T')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'TY')
    JSTF[('Identifier_Or_Function', 'else', 'T')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'p', 'TY')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'TYP')
    JSTF[('Identifier_Or_Function', 'else', 'TY')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'e', 'TYP')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'TYPE')
    JSTF[('Identifier_Or_Function', 'else', 'TYP')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'o', 'TYPE')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'TYPEO')
    JSTF[('Identifier_Or_Function', 'else', 'TYPE')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'f', 'TYPEO')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'TYPEOF')
    JSTF[('Identifier_Or_Function', 'else', 'TYPEO')] = ('Identifier_Or_Function', 'L', 'POP', '')
    for char in WHITESPACES:
        JSTF[('Identifier_Or_Function', char, 'TYPEOF')] = ('Wait_For_Assignment', 'R', 'READ', 'TYPEOF')
    for char in LINEBREAKS:
        JSTF[('Identifier_Or_Function', char, 'TYPEOF')] = ('Wait_For_Assignment', 'R', 'READ', 'TYPEOF')
    JSTF[('Identifier_Or_Function', 'else', 'TYPEOF')] = ('Identifier_Or_Function', 'L', 'POP', '')
    # Unary Expression await prefix
    JSTF[('Wait_For_Assignment', 'a', 'any')] = ('Identifier_Or_Function', 'R', 'PUSH', 'A-A')
    JSTF[('Identifier_Or_Function', 'w', 'A-A')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'A-AW')
    JSTF[('Identifier_Or_Function', 'else', 'A-A')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'a', 'A-AW')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'A-AWA')
    JSTF[('Identifier_Or_Function', 'else', 'A-AW')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'i', 'A-AWA')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'A-AWAI')
    JSTF[('Identifier_Or_Function', 'else', 'A-AWA')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 't', 'A-AWAI')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'A-AWAIT')
    JSTF[('Identifier_Or_Function', 'else', 'A-AWAI')] = ('Identifier_Or_Function', 'L', 'POP', '')
    for char in WHITESPACES:
        JSTF[('Identifier_Or_Function', char, 'A-AWAIT')] = ('Wait_For_Assignment', 'R', 'CHANGE', 'AWAIT')
    for char in LINEBREAKS:
        JSTF[('Identifier_Or_Function', char, 'A-AWAIT')] = ('Wait_For_Assignment', 'R', 'CHANGE', 'AWAIT')
    JSTF[('Identifier_Or_Function', 'else', 'A-AWAIT')] = ('Identifier_Or_Function', 'L', 'POP', '')
    # AsyncArrowFunction
    JSTF[('Identifier_Or_Function', 's', 'A-A')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'A-AS')
    JSTF[('Identifier_Or_Function', 'else', 'A-AS')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'y', 'A-AS')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'A-ASY')
    JSTF[('Identifier_Or_Function', 'else', 'A-AS')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'n', 'A-ASY')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'A-ASYN')
    JSTF[('Identifier_Or_Function', 'else', 'A-ASY')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'c', 'A-ASYN')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'A-ASYNC')
    JSTF[('Identifier_Or_Function', 'else', 'A-ASYN')] = ('Identifier_Or_Function', 'L', 'POP', '')
    for char in WHITESPACES:
        JSTF[('Identifier_Or_Function', char, 'A-ASYNC')] = ('AsyncArrowFunction', 'R', 'CHANGE', 'AF')
    for char in LINEBREAKS:
        JSTF[('Identifier_Or_Function', char, 'A-ASYNC')] = ('Syntax_Error', 'R', 'READ', '')
    JSTF[('Identifier_Or_Function', 'else', 'A-ASYNC')] = ('Identifier_Or_Function', 'L', 'POP', '')
    # Arguments
    # Primary Expression TemplateLiteral
    JSTF[('Wait_For_Assignment', '`', 'any')] = ('TemplateLiteral', 'R', 'PUSH', '`')
    ## nested conditional ?:
    JSTF[('Wait_For_Assignment', 'else', '?:')] = ('Wait_For_Assignment', 'L', 'POP', '?:')
    ##Error fix
    JSTF[('Wait_For_Assignment', '=', '=')] = ('Equality_Expression', 'R', 'READ', '')
    JSTF[('Wait_For_Assignment', 'else', '<')] = ('Wait_For_Assignment', 'L', 'POP', '<')  ## related to tag_skip
    JSTF[('Wait_For_Assignment', 'else', '-')] = (
        'Wait_For_Assignment', 'L', 'POP', '-')  ## related to await expression and characters
    JSTF[('Wait_For_Assignment', 'else', '+S')] = (
        'Wait_For_Assignment', 'L', 'POP', '+S')  ## related to await expression and characters
    JSTF[('Wait_For_Assignment', 'else', '++S')] = (
        'Wait_For_Assignment', 'L', 'POP', '++S')  ## related to delete expression and characters
    JSTF[('Wait_For_Assignment', 'else', '+S')] = (
        'Wait_For_Assignment', 'L', 'POP', '-S')  ## related to await expression and characters
    JSTF[('Wait_For_Assignment', 'else', '++S')] = (
        'Wait_For_Assignment', 'L', 'POP', '--S')  ## related to delete expression and characters
    JSTF[('Wait_For_Assignment', 'else', '!==')] = (
        'Wait_For_Assignment', 'L', 'POP', '+S')  ## related to await expression and characters
    JSTF[('Wait_For_Assignment', 'else', '!=')] = (
        'Wait_For_Assignment', 'L', 'POP', '+S')  ## related to await expression and characters
    JSTF[('Wait_For_Assignment', 'else', '||')] = (
        'Wait_For_Assignment', 'L', 'POP', '||')  ## related to numeric expression expression
    JSTF[('Wait_For_Assignment', 'else', '===')] = (
        'Wait_For_Assignment', 'L', 'POP', '||')  ## related to await expression expression
    JSTF[('Wait_For_Assignment', 'else', '==')] = (
        'Wait_For_Assignment', 'L', 'POP', '||')  ## related to await expression expression
    JSTF[('Wait_For_Assignment', 'else', '<=')] = (
        'Wait_For_Assignment', 'L', 'POP', '<=')  ## related to await expression expression
    JSTF[('Wait_For_Assignment', 'else', '>')] = (
        'Wait_For_Assignment', 'L', 'POP', '<=')  ## related to await expression expression
    JSTF[('Wait_For_Assignment', 'else', '+')] = (
        'Wait_For_Assignment', 'L', 'POP', '+')  ## related to await expression expression
    JSTF[('Wait_For_Assignment', 'else', 'TYPEOF')] = (
        'Wait_For_Assignment', 'L', 'POP', 'TYPEOF')  ## related to await expression expression
    JSTF[('Wait_For_Assignment', 'else', 'THROW')] = (
        'Wait_For_Assignment', 'L', 'POP', 'THROW')  ## related to delete_prefix
    JSTF[('Wait_For_Assignment', 'else', '=')] = ('Wait_For_Assignment', 'L', 'POP', '=')  ## related to delete_prefix
    JSTF[('Wait_For_Assignment', 'else', 'INSTANCEOF')] = ('Wait_For_Assignment', 'L', 'POP', 'INSTANCEOF')
    JSTF[('Wait_For_Assignment', 'else', 'DELETE')] = ('Wait_For_Assignment', 'L', 'POP', 'DELETE')
    JSTF[('Wait_For_Assignment', 'else', 'FUN.IN')] = ('Wait_For_Assignment', 'L', 'POP', 'FUN.IN')  # function input
    JSTF[('Wait_For_Assignment', ')', 'FUN(')] = (
        'Pre_After_Function_No_Line_Terminator', 'R', 'POP', '')
    JSTF[('Wait_For_Assignment', ')', 'AP')] = (
        'Pre_After_Function_No_Line_Terminator', 'R', 'POP', '')
    JSTF[('Wait_For_Assignment', ':', '?')] = ('Wait_For_Assignment', 'R', 'CHANGE', '?:')
    # ClassExpression
    JSTF[('Identifier_Or_Function', 'l', 'C')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'CL')
    JSTF[('Identifier_Or_Function', 'a', 'CL')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'CLA')
    JSTF[('Identifier_Or_Function', 'else', 'CL')] = ('Identifier_Or_Function', 'L', 'POP', 'CO')
    JSTF[('Identifier_Or_Function', 's', 'CLA')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'CLAS')
    JSTF[('Identifier_Or_Function', 'else', 'CON')] = ('Identifier_Or_Function', 'L', 'POP', 'CLA')
    JSTF[('Identifier_Or_Function', 's', 'CLAS')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'CLASS')
    JSTF[('Identifier_Or_Function', 'else', 'CLAS')] = ('Identifier_Or_Function', 'L', 'POP', 'CLAS')
    for char in WHITESPACES:
        JSTF[('Identifier_Or_Function', char, 'CLASS')] = ('ClassExpression', 'R', 'CHANGE', 'CE')
    for char in LINEBREAKS:
        JSTF[('Identifier_Or_Function', char, 'CLASS')] = ('ClassExpression', 'R', 'CHANGE', 'CE')
    JSTF[('Identifier_Or_Function', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'POP', '')
    # *********************************  Pre_Identifier_Or_Function State Rules    ***********************************
    JSTF[('Pre_Identifier_Or_Function', 'n', 'any')] = ('Pre_NullLiteral_pre1', 'R', 'READ', '')
    JSTF[('Pre_NullLiteral_pre1', 'u', 'any')] = ('Pre_NullLiteral_pre2', 'R', 'READ', '')
    JSTF[('Pre_NullLiteral_pre1', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('Pre_NullLiteral_pre2', 'l', 'any')] = ('Pre_NullLiteral_pre3', 'R', 'READ', '')
    JSTF[('Pre_NullLiteral_pre2', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('Pre_NullLiteral_pre3', 'l', 'any')] = ('Pre_NullLiteral', 'R', 'READ', '')
    JSTF[('Pre_NullLiteral_pre3', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    for char in WHITESPACES:
        JSTF[('Pre_NullLiteral', char, 'any')] = ('Pre_After_Assignment_No_Line_Terminator', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('Pre_NullLiteral', char, 'any')] = ('After_Assignment', 'R', 'READ', '')
    JSTF[('Pre_NullLiteral', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('Pre_Identifier_Or_Function', 'f', 'any')] = ('Pre_BooleanLiteralF_pre1', 'R', 'READ', '')
    JSTF[('Pre_BooleanLiteralF_pre1', 'a', 'any')] = ('Pre_BooleanLiteralF_pre2', 'R', 'READ', '')
    JSTF[('Pre_BooleanLiteralF_pre1', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('Pre_BooleanLiteralF_pre2', 'l', 'any')] = ('Pre_BooleanLiteralF_pre3', 'R', 'READ', '')
    JSTF[('Pre_BooleanLiteralF_pre2', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('Pre_BooleanLiteralF_pre3', 's', 'any')] = ('Pre_BooleanLiteralF_pre4', 'R', 'READ', '')
    JSTF[('Pre_BooleanLiteralF_pre3', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('Pre_BooleanLiteralF_pre4', 'e', 'any')] = ('Pre_BooleanLiteral', 'R', 'READ', '')
    JSTF[('Pre_BooleanLiteralF_pre4', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    for char in WHITESPACES:
        JSTF[('Pre_BooleanLiteral', char, 'any')] = ('Pre_After_Assignment_No_Line_Terminator', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('Pre_BooleanLiteral', char, 'any')] = ('After_Assignment', 'R', 'READ', '')
    JSTF[('Pre_BooleanLiteral', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('Pre_Identifier_Or_Function', 't', 'any')] = ('Pre_BooleanLiteralT_pre1', 'R', 'READ', '')
    JSTF[('Pre_BooleanLiteralT_pre1', 'r', 'any')] = ('Pre_BooleanLiteralT_pre2', 'R', 'READ', '')
    JSTF[('Pre_BooleanLiteralT_pre1', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('Pre_BooleanLiteralT_pre2', 'u', 'any')] = ('Pre_BooleanLiteralT_pre3', 'R', 'READ', '')
    JSTF[('Pre_BooleanLiteralT_pre2', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('Pre_BooleanLiteralT_pre3', 'e', 'any')] = ('Pre_BooleanLiteral', 'R', 'READ', '')
    JSTF[('Pre_BooleanLiteralT_pre3', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    for char in JS_Alpha_Digits:
        if (char != 't' and char != 'f' and char != 'n'):
            JSTF[('Pre_Identifier_Or_Function', char, 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    # *********************************  Identifier_Or_Function State Rules    ***********************************
    # go back to Script_Start
    JSTF[('Identifier_Or_Function', ';', 'any')] = ('Check_For_Empty_Stack', 'L', 'READ', '')
    for char in JS_Alpha_Digits:
        JSTF[('Identifier_Or_Function', char, 'any')] = ('Identifier_Or_Function', 'R', 'READ', '')

    for char in WHITESPACES:
        JSTF[('Identifier_Or_Function', char, 'any')] = ('Pre_After_Identifier_Or_Function', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('Identifier_Or_Function', char, 'any')] = ('After_Assignment', 'R', 'READ', '')
    ## distingiush between first character of it and non-first character -- TO DO
    JSTF[('Identifier_Or_Function', 'else', '=')] = ('Identifier_Or_Function', 'L', 'POP', '=')
    JSTF[('Identifier_Or_Function', '.', 'any')] = ('Identifier_Or_Function_Class', 'R', 'PUSH', 'CLASS.')
    JSTF[('Identifier_Name', '.', 'any')] = ('Identifier_Or_Function_Class', 'R', 'PUSH', 'CLASS.')
    # for char in JS_Alpha_Digits:
    JSTF[('Identifier_Or_Function', "=", 'any')] = ('Pre_After_Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('Identifier_Or_Function', "else", 'any')] = ('Pre_After_Assignment_No_Line_Terminator', 'L', 'READ', '')
    # *********************************  Identifier_Or_Function_Class State Rules    ***********************************
    for char in WHITESPACES:
        JSTF[('Identifier_Or_Function_Class', char, 'any')] = (
            'Pre_After_Assignment_No_Line_Terminator', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('Identifier_Or_Function_Class', char, 'any')] = ('After_Assignment', 'R', 'READ', '')
    for char in JS_Alpha_Digits:
        JSTF[('Identifier_Or_Function_Class', char, 'CLASS.')] = ('Identifier_Or_Function', 'L', 'POP', '')
    # *********************************  ArrayLiteral State Rules    ***********************************
    for char in WHITESPACES:
        JSTF[('ArrayLiteral', char, 'any')] = ('ArrayLiteral', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('ArrayLiteral', char, 'any')] = ('ArrayLiteral', 'R', 'READ', '')

    JSTF[('ArrayLiteral', ',', 'any')] = ('ArrayLiteral', 'R', 'READ', '')
    # SpreadElement
    JSTF[('ArrayLiteral', '.', 'any')] = ('SpreadElement1', 'READ', '')
    JSTF[('SpreadElement1', 'else', 'any')] = ('Syntax_Error', 'READ', '')
    JSTF[('SpreadElement1', '.', 'any')] = ('SpreadElement2', 'READ', '')
    JSTF[('SpreadElement2', 'else', 'any')] = ('Syntax_Error', 'READ', '')
    JSTF[('SpreadElement2', '.', 'any')] = ('Wait_For_Assignment', 'PUSH', '...')

    JSTF[('ArrayLiteral', 'else', 'any')] = ('Assignment', 'L', 'READ', '')
    # *********************************  ObjectLiteral State Rules    ***********************************
    for char in WHITESPACES:
        JSTF[('ObjectLiteral', char, 'any')] = ('ObjectLiteral', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('ObjectLiteral', char, 'any')] = ('ObjectLiteral', 'R', 'READ', '')
    for char in ASCII_alpha:
        JSTF[('ObjectLiteral', char, '{')] = ('Identifier_Name', 'L', 'CHANGE', '$I{I')
        JSTF[('ObjectLiteral', char, '{{')] = (
            'ObjectLiteral', 'L', 'CHANGE', '{')  ## skip empty element of ObjectLiteral
    JSTF[('ObjectLiteral', '_', '{{')] = (
        'ObjectLiteral', 'R', 'CHANGE', '{')  ## skip empty element of ObjectLiteral
    JSTF[('ObjectLiteral', ',', '{')] = ('ObjectLiteral', 'R', 'CHANGE', '{{')  ## skip  empty element of ObjectLiteral
    JSTF[('ObjectLiteral', '}', '{{')] = ('Pre_After_Assignment_No_Line_Terminator', 'R', 'POP', '{{')
    JSTF[('ObjectLiteral', '}', '{')] = ('Pre_After_Assignment_No_Line_Terminator', 'R', 'POP', '{')
    # LiteralPropertyName
    JSTF[('ObjectLiteral', '"', '{')] = ('Double_Quote_Inside_Assignment_Pushed', 'R', 'CHANGE', '{I')
    JSTF[('ObjectLiteral', '"', '{{')] = ('Double_Quote_Inside_Assignment_Pushed', 'R', 'CHANGE', '{')
    JSTF[('ObjectLiteral', "'", '{')] = ('Single_Quote_Inside_Assignment_Pushed', 'R', 'CHANGE', '{I')
    JSTF[('ObjectLiteral', "'", '{{')] = ('Single_Quote_Inside_Assignment_Pushed', 'R', 'CHANGE', '{')
    for char in Digits:
        JSTF[('ObjectLiteral', char, '{')] = ('Numeric_Assignment', 'L', 'CHANGE', '{I')
        JSTF[('ObjectLiteral', char, '{{')] = ('Numeric_Assignment', 'L', 'CHANGE', '{')
    JSTF[('ObjectLiteral', '[', '{')] = ('Wait_For_Assignment', 'R', 'CHANGE', '{I[')
    JSTF[('ObjectLiteral', '[', '{{')] = ('Wait_For_Assignment', 'L', 'CHANGE', '{')
    # *********************************  ObjectLiteral_Wait_For_Assignment State Rules    ***********************************
    # *********************************  Assignment State Rules  ****** It's going to be something close to AssignmentExpression (12.15) in ecma-262
    # go back to Script_Start
    JSTF[('Assignment', ';', 'any')] = (
        'Check_For_Empty_Stack', 'L', 'READ', '')  # Can we skip empty name for variable?
    # PrimaryExpression in 12.2 ECMA262
    JSTF[('Assignment', 't', 'any')] = ('PrimaryExpression_this1', 'R', 'READ', '')
    JSTF[('PrimaryExpression_this1', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('PrimaryExpression_this1', 'h', 'any')] = ('PrimaryExpression_this2', 'R', 'READ', '')
    JSTF[('PrimaryExpression_this2', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('PrimaryExpression_this2', 'i', 'any')] = ('PrimaryExpression_this3', 'R', 'READ', '')
    JSTF[('PrimaryExpression_this3', 's', 'any')] = ('PrimaryExpression_this', 'R', 'READ', '')
    JSTF[('PrimaryExpression_this3', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')

    JSTF[('Assignment', ']', '[')] = ('Pre_After_Function_No_Line_Terminator', 'R', 'POP', '')
    # Skip empty parentheses
    JSTF[('Assignment', ',', '...')] = ('Syntax_Error', 'R', 'POP', '')
    JSTF[('Assignment', ']', '...')] = ('Syntax_Error', 'R', 'POP', '')
    JSTF[('Assignment', 'else', '...')] = ('Assignment', 'L', 'POP', '...')
    # Skip empty conditional statement in else statement part
    JSTF[('Assignment', 'else', ':?')] = ('Assignment', 'L', 'POP', '?:')
    # Skip empty LogicalORExpression and bitwiseORExpression
    JSTF[('Assignment', 'else', '||')] = ('Assignment', 'L', 'POP', '||')
    JSTF[('Assignment', 'else', '|')] = ('Assignment', 'L', 'POP', '|')
    # Skip empty LogicalANDExpression and BitwiseAndExpression
    JSTF[('Wait_For_Assignment', 'else', '&&')] = ('Wait_For_Assignment', 'L', 'POP', '&&')
    JSTF[('Assignment', 'else', '&&')] = ('Assignment', 'L', 'POP', '&&')
    JSTF[('Assignment', 'else', '&')] = ('Assignment', 'L', 'POP', '&')
    # Skip empty bitwiseXORExpression
    JSTF[('Assignment', 'else', '^')] = ('Assignment', 'L', 'POP', '^')
    # Skip empty EqualityExpression
    JSTF[('Assignment', 'else', '==')] = ('Assignment', 'L', 'POP', '==')
    JSTF[('Assignment', 'else', '===')] = ('Assignment', 'L', 'POP', '===')
    JSTF[('Assignment', 'else', '!=')] = ('Assignment', 'L', 'POP', '!=')
    JSTF[('Assignment', 'else', '!==')] = ('Assignment', 'L', 'POP', '!==')
    # Skip RelationalExpression and ShiftExpression
    JSTF[('Assignment', 'else', '<')] = ('Assignment', 'L', 'POP', '<')
    JSTF[('Assignment', 'else', '<<')] = ('Assignment', 'L', 'POP', '<<')
    JSTF[('Assignment', 'else', '<=')] = ('Assignment', 'L', 'POP', '<=')
    JSTF[('Assignment', 'else', '>')] = ('Assignment', 'L', 'POP', '>')
    JSTF[('Assignment', 'else', '>>')] = ('Assignment', 'L', 'POP', '>>')
    JSTF[('Assignment', 'else', '>=')] = ('Assignment', 'L', 'POP', '>=')
    JSTF[('Assignment', 'else', '>>>')] = ('Assignment', 'L', 'POP', '>>>')
    JSTF[('Wait_For_Assignment', 'else', 'IN')] = ('Assignment', 'L', 'POP', 'IN')
    JSTF[('Assignment', 'else', 'IN')] = ('Assignment', 'L', 'POP', 'IN')
    JSTF[('Assignment', 'else', 'INSTANCEOF')] = ('Assignment', 'L', 'POP', 'INSTANCEOF')
    # skip Additive and Multiplicative Expressions
    JSTF[('Assignment', 'else', '+')] = ('Assignment', 'L', 'POP', '+')
    JSTF[('Assignment', 'else', '-')] = ('Assignment', 'L', 'POP', '-')
    JSTF[('Assignment', 'else', '**')] = ('Assignment', 'L', 'POP', '**')
    JSTF[('Assignment', 'else', '*=')] = ('Assignment', 'L', 'POP', '*=')
    JSTF[('Assignment', 'else', '*')] = ('Assignment', 'L', 'POP', '*')
    JSTF[('Assignment', 'else', '/')] = ('Assignment', 'L', 'POP', '/')
    JSTF[('Assignment', 'else', '%')] = ('Assignment', 'L', 'POP', '%')
    # Skip Unary Expression Prefixes
    JSTF[('Assignment', 'else', '+S')] = ('Assignment', 'L', 'POP', '+S')
    JSTF[('Assignment', 'else', '++S')] = ('Assignment', 'L', 'POP', '++S')
    JSTF[('Assignment', 'else', '-S')] = ('Assignment', 'L', 'POP', '-S')
    JSTF[('Assignment', 'else', '--S')] = ('Assignment', 'L', 'POP', '--S')
    JSTF[('Assignment', 'else', '~S')] = ('Assignment', 'L', 'POP', '~S')
    JSTF[('Assignment', 'else', '!S')] = ('Assignment', 'L', 'POP', '!S')
    JSTF[('Assignment', 'else', 'VOID')] = ('Assignment', 'L', 'POP', 'VOID')
    JSTF[('Assignment', 'else', 'DELETE')] = ('Assignment', 'L', 'POP', 'DELETE')
    JSTF[('Assignment', 'else', 'TYPEOF')] = ('Assignment', 'L', 'POP', 'TYPEOF')
    JSTF[('Assignment', 'else', 'AWAIT')] = ('Assignment', 'L', 'POP', 'AWAIT')
    JSTF[('Assignment', '"', 'any')] = ('Double_Quote_Inside_Assignment_Pushed', 'R', 'PUSH', '"')
    JSTF[('Assignment', "'", 'any')] = ('Single_Quote_Inside_Assignment_Pushed', 'R', 'PUSH', "'")
    for char in Digits:
        JSTF[('Assignment', char, 'any')] = ('Numeric_Assignment', 'R', 'READ', '')
        JSTF[('Assignment', char, '=')] = ('Numeric_Assignment', 'R', 'POP', '=')

    for char in Digits:
        JSTF[('Specify_Assignment_Type', char, 'any')] = ('Numeric_Assignment', 'R', 'READ', '')
        JSTF[('Specify_Assignment_Type', char, '=')] = ('Numeric_Assignment', 'R', 'POP', '=')

    for char in ASCII_alpha:
        if (char != 't' and char != 'n' and char != 'f' and char != 'y' and char != 's'):
            JSTF[('Assignment', char, 'any')] = ('Pre_Identifier_Or_Function', 'L', 'READ', '')
            JSTF[('Assignment', char, '=')] = ('Pre_Identifier_Or_Function', 'L', 'POP', '=')
    # added to pass errors for Iteration_Statement_For case2
    JSTF[('Assignment', ')', 'FOR(VARIL;;')] = ('Specify_Assignment_Type', 'R', 'CHANGE', 'FOR(VARIL;;)')
    # case5 and case8
    JSTF[('Assignment', ')', 'FOR(VARFB')] = ('Specify_Assignment_Type', 'R', 'CHANGE', 'FOR(VARFB)')
    # NewExpression
    JSTF[('Assignment', 'n', 'any')] = ('Wait_For_Assignment_New_Expression1', 'R', 'READ', '')
    JSTF[('Wait_For_Assignment_New_Expression1', 'e', 'any')] = (
        'Wait_For_Assignment_New_Expression2', 'R', 'READ', '')
    JSTF[('Wait_For_Assignment_New_Expression1', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('Wait_For_Assignment_New_Expression2', 'w', 'any')] = (
        'Wait_For_Assignment_New_Expression', 'R', 'READ', '')
    JSTF[('Wait_For_Assignment_New_Expression2', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    for char in WHITESPACES:
        JSTF[('Wait_For_Assignment_New_Expression', char, 'any')] = ('NewExpression', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('Wait_For_Assignment_New_Expression', char, 'any')] = ('NewExpression', 'R', 'READ', '')
    JSTF[('Wait_For_Assignment_New_Expression', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    # 14.1 FunctionExpression
    JSTF[('Assignment', 'f', 'any')] = ('Identifier_Or_Function', 'R', 'PUSH', 'A-F')
    JSTF[('Identifier_Or_Function', 'u', 'A-F')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'A-FU')
    JSTF[('Identifier_Or_Function', 'else', 'A-F')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'n', 'A-FU')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'A-FUN')
    JSTF[('Identifier_Or_Function', 'else', 'A-FU')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'c', 'A-FUN')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'A-FUNC')
    JSTF[('Identifier_Or_Function', 'else', 'A-FUN')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 't', 'A-FUNC')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'A-FUNCT')
    JSTF[('Identifier_Or_Function', 'else', 'A-FUNC')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'i', 'A-FUNCT')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'A-FUNCTI')
    JSTF[('Identifier_Or_Function', 'else', 'A-FUNCT')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'o', 'A-FUNCTI')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'A-FUNCTIO')
    JSTF[('Identifier_Or_Function', 'else', 'A-FUNCTI')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'n', 'A-FUNCTIO')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'A-FUNCTION')
    JSTF[('Identifier_Or_Function', 'else', 'A-FUNCTIO')] = ('Identifier_Or_Function', 'L', 'POP', '')
    for char in WHITESPACES:
        JSTF[('Identifier_Or_Function', char, 'A-FUNCTION')] = ('FunctionExpression', 'R', 'CHANGE', 'FE')
    for char in LINEBREAKS:
        JSTF[('Identifier_Or_Function', char, 'A-FUNCTION')] = ('FunctionExpression', 'R', 'CHANGE', 'FE')
    JSTF[('Identifier_Or_Function', '(', 'A-FUNCTION')] = ('FunctionExpression', 'L', 'CHANGE', 'FD')
    JSTF[('Identifier_Or_Function', 'else', 'A-FUNCTION')] = ('Identifier_Or_Function', 'L', 'POP', '')
    # ArrowParameters
    JSTF[('Assignment', '(', 'any')] = ('ArrowParameters', 'R', 'PUSH', 'AP')
    JSTF[('Assignment', ')', 'AP')] = ('Pre_After_Function_No_Line_Terminator', 'R', 'POP', 'AP')
    # YieldExpression
    JSTF[('Assignment', 'y', 'any')] = ('YieldExpression1', 'R', 'READ', '')
    JSTF[('YieldExpression1', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('YieldExpression1', 'i', 'any')] = ('YieldExpression2', 'R', 'READ', '')
    JSTF[('YieldExpression2', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('YieldExpression2', 'e', 'any')] = ('YieldExpression3', 'R', 'READ', '')
    JSTF[('YieldExpression3', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('YieldExpression3', 'l', 'any')] = ('YieldExpression4', 'R', 'READ', '')
    JSTF[('YieldExpression4', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('YieldExpression4', 'd', 'any')] = ('YieldExpression5', 'R', 'READ', '')
    for char in WHITESPACES:
        JSTF[('YieldExpression5', char, 'any')] = ('YieldExpression', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('YieldExpression5', char, 'any')] = ('After_Assignment', 'R', 'READ', '')
    JSTF[('YieldExpression5', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    # SuperCall
    JSTF[('Assignment', 's', 'any')] = ('SuperCall1', 'R', 'READ', '')
    JSTF[('SuperCall1', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('SuperCall1', 'u', 'any')] = ('SuperCall2', 'R', 'READ', '')
    JSTF[('SuperCall2', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('SuperCall2', 'p', 'any')] = ('SuperCall3', 'R', 'READ', '')
    JSTF[('SuperCall3', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('SuperCall3', 'e', 'any')] = ('SuperCall4', 'R', 'READ', '')
    JSTF[('SuperCall4', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('SuperCall4', 'r', 'any')] = ('SuperCall5', 'R', 'READ', '')
    for char in WHITESPACES:
        JSTF[('SuperCall5', char, 'any')] = ('Super_Call', 'R', 'PUSH', 'SUPER')
    for char in LINEBREAKS:
        JSTF[('SuperCall5', char, 'any')] = ('Super_Call', 'R', 'PUSH', 'SUPER')
    JSTF[('SuperCall5', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    # RegularExpressionLiteral
    JSTF[('Assignment', '/', 'any')] = ('RegularExpressionLiteral', 'R', 'PUSH', 'REL//')
    JSTF[('Assignment', 'else', 'any')] = ('Specify_Assignment_Type', 'L', 'READ', '')
    JSTF[('Assignment', ')', 'FUN(')] = ('Pre_After_Function_No_Line_Terminator', 'R', 'POP', '')
    # *********************************  YieldExpression State Rules    ***********************************
    for char in WHITESPACES:
        JSTF[('YieldExpression', char, 'any')] = ('YieldExpression', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('YieldExpression', char, 'any')] = ('After_Assignment', 'R', 'READ', '')
    JSTF[('YieldExpression', '*', 'any')] = ('Wait_For_Assignment', 'R', 'READ', '')
    JSTF[('YieldExpression', 'else', 'any')] = ('Wait_For_Assignment', 'L', 'READ', '')
    # *********************************  Numeric_Assignment State Rules    ***********************************
    for char in Digits:
        JSTF[('Numeric_Assignment', char, 'any')] = ('Numeric_Assignment', 'R', 'READ', '')

    JSTF[('Numeric_Assignment', '.', 'any')] = ('Numeric_Assignment', 'R', 'READ', '')
    JSTF[('Numeric_Assignment', 'else', 'any')] = ('Pre_After_Assignment_No_Line_Terminator', 'L', 'READ', '')
    # ********************************* PrimaryExpression_this State Rules    ***********************************
    for char in WHITESPACES:
        JSTF[('PrimaryExpression_this', char, 'any')] = ('Pre_After_Assignment_No_Line_Terminator', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('PrimaryExpression_this', char, 'any')] = ('After_Assignment', 'R', 'READ', '')
    JSTF[('PrimaryExpression_this', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    # *********************************  Double_Quote_Inside_Assignment_Pushed State Rules    ***********************************
    JSTF[('Double_Quote_Inside_Assignment_Pushed', '"', '"')] = ('Quote_Skipped', 'R', 'POP', '"')
    JSTF[('Double_Quote_Inside_Assignment_Pushed', "'", '"')] = (
        'Double_Quote_Inside_Assignment_Pushed', 'R', 'READ', "")
    JSTF[('Double_Quote_Inside_Assignment_Pushed', 'else', '"')] = (
        'Double_Quote_Inside_Assignment_Pushed', 'R', 'READ', '')
    JSTF[('Double_Quote_Inside_Assignment_Pushed', '\\', '"')] = (
        'Double_Quote_Inside_Assignment_Pushed_Skip', 'R', 'READ', '')
    JSTF[('Double_Quote_Inside_Assignment_Pushed_Skip', 'else', '"')] = (
        'Double_Quote_Inside_Assignment_Pushed', 'R', 'READ', '')
    JSTF[('Double_Quote_Inside_Assignment_Pushed', 'else', 'any')] = (
        'Double_Quote_Inside_Assignment_Pushed', 'L', 'PUSH', '"')
    # Potential_JSON state
    JSTF[('Double_Quote_Inside_Assignment_Pushed', '"', "B{JSON")] = ('Potential_JSON', 'R', 'CHANGE', "B{JSON_S")
    JSTF[('Double_Quote_Inside_Assignment_Pushed', 'else', "B{JSON")] = (
        'Double_Quote_Inside_Assignment_Pushed', 'R', 'READ', '')
    # *********************************  Single_Quote_Inside_Assignment_Pushed State Rules    ***********************************
    JSTF[('Single_Quote_Inside_Assignment_Pushed', "'", "'")] = ('Quote_Skipped', 'R', 'POP', "'")
    JSTF[('Single_Quote_Inside_Assignment_Pushed', '"', "'")] = (
        'Single_Quote_Inside_Assignment_Pushed', 'R', 'READ', "")
    JSTF[('Single_Quote_Inside_Assignment_Pushed', 'else', "'")] = (
        'Single_Quote_Inside_Assignment_Pushed', 'R', 'READ', '')
    JSTF[('Single_Quote_Inside_Assignment_Pushed', '\\', "'")] = (
        'Single_Quote_Inside_Assignment_Pushed_Skip', 'R', 'READ', '')
    JSTF[('Single_Quote_Inside_Assignment_Pushed_Skip', 'else', "'")] = (
        'Single_Quote_Inside_Assignment_Pushed', 'R', 'READ', '')
    JSTF[('Single_Quote_Inside_Assignment_Pushed', 'else', 'any')] = (
        'Single_Quote_Inside_Assignment_Pushed', 'L', 'PUSH', "'")
    # Potential_JSON state
    JSTF[('Single_Quote_Inside_Assignment_Pushed', "'", "B{JSON")] = ('Potential_JSON', 'R', 'CHANGE', "B{JSON_S")
    JSTF[('Single_Quote_Inside_Assignment_Pushed', 'else', "B{JSON")] = (
        'Single_Quote_Inside_Assignment_Pushed', 'R', 'READ', '')
    # *********************************  Quote_Skipped State Rules    ******************************************************
    JSTF[('Quote_Skipped', 'else', '"')] = ('Double_Quote_Inside_Assignment_Pushed', 'L', 'READ', '')
    JSTF[('Quote_Skipped', 'else', "'")] = ('Single_Quote_Inside_Assignment_Pushed', 'L', 'READ', '')
    JSTF[('Quote_Skipped', 'else', "any")] = ('Pre_After_Assignment_No_Line_Terminator', 'L', 'READ', '')
    # ********************************* Pre_After_Assignment_No_Line_Terminator Rules    ***********************************
    for char in WHITESPACES:
        JSTF[('Pre_After_Assignment_No_Line_Terminator', char, 'any')] = (
            'Pre_After_Assignment_No_Line_Terminator', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('Pre_After_Assignment_No_Line_Terminator', char, 'any')] = ('After_Assignment', 'R', 'READ', '')

    JSTF[('Pre_After_Assignment_No_Line_Terminator', '+', 'any')] = (
        'Pre_After_Assignment_No_Line_Terminator_Plus', 'R', 'READ', '')
    JSTF[('Pre_After_Assignment_No_Line_Terminator_Plus', '+', 'any')] = (
        'Pre_After_Assignment_No_Line_Terminator', 'R', 'READ', '')
    JSTF[('Pre_After_Assignment_No_Line_Terminator_Plus', '=', 'any')] = (
        'Wait_For_Assignment', 'R', 'READ', '')
    JSTF[('Pre_After_Assignment_No_Line_Terminator_Plus', 'else', 'any')] = ('Wait_For_Assignment', 'L', 'PUSH', '+')
    JSTF[('Pre_After_Assignment_No_Line_Terminator', '-', 'any')] = (
        'Pre_After_Assignment_No_Line_Terminator_Minus', 'R', 'READ', '')
    JSTF[('Pre_After_Assignment_No_Line_Terminator_Minus', '-', 'any')] = (
        'Pre_After_Assignment_No_Line_Terminator', 'R', 'READ', '')
    JSTF[('Pre_After_Assignment_No_Line_Terminator_Minus', '=', 'any')] = ('Wait_For_Assignment', 'R', 'READ', '')
    JSTF[('Pre_After_Assignment_No_Line_Terminator_Minus', 'else', 'any')] = ('Wait_For_Assignment', 'L', 'PUSH', '-')
    JSTF[('Pre_After_Assignment_No_Line_Terminator', 'else', 'any')] = ('After_Assignment', 'L', 'READ', '')
    JSTF[('Pre_After_Assignment_No_Line_Terminator', '.', 'any')] = (
        'Identifier_Or_Function_Class', 'R', 'PUSH', 'CLASS.')
    # ********************************* After_Assignment Rules    ************************************
    for char in WHITESPACES:
        JSTF[('After_Assignment', char, 'any')] = ('After_Assignment', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('After_Assignment', char, 'any')] = ('After_Assignment', 'R', 'READ', '')
    ## If and with statements
    JSTF[('After_Assignment', ',', 'IF(')] = ('If_Conditional_Statement', 'L', 'READ', '')
    JSTF[('After_Assignment', ',', 'WITH(')] = ('With_Statement', 'L', 'READ', '')
    JSTF[('After_Assignment', ',', 'WHILE(')] = ('Iteration_Statement_While', 'L', 'READ', '')
    JSTF[('Specify_Assignment_Type', ')', 'IF(')] = ('If_Conditional_Statement', 'L', 'READ', '')  # 1/29/10
    JSTF[('After_Assignment', ')', 'IF(')] = ('If_Conditional_Statement', 'L', 'READ', '')
    JSTF[('After_Assignment', ')', 'WITH(')] = ('With_Statement', 'L', 'READ', '')
    JSTF[('After_Assignment', ')', 'WHILE(')] = ('Iteration_Statement_While', 'L', 'READ', '')
    # for char in JSOperators:
    #     JSTF[('After_Assignment', char, 'any')] = ('Wait_For_Assignment', 'R', 'READ', '')
    JSTF[('After_Assignment', ';', 'any')] = ('Check_For_Empty_Stack', 'L', 'READ', '')
    JSTF[('After_Assignment', '=', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', '=')
    ## ConditionalExpression
    JSTF[('After_Assignment', '?', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', '?')
    JSTF[('After_Assignment', ':', '?')] = ('Wait_For_Assignment', 'R', 'CHANGE', '?:')
    ## LogicalORExpression
    JSTF[('After_Assignment', '|', 'any')] = ('BitwiseORExpression', 'R', 'READ', '')
    JSTF[('After_Assignment', '|', '=')] = ('BitwiseORExpression', 'R', 'READ', '')
    JSTF[('BitwiseORExpression', '|', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', '||')
    JSTF[('BitwiseORExpression', '=', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', '||')
    JSTF[('BitwiseORExpression', 'else', 'any')] = ('Wait_For_Assignment', 'L', 'PUSH', '|')
    # LogicalORExpression and BitwiseANDExpression
    JSTF[('After_Assignment', '&', 'any')] = ('BitwiseANDExpression', 'R', 'READ', '')
    JSTF[('BitwiseANDExpression', '&', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', '&&')
    JSTF[('BitwiseANDExpression', '&', 'any')] = ('Wait_For_Assignment', 'L', 'PUSH', '&')
    # BitwiseXORRExpression
    JSTF[('After_Assignment', '^', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', '^')
    # EqualityExpression
    JSTF[('After_Assignment', '=', '=')] = ('Equality_Expression', 'R', 'READ', '')
    ### ALL assignments done with '=' are covered here we dont't need to pop it up in skip binding pattern
    JSTF[('After_Assignment', 'else', '=')] = ('Wait_For_Assignment', 'L', 'POP', '=')
    JSTF[('After_Assignment', ',', '=')] = (
        'Wait_For_Assignment', 'R', 'POP', '=')  ##skipping errors for assignments with comma

    JSTF[('Equality_Expression', '=', '=')] = ('Wait_For_Assignment', 'R', 'CHANGE', '===')
    JSTF[('Equality_Expression', 'else', '=')] = ('Wait_For_Assignment', 'L', 'CHANGE', '==')

    JSTF[('After_Assignment', '!', 'any')] = ('Non_Equality_Expression', 'R', 'PUSH', '!')
    JSTF[('Non_Equality_Expression', '=', '!')] = ('Non_Equality_Expression', 'R', 'CHANGE', '!=')
    JSTF[('Non_Equality_Expression', 'else', '!')] = ('Wait_For_Assignment', 'L', 'POP', '')
    JSTF[('Non_Equality_Expression', '=', '!=')] = ('Non_Equality_Expression', 'R', 'CHANGE', '!==')
    JSTF[('Non_Equality_Expression', 'else', '!=')] = ('Wait_For_Assignment', 'L', 'READ', '')
    JSTF[('Non_Equality_Expression', 'else', '!==')] = ('Wait_For_Assignment', 'L', 'READ', '')
    # RelationalExpression and ShiftExpression
    JSTF[('After_Assignment', '<', 'any')] = ('RelationalExpressionG', 'R', 'READ', '')
    JSTF[('RelationalExpressionG', '=', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', '<=')
    JSTF[('RelationalExpressionG', '<', 'any')] = ('RelationalExpressionGG', 'R', 'READ', '')
    JSTF[('RelationalExpressionG', chr(47), 'any')] = ('Tag_Skip', 'R', 'PUSH', '</')
    JSTF[('RelationalExpressionG', 'else', 'any')] = ('Wait_For_Assignment', 'L', 'PUSH', '<')
    JSTF[('RelationalExpressionGG', '=', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', '*=')  ## Similar to *=
    JSTF[('RelationalExpressionGG', 'else', 'any')] = ('Wait_For_Assignment', 'L', 'PUSH', '<')

    JSTF[('After_Assignment', '>', 'any')] = ('RelationalExpressionL', 'R', 'READ', '')
    JSTF[('RelationalExpressionL', '>', 'any')] = ('RelationalExpressionLL', 'R', 'READ', '')
    JSTF[('RelationalExpressionL', '=', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', '<=')
    JSTF[('RelationalExpressionLL', '>', 'any')] = ('RelationalExpressionLLL', 'R', 'READ', '')
    JSTF[('RelationalExpressionLLL', 'else', 'any')] = ('Wait_For_Assignment', 'L', 'PUSH', '>>>')
    JSTF[('RelationalExpressionLLL', '=', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', '*=')
    JSTF[('RelationalExpressionLL', 'else', 'any')] = ('Wait_For_Assignment', 'L', 'PUSH', '>>')
    JSTF[('RelationalExpressionLL', '=', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', '*=')
    JSTF[('RelationalExpressionL', 'else', 'any')] = ('Wait_For_Assignment', 'L', 'PUSH', '>')

    JSTF[('After_Assignment', 'i', 'any')] = ('RelationalExpressionIN1', 'R', 'READ', '')
    JSTF[('After_Assignment', 'i', '{I')] = ('RelationalExpressionIN1', 'R', 'CHANGE', '{')
    JSTF[('RelationalExpressionIN1', 'n', 'any')] = ('RelationalExpressionIN2', 'R', 'READ', '')
    JSTF[('RelationalExpressionIN1', 'else', 'any')] = ('ASI', 'L', 'PUSH', 'NIN')
    for char in WHITESPACES:
        JSTF[('RelationalExpressionIN2', char, 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', 'IN')

    for char in LINEBREAKS:
        JSTF[('RelationalExpressionIN2', char, 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', 'IN')
    JSTF[('RelationalExpressionIN2', 's', 'any')] = ('RelationalExpressionIN3', 'R', 'READ', '')
    JSTF[('RelationalExpressionIN2', 'else', 'any')] = ('Syntax_Error', 'L', 'READ', '')
    JSTF[('RelationalExpressionIN3', 't', 'any')] = ('RelationalExpressionIN4', 'R', 'READ', '')
    JSTF[('RelationalExpressionIN3', 'else', 'any')] = ('Syntax_Error', 'L', 'READ', '')
    JSTF[('RelationalExpressionIN4', 'a', 'any')] = ('RelationalExpressionIN5', 'R', 'READ', '')
    JSTF[('RelationalExpressionIN4', 'else', 'any')] = ('Syntax_Error', 'L', 'READ', '')
    JSTF[('RelationalExpressionIN5', 'n', 'any')] = ('RelationalExpressionIN6', 'R', 'READ', '')
    JSTF[('RelationalExpressionIN5', 'else', 'any')] = ('Syntax_Error', 'L', 'READ', '')
    JSTF[('RelationalExpressionIN6', 'c', 'any')] = ('RelationalExpressionIN7', 'R', 'READ', '')
    JSTF[('RelationalExpressionIN6', 'else', 'any')] = ('Syntax_Error', 'L', 'READ', '')
    JSTF[('RelationalExpressionIN7', 'e', 'any')] = ('RelationalExpressionIN8', 'R', 'READ', '')
    JSTF[('RelationalExpressionIN7', 'else', 'any')] = ('Syntax_Error', 'L', 'READ', '')
    JSTF[('RelationalExpressionIN8', 'o', 'any')] = ('RelationalExpressionIN9', 'R', 'READ', '')
    JSTF[('RelationalExpressionIN8', 'else', 'any')] = ('Syntax_Error', 'L', 'READ', '')
    JSTF[('RelationalExpressionIN9', 'f', 'any')] = ('RelationalExpressionIN10', 'R', 'READ', '')
    JSTF[('RelationalExpressionIN9', 'else', 'any')] = ('Syntax_Error', 'L', 'READ', '')
    for char in WHITESPACES:
        JSTF[('RelationalExpressionIN10', char, 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', 'INSTANCEOF')

    for char in LINEBREAKS:
        JSTF[('RelationalExpressionIN10', char, 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', 'INSTANCEOF')
    JSTF[('RelationalExpressionIN10', 'else', 'any')] = ('Syntax_Error', 'L', 'READ', '')
    # Additive and Multiplicative Expressions
    JSTF[('After_Assignment', '+', 'any')] = ('AdditiveExpression', 'R', 'READ', '')
    JSTF[('AdditiveExpression', '=', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', '*=')
    JSTF[('AdditiveExpression', 'else', 'any')] = ('Wait_For_Assignment', 'L', 'PUSH', '+')
    JSTF[('After_Assignment', '-', 'any')] = ('AdditiveExpressionM', 'R', 'READ', '')
    JSTF[('AdditiveExpressionM', '=', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', '*=')
    JSTF[('AdditiveExpressionM', 'else', 'any')] = ('Wait_For_Assignment', 'L', 'PUSH', '-')
    JSTF[('After_Assignment', '*', 'any')] = ('MultiplicativeExpression', 'R', 'READ', '')
    JSTF[('MultiplicativeExpression', '*', 'any')] = ('DoubleMultiplicativeExpression', 'R', 'READ', '')
    JSTF[('MultiplicativeExpression', '=', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', '*=')
    JSTF[('MultiplicativeExpression', 'else', 'any')] = ('Wait_For_Assignment', 'L', 'PUSH', '*')
    JSTF[('DoubleMultiplicativeExpression', '=', 'any')] = (
        'Wait_For_Assignment', 'R', 'PUSH', '*=')  ## actually **= should be pushed
    JSTF[('DoubleMultiplicativeExpression', 'else', 'any')] = ('Wait_For_Assignment', 'L', 'PUSH', '**')
    JSTF[('After_Assignment', '/', 'any')] = ('MultiplicativeExpression1', 'R', 'READ', '')
    JSTF[('MultiplicativeExpression1', '=', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', '*=')
    JSTF[('MultiplicativeExpression1', '/', 'any')] = ('Single_Line_Comment', 'R', 'READ', '')
    JSTF[('MultiplicativeExpression1', '*', 'any')] = ('Multi_Line_Comment', 'R', 'READ', '')
    JSTF[('MultiplicativeExpression1', 'else', 'any')] = ('Wait_For_Assignment', 'L', 'PUSH', '/')
    JSTF[('After_Assignment', '%', 'any')] = ('MultiplicativeExpression2', 'R', 'READ', '')
    JSTF[('MultiplicativeExpression2', '=', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', '*=')
    JSTF[('MultiplicativeExpression2', 'else', 'any')] = ('Wait_For_Assignment', 'L', 'PUSH', '%')
    JSTF[('After_Assignment', '&', 'any')] = ('MultiplicativeExpression3', 'R', 'READ', '')
    JSTF[('MultiplicativeExpression3', '=', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', '*=')
    JSTF[('MultiplicativeExpression3', '&', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', '&&')
    JSTF[('MultiplicativeExpression3', 'else', 'any')] = ('Wait_For_Assignment', 'L', 'READ', '')
    JSTF[('After_Assignment', '^', 'any')] = ('MultiplicativeExpression4', 'R', 'READ', '')
    JSTF[('MultiplicativeExpression4', '=', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', '*=')
    # ObjectLiteral Assignment for PropertyName
    JSTF[('After_Assignment', ':', '{')] = ('Wait_For_Assignment', 'R', 'CHANGE', '{IA')
    JSTF[('After_Assignment', ':', '{I')] = ('Wait_For_Assignment', 'R', 'CHANGE', '{IA')
    JSTF[('After_Assignment', ':', 'BP{I')] = ('Wait_For_Binding_Element', 'R', 'CHANGE', 'BP{IA')
    # Going back to objectLiteral state
    JSTF[('After_Assignment', '}', '{IA')] = ('ObjectLiteral', 'L', 'CHANGE', '{')
    JSTF[('After_Assignment', ',', '{IA')] = ('ObjectLiteral', 'L', 'CHANGE', '{')
    JSTF[('After_Assignment', ']', '{I[')] = ('After_Identifier', 'R', 'CHANGE', '{I')
    # Iteration_Statement_Do
    JSTF[('After_Assignment', ')', 'DO-S(')] = ('Iteration_Statement_Do', 'L', 'READ', '')
    # Iteration_Statement_For
    JSTF[('After_Assignment', ')', 'FOR(VARIL;;')] = (
        'Iteration_Statement_For', 'R', 'CHANGE', 'FOR(VARIL;;)')  # Iteration_Statement_For_Case2
    JSTF[('After_Assignment', ')', 'FOR(VARFB')] = ('Specify_Assignment_Type', 'R', 'CHANGE', 'FOR(VARFB)')
    # Object Binding Pattern
    JSTF[('After_Assignment', ',', 'BP{I')] = (
        'ObjectBindingPattern', 'R', 'CHANGE', 'BP{{')  # ObjectBindingPattern with Assignment
    JSTF[('After_Assignment', '}', 'BP{I')] = (
        'ObjectBindingPattern', 'L', 'CHANGE', 'BP{{')  # ObjectBindingPattern with Assignment
    JSTF[('After_Assignment', ']', 'BP{I[')] = (
        'After_Pre_After_Assignment_No_Line_TerminatorAssignment', 'R', 'CHANGE', 'BP{I')
    # initialization for single name binding of a binding element
    JSTF[('After_Assignment', ',', 'BP{IBE')] = ('ObjectBindingPattern', 'R', 'CHANGE', 'BP{{')
    JSTF[('After_Assignment', '}', 'BP{IBE')] = ('ObjectBindingPattern', 'L', 'CHANGE', 'BP{{')
    # Array Binding Pattern
    JSTF[('After_Assignment', ',', 'BP{I')] = (
        'ArrayBindingPattern', 'R', 'CHANGE', 'BP[')  # ArrayBindingPattern with Assignment
    JSTF[('After_Assignment', ']', 'BP{I')] = (
        'ArrayBindingPattern', 'L', 'CHANGE', 'BP[')  # ArrayBindingPattern with Assignment
    ## cases 3, 6 and 9 of iteration satatement
    JSTF[('After_Assignment', 'else', 'FOR(LETI')] = (
        'Iteration_Statement_For_Let', 'L', 'CHANGE', 'FOR(LETIL')  ### THIS WOULD BE AN EXPRESSION
    JSTF[('After_Assignment', 'else', 'FOR(LETIL')] = ('Iteration_Statement_For_Let', 'L', 'READ', '')
    JSTF[('After_Assignment', ')', 'FOR(LETIE;')] = ('Iteration_Statement_For_Let', 'R', 'CHANGE', 'FOR(LETIE;)')
    # case1 of Iteration Statement
    JSTF[('After_Assignment', ')', 'FOR(E;E;E')] = ('Iteration_Statement_For', 'L', 'CHANGE', 'FOR(E;E;E')
    # of and in
    JSTF[('After_Assignment', 'o', 'FOR(E')] = ('Iteration_Statement_Case6_Of1', 'R', 'READ', '')
    JSTF[('After_Assignment', 'i', 'FOR(E')] = ('Iteration_Statement_Case6_In1', 'R', 'READ', '')
    # Switch Statement
    JSTF[('After_Assignment', ')', 'SWITCH(')] = ('Switch_Statement', 'R', 'READ', '')
    JSTF[('After_Assignment', ':', 'SWITCH(){')] = ('StatementList', 'L', 'PUSH', 'SLF')
    JSTF[('After_Assignment', ':', 'SWITH(){D')] = ('StatementList', 'L', 'PUSH', 'SLF')
    JSTF[('After_Assignment', ',', 'BL')] = ('BindingList', 'L', 'CHANGE', 'BL,')
    # FunctionExpression
    JSTF[('After_Assignment', 'else', 'FE(FP')] = ('FormalParameters', 'L', 'READ', '')
    # ClassHeritage
    JSTF[('After_Assignment', '{', 'CD')] = ('ClassBody', 'R', 'CHANGE', 'CD{')
    # PropertyName
    JSTF[('After_Assignment', ']', '[PN')] = ('After_PropertyName', 'R', 'POP', '')
    JSTF[('After_Assignment', 'else', 'PN')] = ('After_PropertyName', 'L', 'POP', '')
    # SetMethod in MethodDefinition
    JSTF[('After_Assignment', ')', 'SMD(')] = ('GetMethodWaitForBody', 'R', 'CHANGE', 'FD')
    # CoverParenthesizedExpressionAndArrowParameterList
    JSTF[('After_Assignment', ',', 'AP')] = ('ArrowParameters', 'L', 'READ', '')
    # Arguments
    JSTF[('After_Assignment', '(', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', 'FUN($I')
    JSTF[('After_Assignment', ')', 'FUN(')] = ('Pre_After_Function_No_Line_Terminator', 'R', 'POP', '')
    JSTF[('After_Assignment', ')', 'FUN(,')] = ('Pre_After_Function_No_Line_Terminator', 'R', 'POP', '')
    JSTF[('After_Assignment', ',', 'FUN(')] = ('After_Assignment', 'R', 'CHANGE', 'FUN(,')
    JSTF[('After_Assignment', ',', 'FUN(,')] = ('Syntax_Error', 'R', 'READ', '')
    JSTF[('After_Assignment', 'else', 'FUN(,')] = ('Wait_For_Assignment', 'L', 'CHANGE', 'FUN(')
    JSTF[('After_Assignment', '.', 'FUN(')] = ('BindingRestElement1', 'R', 'CHANGE', 'FUN(R')
    JSTF[('After_Assignment', '.', 'FUN(,')] = ('BindingRestElement1', 'R', 'CHANGE', 'FUN(R')
    JSTF[('After_Assignment', ')', 'FUN(R')] = ('Pre_After_Function_No_Line_Terminator', 'R', 'POP', '')
    # CallExpression [Expression]
    JSTF[('After_Assignment', ']', 'FUN[')] = ('Pre_After_Function_No_Line_Terminator', 'R', 'POP', 'FUN[')
    # TemplateLiteral escape expression
    JSTF[('After_Assignment', '}', '${')] = ('TemplateLiteral', 'R', 'POP', '${')
    # Member Expression [ Expression ]
    JSTF[('After_Assignment', '[', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', 'ME[')
    JSTF[('After_Assignment', ']', 'ME[')] = ('Pre_After_Assignment_No_Line_Terminator', 'R', 'POP', 'ME[')
    # Member Expression . IdentifierName
    # Member Expression TemplateLiteral
    JSTF[('After_Assignment', '`', 'any')] = ('TemplateLiteral', 'R', 'PUSH', '`')
    # SuperProperty :  super [Expression]
    JSTF[('After_Assignment', ']', 'SUP[')] = ('Pre_After_Assignment_No_Line_Terminator', 'R', 'POP', 'SUP[')
    JSTF[('After_Assignment', 'else', 'any')] = ('Specify_Assignment_Type', 'L', 'READ', '')
    # Potential_JSON
    JSTF[('After_Assignment', '}', 'B{JSON_S')] = ('Potential_JSON', 'L', 'CHANGE', 'B{JSON_SV')
    JSTF[('After_Assignment', ',', 'B{JSON_S')] = ('Potential_JSON', 'L', 'CHANGE', 'B{JSON_SV')
    JSTF[('After_Assignment', 'else', 'B{JSON_S')] = ('Potential_JSON', 'L', 'CHANGE', 'B{JSON_SV')
    # for statement
    # IterationStatement_For_Case2 it needs to be assignments
    JSTF[('After_Assignment', 'else', 'FOR(VARIL;;)')] = (
        'Specify_Assignment_Type', 'L', 'POP', '')  # Iteration_Statement_For_Case2
    for operatorjs in JSSTRPunctuators:
        JSTF[('After_Assignment', operatorjs, 'FOR(VARIL;;)')] = (
            'After_Assignment', 'L', 'POP', '')
    # switch statement
    JSTF[('After_Assignment', ')', 'SWITCH(')] = ('Switch_Statement', 'L', 'READ', '')
    # ********************************* Check_For_Empty_Stack Rules    ***********************************
    for char in WHITESPACES:
        JSTF[('Check_For_Empty_Stack', char, 'any')] = ('Check_For_End_Of_Block', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('Check_For_Empty_Stack', char, 'any')] = ('Check_For_End_Of_Block', 'R', 'READ', '')
    # End_Of_Statement_Punctuator=[';', '}']
    JSTF[('Check_For_Empty_Stack', ';', 'VAR')] = ('Check_For_Empty_Stack', 'L', 'POP', '')
    JSTF[('Check_For_Empty_Stack', ';', '=')] = ('Check_For_Empty_Stack', 'L', 'POP', '')
    JSTF[('Check_For_Empty_Stack', ';', 'FUN.IN')] = ('Check_For_Empty_Stack', 'L', 'POP', '')
    # Block_Statement
    JSTF[('Check_For_Empty_Stack', ';', 'B{{')] = ('Block_Statement', 'R', 'CHANGE', 'B{')
    JSTF[('Check_For_Empty_Stack', ';', 'B{')] = ('Block_Statement', 'R', 'READ', '')
    JSTF[('Check_For_Empty_Stack', '}', 'B{')] = ('Check_For_End_Of_Block', 'R', 'POP', 'B{')
    JSTF[('Check_For_Empty_Stack', ';', '$$$')] = ('Script_Start', 'R', 'READ', '')
    # IfStatement
    JSTF[('Check_For_Empty_Stack', ';', 'IF()')] = ('Specify_Assignment_Type', 'R', 'CHANGE', 'IF()ELSE')
    # elseStatement
    JSTF[('Check_For_Empty_Stack', ';', 'IF()ELSE')] = ('Specify_Assignment_Type', 'R', 'READ', 'IF()ELSE')
    JSTF[('Check_For_Empty_Stack', ';', 'II')] = ('Check_For_Empty_Stack', 'L', 'POP', 'II')
    # With_Statement
    JSTF[('Check_For_Empty_Stack', ';', 'WITH()')] = ('Check_For_Empty_Stack', 'R', 'POP', 'WITH()')
    # Iteration_Statement_Do
    JSTF[('Check_For_Empty_Stack', ';', 'DO-S')] = ('Iteration_Statement_Do', 'R', 'POP', 'DO-S()')
    JSTF[('Check_For_Empty_Stack', ';', 'DO-S()')] = ('Check_For_Empty_Stack', 'R', 'POP', 'DO-S()')
    # Iteration_Statement_While
    JSTF[('Check_For_Empty_Stack', ';', 'WHILE()')] = ('Check_For_Empty_Stack', 'L', 'POP', 'WHILE')
    # IterationStatement_For_Case2
    JSTF[('Check_For_Empty_Stack', ';', 'FOR(VARI')] = (
        'Iteration_Statement_For', 'R', 'CHANGE', 'FOR(VARIL;')  # Iteration_Staement_For_Case2
    JSTF[('Check_For_Empty_Stack', ';', 'FOR(VARIL')] = (
        'Iteration_Statement_For', 'R', 'CHANGE', 'FOR(VARIL;')  # Iteration_Staement_For_Case2
    JSTF[('Check_For_Empty_Stack', ';', 'FOR(VARIL;')] = (
        'Iteration_Statement_For', 'R', 'CHANGE', 'FOR(VARIL;;')  # Iteration_Staement_For_Case2
    JSTF[('Check_For_Empty_Stack', ';', 'FOR(VARIL;;)')] = (
        'Check_For_Empty_Stack', 'L', 'POP', 'FOR(VARIL;;)')  # Iteration_Staement_For_Case2
    JSTF[('Check_For_Empty_Stack', ';', 'FOR(VARFB)')] = (
        'Check_For_Empty_Stack', 'L', 'POP', 'FOR(VARFB)')  # Iteration_Staement_For_Case2
    # IterationStatement_For_Case3
    JSTF[('Check_For_Empty_Stack', ';', 'FOR(VARIE')] = ('Iteration_Statement_LET', 'R', 'CHANGE', 'FOR(VARIE;')
    # cases 1, 4 and 7 of Iteration Statement
    JSTF[('Check_For_Empty_Stack', ';', 'FOR(E')] = ('Iteration_Statement_For', 'R', 'CHANGE', 'FOR(E;')
    JSTF[('Check_For_Empty_Stack', ';', 'FOR(E;E')] = ('Iteration_Statement_For', 'R', 'CHANGE', 'FOR(E;E;')
    # Switch Statement
    JSTF[('Check_For_Empty_Stack', '}', 'SWITCH(){D')] = ('Check_For_Empty_Stack', 'R', 'POP', '')
    JSTF[('Check_For_Empty_Stack', ';', 'SL')] = ('StatementList', 'R', 'READ', '')
    JSTF[('Check_For_Empty_Stack', ';', 'SLF')] = ('StatementList', 'R', 'CHANGE', 'SL')
    JSTF[('Check_For_Empty_Stack', ';', 'BL')] = ('StatementList', 'R', 'POP', '')
    # Labeled_Statement
    JSTF[('Check_For_Empty_Stack', ';', 'LS')] = ('Check_For_Empty_Stack', 'L', 'POP', '')
    # Throw Statement
    JSTF[('Check_For_Empty_Stack', 'else', 'THROW')] = ('Check_For_Empty_Stack', 'L', 'POP', '')
    # Throw Statement
    JSTF[('Check_For_Empty_Stack', ',', 'THROW')] = ('Check_For_Empty_Stack', 'R', 'READ', '')
    # DEBUGGER Statement
    JSTF[('Check_For_Empty_Stack', ';', 'DEBUGGER')] = ('Check_For_Empty_Stack', 'L', 'POP', '')
    JSTF[('Check_For_Empty_Stack', 'else', 'any')] = ('Specify_Assignment_Type', 'L', 'READ', '')
    ## Function Statements
    JSTF[('Check_For_Empty_Stack', ';', 'FE(){')] = ('FunctionBody', 'R', 'READ', '')
    JSTF[('Check_For_Empty_Stack', ';', '{')] = ('Specify_Assignment_Type', 'R', 'CHANGE', 'B{')
    JSTF[('Check_For_Empty_Stack', '}', 'any')] = ('Check_For_End_Of_Block', 'L', 'READ', '')
    for signt in popsignes:
        JSTF[('Check_For_Empty_Stack', 'else', signt)] = ('Check_For_Empty_Stack', 'L', 'POP', signt)
        JSTF[('Specify_Assignment_Type', 'else', signt)] = ('Check_For_Empty_Stack', 'L', 'POP', signt)
    # ********************************* Check_For_End_Of_Block State Rules    ***********************************
    for char in WHITESPACES:
        JSTF[('Check_For_End_Of_Block', char, 'any')] = ('Check_For_End_Of_Block', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('Check_For_End_Of_Block', char, 'any')] = ('Check_For_End_Of_Block', 'R', 'READ', '')
    JSTF[('Check_For_End_Of_Block', '}', 'B{')] = ('Check_For_End_Of_Block', 'L', 'POP', 'B{')
    JSTF[('Check_For_End_Of_Block', 'else', '$$$')] = ('Script_Start', 'L', 'READ', '')
    JSTF[('Check_For_End_Of_Block', 'else', 'any')] = ('Specify_Assignment_Type', 'L', 'READ', '')
    # IfStatement
    JSTF[('Check_For_End_Of_Block', 'else', 'IF()')] = ('Specify_Assignment_Type', 'L', 'CHANGE', 'IF()ELSE')
    # IfStatement
    JSTF[('Check_For_End_Of_Block', 'else', 'IF()ELSE')] = ('Specify_Assignment_Type', 'L', 'READ', 'IF()ELSE')
    JSTF[('Check_For_End_Of_Block', '}', 'IF()ELSE')] = ('Check_For_End_Of_Block', 'L', 'POP', 'IF()ELSE')
    JSTF[('Check_For_End_Of_Block', 'else', 'II')] = ('Check_For_Empty_Stack', 'L', 'POP', 'II')
    # With_Statement
    JSTF[('Check_For_End_Of_Block', 'else', 'WITH()')] = ('Check_For_Empty_Stack', 'L', 'POP', 'WITH()')
    # Iteration_Statement_Do
    JSTF[('Check_For_End_Of_Block', 'else', 'DO-S')] = ('Iteration_Statement_Do', 'L', 'CHANGE', 'DO-S()')
    JSTF[('Check_For_End_Of_Block', 'else', 'DO-S()')] = ('Check_For_Empty_Stack', 'L', 'POP', 'DO-S()')
    # Iteration_Statement_While
    JSTF[('Check_For_End_Of_Block', 'else', 'WHILE()')] = ('Check_For_Empty_Stack', 'L', 'POP', 'WHILE')
    # IterationStatement_For_Case2
    JSTF[('Check_For_End_Of_Block', 'else', 'FOR(VARFB)')] = (
        'Check_For_Empty_Stack', 'L', 'POP', 'FOR(VARFB)')  # Iteration_Staement_For_Case2
    # end of block statement
    JSTF[('Check_For_End_Of_Block', '}', 'B{')] = ('Check_For_End_Of_Block', 'R', 'POP', 'B{')
    JSTF[('Check_For_End_Of_Block', '}', 'B{{')] = ('Check_For_End_Of_Block', 'R', 'POP', 'B{')
    # Switch Statement
    # JSTF[('Check_For_End_Of_Block', '}', 'SWITCH(){D')] = ('Check_For_Empty_Stack', 'R', 'POP', '')
    JSTF[('Check_For_End_Of_Block', '}', 'SL')] = ('StatementList', 'L', 'POP', '')
    JSTF[('Check_For_End_Of_Block', 'else', 'SL')] = ('StatementList', 'L', 'READ', '')
    JSTF[('Check_For_End_Of_Block', 'else', 'SLF')] = ('StatementList', 'L', 'CHANGE', 'SL')
    JSTF[('Check_For_End_Of_Block', 'else', 'BL')] = ('StatementList', 'L', 'POP', '')
    # Labeled_Statement
    JSTF[('Check_For_End_Of_Block', 'else', 'LS')] = ('Check_For_Empty_Stack', 'L', 'POP', '')
    # Try_Statement
    JSTF[('Check_For_End_Of_Block', 'else', 'TRY')] = ('Try_Statement', 'L', 'CHANGE', 'TRY{}')
    JSTF[('Check_For_End_Of_Block', 'else', 'TRY{}FINALLY')] = ('Try_Statement', 'L', 'CHANGE', 'TRY{}FINALLY{}')
    JSTF[('Check_For_End_Of_Block', 'else', 'TRY{}CATCH(P)')] = ('Catch_Statement', 'L', 'CHANGE', 'TRY{}CATCH(P){}')
    JSTF[('Check_For_End_Of_Block', 'else', 'TRY{}FINALLY{}CATCH(P)')] = (
        'Try_Statement', 'L', 'CHANGE', 'TRY{}FINALLY{}CATCH(P){}')
    ## Function Statements
    JSTF[('Check_For_End_Of_Block', 'else', 'FE(){')] = ('FunctionBody', 'L', 'READ', '')
    # ClassElement inside ClassDeclaration
    JSTF[('Check_For_End_Of_Block', 'else', 'CD{')] = ('FunctionBody', 'L', 'READ', '')
    # ClassExpression
    JSTF[('Check_For_End_Of_Block', 'else', 'CE')] = ('Pre_After_Assignment_No_Line_Terminator_Minus', 'L', 'POP', 'CE')
    # Throw Statement
    JSTF[('Check_For_End_Of_Block', 'else', 'THROW')] = ('Check_For_Empty_Stack', 'L', 'READ', '')
    # Throw Statement
    JSTF[('Check_For_End_Of_Block', '}', 'THROW')] = ('Check_For_End_Of_Block', 'L', 'POP', '')
    JSTF[('Check_For_End_Of_Block', ',', 'FUN(')] = ('Specify_Assignment_Type', 'R', 'READ', '')
    JSTF[('Check_For_End_Of_Block', ',', 'FUN(')] = ('Specify_Assignment_Type', 'R', 'READ', '')
    ## Error regarding a list of assignments after a blobk
    JSTF[('Check_For_End_Of_Block', ',', '=')] = ('Specify_Assignment_Type', 'R', 'POP', '')
    # for statement
    JSTF[('Check_For_End_Of_Block', '}', 'FOR(VARIL;;)')] = (
        'Check_For_End_Of_Block', 'L', 'POP', 'FOR(VARIL;;)')  # Iteration_Staement_For_Case2
    # conditional if else with ? :
    JSTF[('Check_For_End_Of_Block', ':', '?')] = ('Wait_For_Assignment', 'R', 'CHANGE', '?:')
    # next element of object literal
    JSTF[('Check_For_End_Of_Block', ',', '{IA')] = ('After_Assignment', 'L', 'CHANGE', '{I')
    JSTF[('Check_For_End_Of_Block', '}', '{IA')] = ('Check_For_End_Of_Block', 'R', 'POP', '')
    ## Assignments with a block structure and then comma
    JSTF[('Check_For_End_Of_Block', ',', 'any')] = ('Wait_For_Assignment', 'R', 'READ', '')
    JSTF[('Check_For_End_Of_Block', '(', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', 'FUN($I')
    # ********************************* If_Conditional_Statement Rules    ***********************************
    for char in WHITESPACES:
        JSTF[('If_Conditional_Statement', char, 'any')] = ('If_Conditional_Statement', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('If_Conditional_Statement', char, 'any')] = ('If_Conditional_Statement', 'R', 'READ', '')

    JSTF[('If_Conditional_Statement', '(', 'IF')] = ('If_Conditional_Statement', 'R', 'CHANGE', 'IF((')
    JSTF[('If_Conditional_Statement', 'else', 'IF((')] = ('Wait_For_Assignment', 'L', 'CHANGE', 'IF(')
    JSTF[('If_Conditional_Statement', ')', 'IF((')] = ('Syntax_Error', 'R', 'READ', '')
    JSTF[('If_Conditional_Statement', ',', 'IF((')] = ('Syntax_Error', 'R', 'READ', '')
    JSTF[('If_Conditional_Statement', ',', 'IF(')] = ('If_Conditional_Statement', 'R', 'CHANGE', 'IF((')
    JSTF[('If_Conditional_Statement', ')', 'IF(')] = ('Specify_Assignment_Type', 'R', 'CHANGE', 'IF()')
    # ********************************* With_Statement Rules    ***********************************
    for char in WHITESPACES:
        JSTF[('With_Statement', char, 'any')] = ('With_Statement', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('With_Statement', char, 'any')] = ('With_Statement', 'R', 'READ', '')

    JSTF[('With_Statement', '(', 'WITH')] = ('With_Statement', 'R', 'CHANGE', 'WITH((')
    JSTF[('With_Statement', 'else', 'WITH((')] = ('Wait_For_Assignment', 'L', 'CHANGE', 'WITH(')
    JSTF[('With_Statement', ')', 'WITH((')] = ('Syntax_Error', 'R', 'READ', '')
    JSTF[('With_Statement', ',', 'WITH((')] = ('Syntax_Error', 'R', 'READ', '')
    JSTF[('With_Statement', ',', 'WITH(')] = ('With_Statement', 'R', 'CHANGE', 'WITH((')
    JSTF[('With_Statement', ')', 'WITH(')] = ('Specify_Assignment_Type', 'R', 'CHANGE', 'WITH()')
    # ********************************* Iteration_Statement_Do Rules    ***********************************
    for char in WHITESPACES:
        JSTF[('Iteration_Statement_Do', char, 'any')] = ('Iteration_Statement_Do', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('Iteration_Statement_Do', char, 'any')] = ('Iteration_Statement_Do', 'R', 'READ', '')

    JSTF[('Iteration_Statement_Do', 'else', 'DO')] = ('Specify_Assignment_Type', 'L', 'CHANGE', 'DO-S')
    JSTF[('Iteration_Statement_Do', 'else', 'any')] = ('Specify_Assignment_Type', 'L', 'CHANGE', 'DO-S')  # 1/28/20
    JSTF[('Iteration_Statement_Do', '(', 'DO-S')] = ('Wait_For_Assignment', 'R', 'CHANGE', 'DO-S(')
    JSTF[('Iteration_Statement_Do', ')', 'DO-S(')] = ('If_Conditional_Statement', 'R', 'CHANGE', 'DO-S()')
    JSTF[('Iteration_Statement_Do', ';', 'DO-S()')] = ('Check_For_Empty_Stack', 'L', 'CHANGE', 'DO-S()')
    JSTF[('Iteration_Statement_Do', '}', 'DO-S()')] = ('Check_For_End_Of_Block', 'R', 'POP', 'DO-S()')
    # ********************************* Iteration_Statement_While Rules    ***********************************
    for char in WHITESPACES:
        JSTF[('Iteration_Statement_While', char, 'any')] = ('Iteration_Statement_While', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('Iteration_Statement_While', char, 'any')] = ('Iteration_Statement_While', 'R', 'READ', '')

    JSTF[('Iteration_Statement_While', '(', 'WHILE')] = ('Iteration_Statement_While', 'R', 'CHANGE', 'WHILE((')
    JSTF[('Iteration_Statement_While', 'else', 'WHILE((')] = ('Wait_For_Assignment', 'L', 'CHANGE', 'WHILE(')
    JSTF[('Iteration_Statement_While', ')', 'WHILE((')] = ('Syntax_Error', 'R', 'READ', '')
    JSTF[('Iteration_Statement_While', ',', 'WHILE((')] = ('Syntax_Error', 'R', 'READ', '')
    JSTF[('Iteration_Statement_While', ',', 'WHILE(')] = ('Iteration_Statement_While', 'R', 'CHANGE', 'WHILE((')
    JSTF[('Iteration_Statement_While', ')', 'WHILE(')] = ('Specify_Assignment_Type', 'R', 'CHANGE', 'WHILE()')
    # ********************************* Iteration_Statement_For Rules    ***********************************
    for char in WHITESPACES:
        JSTF[('Iteration_Statement_For', char, 'any')] = ('Iteration_Statement_For', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('Iteration_Statement_For', char, 'any')] = ('Iteration_Statement_For', 'R', 'READ', '')

    JSTF[('Iteration_Statement_For', '(', 'FOR')] = ('Iteration_Statement_For', 'R', 'CHANGE', 'FOR(')
    # var
    JSTF[('Iteration_Statement_For', 'v', 'FOR(')] = ('Iteration_Statement_For', 'R', 'CHANGE', 'FOR(V')
    JSTF[('Iteration_Statement_For', 'a', 'FOR(V')] = ('Iteration_Statement_For', 'R', 'CHANGE', 'FOR(VA')
    JSTF[('Iteration_Statement_For', 'else', 'FOR(V')] = ('Syntax_Error', 'L', 'POP' 'FOR(V')
    JSTF[('Iteration_Statement_For', 'r', 'FOR(VA')] = ('Iteration_Statement_For', 'R', 'CHANGE', 'FOR(VAR')
    JSTF[('Iteration_Statement_For', 'else', 'FOR(VA')] = ('Syntax_Error', 'L', 'POP' 'FOR(VA')
    for char in WHITESPACES:
        JSTF[('Iteration_Statement_For', char, 'FOR(VAR')] = ('Iteration_Statement_For_Var', 'R', 'CHANGE', 'FOR(VAR')

    for char in LINEBREAKS:
        JSTF[('Iteration_Statement_For', char, 'FOR(VAR')] = ('Iteration_Statement_For_Var', 'R', "CHANGE", 'FOR(VAR')

    JSTF[('Iteration_Statement_For', char, 'FOR(VAR')] = ('Iteration_Statement_For_Var', 'R', "CHANGE", 'FOR(VAR')
    JSTF[('Iteration_Statement_For', char, 'FOR(VAR')] = ('Syntax_Error', 'L', 'POP' 'FOR(V')

    # let
    JSTF[('Iteration_Statement_For', 'l', 'FOR(')] = ('Iteration_Statement_For_Let1', 'R', 'READ', '')
    JSTF[('Iteration_Statement_For_Let1', 'e', 'FOR(')] = ('Iteration_Statement_For_Let2', 'R', 'READ', '')
    JSTF[('Iteration_Statement_For_Let2', 't', 'FOR(')] = ('Iteration_Statement_For_Let3', 'R', 'READ', '')
    for char in WHITESPACES:
        JSTF[('Iteration_Statement_For_Let3', char, 'FOR(')] = ('Iteration_Statement_For_Let', 'R', 'CHANGE', 'FOR(LET')

    for char in LINEBREAKS:
        JSTF[('Iteration_Statement_For_Let3', char, 'FOR(')] = ('Iteration_Statement_For_Let', 'R', "CHANGE", 'FOR(LET')
    # const
    JSTF[('Iteration_Statement_For', 'c', 'FOR((')] = ('Iteration_Statement_For_Const1', 'R', 'CHANGE', 'FOR(')
    JSTF[('Iteration_Statement_For_Const1', 'o', 'FOR(')] = ('Iteration_Statement_For_Const2', 'R', 'READ', '')
    JSTF[('Iteration_Statement_For_Const2', 'n', 'FOR(')] = ('Iteration_Statement_For_Const3', 'R', 'READ', '')
    JSTF[('Iteration_Statement_For_Const3', 's', 'FOR(')] = ('Iteration_Statement_For_Const4', 'R', 'READ', '')
    JSTF[('Iteration_Statement_For_Const4', 't', 'FOR(')] = ('Iteration_Statement_For_Const5', 'R', 'READ', '')
    for char in WHITESPACES:
        JSTF[('Iteration_Statement_For_Const5', char, 'FOR(')] = (
            'Iteration_Statement_For_Let', 'R', 'CHANGE', 'FOR(LET')

    for char in LINEBREAKS:
        JSTF[('Iteration_Statement_For_Const5', char, 'FOR(')] = (
            'Iteration_Statement_For_Let', 'R', "CHANGE", 'FOR(LET')
    # Case 1, 4 and 7
    JSTF[('Iteration_Statement_For', 'else', 'FOR(')] = ('Wait_For_Assignment', 'L', 'CHANGE', 'FOR(E')
    JSTF[('Iteration_Statement_For', ';', 'FOR(')] = ('Iteration_Statement_For', 'R', 'CHANGE', 'FOR(E;')
    JSTF[('Iteration_Statement_For', 'else', 'FOR(E;')] = ('Wait_For_Assignment', 'L', 'CHANGE', 'FOR(E;E')
    JSTF[('Iteration_Statement_For', ';', 'FOR(E;')] = ('Iteration_Statement_For', 'R', 'CHANGE', 'FOR(E;E;')
    JSTF[('Iteration_Statement_For', 'else', 'FOR(E;E;')] = ('Wait_For_Assignment', 'L', 'CHANGE', 'FOR(E;E;E')
    JSTF[('Iteration_Statement_For', ')', 'FOR(E;E;')] = ('Specify_Assignment_Type', 'R', 'POP', 'FOR(E;E;')
    JSTF[('Iteration_Statement_For', ')', 'FOR(E;E;E')] = ('Specify_Assignment_Type', 'R', 'POP', 'FOR(E;E;E')
    # ****************** Iteration_Statement_For_Var Rules --- Case2, 5 and 8 in IterationStatement    *************
    for char in WHITESPACES:
        JSTF[('Iteration_Statement_For_Var', char, 'any')] = ('Iteration_Statement_For_Var', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('Iteration_Statement_For_Var', char, 'any')] = ('Iteration_Statement_For_Var', 'R', "READ", '')
    # A Single Identifier --- Could be any of cases 2,5 or 8
    for char in ASCII_alpha:
        JSTF[('Iteration_Statement_For_Var', char, 'FOR(VAR')] = ('Identifier_Name', 'L', 'CHANGE', '$IFOR(VARI')
    # case 2
    # IterationStatement_For_Case2
    JSTF[('Iteration_Statement_For', 'else', 'FOR(VARIL;')] = (
        'Wait_For_Assignment', 'L', 'READ', '')  # Iteration_Statement_For_Case2
    JSTF[('Iteration_Statement_For', 'else', 'FOR(VARIL;;')] = (
        'Wait_For_Assignment', 'L', 'READ', '')  # Iteration_Statement_For_Case2
    JSTF[('Iteration_Statement_For', 'else', 'FOR(VARIL;;)')] = (
        'Specify_Assignment_Type', 'L', 'READ', '')  # Iteration_Statement_For_Case2
    # case5 and case8 -- transer into BindingPattern State
    JSTF[('Iteration_Statement_For_Var', '{', 'FOR(VAR')] = ('BindingPattern', 'L', 'READ', '')
    JSTF[('Iteration_Statement_For_Var', '[', 'FOR(VAR')] = ('BindingPattern', 'L', 'READ', '')
    # *********************************     BindingPattern State Rules    *****************************************
    JSTF[('BindingPattern', '{', 'any')] = ('ObjectBindingPattern', 'R', 'PUSH', 'BP{{')
    JSTF[('BindingPattern', '[', 'any')] = ('ArrayBindingPattern', 'R', 'PUSH', 'BP[')
    # *********************************     ObjectBindingPattern State Rules    ***********************************
    for char in WHITESPACES:
        JSTF[('ObjectBindingPattern', char, 'any')] = ('ObjectBindingPattern', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('ObjectBindingPattern', char, 'any')] = ('ObjectBindingPattern', 'R', 'READ', '')

    JSTF[('ObjectBindingPattern', '}', 'BP{{')] = ('Skip_BindingPattern', 'R', 'POP', 'BP{{')
    JSTF[('ObjectBindingPattern', '}', 'BP{')] = ('Skip_BindingPattern', 'R', 'POP', 'BP{')
    # Single Name Binding
    for char in ASCII_alpha:
        JSTF[('ObjectBindingPattern', char, 'BP{')] = ('Identifier_Name', 'L', 'PUSH', '$IBP{I')
        JSTF[('ObjectBindingPattern', char, 'BP{{')] = (
            'ObjectBindingPattern', 'L', 'CHANGE', 'BP{')  ## skip empty element of Object Binding Pattern

    JSTF[('ObjectBindingPattern', ',', 'BP{')] = (
        'ObjectBindingPattern', 'R', 'CHANGE', 'BP{{')  ## skip  empty element of Object Binding Pattern
    # Property Name
    JSTF[('ObjectBindingPattern', '"', 'BP{')] = ('Double_Quote_Inside_Assignment_Pushed', 'R', 'CHANGE', 'BP{I')
    JSTF[('ObjectBindingPattern', '"', 'BP{{')] = ('Double_Quote_Inside_Assignment_Pushed', 'L', 'CHANGE', 'BP{')
    JSTF[('ObjectBindingPattern', "'", 'BP{')] = ('Single_Quote_Inside_Assignment_Pushed', 'R', 'CHANGE', 'BP{I')
    JSTF[('ObjectBindingPattern', "'", 'BP{{')] = ('Single_Quote_Inside_Assignment_Pushed', 'L', 'CHANGE', 'BP{')
    for char in Digits:
        JSTF[('ObjectBindingPattern', char, '{')] = ('Numeric_Assignment', 'L', 'CHANGE', 'BP{I')
        JSTF[('ObjectBindingPattern', char, '{{')] = ('Numeric_Assignment', 'L', 'CHANGE', 'BP{')

    JSTF[('ObjectBindingPattern', '[', 'BP{')] = ('Wait_For_Assignment', 'R', 'CHANGE', 'BP{I[')
    JSTF[('ObjectBindingPattern', '[', 'BP{{')] = ('Wait_For_Assignment', 'L', 'CHANGE', 'BP{')
    # *********************************     Wait_For_Binding_Element State Rules    ******************************
    for char in WHITESPACES:
        JSTF[('Wait_For_Binding_Element', char, 'any')] = ('Wait_For_Binding_Element', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('Wait_For_Binding_Element', char, 'any')] = ('Wait_For_Binding_Element', 'R', 'READ', '')
    # Single Name Binding
    for char in ASCII_alpha:
        JSTF[('Wait_For_Binding_Element', char, 'BP{IA')] = ('Identifier_Name', 'L', 'CHANGE', '$IBP{IBE')
        JSTF[('Wait_For_Binding_Element', char, 'BP[')] = ('Identifier_Name', 'L', 'PUSH', '$IBP[I')
        JSTF[('Wait_For_Binding_Element', char, 'SMD(')] = ('Identifier_Name', 'L', 'PUSH', '$I')
    # go to binding Pattern State
    JSTF[('Wait_For_Binding_Element', '{', 'any')] = ('BindingPattern', 'L', 'READ', '')
    JSTF[('Wait_For_Binding_Element', '[', 'any')] = ('BindingPattern', 'L', 'READ', '')
    # *********************************     ArrayBindingPattern State Rules    ***********************************
    for char in WHITESPACES:
        JSTF[('ArrayBindingPattern', char, 'any')] = ('ArrayBindingPattern', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('ArrayBindingPattern', char, 'any')] = ('ArrayBindingPattern', 'R', 'READ', '')

    JSTF[('ArrayBindingPattern', ',', 'BP[')] = ('ArrayBindingPattern', 'R', 'R', 'READ', '')
    JSTF[('ArrayBindingPattern', 'else', 'BP[')] = ('Wait_For_Binding_Element', 'L', 'READ', '')

    JSTF[('ObjectBindingPattern', ']', 'BP[')] = ('Skip_tBindingPattern', 'R', 'POP', 'BP[')
    # SpreadElement
    JSTF[('ArrayBindingPattern', '.', 'any')] = ('BindingRestElement1', 'R', 'READ', '')
    JSTF[('BindingRestElement1', 'else', 'any')] = ('Syntax_Error', 'R', 'READ', '')
    JSTF[('BindingRestElement1', '.', 'any')] = ('BindingRestElement2', 'R', 'READ', '')
    JSTF[('BindingRestElement2', 'else', 'any')] = ('Syntax_Error', 'READ', '')
    JSTF[('BindingRestElement2', '.', 'BP[')] = ('Wait_For_BindingRestElement', 'R', 'CHANGE', 'BP[...')
    JSTF[('BindingRestElement2', '.', 'FE(R')] = ('Wait_For_BindingRestElement', 'R', 'READ', '')
    JSTF[('BindingRestElement2', '.', 'AP')] = ('Wait_For_BindingRestElement', 'R', 'CHANGE', 'APR')
    JSTF[('BindingRestElement2', '.', 'FUN(R')] = ('Wait_For_Assignment', 'R', 'CHANGE', 'APR')
    # *********************************     Skip_BindingPattern State Rules    ***********************************
    for char in WHITESPACES:
        JSTF[('Skip_BindingPattern', char, 'any')] = ('Skip_BindingPattern', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('Skip_BindingPatternPattern', char, 'any')] = ('Skip_BindingPattern', 'R', 'READ', '')
    # When Binding Pattern is invoked inside a BindingElement
    JSTF[('Skip_BindingPattern', '=', 'BP{IA')] = (
        'Wait_For_Assignment', 'R', 'CHANGE', 'BP{IBE')  # act as if it's a simple assignment like single nameBinding
    JSTF[('Skip_BindingPattern', 'else', 'BP{IA')] = ('ObjectBindingPattern', 'L', 'CHANGE', 'BP{')
    JSTF[('Skip_BindingPattern', 'else', 'BP[')] = ('ArrayBindingPattern', 'L', 'READ', '')
    # case 5 and case8 when ForBinding is a BindingPattern
    JSTF[('Skip_BindingPattern', 'else', 'FOR(VAR')] = ('After_Identifier', 'L', 'POP', 'FOR(VARBP')
    # BindingRestElement
    JSTF[('Skip_BindingPattern', 'else', 'BP[...')] = ('Wait_For_End_Of_ArrayBindingPattern', 'L', 'READ', '')
    ## skip out of first Binding pattern for let and const cases... Checking the possibility of turning into lexical declaration
    JSTF[('Skip_BindingPattern', '=', 'FOR(LETI')] = ('Wait_For_Assignment', 'R', 'CHANGE', 'FOR(LETIL')
    JSTF[('Skip_BindingPattern', ',', 'FOR(LETI')] = ('Iteration_Statement_For_Let', 'R', 'CHANGE', 'FOR(LETIL')
    JSTF[('Skip_BindingPattern', 'else', 'FOR(LETI')] = ('Iteration_Statement_For_Let', 'L', 'READ', '')
    ## cases 3, 6 and 9 of iteration statements
    JSTF[('Skip_BindingPattern', 'else', 'FOR(LET')] = ('Iteration_Statement_For_Let', 'L', 'CHANGE', 'FOR(LETI')
    JSTF[('Skip_BindingPattern', 'else', 'FOR(LETIL')] = ('After_Identifier', 'L', 'CHANGE', 'FOR(LETILBP')
    # Switch Statement
    JSTF[('Skip_BindingPattern', '=', 'BL')] = ('Wait_For_Assignment', 'R', 'READ', '')
    # Catch_Statement
    JSTF[('Skip_BindingPattern', 'else', 'TRY{}CATCH(')] = ('Catch_Statement', 'L', 'CHANGE', 'TRY{}CATCH(P')
    JSTF[('Skip_BindingPattern', 'else', 'TRY{}FINALLY{}CATCH(')] = (
        'Catch_Statement', 'L', 'CHANGE', 'TRY{}FINALLY{}CATCH(P')
    # FunctionExpression
    JSTF[('Skip_BindingPattern', '=', 'FE(FP')] = ('Wait_For_Assignment', 'R', 'READ', '')
    JSTF[('Skip_BindingPattern', ')', 'FE(R')] = ('FunctionExpression', 'R', 'CHANGE', 'FE()')
    # SetMethod in MethodDefinition
    JSTF[('Skip_BindingPattern', ')', 'SMD(')] = ('GetMethodWaitForBody', 'R', 'CHANGE', 'FD')
    JSTF[('Skip_BindingPattern', '=', 'SMD(')] = ('Wait_For_Assignment', 'R', 'READ', '')
    # Arrow Parameter
    JSTF[('Skip_BindingPattern', ')', 'APR')] = ('Pre_After_Identifier_Or_Function', 'R', 'POP', 'APR')
    # *********************************     Wait_For_BindingRestElement1 State Rules    ***********************************
    for char in WHITESPACES:
        JSTF[('Wait_For_BindingRestElement', char, 'any')] = ('Wait_For_BindingRestElement', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('Wait_For_BindingRestElement', char, 'any')] = ('Wait_For_BindingRestElement', 'R', 'READ', '')

    for char in ASCII_alpha:
        JSTF[('Wait_For_BindingRestElement', char, 'any')] = ('Identifier_Name', 'L', 'PUSH', '$I')

    JSTF[('Wait_For_BindingRestElement', '{', 'any')] = ('BindingPattern', 'L', 'READ', '')
    JSTF[('Wait_For_BindingRestElement', '[', 'any')] = ('BindingPattern', 'L', 'READ', '')
    # *********************************     Wait_For_End_Of_ArrayBindingPattern State Rules    *****************************
    for char in WHITESPACES:
        JSTF[('Wait_For_End_Of_ArrayBindingPattern', char, 'any')] = (
            'Wait_For_End_Of_ArrayBindingPattern', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('Wait_For_End_Of_ArrayBindingPattern', char, 'any')] = (
            'Wait_For_End_Of_ArrayBindingPattern', 'R', 'READ', '')

    JSTF[('Wait_For_End_Of_ArrayBindingPattern', ']', 'BP[...')] = ('Skip_tBindingPattern', 'R', 'POP', 'BP[...')
    # ******************************* Iteration_Statement_For_Let Rules --- Case3, 6 and 9 in IterationStatement ************
    for char in WHITESPACES:
        JSTF[('Iteration_Statement_For_Let', char, 'any')] = ('Iteration_Statement_For_Let', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('Iteration_Statement_For_Let', char, 'any')] = ('Iteration_Statement_For_Let', 'R', "READ", '')

    for char in ASCII_alpha:
        JSTF[('Iteration_Statement_For_Let', char, 'FOR(LET')] = ('Identifier_Name', 'L', 'CHANGE', '$IFOR(LETI')
        JSTF[('Iteration_Statement_For_Let', 'char', 'FOR(LETIL,')] = ('Identifier_Name', 'L', 'CHANGE', '$IFOR(LETIL')

    JSTF[('Iteration_Statement_For_Let', '{', 'FOR(LET')] = ('BindingPattern', 'L', 'READ', '')
    JSTF[('Iteration_Statement_For_Let', '[', 'FOR(LET')] = ('BindingPattern', 'L', 'READ', '')
    JSTF[('Iteration_Statement_For_Let', '{', 'FOR(LETIL,')] = ('BindingPattern', 'L', 'CHANGE', 'FOR(LETIL')
    JSTF[('Iteration_Statement_For_Let', '[', 'FOR(LETIL,')] = ('BindingPattern', 'L', 'CHANGE', 'FOR(LETIL')
    # of and in after Binding Pattern
    JSTF[('Iteration_Statement_For_Let', 'i', 'FOR(LETI')] = ('Iteration_Statement_Case6_In1', 'R', 'READ', '')
    # cases 3, 6 and 9 of iteration statement
    JSTF[('Iteration_Statement_For_Let', 'o', 'FOR(LETI')] = ('Iteration_Statement_Case6_Of1', 'R', 'READ', '')
    JSTF[('Iteration_Statement_For_Let', ',', 'FOR(LETIL')] = (
        'Iteration_Statement_For_Let', 'R', 'CHANGE', 'FOR(LETIL,')
    JSTF[('Iteration_Statement_For_Let', 'else', 'FOR(LETI')] = ('Wait_For_Assignment', 'L', 'CHANGE', 'FOR(LETIE')
    JSTF[('Iteration_Statement_For_Let', 'else', 'FOR(LETIL')] = ('Wait_For_Assignment', 'L', 'CHANGE', 'FOR(LETIE')
    JSTF[('Iteration_Statement_For_Let', ';', 'FOR(LETIE')] = ('Check_For_Empty_Stack', 'L', 'READ', '')
    JSTF[('Iteration_Statement_For_Let', ')', 'FOR(LETIE;')] = ('Specify_Assignment_Type', 'L', 'POP', '')
    JSTF[('Iteration_Statement_For_Let', 'else', 'FOR(LETIE;)')] = ('Specify_Assignment_Type', 'L', 'POP', '')
    # ********************************* Switch_Statement Rules    ***********************************************************
    for char in WHITESPACES:
        JSTF[('Switch_Statement', char, 'any')] = ('Switch_Statement', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('Switch_Statement', char, 'any')] = ('Switch_Statement', 'R', 'READ', '')

    JSTF[('Switch_Statement', '(', 'SWITCH')] = ('Switch_Statement', 'R', 'CHANGE', 'SWITCH(')
    JSTF[('Switch_Statement', 'else', 'SWITCH(')] = ('Assignment', 'L', 'READ', '')
    JSTF[('Switch_Statement', ')', 'SWITCH(')] = ('Switch_Statement', 'R', 'CHANGE', 'SWITCH()')
    JSTF[('Switch_Statement', '{', 'SWITCH()')] = ('Wait_For_Switch_Block', 'R', 'CHANGE', 'SWITCH(){')
    JSTF[('StatementList', '}', 'SWITCH(){D')] = ('Check_For_End_Of_Block', 'R', 'POP', '')  ##???
    JSTF[('StatementList', '}', 'SWITCH(){')] = ('Check_For_End_Of_Block', 'R', 'POP', '')  ##???

    # ********************************* Switch_Statement Rules    **********************************************************
    for char in WHITESPACES:
        JSTF[('Wait_For_Switch_Block', char, 'any')] = ('Wait_For_Switch_Block', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('Wait_For_Switch_Block', char, 'any')] = ('Wait_For_Switch_Block', 'R', 'READ', '')
    # Default
    JSTF[('Wait_For_Switch_Block', 'd', 'SWITCH(){')] = ('Default_Block1', 'R', 'READ', '')
    JSTF[('Default_Block1', 'e', 'any')] = ('Default_Block2', 'R', 'READ', '')
    JSTF[('Default_Block1', 'else', 'any')] = ('Syntax_Error', 'R', 'READ', '')
    JSTF[('Default_Block2', 'f', 'any')] = ('Default_Block3', 'R', 'READ', '')
    JSTF[('Default_Block2', 'else', 'any')] = ('Syntax_Error', 'R', 'READ', '')
    JSTF[('Default_Block3', 'a', 'any')] = ('Default_Block4', 'R', 'READ', '')
    JSTF[('Default_Block3', 'else', 'any')] = ('Syntax_Error', 'R', 'READ', '')
    JSTF[('Default_Block4', 'u', 'any')] = ('Default_Block5', 'R', 'READ', '')
    JSTF[('Default_Block4', 'else', 'any')] = ('Syntax_Error', 'R', 'READ', '')
    JSTF[('Default_Block5', 'l', 'any')] = ('Default_Block6', 'R', 'READ', '')
    JSTF[('Default_Block5', 'else', 'any')] = ('Syntax_Error', 'R', 'READ', '')
    JSTF[('Default_Block6', 't', 'any')] = ('Default_Block7', 'R', 'READ', '')
    JSTF[('Default_Block6', 'else', 'any')] = ('Syntax_Error', 'R', 'READ', '')
    for char in WHITESPACES:
        JSTF[('Default_Block7', char, 'any')] = ('Default_Block', 'R', 'CHANGE', 'SWITCH(){D')
    for char in LINEBREAKS:
        JSTF[('Default_Block7', char, 'any')] = ('Default_Block', 'R', 'CHANGE', 'SWITCH(){D')
    JSTF[('Default_Block7', 'else', 'any')] = ('Syntax_Error', 'L', 'READ', '')
    # case
    JSTF[('Wait_For_Switch_Block', 'c', 'SWITCH(){')] = ('Case_Block1', 'R', 'READ', '')
    JSTF[('Wait_For_Switch_Block', 'c', 'SWITCH(){D')] = ('Case_Block1', 'R', 'READ', '')
    JSTF[('Case_Block1', 'a', 'any')] = ('Case_Block2', 'R', 'READ', '')
    JSTF[('Case_Block1', 'else', 'any')] = ('Syntax_Error', 'R', 'READ', '')
    JSTF[('Case_Block2', 's', 'any')] = ('Case_Block3', 'R', 'READ', '')
    JSTF[('Case_Block2', 'else', 'any')] = ('Syntax_Error', 'R', 'READ', '')
    JSTF[('Case_Block3', 'e', 'any')] = ('Case_Block4', 'R', 'READ', '')
    JSTF[('Case_Block3', 'else', 'any')] = ('Syntax_Error', 'R', 'READ', '')
    for char in WHITESPACES:
        JSTF[('Case_Block4', char, 'any')] = ('Wait_For_Assignment', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('Case_Block4', char, 'any')] = ('Wait_For_Assignment', 'R', 'READ', '')
    JSTF[('Case_Block4', '"', 'any')] = ('Double_Quote_Inside_Assignment_Pushed', 'R', 'PUSH', '"')
    JSTF[('Case_Block4', "'", 'any')] = ('Single_Quote_Inside_Assignment_Pushed', 'R', 'PUSH', "'")
    JSTF[('Case_Block4', 'else', 'any')] = ('Syntax_Error', 'L', 'READ', '')
    # ********************************* Default_Block Rules    **********************************************
    JSTF[('Default_Block', 'else', 'SWITCH(){')] = ('Default_Block', 'L', 'CHANGE', 'SWITCH(){D')
    for char in WHITESPACES:
        JSTF[('Default_Block', char, 'any')] = ('Default_Block', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('Default_Block', char, 'any')] = ('Default_Block', 'R', 'READ', '')

    JSTF[('Default_Block', ':', 'any')] = ('StatementList', 'L', 'PUSH', 'SLF')
    # ********************************* StatementList Rules    **********************************************
    for char in WHITESPACES:
        JSTF[('StatementList', char, 'any')] = ('StatementList', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('StatementList', char, 'any')] = ('StatementList', 'R', 'READ', '')
    # let
    JSTF[('StatementList', 'l', 'SL')] = ('StatementList_Let1', 'R', 'READ', '')
    JSTF[('StatementList_Let1', 'e', 'any')] = ('StatementList_Let2', 'R', 'READ', '')
    JSTF[('StatementList_Let2', 't', 'any')] = ('StatementList_Let3', 'R', 'READ', '')
    for char in WHITESPACES:
        JSTF[('StatementList_Let3', char, 'any')] = ('BindingList', 'R', 'PUSH', 'BL,')

    for char in LINEBREAKS:
        JSTF[('StatementList_Let3', char, 'any')] = ('BindingList', 'R', 'PUSH', 'BL,')
    # const
    JSTF[('StatementList', 'c', 'SL')] = ('StatementList_Const1', 'R', 'READ', '')
    JSTF[('StatementList_Const1', 'o', 'any')] = ('StatementList_Const2', 'R', 'READ', '')
    JSTF[('StatementList_Const2', 'n', 'any')] = ('StatementList_Const3', 'R', 'READ', '')
    JSTF[('StatementList_Const3', 's', 'any')] = ('StatementList_Const4', 'R', 'CHANGE', 'FOR(')
    JSTF[('StatementList_Const4', 't', 'any')] = ('StatementList_Const5', 'R', 'CHANGE', 'FOR(')
    for char in WHITESPACES:
        JSTF[('StatementList_Const5', char, 'any')] = ('BindingList', 'R', 'PUSH', 'BL,')

    for char in LINEBREAKS:
        JSTF[('StatementList_Const5', char, 'any')] = ('BindingList', 'R', 'PUSH', 'BL,')

    JSTF[('StatementList', 'else', 'SL')] = ('Specify_Assignment_Type', 'L', 'READ', 'SL')
    # skip first assignment
    JSTF[('StatementList', ':', 'SLF')] = ('Specify_Assignment_Type', 'R', 'CHANGE', 'SL')
    # case
    JSTF[('StatementList', 'c', 'SL')] = ('StatementList_Case1', 'R', 'READ', '')
    JSTF[('StatementList_Case1', 'a', 'any')] = ('StatementList_Case2', 'R', 'READ', '')
    JSTF[('StatementList_Case1', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('StatementList_Case2', 's', 'any')] = ('StatementList_Case3', 'R', 'READ', '')
    JSTF[('StatementList_Case2', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('StatementList_Case3', 'e', 'any')] = ('StatementList_Case4', 'R', 'READ', '')
    JSTF[('StatementList_Case3', 'else', 'any')] = ('Syntax_Error', 'R', 'READ', '')
    for char in WHITESPACES:
        JSTF[('StatementList_Case4', char, 'SL')] = ('Wait_For_Assignment', 'R', 'POP', '')
        # JSTF[('StatementList_Case4', char, 'SLF')] = ('Syntax_Error', 'R', 'POP', '')
    for char in LINEBREAKS:
        JSTF[('StatementList_Case4', char, 'SL')] = ('Wait_For_Assignment', 'R', 'POP', '')
        # JSTF[('StatementList_Case4', char, 'SLF')] = ('Syntax_Error', 'R', 'READ', '')
    JSTF[('StatementList_Case4', '"', 'SL')] = ('Double_Quote_Inside_Assignment_Pushed', 'R', 'CHANGE', '"')
    JSTF[('StatementList_Case4', "'", 'SL')] = ('Single_Quote_Inside_Assignment_Pushed', 'R', 'CHANGE', "'")
    JSTF[('StatementList_Case4', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    # default block
    JSTF[('StatementList', 'd', 'SL')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'CDB-D')  # Check default block
    JSTF[('StatementList', 'd', 'SLF')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'CDB-D')  # Check default block
    JSTF[('Identifier_Or_Function', 'e', 'CDB-D')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'CDB-DE')
    JSTF[('Identifier_Or_Function', 'else', 'CDB-D')] = ('Identifier_Or_Function', 'L', 'CHANGE', 'SL')
    JSTF[('Identifier_Or_Function', 'f', 'CDB-DE')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'CDB-DEF')
    JSTF[('Identifier_Or_Function', 'else', 'CDB-DE')] = ('Identifier_Or_Function', 'L', 'CHANGE', 'SL')
    JSTF[('Identifier_Or_Function', 'a', 'CDB-DEF')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'CDB-DEFA')
    JSTF[('Identifier_Or_Function', 'else', 'CDB-DEF')] = ('Identifier_Or_Function', 'L', 'CHANGE', 'SL')
    JSTF[('Identifier_Or_Function', 'u', 'CDB-DEFA')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'CDB-DEFAU')
    JSTF[('Identifier_Or_Function', 'else', 'CDB-DEFA')] = ('Identifier_Or_Function', 'L', 'CHANGE', 'SL')
    JSTF[('Identifier_Or_Function', 'l', 'CDB-DEFAU')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'CDB-DEFAUL')
    JSTF[('Identifier_Or_Function', 'else', 'CDB-DEFAU')] = ('Identifier_Or_Function', 'L', 'CHANGE', 'SL')
    JSTF[('Identifier_Or_Function', 't', 'CDB-DEFAUL')] = ('Identifier_Or_Function', 'R', 'CHANGE', 'CDB-DEFAULT')
    JSTF[('Identifier_Or_Function', 'else', 'CDB-DEFAUL')] = ('Identifier_Or_Function', 'L', 'CHANGE', 'SL')
    for char in WHITESPACES:
        JSTF[('Identifier_Or_Function', char, 'CDB-DEFAULT')] = ('Default_Block', 'R', 'POP', '')
    for char in LINEBREAKS:
        JSTF[('Identifier_Or_Function', char, 'CDB-DEFAULT')] = ('Default_Block', 'R', 'POP', '')
    JSTF[('Identifier_Or_Function', ':', 'CDB-DEFAULT')] = ('Default_Block', 'L', 'POP', '')
    JSTF[('Identifier_Or_Function', 'else', 'CDB-DEFAULT')] = ('Identifier_Or_Function', 'L', 'CHANGE', 'SL')
    # ********************************* BindingList Rules    ******************************************************
    for char in WHITESPACES:
        JSTF[('BindingList', char, 'any')] = ('BindingList', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('BindingList', char, 'any')] = ('BindingList', 'R', 'READ', '')

    for char in ASCII_alpha:
        JSTF[('BindingList', char, 'BL,')] = ('Identifier_Name', 'L', 'CHANGE', '$IBL')

    JSTF[('BindingList', '{', 'BL,')] = ('BindingPattern', 'L', 'CHANGE', 'BL')
    JSTF[('BindingList', '[', 'BL,')] = ('BindingPattern', 'L', 'CHANGE', 'BL')
    # ********************************* Labeled_Statement State Rules    *******************************************
    for char in WHITESPACES:
        JSTF[('Labeled_Statement', char, 'any')] = ('Labeled_Statement', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('Labeled_Statement', char, 'any')] = ('Labeled_Statement', 'R', 'READ', '')
    # add function declaration
    # statements
    JSTF[('Labeled_Statement', 'else', 'any')] = ('Specify_Assignment_Type', 'L', 'READ', '')
    # ********************************* Try_Statement State Rules    **********************************************
    for char in WHITESPACES:
        JSTF[('Try_Statement', char, 'any')] = ('Try_Statement', 'R', 'READ', '')
        JSTF[('Try_Statement', char, 'TRY')] = ('Try_Statement', 'R', 'READ', '')
        JSTF[('Try_Statement', char, 'TRY{}')] = ('Try_Statement', 'R', 'READ', '')
        JSTF[('Try_Statement', char, 'TRY{}CATCH')] = ('Try_Statement', 'R', 'READ', '')
        JSTF[('Try_Statement', char, 'TRY{}CATCH(P){}')] = ('Try_Statement', 'R', 'READ', '')
        JSTF[('Try_Statement', char, 'TRY{}FINALLY{}')] = ('Try_Statement', 'R', 'READ', '')
        JSTF[('Try_Statement', char, 'TRY{}FINALLY{}CATCH')] = ('Try_Statement', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('Try_Statement', char, 'any')] = ('Try_Statement', 'R', 'READ', '')
        JSTF[('Try_Statement', char, 'TRY{}CATCH')] = ('Try_Statement', 'R', 'READ', '')
        JSTF[('Try_Statement', char, 'TRY{}CATCH(P){}')] = ('Try_Statement', 'R', 'READ', '')
        JSTF[('Try_Statement', char, 'TRY{}FINALLY{}')] = ('Try_Statement', 'R', 'READ', '')
        JSTF[('Try_Statement', char, 'TRY{}FINALLY{}CATCH')] = ('Try_Statement', 'R', 'READ', '')
    JSTF[('Try_Statement', '{', 'TRY')] = ('Block_Statement', 'R', 'PUSH', 'B{{')
    JSTF[('Try_Statement', '{', 'TRY{}FINALLY')] = ('Block_Statement', 'R', 'PUSH', 'B{{')
    # catch
    JSTF[('Try_Statement', 'c', 'TRY{}')] = ('Try_Statement', 'R', 'CHANGE', 'TRY{}C')
    JSTF[('Try_Statement', 'c', 'TRY{}CATCH(P){}')] = ('Try_Statement', 'R', 'CHANGE', 'TRY{}C')
    JSTF[('Try_Statement', 'c', 'TRY{}FINALLY{}CATCH(P){}')] = ('Try_Statement', 'R', 'CHANGE', 'TRY{}FINALLY{}C')
    JSTF[('Try_Statement', 'c', 'TRY{}FINALLY{}')] = ('Try_Statement', 'R', 'CHANGE', 'TRY{}FINALLY{}C')
    JSTF[('Try_Statement', 'else', 'TRY{}')] = ('Syntax_Error', 'R', 'POP', '')
    JSTF[('Try_Statement', 'else', 'TRY{}FINALLY{}')] = ('Syntax_Error', 'R', 'POP', '')
    JSTF[('Try_Statement', 'a', 'TRY{}C')] = ('Try_Statement', 'R', 'CHANGE', 'TRY{}CA')
    JSTF[('Try_Statement', 'a', 'TRY{}FINALLY{}C')] = ('Try_Statement', 'R', 'CHANGE', 'TRY{}FINALLY{}CA')
    JSTF[('Try_Statement', 'else', 'TRY{}C')] = ('Syntax_Error', 'R', 'POP', '')
    JSTF[('Try_Statement', 'else', 'TRY{}FINALLY{}C')] = ('Syntax_Error', 'R', 'POP', '')
    JSTF[('Try_Statement', 't', 'TRY{}CA')] = ('Try_Statement', 'R', 'CHANGE', 'TRY{}CAT')
    JSTF[('Try_Statement', 't', 'TRY{}FINALLY{}CA')] = ('Try_Statement', 'R', 'CHANGE', 'TRY{}FINALLY{}CAT')
    JSTF[('Try_Statement', 'else', 'TRY{}CA')] = ('Syntax_Error', 'R', 'POP', '')
    JSTF[('Try_Statement', 'else', 'TRY{}FINALLY{}CA')] = ('Syntax_Error', 'R', 'POP', '')
    JSTF[('Try_Statement', 'c', 'TRY{}CAT')] = ('Try_Statement', 'R', 'CHANGE', 'TRY{}CATC')
    JSTF[('Try_Statement', 'c', 'TRY{}FINALLY{}CAT')] = ('Try_Statement', 'R', 'CHANGE', 'TRY{}FINALLY{}CATC')
    JSTF[('Try_Statement', 'else', 'TRY{}CAT')] = ('Syntax_Error', 'R', 'POP', '')
    JSTF[('Try_Statement', 'else', 'TRY{}FINALLY{}CAT')] = ('Syntax_Error', 'R', 'POP', '')
    JSTF[('Try_Statement', 'h', 'TRY{}CATC')] = ('Try_Statement', 'R', 'CHANGE', 'TRY{}CATCH')
    JSTF[('Try_Statement', 'h', 'TRY{}FINALLY{}CATC')] = ('Try_Statement', 'R', 'CHANGE', 'TRY{}FINALLY{}CATCH')
    JSTF[('Try_Statement', 'else', 'TRY{}CATC')] = ('Syntax_Error', 'R', 'POP', '')
    JSTF[('Try_Statement', 'else', 'TRY{}FINALLY{}CATC')] = ('Syntax_Error', 'R', 'POP', '')
    JSTF[('Try_Statement', 'else', 'TRY{}CATCH')] = ('Syntax_Error', 'R', 'POP', '')
    JSTF[('Try_Statement', 'else', 'TRY{}FINALLY{}CATCH')] = ('Syntax_Error', 'R', 'POP', '')
    for char in WHITESPACES:
        JSTF[('Try_Statement', char, 'TRY{}CATCH')] = ('Catch_Statement', 'R', 'CHANGE', 'TRY{}CATCH')
        JSTF[('Try_Statement', char, 'TRY{}FINALLY{}CATCH')] = ('Catch_Statement', 'R', 'CHANGE', 'TRY{}FINALLY{}CATCH')
    for char in LINEBREAKS:
        JSTF[('Try_Statement', char, 'TRY{}CATCH')] = ('Catch_Statement', 'R', 'CHANGE', 'TRY{}CATCH')
        JSTF[('Try_Statement', char, 'TRY{}FINALLY{}CATCH')] = ('Catch_Statement', 'R', 'CHANGE', 'TRY{}FINALLY{}CATCH')
    JSTF[('Try_Statement', '(', 'TRY{}CATCH')] = ('Catch_Statement', 'L', 'CHANGE', 'TRY{}CATCH')
    JSTF[('Try_Statement', '(', 'TRY{}FINALLY{}CATCH')] = ('Catch_Statement', 'L', 'CHANGE', 'TRY{}FINALLY{}CATCH')
    JSTF[('Try_Statement', 'else', 'any')] = ('Syntax_Error', 'L', 'POP', '')
    JSTF[('Try_Statement', 'else', 'TRY{}FINALLY{}')] = ('Check_For_End_Of_Block', 'L', 'POP', '')
    JSTF[('Try_Statement', 'else', 'TRY{}CATCH(P){}')] = ('Check_For_End_Of_Block', 'L', 'POP', '')
    JSTF[('Try_Statement', 'else', 'TRY{}FINALLY{}CATCH(P){}')] = ('Check_For_End_Of_Block', 'L', 'POP', '')
    # finally
    JSTF[('Try_Statement', 'f', 'try{}')] = ('Try_Statement', 'R', 'CHANGE', 'try{}F')
    JSTF[('Try_Statement', 'i', 'try{}F')] = ('Try_Statement', 'R', 'CHANGE', 'try{}FI')
    JSTF[('Try_Statement', 'else', 'try{}F')] = ('Syntax_Error', 'R', 'POP', '')
    JSTF[('Try_Statement', 'n', 'try{}FI')] = ('Try_Statement', 'R', 'CHANGE', 'try{}FIN')
    JSTF[('Try_Statement', 'else', 'try{}FI')] = ('Syntax_Error', 'R', 'POP', '')
    JSTF[('Try_Statement', 'a', 'try{}FIN')] = ('Try_Statement', 'R', 'CHANGE', 'try{}FINA')
    JSTF[('Try_Statement', 'else', 'try{}FIN')] = ('Syntax_Error', 'R', 'POP', '')
    JSTF[('Try_Statement', 'l', 'try{}FINA')] = ('Try_Statement', 'R', 'CHANGE', 'try{}FINAL')
    JSTF[('Try_Statement', 'else', 'try{}FINA')] = ('Syntax_Error', 'R', 'POP', '')
    JSTF[('Try_Statement', 'l', 'try{}FINAL')] = ('Try_Statement', 'R', 'CHANGE', 'try{}FINALL')
    JSTF[('Try_Statement', 'else', 'try{}FINAL')] = ('Syntax_Error', 'R', 'POP', '')
    JSTF[('Try_Statement', 'y', 'try{}FINALL')] = ('Try_Statement', 'R', 'CHANGE', 'try{}FINALLY')
    JSTF[('Try_Statement', 'else', 'try{}FINALL')] = ('Syntax_Error', 'R', 'POP', '')
    for char in WHITESPACES:
        JSTF[('Try_Statement', char, 'try{}FINALLY')] = ('Catch_Statement', 'R', 'CHANGE', 'TRY{}FINALLY')
    for char in LINEBREAKS:
        JSTF[('Try_Statement', char, 'try{}FINALLY')] = ('Catch_Statement', 'R', 'CHANGE', 'TRY{}FINALLY')
    JSTF[('Try_Statement', 'else', 'try{}FINALLY')] = ('Syntax_Error', 'L', 'POP', '')
    # ********************************* Catch_Statement State Rules    *******************************************
    for char in WHITESPACES:
        JSTF[('Catch_Statement', char, 'any')] = ('Catch_Statement', 'R', 'READ', '')

    for char in LINEBREAKS:
        JSTF[('Catch_Statement', char, 'any')] = ('Catch_Statement', 'R', 'READ', '')

    JSTF[('Catch_Statement', '(', 'TRY{}CATCH')] = ('Catch_Statement', 'R', 'CHANGE', 'TRY{}CATCH(')
    JSTF[('Catch_Statement', '(', 'TRY{}FINALLY{}CATCH')] = ('Catch_Statement', 'R', 'CHANGE', 'TRY{}finally{}CATCH(')
    # Catch Parameter
    # BindingIdentifier
    for char in ASCII_alpha:
        JSTF[('Catch_Statement', char, 'TRY{}CATCH(')] = ('Identifier_Name', 'L', 'CHANGE', '$ITRY{}CATCH(P')
        JSTF[('Catch_Statement', char, 'TRY{}FINALLY{}CATCH(')] = (
            'Identifier_Name', 'L', 'CHANGE', '$ITRY{}FINALLY{}CATCH(P')
    # go to binding Pattern State
    JSTF[('Catch_Statement', '{', 'any')] = ('BindingPattern', 'L', 'READ', '')
    JSTF[('Catch_Statement', '[', 'any')] = ('BindingPattern', 'L', 'READ', '')
    JSTF[('Catch_Statement', ')', 'TRY{}CATCH(P')] = ('Catch_Statement', 'R', 'CHANGE', 'TRY{}CATCH(P)')
    JSTF[('Catch_Statement', ')', 'TRY{}FINALLY{}CATCH(P')] = (
        'Catch_Statement', 'R', 'CHANGE', 'TRY{}FINALLY{}CATCH(P)')
    JSTF[('Catch_Statement', '{', 'TRY{}CATCH(P)')] = ('Block_Statement', 'R', 'PUSH', 'B{{')
    JSTF[('Catch_Statement', '{', 'TRY{}FINALLY{}CATCH(P)')] = ('Block_Statement', 'R', 'PUSH', 'B{{')
    JSTF[('Catch_Statement', 'else', 'TRY{}FINALLY{}')] = ('Check_For_End_Of_Block', 'L', 'POP', '')
    JSTF[('Catch_Statement', 'else', 'TRY{}CATCH(P){}')] = ('Check_For_End_Of_Block', 'L', 'POP', '')
    JSTF[('Catch_Statement', 'else', 'TRY{}FINALLY{}CATCH(P){}')] = ('Check_For_End_Of_Block', 'L', 'POP', '')
    # ********************************* FunctionExpression State Rules    *****************************************
    for char in WHITESPACES:
        JSTF[('FunctionExpression', char, 'any')] = ('FunctionExpression', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('FunctionExpression', char, 'any')] = ('FunctionExpression', 'R', 'READ', '')
    for char in ASCII_alpha:
        JSTF[('FunctionExpression', char, 'FE')] = ('Identifier_Name', 'L', 'PUSH', '$I')
        JSTF[('FunctionExpression', char, 'FE*')] = ('Identifier_Name', 'L', 'CHANGE', '$IFE')

    JSTF[('FunctionExpression', '_', 'FE')] = ('Identifier_Name', 'L', 'PUSH', '$I')
    JSTF[('FunctionExpression', '_', 'FE*')] = ('Identifier_Name', 'L', 'CHANGE', '$IFE')
    JSTF[('FunctionExpression', '(', 'FE')] = ('FormalParameters', 'R', 'CHANGE', 'FE((')
    JSTF[('FunctionExpression', '(', 'FE*')] = ('FormalParameters', 'R', 'CHANGE', 'FE((')
    # GeneratorExpression
    JSTF[('FunctionExpression', '*', 'FE')] = ('FunctionExpression', 'R', 'CHANGE', 'FE*')
    # Same behaviour for function declarations
    JSTF[('FunctionExpression', 'else', 'FD')] = ('FunctionExpression', 'L', 'PUSH', 'FE')
    # ********************************* FunctionDeclaration State Rules    ****************************************
    for char in WHITESPACES:
        JSTF[('FunctionDeclaration', char, 'FD')] = ('FunctionDeclaration', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('FunctionDeclaration', char, 'FD')] = ('FunctionDeclaration', 'R', 'READ', '')
    # Generator Declaration
    JSTF[('FunctionDeclaration', '*', 'FD')] = ('FunctionExpression', 'R', 'READ', '')
    for char in ASCII_alpha:
        JSTF[('FunctionDeclaration', char, 'FD')] = ('FunctionExpression', 'L', 'READ', '')
    JSTF[('FunctionDeclaration', '_', 'FD')] = ('FunctionExpression', 'L', 'READ', '')
    JSTF[('FunctionDeclaration', '(', 'FD')] = ('FunctionExpression', 'L', 'READ', 'FD')
    # ********************************* FormalParameters State Rules    ******************************************
    for char in WHITESPACES:
        JSTF[('FormalParameters', char, 'any')] = ('FormalParameters', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('FormalParameters', char, 'any')] = ('FormalParameters', 'R', 'READ', '')
    # FornalParameter -->  BindingElement
    for char in ASCII_alpha:
        JSTF[('FormalParameters', 'else', 'any')] = ('Identifier_Name', 'L', 'CHANGE', '$IFE(FP')
    JSTF[('FormalParameters', '{', 'any')] = ('BindingPattern', 'L', 'CHANGE', 'FE(FP')
    JSTF[('FormalParameters', '[', 'any')] = ('BindingPattern', 'L', 'CHANGE', 'FE(FP')
    JSTF[('FormalParameters', ',', 'FE((')] = ('Syntax_Error', 'R', 'READ', '')
    JSTF[('FormalParameters', ',', 'any')] = ('FormalParameters', 'R', 'READ', '')
    # BindingRestElement
    JSTF[('FormalParameters', '.', 'FE((')] = ('FormalParameters', 'L', 'CHANGE', 'FE(FP')
    JSTF[('FormalParameters', '.', 'FE(FP')] = ('BindingRestElement1', 'R', 'CHANGE', 'FE(R')
    JSTF[('FormalParameters', ')', 'FE(FP')] = ('FormalParameters', 'R', 'CHANGE', 'FE()')
    # Function Body Section
    JSTF[('FormalParameters', '{', 'FE()')] = ('FunctionBody', 'R', 'CHANGE', 'FE(){{')
    # ********************************* FunctionBody State Rules    **********************************************
    for char in WHITESPACES:
        JSTF[('FunctionBody', char, 'any')] = ('FunctionBody', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('FunctionBody', char, 'any')] = ('FunctionBody', 'R', 'READ', '')
    JSTF[('FunctionBody', 'else', 'FE(){{')] = ('Specify_Assignment_Type', 'L', 'CHANGE', 'FE(){')
    JSTF[('FunctionBody', 'else', 'FE(){')] = ('Specify_Assignment_Type', 'L', 'READ', '')
    JSTF[('FunctionBody', '}', 'FE(){{')] = ('After_FunctionBody', 'R', 'POP', '')
    JSTF[('FunctionBody', '}', 'FE(){')] = ('After_FunctionBody', 'R', 'POP', '')
    # ********************************* After_FunctionBody State Rules    ****************************************
    for char in WHITESPACES:
        JSTF[('After_FunctionBody', char, 'any')] = ('After_FunctionBody', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('After_FunctionBody', char, 'any')] = ('After_FunctionBody', 'R', 'READ', '')
    JSTF[('After_FunctionBody', 'else', 'FD')] = ('Check_For_End_Of_Block', 'L', 'POP', '')
    JSTF[('After_FunctionBody', ';', 'FD')] = ('Check_For_Empty_Stack', 'R', 'POP', '')
    # AsyncFunctionExpression
    JSTF[('After_FunctionBody', 'else', 'AE')] = ('Pre_After_Assignment_No_Line_Terminator', 'L', 'POP', '')
    JSTF[('After_FunctionBody', 'else', 'any')] = ('Pre_After_Assignment_No_Line_Terminator', 'L', 'READ', '')
    # conditional if else with ? :
    JSTF[('After_FunctionBody', ':', '?')] = ('Wait_For_Assignment', 'R', 'CHANGE', '?:')
    ## Assignments with a function decleration and then comma
    JSTF[('After_FunctionBody', ',', 'FD')] = ('After_Function_Body_Wait_For_Assignment', 'R', 'POP', '')
    ## {IA assignment of a function
    JSTF[('After_FunctionBody', ',', '{IA')] = ('After_Function_Body_Wait_For_Assignment', 'L', 'CHANGE', '{I')
    # ****************************** After_Function_Body_Wait_For_Assignment State Rules    **********************
    JSTF[('After_Function_Body_Wait_For_Assignment', 'else', '{IA')] = (
        'After_Function_Body_Wait_For_Assignment', 'L', 'CHANGE', '{I')
    JSTF[('After_Function_Body_Wait_For_Assignment', 'else', 'any')] = ('Wait_For_Assignment', 'L', 'READ', '')
    # ********************************* AsyncDeclaration State Rules    ******************************************
    for char in WHITESPACES:
        JSTF[('AsyncDeclaration', char, 'any')] = ('AsyncDeclaration', 'R', 'READ', '')

    JSTF[('AsyncDeclaration', 'f', 'any')] = ('AFunctionExpression1', 'READ', '')
    JSTF[('AFunctionExpression1', 'else', 'any')] = ('Syntax_Error', 'L', 'READ', '')
    JSTF[('AFunctionExpression1', 'u', 'any')] = ('AFunctionExpression2', 'R', 'READ', '')
    JSTF[('AFunctionExpression2', 'else', 'any')] = ('Syntax_Error', 'L', 'READ', '')
    JSTF[('AFunctionExpression2', 'n', 'any')] = ('AFunctionExpression3', 'R', 'READ', '')
    JSTF[('AFunctionExpression3', 'else', 'any')] = ('Syntax_Error', 'L', 'READ', '')
    JSTF[('AFunctionExpression3', 'c', 'any')] = ('AFunctionExpression4', 'R', 'READ', '')
    JSTF[('AFunctionExpression4', 't', 'any')] = ('AFunctionExpression5', 'R', 'READ', '')
    JSTF[('AFunctionExpression4', 'else', 'any')] = ('Syntax_Error', 'L', 'READ', '')
    JSTF[('AFunctionExpression5', 'i', 'any')] = ('AFunctionExpression6', 'R', 'READ', '')
    JSTF[('AFunctionExpression5', 'else', 'any')] = ('Syntax_Error', 'L', 'READ', '')
    JSTF[('AFunctionExpression6', 'o', 'any')] = ('AFunctionExpression7', 'R', 'READ', '')
    JSTF[('AFunctionExpression6', 'else', 'any')] = ('Syntax_Error', 'L', 'READ', '')
    JSTF[('AFunctionExpression7', 'n', 'any')] = ('AFunctionExpression8', 'R', 'READ', '')
    JSTF[('AFunctionExpression7', 'else', 'any')] = ('Syntax_Error', 'L', 'READ', '')
    for char in WHITESPACES:
        JSTF[('AFunctionExpression8', char, 'any')] = ('FunctionExpression', 'R', 'PUSH', 'FE')
    for char in LINEBREAKS:
        JSTF[('AFunctionExpression8', char, 'any')] = ('FunctionExpression', 'R', 'PUSH', 'FE')
    JSTF[('AFunctionExpression8', 'else', 'any')] = ('Syntax_Error', 'L', 'READ', '')
    # ********************************* ClassDeclaration State Rules    *******************************************
    for char in WHITESPACES:
        JSTF[('ClassDeclaration', char, 'any')] = ('ClassDeclaration', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('ClassDeclaration', char, 'any')] = ('ClassDeclaration', 'R', 'READ', '')
    for char in ASCII_alpha:
        JSTF[('ClassDeclaration', char, 'CD')] = ('Identifier_Name', 'L', 'PUSH', '$I')
    JSTF[('FunctionExpression', 'else', 'CD')] = ('ClassTail', 'L', 'READ', '')
    # ********************************* ClassTail State Rules    ***************************************************
    for char in WHITESPACES:
        JSTF[('ClassTail', char, 'any')] = ('ClassTail', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('ClassTail', char, 'any')] = ('ClassTail', 'R', 'READ', '')
    # ClassHeritage
    JSTF[('ClassTail', 'e', 'CD')] = ('ClassHeritage1', 'READ', '')
    JSTF[('ClassHeritage1', 'x', 'any')] = ('ClassHeritage2', 'R', 'READ', '')
    JSTF[('ClassHeritage1', 'else', 'any')] = ('Syntax_Error', 'L', 'READ', '')
    JSTF[('ClassHeritage2', 't', 'any')] = ('ClassHeritage3', 'R', 'READ', '')
    JSTF[('ClassHeritage2', 'else', 'any')] = ('Syntax_Error', 'L', 'READ', '')
    JSTF[('ClassHeritage3', 'e', 'any')] = ('ClassHeritage4', 'R', 'READ', '')
    JSTF[('ClassHeritage3', 'else', 'any')] = ('Syntax_Error', 'L', 'READ', '')
    JSTF[('ClassHeritage4', 'n', 'any')] = ('ClassHeritage5', 'R', 'READ', '')
    JSTF[('ClassHeritage4', 'else', 'any')] = ('Syntax_Error', 'L', 'READ', '')
    JSTF[('ClassHeritage5', 'd', 'any')] = ('ClassHeritage6', 'R', 'READ', '')
    JSTF[('ClassHeritage5', 'else', 'any')] = ('Syntax_Error', 'L', 'READ', '')
    JSTF[('ClassHeritage6', 's', 'any')] = ('ClassHeritage7', 'R', 'READ', '')
    JSTF[('ClassHeritage6', 'else', 'any')] = ('Syntax_Error', 'L', 'READ', '')
    for char in WHITESPACES:
        JSTF[('ClassHeritage7', char, 'any')] = ('Wait_For_Assignment', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('ClassHeritage7', char, 'any')] = ('Wait_For_Assignment', 'R', 'READ', '')
    JSTF[('ClassHeritage7', 'else', 'any')] = ('Syntax_Error', 'L', 'READ', '')
    JSTF[('ClassTail', '{', 'CD')] = ('ClassBody', 'R', 'CHANGE', 'CD{')
    # ********************************* ClassBody State Rules    ************************************************
    for char in WHITESPACES:
        JSTF[('ClassBody', char, 'any')] = ('ClassBody', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('ClassBody', char, 'any')] = ('ClassBody', 'R', 'READ', '')
    # extends
    JSTF[('ClassBody', ';', 'CD{')] = ('ClassBody', 'R', 'READ', '')
    JSTF[('ClassBody', '}', 'CD{')] = ('Check_For_End_Of_Block', 'R', 'POP', '')
    # ********************************* MethodDefinition  State Rules    ****************************************
    for char in WHITESPACES:
        JSTF[('MethodDefinition', char, 'any')] = ('MethodDefinition', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('MethodDefinition', char, 'any')] = ('MethodDefinition', 'R', 'READ', '')
    # AsyncMethod
    JSTF[('MethodDefinition', 'a', 'any')] = ('MAsyncDeclaration1', 'READ', '')
    JSTF[('MAsyncDeclaration1', 's', 'any')] = ('MAsyncDeclaration2', 'R', 'READ', '')
    JSTF[('MAsyncDeclaration2', 'y', 'any')] = ('MAsyncDeclaration3', 'R', 'READ', '')
    JSTF[('MAsyncDeclaration3', 'n', 'any')] = ('MAsyncDeclaration4', 'R', 'READ', '')
    JSTF[('MAsyncDeclaration4', 'c', 'any')] = ('MAsyncDeclaration5', 'R', 'READ', '')
    for char in WHITESPACES:
        JSTF[('MAsyncDeclaration5', char, 'any')] = ('AsyncMethodDeclaration', 'R', 'READ', '')
    # GeneratorMethod
    JSTF[('MethodDefinition', '*', 'any')] = ('Wait_For_PropertyName', 'R', 'PUSH', 'AMD')
    # getMethod
    JSTF[('MethodDefinition', 'g', 'any')] = ('GetMethodDeclaration1', 'READ', '')
    JSTF[('GetMethodDeclaration1', 'e', 'any')] = ('GetMethodDeclaration2', 'R', 'READ', '')
    JSTF[('GetMethodDeclaration2', 't', 'any')] = ('GetMethodDeclaration3', 'R', 'READ', '')
    for char in WHITESPACES:
        JSTF[('GetMethodDeclaration3', char, 'any')] = ('Wait_For_PropertyName', 'R', 'PUSH', 'GMD')
    for char in LINEBREAKS:
        JSTF[('GetMethodDeclaration3', char, 'any')] = ('Wait_For_PropertyName', 'R', 'PUSH', 'GMD')
    # setMethod
    JSTF[('MethodDefinition', 's', 'any')] = ('SetMethodDeclaration1', 'READ', '')
    JSTF[('SetMethodDeclaration1', 'e', 'any')] = ('SetMethodDeclaration2', 'R', 'READ', '')
    JSTF[('SetMethodDeclaration2', 't', 'any')] = ('SetMethodDeclaration3', 'R', 'READ', '')
    for char in WHITESPACES:
        JSTF[('SetMethodDeclaration3', char, 'any')] = ('Wait_For_PropertyName', 'R', 'PUSH', 'SMD')
    for char in LINEBREAKS:
        JSTF[('SetMethodDeclaration3', char, 'any')] = ('Wait_For_PropertyName', 'R', 'PUSH', 'SMD')
    # ********************************* AsyncMethodDeclaration State Rules    ************************************
    for char in WHITESPACES:
        JSTF[('AsyncMethodDeclaration', char, 'any')] = ('AsyncMethodDeclaration', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('AsyncMethodDeclaration', char, 'any')] = ('Syntax_Error', 'R', 'READ', '')
    JSTF[('AsyncMethodDeclaration', 'else', 'any')] = ('Wait_For_PropertyName', 'L', 'PUSH', 'AMD')
    # ********************************* Wait_For_PropertyName State Rules    *************************************
    for char in WHITESPACES:
        JSTF[('Wait_For_PropertyName', char, 'any')] = ('Wait_For_PropertyName', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('Wait_For_PropertyName', char, 'any')] = ('Wait_For_PropertyName', 'R', 'READ', '')
    # LiteralPropertyName
    JSTF[('Wait_For_PropertyName', '"', 'any')] = ('Double_Quote_Inside_Assignment_Pushed', 'R', 'PUSH', 'PN')
    JSTF[('Wait_For_PropertyName', "'", 'any')] = ('Single_Quote_Inside_Assignment_Pushed', 'R', 'PUSH', 'PN')
    for char in Digits:
        JSTF[('Wait_For_PropertyName', char, 'any')] = ('Numeric_Assignment', 'L', 'PUSH', 'PN')
    for char in ASCII_alpha:
        JSTF[('Wait_For_PropertyName', char, 'any')] = ('Identifier_Name', 'L', 'PUSH', '$IPN')
    JSTF[('ObjectLiteral', '[', 'any')] = ('Wait_For_Assignment', 'L', 'PUSH', '[PN')
    # ********************************* After_PropertyName State Rules    ****************************************
    for char in WHITESPACES:
        JSTF[('After_PropertyName', char, 'any')] = ('After_PropertyName', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('After_PropertyName', char, 'any')] = ('After_PropertyName', 'R', 'READ', '')
    JSTF[('After_PropertyName', '(', 'AMD')] = ('FunctionExpression', 'R', 'CHANGE', 'FE((')
    # GetMethod
    JSTF[('After_PropertyName', '(', 'GMD')] = ('After_PropertyName', 'R', 'CHANGE', 'GMD(')
    JSTF[('After_PropertyName', ')', 'GMD(')] = ('After_PropertyName', 'R', 'CHANGE', 'GMD()')
    JSTF[('After_PropertyName', '{', 'GMD()')] = ('GetMethodWaitForBody', 'L', 'CHANGE', 'FD')
    # SetMethod
    JSTF[('After_PropertyName', '(', 'SMD')] = ('Wait_For_Binding_Element', 'R', 'CHANGE', 'SMD(')
    # ********************************* GetMethodWaitForBody State Rules    *************************************
    for char in WHITESPACES:
        JSTF[('GetMethodWaitForBody', char, 'any')] = ('GetMethodWaitForBody', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('GetMethodWaitForBody', char, 'any')] = ('GetMethodWaitForBody', 'R', 'READ', '')
    JSTF[('GetMethodWaitForBody', '{', 'FD')] = ('FunctionBody', 'R', 'CHANGE', 'FE(){{')
    # *********************************  Pre_After_Identifier_Or_Function State Rules    **************************
    for char in WHITESPACES:
        JSTF[('Pre_After_Identifier_Or_Function', char, 'any')] = ('Pre_After_Identifier_Or_Function', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('Pre_After_Identifier_Or_Function', char, 'any')] = ('After_Assignment', 'R', 'READ', '')
    JSTF[('Pre_After_Identifier_Or_Function', "=", 'any')] = ('Pre_After_Identifier_Or_Function', 'R', 'PUSH', '=')
    JSTF[('Pre_After_Identifier_Or_Function', ">", '=')] = ('ArrowFunction_ConciseBody', 'R', 'POP', '=')
    JSTF[('Pre_After_Identifier_Or_Function', "else", '=')] = ('Wait_For_Assignment', 'L', 'READ', '')
    JSTF[('Pre_After_Identifier_Or_Function', ".", 'any')] = ('Identifier_Or_Function_Class', 'R', 'PUSH', 'CLASS.')
    JSTF[('Pre_After_Identifier_Or_Function', "else", 'any')] = (
        'Pre_After_Assignment_No_Line_Terminator', 'L', 'READ', '')
    # ****************  ArrowParameters State Rules  ***************************************************************
    for char in WHITESPACES:
        JSTF[('ArrowParameters', char, 'any')] = ('ArrowParameters', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('ArrowParameters', char, 'any')] = ('ArrowParameters', 'R', 'READ', '')

    JSTF[('ArrowParameters', ')', 'AP')] = ('Pre_After_Identifier_Or_Function', 'R', 'POP', 'AP')
    JSTF[('ArrowParameters', ')', 'AP,')] = ('Pre_After_Identifier_Or_Function', 'R', 'POP', 'AP,')
    JSTF[('ArrowParameters', ',', 'AP')] = ('ArrowParameters', 'R', 'CHANGE', 'AP,')
    JSTF[('ArrowParameters', ',', 'AP,')] = ('Syntax_Error', 'R', 'READ', '')
    JSTF[('ArrowParameters', 'else', 'any')] = ('Wait_For_Assignment', 'L', 'CHANGE', 'AP')
    JSTF[('ArrowParameters', '.', 'any')] = ('BindingRestElement1', 'R', 'CHANGE', 'AP')
    # *********************************  ArrowFunction_ConciseBody State Rules    **********************************
    for char in WHITESPACES:
        JSTF[('ArrowFunction_ConciseBody', char, 'any')] = ('ArrowFunction_ConciseBody', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('ArrowFunction_ConciseBody', char, 'any')] = ('ArrowFunction_ConciseBody', 'R', 'READ', '')
    JSTF[('ArrowFunction_ConciseBody', "{", 'any')] = ('FunctionBody', 'R', 'CHANGE', 'FE(){{')
    JSTF[('ArrowFunction_ConciseBody', "else", 'any')] = ('Wait_For_Assignment', 'L', 'READ', '')
    # *********************************  AsyncArrowFunction State Rules    *****************************************
    for char in WHITESPACES:
        JSTF[('AsyncArrowFunction', char, 'any')] = ('AsyncArrowFunction', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('AsyncArrowFunction', char, 'any')] = ('Syntax_Error', 'R', 'READ', '')
    for char in ASCII_alpha:
        JSTF[('AsyncArrowFunction', char, 'AF')] = ('Identifier_Name', 'L', 'PUSH', '$I')

    JSTF[('AsyncArrowFunction', '=', 'AFB')] = ('Pre_After_Identifier_Or_Function', 'L', 'POP', 'AFB')
    # AsyncFunctionExpression
    JSTF[('AsyncArrowFunction', 'f', 'any')] = ('AsyncDeclaration', 'L', 'PUSH', 'AE')
    # *******************************  Pre_After_Function_No_Line_Terminator State Rules    *************************
    for char in WHITESPACES:
        JSTF[('Pre_After_Function_No_Line_Terminator', char, 'any')] = (
            'Pre_After_Function_No_Line_Terminator', 'R', 'READ', '')

    # arguments
    JSTF[('Pre_After_Function_No_Line_Terminator', '(', 'any')] = ('After_Assignment', 'R', 'PUSH', 'FUN($I')
    # CallExpression [Expression]
    JSTF[('Pre_After_Function_No_Line_Terminator', '[', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', 'FUN[')
    # CallExpression . Identifier
    JSTF[('Pre_After_Function_No_Line_Terminator', '.', 'any')] = ('Wait_For_Identifier_Name', 'R', 'PUSH', 'FUN.IN')
    # CallExpression TemplateLiteral
    JSTF[('Pre_After_Function_No_Line_Terminator', '`', 'any')] = ('TemplateLiteral', 'R', 'PUSH', 'FUN`')
    JSTF[('Pre_After_Function_No_Line_Terminator', "else", 'any')] = (
        'After_Assignment', 'L', 'READ', '')
    # *********************************  Wait_For_Identifier_Name State Rules    **************************************
    for char in WHITESPACES:
        JSTF[('Wait_For_Identifier_Name', char, 'any')] = ('Wait_For_Identifier_Name', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('Wait_For_Identifier_Name', char, 'any')] = ('Wait_For_Identifier_Name', 'R', 'READ', '')
    for char in ASCII_alpha:
        JSTF[('Wait_For_Identifier_Name', char, 'any')] = ('Identifier_Name', 'L', 'PUSH', '$I')
    # *********************************  TemplateLiteral State Rules    ***********************************************
    for char in ASCII_alpha:
        JSTF[('TemplateLiteral', char, 'any')] = ('TemplateLiteral', 'R', 'READ', '')

    JSTF[('TemplateLiteral', '`', 'FUN`')] = ('Skip_TemplateLiteral_Function', 'R', 'POP', 'FUN`')
    JSTF[('TemplateLiteral', '`', '`')] = ('Skip_TemplateLiteral', 'R', 'POP', '`')
    JSTF[('TemplateLiteral', '$', 'any')] = ('TemplateLiteral_Wait_For_Expression', 'R', 'PUSH', '$')
    # *********************************  Skip_TemplateLiteral State Rules    *******************************************
    JSTF[('Skip_TemplateLiteral', 'else', 'FUN`')] = ('TemplateLiteral', 'L', 'READ', '')
    JSTF[('Skip_TemplateLiteral', 'else', '`')] = ('TemplateLiteral', 'L', 'READ', '')
    JSTF[('Skip_TemplateLiteral', 'else', 'any')] = ('Pre_After_Assignment_No_Line_Terminator', 'L', 'READ', '')
    # *********************************  Skip_TemplateLiteral_Function State Rules    ***********************************
    JSTF[('Skip_TemplateLiteral_Function', 'else', 'FUN`')] = ('TemplateLiteral', 'L', 'READ', '')
    JSTF[('Skip_TemplateLiteral_Function', 'else', '`')] = ('TemplateLiteral', 'L', 'READ', '')
    JSTF[('Skip_TemplateLiteral', 'else', 'any')] = ('Pre_After_Function_No_Line_Terminator', 'L', 'READ', '')
    # *********************************  TemplateLiteral_Wait_For_Expression State Rules    *****************************
    for char in WHITESPACES:
        JSTF[('TemplateLiteral_Wait_For_Expression', char, 'any')] = (
            'TemplateLiteral_Wait_For_Expression', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('TemplateLiteral_Wait_For_Expression', char, 'any')] = (
            'TemplateLiteral_Wait_For_Expression', 'R', 'READ', '')

    JSTF[('TemplateLiteral_Wait_For_Expression', '{', '$')] = ('Wait_For_Assignment', 'R', 'CHANGE', '${')
    JSTF[('TemplateLiteral_Wait_For_Expression', '}', '${')] = ('TemplateLiteral', 'R', 'CHANGE', 'FUN`')
    # *********************************  Super_Call State Rules    ******************************************************
    # SuperCall and SuperProperty
    for char in WHITESPACES:
        JSTF[('Super_Call', char, 'any')] = ('Super_Call', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('Super_Call', char, 'any')] = ('Super_Call', 'R', 'READ', '')
    JSTF[('Super_Call', '(', 'SUPER')] = ('After_Assignment', 'R', 'CHANGE', 'FUN(')
    JSTF[('Super_Call', '[', 'SUPER')] = ('Wait_For_Assignment', 'R', 'CHANGE', 'SUP[')
    JSTF[('Super_Call', '.', 'SUPER')] = ('Wait_For_Identifier_Name', 'R', 'CHANGE', 'SUP.IN')
    # *********************************  NewExpression State Rules    **************************************************
    # NewProperty and NewTarget
    for char in WHITESPACES:
        JSTF[('NewExpression', char, 'any')] = ('NewExpression', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('NewExpression', char, 'any')] = ('NewExpression', 'R', 'READ', '')

    JSTF[('NewExpression', '.', 'any')] = ('Wait_For_Target', 'R', 'READ', '')
    JSTF[('NewExpression', 'else', 'any')] = ('Wait_For_Assignment', 'L', 'READ', '')
    # *********************************  Wait_For_Target State Rules    *************************************************
    for char in WHITESPACES:
        JSTF[('Wait_For_Target', char, 'any')] = ('Wait_For_Target', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('Wait_For_Target', char, 'any')] = ('Wait_For_Target', 'R', 'READ', '')
    JSTF[('Wait_For_Target', 't', 'any')] = ('TargetExpression1', 'R', 'READ', '')
    JSTF[('TargetExpression1', 'a', 'any')] = ('TargetExpression2', 'R', 'READ', '')
    JSTF[('TargetExpression1', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('TargetExpression2', 'r', 'any')] = ('TargetExpression3', 'R', 'READ', '')
    JSTF[('TargetExpression2', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('TargetExpression3', 'g', 'any')] = ('TargetExpression4', 'R', 'READ', '')
    JSTF[('TargetExpression3', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('TargetExpression4', 'e', 'any')] = ('TargetExpression5', 'R', 'READ', '')
    JSTF[('TargetExpression4', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    JSTF[('TargetExpression5', 't', 'any')] = ('TargetExpression6', 'R', 'READ', '')
    JSTF[('TargetExpression5', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    for char in WHITESPACES:
        JSTF[('TargetExpression6', char, 'any')] = ('Pre_After_Assignment_No_Line_Terminator', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('TargetExpression6', char, 'any')] = ('After_Assignment', 'R', 'READ', '')
    JSTF[('TargetExpression6', 'else', 'any')] = ('Identifier_Or_Function', 'L', 'READ', '')
    # *********************************  ClassExpression State Rules    *************************************************
    for char in WHITESPACES:
        JSTF[('ClassExpression', char, 'any')] = ('ClassExpression', 'R', 'READ', '')
    for char in LINEBREAKS:
        JSTF[('ClassExpression', char, 'any')] = ('ClassExpression', 'R', 'READ', '')
    JSTF[('ClassExpression', 'else', 'CE')] = ('ClassDeclaration', 'L', 'PUSH', 'CD')
    # *********************************  RegularExpressionLiteral State Rules    ****************************************
    JSTF[('RegularExpressionLiteral', '/', 'REL//')] = ('Single_Line_Comment', 'R', 'POP', '')
    JSTF[('RegularExpressionLiteral', '*', 'REL//')] = ('Multi_Line_Comment', 'R', 'POP', '')
    JSTF[('RegularExpressionLiteral', 'else', 'REL//')] = ('RegularExpressionLiteral', 'L', 'CHANGE', 'REL')
    JSTF[('RegularExpressionLiteral', 'else', 'REL')] = ('RegularExpressionLiteral', 'R', 'CHANGE', 'REL')
    JSTF[('RegularExpressionLiteral', '/', 'REL')] = ('RegularExpressionFlags', 'R', 'POP', 'REL')
    JSTF[('RegularExpressionLiteral', '\\', 'REL')] = ('RegularExpressionBackslashSequence', 'R', 'READ', '')
    JSTF[('RegularExpressionLiteral', '[', 'REL')] = ('RegularExpressionClass', 'R', 'PUSH', 'RELC')
    # *********************************  RegularExpressionBackslashSequence State Rules    *******************************
    for char in Source_Char_Without_Non_Terminator:
        if (char != '*' and char != '/' and char != '\\' and char != '['):
            JSTF[('RegularExpressionBackslashSequence', char, 'REL')] = ('RegularExpressionLiteral', 'R', 'READ', '')
            JSTF[('RegularExpressionBackslashSequence', char, 'RELC')] = ('RegularExpressionClass', 'R', 'READ', '')

    JSTF[('RegularExpressionBackslashSequence', '.', 'REL')] = ('RegularExpressionLiteral', 'R', 'READ', '')
    JSTF[('RegularExpressionBackslashSequence', '?', 'REL')] = ('RegularExpressionLiteral', 'R', 'READ', '')
    JSTF[('RegularExpressionBackslashSequence', '.', 'RELC')] = ('RegularExpressionClass', 'R', 'READ', '')
    JSTF[('RegularExpressionBackslashSequence', '/', 'REL')] = ('RegularExpressionLiteral', 'R', 'READ', '')
    JSTF[('RegularExpressionBackslashSequence', '/', 'RELC')] = ('RegularExpressionClass', 'R', 'READ', '')
    JSTF[('RegularExpressionBackslashSequence', '\\', 'REL')] = ('RegularExpressionLiteral', 'R', 'READ', '')
    JSTF[('RegularExpressionBackslashSequence', '\\', 'RELC')] = ('RegularExpressionClass', 'R', 'READ', '')
    JSTF[('RegularExpressionBackslashSequence', ']', 'REL')] = ('RegularExpressionLiteral', 'R', 'READ', '')
    JSTF[('RegularExpressionBackslashSequence', ']', 'RELC')] = ('RegularExpressionClass', 'R', 'READ', '')
    JSTF[('RegularExpressionBackslashSequence', '[', 'REL')] = ('RegularExpressionLiteral', 'R', 'READ', '')
    JSTF[('RegularExpressionBackslashSequence', '[', 'RELC')] = ('RegularExpressionClass', 'R', 'READ', '')
    JSTF[('RegularExpressionBackslashSequence', ')', 'REL')] = ('RegularExpressionLiteral', 'R', 'READ', '')
    JSTF[('RegularExpressionBackslashSequence', ')', 'RELC')] = ('RegularExpressionClass', 'R', 'READ', '')
    JSTF[('RegularExpressionBackslashSequence', '(', 'REL')] = ('RegularExpressionLiteral', 'R', 'READ', '')
    JSTF[('RegularExpressionBackslashSequence', '(', 'RELC')] = ('RegularExpressionClass', 'R', 'READ', '')
    JSTF[('RegularExpressionBackslashSequence', "'", 'REL')] = ('RegularExpressionLiteral', 'R', 'READ', '')
    JSTF[('RegularExpressionBackslashSequence', "'", 'RELC')] = ('RegularExpressionClass', 'R', 'READ', '')
    JSTF[('RegularExpressionBackslashSequence', '"', 'REL')] = ('RegularExpressionLiteral', 'R', 'READ', '')
    JSTF[('RegularExpressionBackslashSequence', '"', 'RELC')] = ('RegularExpressionClass', 'R', 'READ', '')
    JSTF[('RegularExpressionBackslashSequence', '-', 'REL')] = ('RegularExpressionLiteral', 'R', 'READ', '')
    JSTF[('RegularExpressionBackslashSequence', '-', 'RELC')] = ('RegularExpressionClass', 'R', 'READ', '')
    JSTF[('RegularExpressionBackslashSequence', '^', 'REL')] = ('RegularExpressionLiteral', 'R', 'READ', '')
    JSTF[('RegularExpressionBackslashSequence', '^', 'RELC')] = ('RegularExpressionClass', 'R', 'READ', '')
    # *********************************  RegularExpressionClass State Rules    ******************************************
    for char in Source_Char_Without_Non_Terminator:
        if (char != '\\' and char != ']'):
            JSTF[('RegularExpressionClass', char, 'any')] = ('RegularExpressionClass', 'R', 'READ', '')
    JSTF[('RegularExpressionClass', '-', 'any')] = ('RegularExpressionClass', 'R', 'READ', '')
    JSTF[('RegularExpressionClass', ']', 'RELC')] = ('RegularExpressionLiteral', 'R', 'POP', 'RELC')
    JSTF[('RegularExpressionClass', '\\', 'RELC')] = ('RegularExpressionBackslashSequence', 'R', 'READ', '')
    JSTF[('RegularExpressionClass', '^', 'any')] = ('RegularExpressionClass', 'R', 'READ', '')
    JSTF[('RegularExpressionClass', 'else', 'any')] = ('RegularExpressionClass', 'R', 'READ', '')
    # *********************************  RegularExpressionFlags State Rules    ******************************************
    RE_skip_characters = ['i']  ##needs other chars
    for char in RE_skip_characters:
        JSTF[('RegularExpressionFlags', char, 'any')] = ('RegularExpressionFlags', 'R', 'READ', '')
    JSTF[('RegularExpressionFlags', 'else', 'any')] = ('Pre_After_Function_No_Line_Terminator', ' L', 'READ', '')
    #   *********************************  Single_Line_Comment State Rules    *******************************************
    for char in LINEBREAKS:
        JSTF[('Single_Line_Comment', char, 'any')] = ('After_Comment', 'R', 'READ', '')
    JSTF[('Single_Line_Comment', 'else', 'any')] = ('Single_Line_Comment', 'R', 'READ', '')
    #   *********************************  Single_Line_Comment State Rules    *******************************************
    JSTF[('Multi_Line_Comment', "*", 'any')] = ('Multi_Line_Comment', 'R', 'PUSH', '*')
    JSTF[('Multi_Line_Comment', 'else', 'any')] = ('Multi_Line_Comment', 'R', 'READ', '')
    JSTF[('Multi_Line_Comment', '/', '*')] = ('After_Comment', 'R', 'POP', '')
    JSTF[('Multi_Line_Comment', 'else', '*')] = ('Multi_Line_Comment', 'R', 'POP', '')
    JSTF[('After_Assignment', ',', 'any')] = ('Wait_For_Assignment', 'R', 'READ', '')
    #   *********************************  Tag_Skip State Rules    ******************************************************
    JSTF[('Tag_Skip', chr(47), '<')] = ('Tag_Skip', 'R', 'CHANGE', '</')
    JSTF[('Tag_Skip', 'else', '<')] = ('RelationalExpressionG', 'L', 'POP', '')
    JSTF[('Tag_Skip', 's', '</')] = ('Tag_Skip', 'R', 'CHANGE', 'S')
    JSTF[('Tag_Skip', 'S', '</')] = ('Tag_Skip', 'R', 'CHANGE', 'S')
    JSTF[('Tag_Skip', 'else', '</')] = ('Tag_name_JS', 'L', 'POP', '')
    JSTF[('Tag_Skip', 'c', 'S')] = ('Tag_Skip', 'R', 'CHANGE', 'SC')
    JSTF[('Tag_Skip', 'C', 'S')] = ('Tag_Skip', 'R', 'CHANGE', 'SC')
    JSTF[('Tag_Skip', 'else', 'S')] = ('Tag_name_JS', 'L', 'POP', '')
    JSTF[('Tag_Skip', 'r', 'SC')] = ('Tag_Skip', 'R', 'CHANGE', 'SCR')
    JSTF[('Tag_Skip', 'R', 'SC')] = ('Tag_Skip', 'R', 'CHANGE', 'SCR')
    JSTF[('Tag_Skip', 'else', 'SC')] = ('Tag_name_JS', 'L', 'POP', '')
    JSTF[('Tag_Skip', 'i', 'SCR')] = ('Tag_Skip', 'R', 'CHANGE', 'SCRI')
    JSTF[('Tag_Skip', 'I', 'SCR')] = ('Tag_Skip', 'R', 'CHANGE', 'SCRI')
    JSTF[('Tag_Skip', 'else', 'SCR')] = ('Tag_name_JS', 'L', 'POP', '')
    JSTF[('Tag_Skip', 'p', 'SCRI')] = ('Tag_Skip', 'R', 'CHANGE', 'SCRIP')
    JSTF[('Tag_Skip', 'P', 'SCRI')] = ('Tag_Skip', 'R', 'CHANGE', 'SCRIP')
    JSTF[('Tag_Skip', 'else', 'SCRI')] = ('Tag_name_JS', 'L', 'POP', '')
    JSTF[('Tag_Skip', 't', 'SCRIP')] = ('Tag_Skip', 'R', 'CHANGE', 'SCRIPT')
    JSTF[('Tag_Skip', 'T', 'SCRIP')] = ('Tag_Skip', 'R', 'CHANGE', 'SCRIPT')
    JSTF[('Tag_Skip', 'else', 'SCRIP')] = ('Tag_name_JS', 'L', 'POP', '')
    JSTF[('Tag_Skip', '>', 'SCRIPT')] = ('Transition_Back_To_HTML', 'R', 'POP', 'SCRIPT')
    JSTF[('Tag_Skip', 'else', 'SCRIPT')] = ('Tag_name_JS', 'L', 'POP', '')
    JSTF[('Tag_Skip', 'else', 'any')] = ('Tag_name_JS', 'R', 'POP', '')
    JSTF[('Tag_name_JS', 'else', 'any')] = ('Transition_Back_To_HTML_Syntax', 'L', 'READ', '')
    #   *****************  Avoid matching strings with keyword substrings  for Identifier_Name   ***************************
    for char in Identifier_List:
        JSTF[('Identifier_Name', 'n', char)] = ('NullLiteral_I_pre1', 'R', 'CHANGE', char[2:])
        JSTF[('Identifier_Name', 'f', char)] = ('BooleanLiteralF_I_pre1', 'R', 'CHANGE', char[2:])
        # True keyword
        JSTF[('Identifier_Name', 't', char)] = ('Identifier_Or_Function', 'R', 'PUSH', 'T')
        JSTF[('Identifier_Name', 'else', char)] = ('Identifier_Name', 'L', 'CHANGE', char[2:])
        JSTF[('Identifier_Or_Function', 'else', char)] = ('Identifier_Or_Function', 'L', 'CHANGE', char[2:])

    JSTF[('Identifier_Name', 'n', '$I')] = ('NullLiteral_I_pre1', 'R', 'POP', '')
    JSTF[('Identifier_Name', 'f', '$I')] = ('BooleanLiteralF_I_pre1', 'R', 'POP', '')
    # True keyword
    JSTF[('Identifier_Name', 't', '$I')] = ('Identifier_Name', 'R', 'PUSH', 'T')
    JSTF[('Identifier_Name', 'r', 'T')] = ('Identifier_Name', 'R', 'CHANGE', 'TR')
    JSTF[('Identifier_Name', 'else', 'T')] = ('Identifier_Name', 'L', 'POP', 'T')
    JSTF[('Identifier_Name', 'u', 'TR')] = ('Identifier_Name', 'R', 'CHANGE', 'TRU')
    JSTF[('Identifier_Name', 'else', 'TR')] = ('Identifier_Name', 'L', 'POP', 'TR')
    JSTF[('Identifier_Name', 'e', 'TRU')] = ('Identifier_Name', 'R', 'CHANGE', 'TRUE')
    JSTF[('Identifier_Name', 'else', 'TRU')] = ('Identifier_Name', 'L', 'POP', '')
    for char in WHITESPACES:
        JSTF[('Identifier_Name', char, 'TRUE')] = ('True_Keyword', 'R', 'POP', '')
    for char in LINEBREAKS:
        JSTF[('Identifier_Name', char, 'TRUE')] = ('True_Keyword', 'R', 'POP', '')
    JSTF[('Identifier_Name', 'else', 'TRUE')] = ('Identifier_Name', 'L', 'POP', '')
    for char in Identifier_List:
        JSTF[('True_Keyword', 'else', char)] = ('After_Identifier', 'L', 'CHANGE', char[2:])
    JSTF[('Identifier_Or_Function', 'else', '$I')] = ('Identifier_Or_Function', 'L', 'POP', '')
    JSTF[('Identifier_Name', 'else', '$I')] = ('Identifier_Name', 'L', 'POP', '')
    # 'Syntax_Error'
    JSTF[('Syntax_Error', 'else', 'any')] = ('Syntax_Error', 'R', 'READ', '')
    JSTF[('Syntax_Error', '<', 'any')] = ('Tag_open_JS', 'L', 'READ', '')
    JSTF[('Tag_open_JS', '<', 'any')] = ('Transition_Back_To_HTML_Syntax', 'L', 'READ', '')
    ###Loops
    JSTF[('After_Identifier', '}', 'any')] = ('Check_For_End_Of_Block', 'L', 'READ', '')
    JSTF[('After_Assignment', '/', 'FUN($I')] = ('RegularExpressionLiteralFunction', 'L', 'CHANGE', 'FUN(')
    JSTF[('Wait_For_Assignment', '/', 'FUN($I')] = ('RegularExpressionLiteralFunction', 'L', 'CHANGE', 'FUN(')
    JSTF[('RegularExpressionLiteralFunction', '/', 'FUN(')] = ('RegularExpressionLiteral', 'R', 'PUSH', 'REL//')
    JSTF[('After_Assignment', 'else', 'FUN($I')] = ('After_Assignment', 'L', 'CHANGE', 'FUN(')
    JSTF[('Wait_For_Assignment', 'else', 'FUN($I')] = ('Wait_For_Assignment', 'L', 'CHANGE', 'FUN(')
    # html comment
    JSTF[('Wait_For_Assignment', '<', 'any')] = ('Tag_Skip', 'R', 'PUSH', '<')
    JSTF[('Tag_Skip', '!', '<')] = ('Tag_Skip', 'R', 'CHANGE', '<!')
    JSTF[('Tag_Skip', '-', '<!')] = ('Tag_Skip', 'R', 'CHANGE', '<!-')
    JSTF[('Tag_Skip', 'else', '<!')] = ('Syntax_Error', 'R', 'POP', '<!')
    JSTF[('Tag_Skip', '-', '<!-')] = ('Single_Line_Comment', 'R', 'POP', '<!-')
    JSTF[('Tag_Skip', 'else', '<!-')] = ('Syntax_Error', 'R', 'POP', '<!-')
    # comments
    JSTF[('MultiplicativeExpression1', '/', 'any')] = ('Single_Line_Comment', 'R', 'READ', '')
    # After_Comment
    JSTF[('After_Comment', 'else', '=')] = ('Wait_For_Assignment', 'L', 'READ', '')
    JSTF[('After_Comment', 'else', 'IF()ELSE')] = ('Specify_Assignment_Type', 'L', 'READ', '')
    # needs more work
    JSTF[('After_Comment', 'else', 'any')] = ('Specify_Assignment_Type', 'L', 'READ', '')
    #   *********************************  Single_Line_Comment State Rules    *****************************************
    JSTF[('Single_Line_Comment', '<', 'any')] = ('Single_Line_Comment', 'R', 'PUSH', '<')
    JSTF[('Single_Line_Comment', chr(47), '<')] = ('Single_Line_Comment', 'R', 'CHANGE', '</')
    JSTF[('Single_Line_Comment', 'else', '<')] = ('Single_Line_Comment', 'L', 'POP', '')
    JSTF[('Single_Line_Comment', 's', '</')] = ('Single_Line_Comment', 'R', 'CHANGE', 'S')
    JSTF[('Single_Line_Comment', 'S', '</')] = ('Single_Line_Comment', 'R', 'CHANGE', 'S')
    JSTF[('Single_Line_Comment', 'else', '</')] = ('Single_Line_Comment', 'L', 'POP', '')
    JSTF[('Single_Line_Comment', 'c', 'S')] = ('Single_Line_Comment', 'R', 'CHANGE', 'SC')
    JSTF[('Single_Line_Comment', 'C', 'S')] = ('Single_Line_Comment', 'R', 'CHANGE', 'SC')
    JSTF[('Single_Line_Comment', 'else', 'S')] = ('Single_Line_Comment', 'L', 'POP', '')
    JSTF[('Single_Line_Comment', 'r', 'SC')] = ('Single_Line_Comment', 'R', 'CHANGE', 'SCR')
    JSTF[('Single_Line_Comment', 'R', 'SC')] = ('Single_Line_Comment', 'R', 'CHANGE', 'SCR')
    JSTF[('Single_Line_Comment', 'else', 'SC')] = ('Single_Line_Comment', 'L', 'POP', '')
    JSTF[('Single_Line_Comment', 'i', 'SCR')] = ('Single_Line_Comment', 'R', 'CHANGE', 'SCRI')
    JSTF[('Single_Line_Comment', 'I', 'SCR')] = ('Single_Line_Comment', 'R', 'CHANGE', 'SCRI')
    JSTF[('Single_Line_Comment', 'else', 'SCR')] = ('Single_Line_Comment', 'L', 'POP', '')
    JSTF[('Single_Line_Comment', 'p', 'SCRI')] = ('Single_Line_Comment', 'R', 'CHANGE', 'SCRIP')
    JSTF[('Single_Line_Comment', 'P', 'SCRI')] = ('Single_Line_Comment', 'R', 'CHANGE', 'SCRIP')
    JSTF[('Single_Line_Comment', 'else', 'SCRI')] = ('Single_Line_Comment', 'L', 'POP', '')
    JSTF[('Single_Line_Comment', 't', 'SCRIP')] = ('Single_Line_Comment', 'R', 'CHANGE', 'SCRIPT')
    JSTF[('Single_Line_Comment', 'T', 'SCRIP')] = ('Single_Line_Comment', 'R', 'CHANGE', 'SCRIPT')
    JSTF[('Single_Line_Comment', 'else', 'SCRIP')] = ('Single_Line_Comment', 'L', 'POP', '')
    JSTF[('Single_Line_Comment', '>', 'SCRIPT')] = ('Transition_Back_To_HTML', 'R', 'POP', 'SCRIPT')
    JSTF[('Single_Line_Comment', 'else', 'SCRIPT')] = ('Single_Line_Comment', 'L', 'POP', '')
    JSTF[('IN_ASI', 'else', 'any')] = ('ASI', 'L', 'READ', '')
    JSTF[('RegularExpressionBackslashSequence', '+', 'any')] = ('RegularExpressionLiteral', 'R', 'READ', '')
    JSTF[('RegularExpressionLiteral', '\\', 'RELC')] = ('RegularExpressionBackslashSequence', 'R', 'READ', '')
    JSTF[('Wait_For_Assignment', '>', '--S')] = ('After_Assignment', 'R', 'POP', '')
    JSTF[('ObjectLiteral', '/', '{{')] = ('Wait_For_Assignment', 'L', 'CHANGE', '{')
    JSTF[('ObjectLiteral', 'else', 'any')] = ('Wait_For_Assignment', 'L', 'READ', '')
    JSTF[('Wait_For_Assignment', 'f', 'FUN(')] = ('Identifier_Or_Function', 'R', 'PUSH', 'F')
    JSTF[('Wait_For_Assignment', 'F', 'FUN(')] = ('Identifier_Or_Function', 'R', 'PUSH', 'F')
    JSTF[('Identifier_Or_Function', '(', 'any')] = ('Wait_For_Assignment', 'R', 'PUSH', 'FUN($I')
    JSTF[('RegularExpressionBackslashSequence', 'else', 'any')] = ('RegularExpressionLiteral', 'R', 'READ', '')
