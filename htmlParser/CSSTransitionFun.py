



class CSSTransitionFun():
    cssStates = {'CSS_Start'
                 }  # we will complete it by code
    WHITESPACES = [' ', '\t']
    LINEBREAKS = ['\n', '\r', '\f', '\r\n']
    EOF = chr(0)
    ASCII_upper = list()
    for i in range(65, 91):
        ASCII_upper.append(chr(i))

    ASCII_lower = list()
    for i in range(97, 123):
        ASCII_lower.append(chr(i))

    ASCII_alpha = ASCII_upper + ASCII_lower
    Digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    CSS_Alpha_Digits = ASCII_alpha + Digits
    CSSTF = dict()
    # *********************************  CSS_Start State Rules    *******************************
    for char in WHITESPACES:
        CSSTF[('CSS_Start', char, '$$$')] = ('CSS_Start', 'R', 'READ', '')
    for char in LINEBREAKS:
        CSSTF[('CSS_Start', char, '$$$')] = ('CSS_Start', 'R', 'READ', '')
    CSSTF[('CSS_Start', 'else', '$$$')] = ('Component_Value', 'L', 'READ', '')
    # *********************************  Component_Value State Rules    *************************
    CSSTF[('Component_Value', '\\', 'any')] = ('BackSlash_Processing', 'R', 'READ', '')
    for char in ASCII_alpha:
        CSSTF[('Component_Value', char, 'any')] = ('Ident_Token', 'R', 'READ', '')
    CSSTF[('Component_Value', '-', 'any')] = ('Ident_Token', 'R', 'PUSH', '#')  ## also cover non ascii
    CSSTF[('Component_Value', '#', 'any')] = ('Ident_Token', 'R', 'READ', '')
    CSSTF[('Component_Value', "'", 'any')] = ('Quote_String_Token', 'R', 'PUSH', "'")
    CSSTF[('Component_Value', '"', 'any')] = ('Double_Quote_String_Token', 'R', 'PUSH', '"')
    CSSTF[('Component_Value', '+', 'any')] = ('Number_Token', 'R', 'READ', '')
    CSSTF[('Component_Value', '-', 'any')] = ('Number_Token', 'R', 'READ', '')
    CSSTF[('Component_Value', '@', 'any')] = ('Wait_For_At_Ident_Token', 'R', 'READ', '')
    CSSTF[('Component_Value', '/', 'any')] = ('Wait_For_Comment', 'R', 'READ', '')
    for char in Digits:
        CSSTF[('Component_Value', char, 'any')] = ('Number_Token', 'R', 'READ', '')
    ## Blocks
    CSSTF[('Component_Value', '(', 'any')] = ('Block', 'L', 'PUSH', '(')
    CSSTF[('Component_Value', '{', 'any')] = ('Block', 'L', 'PUSH', '{')
    CSSTF[('Component_Value', '[', 'any')] = ('Block', 'L', 'PUSH', '[')
    CSSTF[('Component_Value', ')', '(')] = ('Block', 'L', 'POP', '(')
    CSSTF[('Component_Value', '}', '{')] = ('Block', 'L', 'POP', '{')
    CSSTF[('Component_Value', ']', '[')] = ('Block', 'L', 'POP', '[')
    CSSTF[('Component_Value', ':', 'any')] = ('Colon_Token', 'L', 'READ', '')
    CSSTF[('Component_Value', ';', 'any')] = ('Semicolon_Token', 'L', 'READ', '')
    ## Any other kind of unexpected tokens
    CSSTF[('Component_Value', 'else', 'any')] = ('Component_Value', 'R', 'READ', '')
    CSSTF[('Component_Value', '<', 'any')] = ('CSS_Tag_Skip', 'R', 'PUSH', '<')
    # *********************************  Wait_For_Comment State Rules    *********************
    CSSTF[('Wait_For_Comment', '*', 'any')] = ('Comment_Token', 'R', 'READ', '')
    CSSTF[('Wait_For_Comment', 'else', 'any')] = ('Return_State', 'L', 'READ', '')
    # *********************************  Comment_Token State Rules    *************************
    CSSTF[('Comment_Token', '*', 'any')] = ('Wait_For_Comment_End', 'R', 'READ', '')
    CSSTF[('Comment_Token', 'else', 'any')] = ('Comment_Token', 'R', 'READ', '')
    # *********************************  Wait_For_Comment_End State Rules    ******************
    CSSTF[('Wait_For_Comment_End', '/', 'any')] = ('Component_Value', 'R', 'READ', '')
    CSSTF[('Wait_For_Comment_End', 'else', 'any')] = ('Comment_Token', 'R', 'READ', '')
    # *********************************  Wait_For_At_Ident_Token State Rules    ****************
    CSSTF[('Wait_For_At_Ident_Token', '-', 'any')] = ('At_Keyword_Token', 'R', 'READ', '')
    CSSTF[('Wait_For_At_Ident_Token', '_', 'any')] = ('At_Keyword_Token', 'R', 'READ', '')
    for char in CSS_Alpha_Digits:
        CSSTF[('Wait_For_At_Ident_Token', char, 'any')] = ('At_Keyword_Token', 'R', 'READ', '')
    CSSTF[('Wait_For_At_Ident_Token', 'else', 'any')] = ('Return_State', 'L', 'READ', '')
    # *********************************  At_Keyword_Token State Rules    ************************
    CSSTF[('At_Keyword_Token', '-', 'any')] = ('At_Keyword_Token', 'R', 'READ', '')
    CSSTF[('At_Keyword_Token', '_', 'any')] = ('At_Keyword_Token', 'R', 'READ', '')
    for char in CSS_Alpha_Digits:
        CSSTF[('At_Keyword_Token', char, 'any')] = ('At_Keyword_Token', 'R', 'READ', '')
    CSSTF[('At_Keyword_Token', 'else', 'any')] = ('Return_State', 'L', 'READ', '')
    # *********************************  Number_Token State Rules    ******************************
    CSSTF[('Number_Token', '.', 'any')] = ('Number_Token_Dotted', 'R', 'READ', '')
    for char in Digits:
        CSSTF[('Number_Token', char, 'any')] = ('Number_Token', 'R', 'READ', '')
    for char in ASCII_alpha:
        CSSTF[('Number_Token', char, 'any')] = ('Ident_Token', 'R', 'READ', '')
    CSSTF[('Number_Token', '-', 'any')] = ('Ident_Token', 'R', 'READ', '')
    CSSTF[('Number_Token', '_', 'any')] = ('Ident_Token', 'R', 'READ', '')
    CSSTF[('Number_Token', 'e', 'any')] = ('Number_Token_Scientific_Pre', 'R', 'READ', '')
    CSSTF[('Number_Token', 'E', 'any')] = ('Number_Token_Scientific_Pre', 'R', 'READ', '')
    CSSTF[('Number_Token', 'else', 'any')] = ('Return_State', 'L', 'READ', '')
    # *********************************  Number_Token_Dotted State Rules    *************************
    for char in Digits:
        CSSTF[('Number_Token_Dotted', char, 'any')] = ('Number_Token_Dotted', 'R', 'READ', '')
    CSSTF[('Number_Token_Dotted', 'e', 'any')] = ('Number_Token_Scientific_Pre', 'R', 'READ', '')
    CSSTF[('Number_Token_Dotted', 'E', 'any')] = ('Number_Token_Scientific_Pre', 'R', 'READ', '')
    CSSTF[('Number_Token_Dotted', 'else', 'any')] = ('Return_State', 'L', 'READ', '')
    # *********************************  Number_Token_Scientific_Pre State Rules    ******************
    for char in Digits:
        CSSTF[('Number_Token_Scientific_Pre', char, 'any')] = ('Number_Token_Scientific', 'R', 'READ', '')
    CSSTF[('Number_Token_Scientific_Pre', '+', 'any')] = ('Number_Token_Scientific', 'R', 'READ', '')
    CSSTF[('Number_Token_Scientific_Pre', '-', 'any')] = ('Number_Token_Scientific', 'R', 'READ', '')
    CSSTF[('Number_Token_Scientific_Pre', 'else', 'any')] = ('Return_State', 'L', 'READ', '')
    # *********************************  Number_Token_Scientific_Pre State Rules    *******************
    for char in Digits:
        CSSTF[('Number_Token_Scientific', char, 'any')] = ('Number_Token_Scientific', 'R', 'READ', '')
    CSSTF[('Number_Token_Scientific', 'else', 'any')] = ('Return_State', 'L', 'READ', '')
    # *********************************  Double_Quote_String_Token State Rules *************************
    CSSTF[('Double_Quote_String_Token', "'", 'any')] = ('Quote_String_Token', 'R', 'PUSH', "'")
    CSSTF[('Double_Quote_String_Token', '"', '"')] = ('Return_State', 'R', 'POP', '"')
    CSSTF[('Double_Quote_String_Token', 'else', 'any')] = ('Double_Quote_String_Token', 'R', 'READ', '')
    # *********************************  Quote_String_Token State Rules    ******************************
    CSSTF[('Quote_String_Token', "'", "'")] = ('Return_State', 'R', 'POP', "'")
    CSSTF[('Quote_String_Token', '"', 'any')] = ('Double_Quote_String_Token', 'R', 'PUSH', '"')
    CSSTF[('Quote_String_Token', 'else', 'any')] = ('Quote_String_Token', 'R', 'READ', '')
    # *********************************  Hash_Token State Rules    ***************************************
    for char in CSS_Alpha_Digits:
        CSSTF[('Hash_Token', char, 'any')] = ('Hash_Token', 'R', 'READ', '')  ## also cover non-ascii
    CSSTF[('Hash_Token', 'else', 'any')] = ('Return_State', 'L', 'READ', '')
    # *********************************  Ident_Token State Rules    ***************************************
    CSSTF[('Ident_Token', 'else', '#')] = ('Hash_Token', 'L', 'POP', '')
    CSSTF[('Ident_Token', '-', 'any')] = ('Ident_Token', 'R', 'READ', '')
    CSSTF[('Ident_Token', '_', 'any')] = ('Ident_Token', 'R', 'READ', '')
    for char in CSS_Alpha_Digits:
        CSSTF[('Ident_Token', char, 'any')] = ('Ident_Token', 'R', 'READ', '')  ## also cover non-ascii
    CSSTF[('Ident_Token', 'else', 'any')] = ('Return_State', 'L', 'READ', '')
    # *********************************  Return_State State Rules    **************************************
    CSSTF[('Return_State', 'else', "'")] = ('Quote_String_Token', 'L', 'READ', '')
    CSSTF[('Return_State', 'else', '"')] = ('Double_Quote_String_Token', 'L', 'READ', '')
    CSSTF[('Return_State', 'else', 'any')] = ('Component_Value', 'L', 'READ', '')
    CSSTF[('Return_State', 'else', '$$$')] = ('CSS_Start', 'L', 'READ', '')
    # *********************************  Wait_For_Comment State Rules    ***********************************
    CSSTF[('BackSlash_Processing', 'n', 'any')] = ('Return_State', 'R', 'READ', '')
    CSSTF[('BackSlash_Processing', 'r', 'any')] = ('Return_State', 'R', 'READ', '')
    CSSTF[('BackSlash_Processing', 'f', 'any')] = ('Return_State', 'R', 'READ', '')
    CSSTF[('BackSlash_Processing', 't', 'any')] = ('Return_State', 'R', 'READ', '')
    # *********************************  Semicolon_Token State Rules    ************************************
    CSSTF[('Semicolon_Token', 'else', 'any')] = ('Return_State', 'R', 'READ', '')
    # *********************************  Colon_Token State Rules    ****************************************
    CSSTF[('Colon_Token', 'else', 'any')] = ('Return_State', 'R', 'READ', '')
    # *********************************  Block State Rules    **********************************************
    CSSTF[('Block', 'else', 'any')] = ('Return_State', 'R', 'READ', '')
    # *********************************  Wait_For_Comment State Rules    ***********************************
    CSSTF[('BackSlash_Processing', 'n', 'any')] = ('Return_State', 'R', 'READ', '')
    # *********************************  Single_Line_Comment State Rules    ********************************
    CSSTF[('CSS_Tag_Skip', chr(47), '<')] = ('CSS_Tag_Skip', 'R', 'CHANGE', '</')
    CSSTF[('CSS_Tag_Skip', 'else', '<')] = ('Component_Value', 'L', 'POP', '')
    CSSTF[('CSS_Tag_Skip', 'else', 'any')] = ('Component_Value', 'R', 'POP', '')
    CSSTF[('CSS_Tag_Skip', 's', '</')] = ('CSS_Tag_Skip', 'R', 'CHANGE', 'S')
    CSSTF[('CSS_Tag_Skip', 'S', '</')] = ('CSS_Tag_Skip', 'R', 'CHANGE', 'S')
    CSSTF[('CSS_Tag_Skip', 'else', '</')] = ('Tag_name_ccs', 'L', 'POP', '')
    CSSTF[('CSS_Tag_Skip', 't', 'S')] = ('CSS_Tag_Skip', 'R', 'CHANGE', 'ST')
    CSSTF[('CSS_Tag_Skip', 'T', 'S')] = ('CSS_Tag_Skip', 'R', 'CHANGE', 'ST')
    CSSTF[('CSS_Tag_Skip', 'else', 'S')] = ('Tag_name_ccs', 'L', 'POP', '')
    CSSTF[('CSS_Tag_Skip', 'y', 'ST')] = ('CSS_Tag_Skip', 'R', 'CHANGE', 'STY')
    CSSTF[('CSS_Tag_Skip', 'Y', 'ST')] = ('CSS_Tag_Skip', 'R', 'CHANGE', 'STY')
    CSSTF[('CSS_Tag_Skip', 'else', 'ST')] = ('Tag_name_ccs', 'L', 'POP', '')
    CSSTF[('CSS_Tag_Skip', 'l', 'STY')] = ('CSS_Tag_Skip', 'R', 'CHANGE', 'STYL')
    CSSTF[('CSS_Tag_Skip', 'L', 'STY')] = ('CSS_Tag_Skip', 'R', 'CHANGE', 'STYL')
    CSSTF[('CSS_Tag_Skip', 'else', 'STY')] = ('Tag_name_ccs', 'L', 'POP', '')
    CSSTF[('CSS_Tag_Skip', 'e', 'STYL')] = ('CSS_Tag_Skip', 'R', 'CHANGE', 'STYLE')
    CSSTF[('CSS_Tag_Skip', 'E', 'STYL')] = ('CSS_Tag_Skip', 'R', 'CHANGE', 'STYLE')
    CSSTF[('CSS_Tag_Skip', 'else', 'STYL')] = ('Tag_name_ccs', 'R', 'POP', '')
    CSSTF[('CSS_Tag_Skip', 'else', 'STYLE')] = ('Tag_name_ccs', 'R', 'POP', '')
    CSSTF[('CSS_Tag_Skip', '>', 'STYLE')] = ('Transition_Back_To_HTML', 'R', 'POP', 'STYLE')
    CSSTF[('CSS_Tag_Skip', 'else', 'STYLE')] = ('Tag_name_ccs', 'L', 'POP', '')
    CSSTF[('Tag_name_ccs', 'else', 'STYLE')] = ('Transition_Back_To_HTML_Syntax', 'L', 'READ', '')
    CSSTF[('Syntax_Error', 'else', 'any')] = ('Syntax_Error', 'R', 'READ', '')
