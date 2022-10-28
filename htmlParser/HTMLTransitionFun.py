



class HTMLTransitionFun():
    EOF = chr(0)
    ASCII_upper = list()
    for i in range(65, 90):
        ASCII_upper.append(chr(i))
    ASCII_lower = list()
    for i in range(97, 122):
        ASCII_lower.append(chr(i))

    ASCII_alpha = ASCII_upper + ASCII_lower
    Digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    states = {'Data', 'Character_Reference', 'Tag_open', 'Markup_declaration_open', 'End_tag_open',
              'Tag_name',
              'Bogus_comment', 'Before_attribute_name', 'After_attribute_name', 'Attribute_name',
              'Before_attribute_value',
              'Self_closing_start_tag', 'Attribute_value_double_quoted', 'Attribute_value_single_quoted',
              'Attribute_value_unquoted', 'After_attribute_value_quoted', 'Comment_start', 'Comment_start_dash',
              'Comment',
              'Comment_end', 'Comment_end_dash', 'Comment_end_bang'
              }
    ASCII_Alphanumeric = ASCII_alpha + Digits
    tf = dict()
    ## 12.2.5.1 Data State
    tf[('Data', '&', 'any')] = ('Data', 'R', 'READ', '')
    tf[('Data', '<', 'any')] = ('Tag_open', 'R', 'PUSH', '<')
    tf[('Data', chr(0), 'any')] = ('Data', 'R', 'READ', '')  ## PARSE ERROR
    tf[('Data', EOF, 'any')] = ('Data', 'R', 'READ', '')
    tf[('Data', 'else', 'any')] = ('Data', 'R', 'READ', '')
    ## 12.2.5.6 Tag_open
    tf[('Tag_open', '!', 'any')] = ('Markup_declaration_open', 'R', 'READ', '')
    tf[('Tag_open', '/', 'any')] = ('End_tag_open', 'R', 'PUSH', 'ETO')
    for ascii in ASCII_alpha:
        tf[('Tag_open', ascii, 'any')] = ('Tag_name', 'L', 'PUSH', 'FTN')
    tf[('Tag_open', '?', 'any')] = (
        'Bogus_comment', 'L', 'POP', '<')  ## PARSE ERROR - unexpected-question-mark-instead-of-tag-name
    tf[('Tag_open', EOF, 'any')] = ('Tag_open', 'R', 'POP', '<')  ## PARSE ERROR - eof-before-tag-name
    tf[('Tag_open', 'else', 'any')] = ('Data', 'L', 'READ', '')  ## PARSE ERROR - invalid-first-character-of-tag-name
    ## 12.2.5.7 End_tag_open
    # detect script and style tag
    for ascii in ASCII_alpha:
        tf[('End_tag_open', ascii, 'any')] = ('Tag_name', 'L', 'READ', '')
    tf[('End_tag_open', 's', 'ETO')] = ('Tag_name', 'R', 'POP', '')
    tf[('End_tag_open', 'S', 'ETO')] = ('Tag_name', 'R', 'POP', '')
    tf[('End_tag_open', 'else', 'ETO')] = ('End_tag_open', 'L', 'POP', '')

    tf[('End_tag_open', '>', 'any')] = ('Data', 'R', 'READ', '')  ## PARSE ERROR
    tf[('End_tag_open', '>', '<')] = ('Data', 'R', 'POP', '<')  ## PARSE ERROR
    # check for css or javascript syntax in style or script tag
    tf[('End_tag_open', '>', 'SCRIPT')] = ('Transition_To_JS', 'L', 'POP', 'SCRIPT')
    tf[('End_tag_open', '>', 'STYLE')] = ('Transition_To_CSS', 'L', 'POP', 'STYLE')
    tf[('End_tag_open', EOF, 'any')] = ('Data', 'R', 'POP', '<')  ## PARSE ERROR  - eof-before-tag-name
    tf[('End_tag_open', 'else', 'any')] = (
        'Bogus_comment', 'L', 'POP', '<')  ## PARSE ERROR - invalid-first-character-of-tag-name
    ## 12.2.5.8 Tag_name
    tf[('Tag_name', chr(9), 'any')] = ('Before_attribute_name', 'R', 'READ', '')
    tf[('Tag_name', chr(10), 'any')] = ('Before_attribute_name', 'R', 'READ', '')
    tf[('Tag_name', chr(12), 'any')] = ('Before_attribute_name', 'R', 'READ', '')
    tf[('Tag_name', chr(32), 'any')] = ('Before_attribute_name', 'R', 'READ', '')
    tf[('Tag_name', '/', 'any')] = ('Self_closing_start_tag', 'R', 'READ', '')
    tf[('Tag_name', '>', 'any')] = ('Data', 'R', 'READ', '')
    tf[('Tag_name', '>', '<')] = ('Data', 'R', 'POP', '<')
    # detect script and style tags
    tf[('Tag_name', 'else', 'FTN')] = ('Tag_name', 'L', 'POP', '')
    tf[('Tag_open', 's', 'any')] = ('Tag_name', 'R', 'PUSH', 'S')
    tf[('Tag_open', 'S', 'any')] = ('Tag_name', 'R', 'PUSH', 'S')
    tf[('Tag_name', 's', 'FTN')] = ('Tag_name', 'R', 'PUSH', 'S')
    tf[('Tag_name', 'S', 'FTN')] = ('Tag_name', 'R', 'PUSH', 'S')
    tf[('Tag_name', 'c', 'S')] = ('Tag_name', 'R', 'CHANGE', 'SC')
    tf[('Tag_name', 'C', 'S')] = ('Tag_name', 'R', 'CHANGE', 'SC')
    tf[('Tag_name', 't', 'S')] = ('Tag_name', 'R', 'CHANGE', 'ST')
    tf[('Tag_name', 'T', 'S')] = ('Tag_name', 'R', 'CHANGE', 'ST')
    tf[('Tag_name', 'else', 'S')] = ('Tag_name', 'L', 'POP', '')
    tf[('Tag_name', 'r', 'SC')] = ('Tag_name', 'R', 'CHANGE', 'SCR')
    tf[('Tag_name', 'R', 'SC')] = ('Tag_name', 'R', 'CHANGE', 'SCR')
    tf[('Tag_name', 'else', 'SC')] = ('Tag_name', 'L', 'POP', '')
    tf[('Tag_name', 'y', 'ST')] = ('Tag_name', 'R', 'CHANGE', 'STY')
    tf[('Tag_name', 'Y', 'ST')] = ('Tag_name', 'R', 'CHANGE', 'STY')
    tf[('Tag_name', 'else', 'ST')] = ('Tag_name', 'L', 'POP', '')
    tf[('Tag_name', 'i', 'SCR')] = ('Tag_name', 'R', 'CHANGE', 'SCRI')
    tf[('Tag_name', 'I', 'SCR')] = ('Tag_name', 'R', 'CHANGE', 'SCRI')
    tf[('Tag_name', 'else', 'SCR')] = ('Tag_name', 'L', 'POP', '')
    tf[('Tag_name', 'l', 'STY')] = ('Tag_name', 'R', 'CHANGE', 'STYL')
    tf[('Tag_name', 'L', 'STY')] = ('Tag_name', 'R', 'CHANGE', 'STYL')
    tf[('Tag_name', 'else', 'STY')] = ('Tag_name', 'L', 'POP', '')
    tf[('Tag_name', 'p', 'SCRI')] = ('Tag_name', 'R', 'CHANGE', 'SCRIP')
    tf[('Tag_name', 'P', 'SCRI')] = ('Tag_name', 'R', 'CHANGE', 'SCRIP')
    tf[('Tag_name', 'else', 'SCRI')] = ('Tag_name', 'L', 'POP', '')
    tf[('Tag_name', 'e', 'STYL')] = ('Tag_name', 'R', 'CHANGE', 'STYLE')
    tf[('Tag_name', 'E', 'STYL')] = ('Tag_name', 'R', 'CHANGE', 'STYLE')
    tf[('Tag_name', 'else', 'STYL')] = ('Tag_name', 'L', 'POP', '')
    tf[('Tag_name', 't', 'SCRIP')] = ('Tag_name', 'R', 'CHANGE', 'SCRIPT')
    tf[('Tag_name', 'T', 'SCRIP')] = ('Tag_name', 'R', 'CHANGE', 'SCRIPT')
    tf[('Tag_name', 'else', 'SCRIP')] = ('Tag_name', 'L', 'POP', '')
    # check for css or javascript syntax in style or script tag
    tf[('Tag_name', '>', 'SCRIPT')] = ('Transition_To_JS', 'L', 'POP', 'SCRIPT')
    tf[('Tag_name', '>', 'STYLE')] = ('Transition_To_CSS', 'L', 'POP', 'STYLE')
    for ascii in ASCII_alpha:
        tf[('Tag_name', ascii, 'any')] = ('Tag_name', 'R', 'READ', '')
    tf[('Tag_name', '', 'any')] = ('Tag_name', 'R', 'READ', '')  ## PARSE ERROR
    tf[('Tag_name', EOF, 'any')] = ('Tag_name', 'R', 'POP', '<')  ## PARSE ERROR - eof-in-tag
    tf[('Tag_name', 'else', 'any')] = ('Tag_name', 'R', 'READ', '')
    ## 12.2.5.32  Before_attribute_name
    tf[('Before_attribute_name', chr(9), 'any')] = ('Before_attribute_name', 'R', 'READ', '')
    tf[('Before_attribute_name', chr(10), 'any')] = ('Before_attribute_name', 'R', 'READ', '')
    tf[('Before_attribute_name', chr(12), 'any')] = ('Before_attribute_name', 'R', 'READ', '')
    tf[('Before_attribute_name', chr(32), 'any')] = ('Before_attribute_name', 'R', 'READ', '')
    tf[('Before_attribute_name', '/', 'any')] = ('After_attribute_name', 'L', 'READ', '')
    tf[('Before_attribute_name', '>', 'any')] = ('After_attribute_name', 'L', 'READ', '')
    tf[('Before_attribute_name', EOF, 'any')] = ('After_attribute_name', 'L', 'READ', '')
    tf[('Before_attribute_name', '=', 'any')] = (
        'Attribute_name', 'R', 'READ', '')  ## PARSE ERROR -  unexpected-equals-sign-before-attribute-name
    tf[('Before_attribute_name', 'else', 'any')] = ('Attribute_name', 'L', 'READ', '')
    ## 12.2.5.33    Attribute_name
    tf[('Attribute_name', chr(9), 'any')] = ('After_attribute_name', 'L', 'READ', '')
    tf[('Attribute_name', chr(10), 'any')] = ('After_attribute_name', 'L', 'READ', '')
    tf[('Attribute_name', chr(12), 'any')] = ('After_attribute_name', 'L', 'READ', '')
    tf[('Attribute_name', chr(32), 'any')] = ('After_attribute_name', 'L', 'READ', '')
    tf[('Attribute_name', '/', 'any')] = ('After_attribute_name', 'L', 'READ', '')
    tf[('Attribute_name', '>', 'any')] = ('After_attribute_name', 'L', 'READ', '')
    tf[('Attribute_name', EOF, 'any')] = ('After_attribute_name', 'L', 'READ', '')
    tf[('Attribute_name', '=', 'any')] = ('Before_attribute_value', 'R', 'READ', '')
    for ascii in ASCII_upper:
        tf[('Attribute_name', ascii, 'any')] = ('Attribute_name', 'R', 'READ', '')
    tf[('Attribute_name', '', 'any')] = ('Attribute_name', 'R', 'READ', '')  ### PARSE ERROR - unexpected-null-character
    tf[('Attribute_name', chr(34), 'any')] = ('Attribute_name', 'R', 'READ', '')  ### PARSE ERROR - unexpected-character-in-attribute-name
    tf[('Attribute_name', chr(39), 'any')] = ('Attribute_name', 'R', 'READ', '')  ### PARSE ERROR - unexpected-character-in-attribute-name
    tf[('Attribute_name', '<', 'any')] = ('Attribute_name', 'R', 'READ', '')  ### PARSE ERROR - unexpected-character-in-attribute-name
    tf[('Attribute_name', 'else', 'any')] = ('Attribute_name', 'R', 'READ', '')
    ## 12.2.5.34    After_attribute_name
    tf[('After_attribute_name', chr(9), 'any')] = ('After_attribute_name', 'R', 'READ', '')
    tf[('After_attribute_name', chr(10), 'any')] = ('After_attribute_name', 'R', 'READ', '')
    tf[('After_attribute_name', chr(12), 'any')] = ('After_attribute_name', 'R', 'READ', '')
    tf[('After_attribute_name', chr(32), 'any')] = ('After_attribute_name', 'R', 'READ', '')
    tf[('After_attribute_name', '/', 'any')] = ('Self_closing_start_tag', 'R', 'READ', '')
    tf[('After_attribute_name', '>', 'any')] = ('Data', 'R', 'READ', '')
    tf[('After_attribute_name', '>', '<')] = ('Data', 'R', 'POP', '<')
    # check for css or javascript syntax in style or script tag
    tf[('After_attribute_name', '>', 'SCRIPT')] = ('Transition_To_JS', 'L', 'POP', 'SCRIPT')
    tf[('After_attribute_name', '>', 'STYLE')] = ('Transition_To_CSS', 'L', 'POP', 'STYLE')
    tf[('After_attribute_name', EOF, 'any')] = ('After_attribute_name', 'R', 'READ', '')  ## PARSE ERROR
    tf[('After_attribute_name', EOF, '<')] = (
        'After_attribute_name', 'R', 'POP', '<')  ## PARSE ERROR - EOF is unexpected and we would ignore the whole tag
    tf[('After_attribute_name', '=', 'any')] = ('Before_attribute_value', 'R', 'READ', '')
    tf[('After_attribute_name', 'else', 'any')] = ('Attribute_name', 'L', 'READ', '')
    ## 12.2.5.35    Before_attribute_value
    tf[('Before_attribute_value', chr(9), 'any')] = ('Before_attribute_value', 'R', 'READ', '')
    tf[('Before_attribute_value', chr(10), 'any')] = ('Before_attribute_value', 'R', 'READ', '')
    tf[('Before_attribute_value', chr(12), 'any')] = ('Before_attribute_value', 'R', 'READ', '')
    tf[('Before_attribute_value', chr(32), 'any')] = ('Before_attribute_value', 'R', 'READ', '')
    tf[('Before_attribute_value', chr(34), 'any')] = ('Attribute_value_double_quoted', 'R', 'READ', '')
    tf[('Before_attribute_value', chr(39), 'any')] = ('Attribute_value_single_quoted', 'R', 'READ', '')
    tf[('Before_attribute_value', '>', 'any')] = ('Data', 'L', 'READ', '')  ##  PARSE ERROR
    tf[('Before_attribute_value', '>', '<')] = ('Data', 'L', 'POP', '<')  ##  PARSE ERROR
    # check for css or javascript syntax in style or script tag
    tf[('Before_attribute_value', '>', 'SCRIPT')] = ('Transition_To_JS', 'L', 'POP', 'SCRIPT')
    tf[('Before_attribute_value', '>', 'STYLE')] = ('Transition_To_CSS', 'L', 'POP', 'STYLE')
    tf[('Before_attribute_value', 'else', 'any')] = ('Attribute_value_unquoted', 'L', 'READ', '')
    ## 12.2.5.36   Attribute_value_double_quoted
    tf[('Attribute_value_double_quoted', chr(34), 'any')] = ('After_attribute_value_quoted', 'R', 'READ', '')
    tf[('Attribute_value_double_quoted', '&', 'any')] = ('Attribute_value_double_quoted', 'R', 'READ', '')
    tf[('Attribute_value_double_quoted', '', 'any')] = ('Attribute_value_double_quoted', 'R', 'READ', '')  ##  PARSE ERROR - unexpected-null-character
    tf[('Attribute_value_double_quoted', EOF, 'any')] = ('Attribute_value_double_quoted', 'R', 'READ', '')  ##  PARSE ERROR
    tf[('Attribute_value_double_quoted', EOF, '<')] = ('Attribute_value_double_quoted', 'R', 'POP', '<')  ##  PARSE ERROR
    tf[('Attribute_value_double_quoted', 'else', 'any')] = ('Attribute_value_double_quoted', 'R', 'READ', '')
    ## 12.2.5.37   Attribute_value_single_quoted
    tf[('Attribute_value_single_quoted', chr(39), 'any')] = ('After_attribute_value_quoted', 'R', 'READ', '')
    tf[('Attribute_value_single_quoted', '&', 'any')] = (
        'Attribute_value_single_quoted', 'R', 'READ', '')
    tf[('Attribute_value_single_quoted', '', 'any')] = (
        'Attribute_value_single_quoted', 'R', 'READ', '')  ##  PARSE ERROR - unexpected-null-character
    tf[('Attribute_value_single_quoted', EOF, 'any')] = (
        'Attribute_value_single_quoted', 'R', 'READ', '')  ##  PARSE ERROR
    tf[('Attribute_value_single_quoted', EOF, '<')] = (
        'Attribute_value_single_quoted', 'R', 'POP', '<')  ##  PARSE ERROR
    tf[('Attribute_value_single_quoted', 'else', 'any')] = ('Attribute_value_single_quoted', 'R', 'READ', '')
    ## 12.2.4.38   Attribute_value_unquoted
    tf[('Attribute_value_unquoted', chr(9), 'any')] = ('Before_attribute_name', 'R', 'READ', '')
    tf[('Attribute_value_unquoted', chr(10), 'any')] = ('Before_attribute_name', 'R', 'READ', '')
    tf[('Attribute_value_unquoted', chr(12), 'any')] = ('Before_attribute_name', 'R', 'READ', '')
    tf[('Attribute_value_unquoted', chr(32), 'any')] = ('Before_attribute_name', 'R', 'READ', '')
    tf[('Attribute_value_unquoted', '&', 'any')] = (
        'Attribute_value_unquoted', 'R', 'PUSH', '&')  ### character reference
    ### character reference
    for char in ASCII_Alphanumeric:
        tf[('Attribute_value_unquoted', char, '&')] = (
            'Attribute_value_unquoted', 'R', 'READ', '')  ### character reference
    tf[('Attribute_value_unquoted', 'else', '&')] = (
        'Attribute_value_unquoted', 'R', 'READ', '')  ### character reference
    tf[('Attribute_value_unquoted', '>', 'any')] = ('Data', 'R', 'READ', '')
    tf[('Attribute_value_unquoted', '>', '<')] = ('Data', 'R', 'POP', '<')
    # check for css or javascript syntax in style or script tag
    tf[('Attribute_value_unquoted', '>', 'SCRIPT')] = ('Transition_To_JS', 'L', 'POP', 'SCRIPT')
    tf[('Attribute_value_unquoted', '>', 'STYLE')] = ('Transition_To_CSS', 'L', 'POP', 'STYLE')
    tf[('Attribute_value_unquoted', '', 'any')] = (
        'Attribute_value_unquoted', 'R', 'READ', '')  ### PARSE ERROR - unexpected-null-character
    tf[('Attribute_value_unquoted', EOF, 'any')] = (
        'Attribute_value_unquoted', 'R', 'READ', '')  ### PARSE ERROR
    tf[('Attribute_value_unquoted', EOF, '<')] = (
        'Attribute_value_unquoted', 'R', 'POP', '<')  ### PARSE ERROR
    tf[('Attribute_value_unquoted', '=', 'any')] = ('Attribute_value_unquoted', 'R', 'READ', '')  ### PARSE ERROR
    tf[('Attribute_value_unquoted', chr(34), 'any')] = ('Attribute_value_unquoted', 'R', 'READ', '')  ### PARSE ERROR
    tf[('Attribute_value_unquoted', chr(39), 'any')] = ('Attribute_value_unquoted', 'R', 'READ', '')  ### PARSE ERROR
    tf[('Attribute_value_unquoted', '<', 'any')] = ('Attribute_value_unquoted', 'R', 'READ', '')  ### PARSE ERROR
    tf[('Attribute_value_unquoted', '`', 'any')] = ('Attribute_value_unquoted', 'R', 'READ', '')  ### PARSE ERROR
    tf[('Attribute_value_unquoted', 'else', 'any')] = ('Attribute_value_unquoted', 'R', 'READ', '')
    ## 12.2.5.39    After_attribute_value_quoted
    tf[('After_attribute_value_quoted', chr(9), 'any')] = ('Before_attribute_name', 'R', 'READ', '')
    tf[('After_attribute_value_quoted', chr(10), 'any')] = ('Before_attribute_name', 'R', 'READ', '')
    tf[('After_attribute_value_quoted', chr(12), 'any')] = ('Before_attribute_name', 'R', 'READ', '')
    tf[('After_attribute_value_quoted', chr(32), 'any')] = ('Before_attribute_name', 'R', 'READ', '')
    tf[('After_attribute_value_quoted', '/', 'any')] = ('Self_closing_start_tag', 'R', 'READ', '')
    tf[('After_attribute_value_quoted', '>', 'any')] = ('Data', 'R', 'READ', '')
    tf[('After_attribute_value_quoted', '>', '<')] = ('Data', 'R', 'POP', '<')
    # check for css or javascript syntax in style or script tag
    tf[('After_attribute_value_quoted', '>', 'SCRIPT')] = ('Transition_To_JS', 'L', 'POP', 'SCRIPT')
    tf[('After_attribute_value_quoted', '>', 'STYLE')] = ('Transition_To_CSS', 'L', 'POP', 'STYLE')
    tf[('After_attribute_value_quoted', EOF, 'any')] = ('After_attribute_value_quoted', 'R', 'READ', '')  ## PARSE ERROR
    tf[('After_attribute_value_quoted', EOF, '<')] = ('After_attribute_value_quoted', 'R', 'POP', '<')  ### PARSE ERROR
    tf[('After_attribute_value_quoted', 'else', 'any')] = ('Before_attribute_name', 'L', 'READ', '')  ## PARSE ERROR - missing-whitespace-between-attributes
    ## 12.2.5.40   Self_closing_start_tag
    tf[('Self_closing_start_tag', '>', 'any')] = ('Data', 'R', 'READ', '')
    tf[('Self_closing_start_tag', '>', '<')] = ('Data', 'R', 'POP', '<')
    tf[('Self_closing_start_tag', EOF, 'any')] = ('Self_closing_start_tag', 'R', 'READ', '')  ## PARSE ERROR
    tf[('Self_closing_start_tag', EOF, '<')] = ('Self_closing_start_tag', 'R', 'POP', '<')  ## PARSE ERROR
    tf[('Self_closing_start_tag', 'else', 'any')] = ('Before_attribute_name', 'L', 'READ', '')  ## PARSE ERROR - unexpected-solidus-in-tag
    ## 12.2.5.41   Bogus_comment state
    tf[('Bogus_comment', '>', 'any')] = ('Data', 'R', 'READ', '')
    tf[('Bogus_comment', EOF, 'any')] = ('Bogus_comment', 'R', 'READ', '')
    tf[('Bogus_comment', '', 'any')] = ('Bogus_comment', 'R', 'READ', '')  ## PARSE ERROR
    tf[('Bogus_comment', 'else', 'any')] = ('Bogus_comment', 'R', 'READ', '')
    ## 8.2.5.42 Markup_declaration_open
    tf[('Markup_declaration_open', '-', 'any')] = (
        'Markup_declaration_open_temp', 'R', 'READ', '')  ### detect two adjacent dashes
    tf[('Markup_declaration_open_temp', '-', 'any')] = ('Comment_start', 'R', 'READ', '')  ### detect two adjacent dashes
    tf[('Markup_declaration_open_temp', 'else', 'any')] = ('Bogus_comment', 'R', 'READ', '')  ### detect two adjacent dashes
    ## Add [CDATA[ processing
    tf[('Markup_declaration_open', 'else', 'any')] = ('Bogus_comment', 'R', 'READ', '')
    ## 8.2.5.43 Comment Start state
    tf[('Comment_start', '-', 'any')] = ('Comment_start_dash', 'R', 'READ', '')
    tf[('Comment_start', '>', 'any')] = ('Data', 'R', 'READ', '')
    tf[('Comment_start', '>', '<')] = ('Data', 'R', 'POP', '<')
    tf[('Comment_start', 'else', 'any')] = ('Comment', 'L', 'READ', '')
    ## 8.2.5.44 Comment Start dash state
    tf[('Comment_start_dash', '-', 'any')] = ('Comment', 'R', 'PUSH', 'CE')
    tf[('Comment_start_dash', '>', 'any')] = ('Data', 'R', 'READ', '')
    tf[('Comment_start_dash', '>', '<')] = ('Data', 'R', 'POP', '<')
    tf[('Comment_start_dash', EOF, 'any')] = ('Comment_start_dash', 'R', 'READ','')
    tf[('Comment_start_dash', EOF, '<')] = ('Comment_start_dash', 'R', 'POP','<')
    tf[('Comment_start_dash', 'else', 'any')] = ('Comment', 'L', 'READ', '')
    ## 8.2.5.45 Comment state
    tf[('Comment', '-', 'any')] = ('Comment', 'R', 'PUSH', 'CED')
    tf[('Comment', '', 'any')] = ('Comment', 'R', 'READ', '')  ## PARSE ERROR
    tf[('Comment', '<', 'any')] = ('Comment', 'R', 'PUSH', 'CLTS')
    tf[('Comment', EOF, 'any')] = ('Data', 'L', 'READ', '')
    tf[('Comment', EOF, '<')] = ('Data', 'L', 'POP', '<')
    tf[('Comment', 'else', 'any')] = ('Comment', 'R', 'READ', '')
    ## 8.2.5.46 Comment_less_than_sign
    tf[('Comment', '!', 'CLTS')] = ('Comment', 'R', 'CHANGE', 'CLTSB')
    tf[('Comment', '<', 'CLTS')] = ('Comment', 'R', 'READ', '')
    tf[('Comment', 'else', 'CLTS')] = ('Comment', 'L', 'POP', '')
    ## 8.2.5.47 Comment_less_than_sign_bang
    tf[('Comment', '-', 'CLTSB')] = ('Comment', 'R', 'CHANGE', 'CLTSBD')
    tf[('Comment', 'else', 'CLTSB')] = ('Comment', 'L', 'POP', '')
    ## 8.2.5.48 Comment_less_than_sign_bang_dash
    tf[('Comment', '-', 'CLTSBD')] = ('Comment', 'R', 'CHANGE', 'CLTSBDD')
    tf[('Comment', 'else', 'CLTSBD')] = ('Comment', 'L', 'CHANGE', 'CE')
    ## 8.2.5.49 Comment_less_than_sign_bang_dash_dash
    tf[('Comment', 'else', 'CLTSBDD')] = ('Comment', 'L', 'CHANGE', 'CE')
    ## 8.2.5.50 Comment end dash state
    tf[('Comment', '-', 'CED')] = ('Comment', 'R', 'CHANGE', 'CE')
    tf[('Comment', EOF, 'CED')] = (
        'Comment', 'R', 'POP', 'CED')
    tf[('Comment', 'else', 'CED')] = ('Comment', 'L', 'POP', 'CED')
    ## 8.2.5.51 Comment end state
    tf[('Comment', '>', 'CE')] = ('Comment', 'L', 'POP', 'CE')
    tf[('Comment', '>', '<')] = ('Data', 'R', 'POP', '')
    tf[('Comment', '>', 'any')] = ('Data', 'R', 'READ', '')
    tf[('Comment', '!', 'CE')] = ('Comment', 'R', 'CHANGE', 'CEB')  ## PARSE ERROR
    tf[('Comment', '-', 'CE')] = ('Comment', 'R', 'POP', '')  ## PARSE ERROR
    tf[('Comment', EOF, 'CE')] = ('Comment', 'R', 'POP', '')
    tf[('Comment', 'else', 'CE')] = ('Comment', 'L', 'POP', 'CE')
    tf[('Comment', 'else', 'CEB')] = ('Comment', 'L', 'POP', 'CEB')
    # Transition to new language
    tf[('Transition_To_JS', '>', '<')] = ('Transition_To_JS', 'R', 'CHANGE', '$$$')
    tf[('Transition_To_CSS', '>', '<')] = ('Transition_To_CSS', 'R', 'POP', '<')
    tf[('Transition_To_JS', '>', 'any')] = ('Transition_To_JS', 'R', 'READ', '')
    tf[('Transition_To_CSS', '>', 'any')] = ('Transition_To_CSS', 'R', 'READ', '')
    tf[('Transition_Back_To_HTML', 'else', 'any')] = ('Data', 'L', 'READ', '')
    tf[('Transition_Back_To_HTML_Syntax', 'else', 'any')] = ('Transition_To_CSS', 'L', 'READ', '')
    tf[('Syntax_Error', 'else', 'any')] = ('Syntax_Error', 'R', 'READ', '')
