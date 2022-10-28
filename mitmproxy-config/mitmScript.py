import mitmproxy
import sys
import time
import os



sys.path.insert(0, '../htmlParser')
import HTMLParser


parser = HTMLParser.HTMLParser()

state = {'req': '', 'res': ''}

def request(flow):
    state['req'] = flow.request.url

def response(flow):
    state['res'] = flow.response.content
    try:
        decoding_Type = flow.response.headers["Content-Type"]
    except:
        decoding_Type = ""
    URL = state['req']
    if (URL and "?" in URL):
        try:
            print('HTTP request with params for url: ' + str(URL) + '\n')
        except Exception as e:
            print(e)
        if ('html' in decoding_Type and state['res']):
            if (('utf-8' in decoding_Type or 'UTF-8' in decoding_Type)):
                html = state['res'].decode(encoding='utf-8', errors='ignore')
            else:
                html = ''
        else:
            html = ''
        queries = URL.split("?")
        paramsList = dict()
        params = dict()
        result = ''
        if (len(html) > 1 and len(queries) > 1):
            paramsList = queries[1].split('&')
            for p in paramsList:
                pkeyvalue = p.split('=')
                if (len(pkeyvalue) > 1 and len(pkeyvalue[1]) > 2):
                    params[pkeyvalue[0]] = pkeyvalue[1]
                else:
                    params[pkeyvalue[0]] = 'NULLSTRING'
            try:
                result = parser.findXSSAttackOneReq(html, params, state)
            except (KeyError, ValueError, IndexError) as e:
                result = ''
                print("Error occured here HTML is: \n")
                print(e)
                pass
            r = ''
            if (result != ''):
                r += ("Found Context Injection URL : " + URL)
                flow.response.headers["Context-Auditor"] = "Analysis Results: " + r
                flow.response.status_code = 404
                print(result)
                flow.response.content = str("\n\nBlocked By Context-Auditor").encode("utf8")
