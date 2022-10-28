import ngx
import httplib

def access(r):
    r.log('access phase', ngx.LOG_INFO)
    # conn = httplib.HTTPConnection("127.0.0.1", 8182)
    # # r.ho['X-Out'] = s.recv(5000)
    # conn.request('GET', '/')
    # resp = conn.getresponse()
    # r.ho['X-Out'] = type(r)
    # r.ctx['resp'] = resp.read()
    # r.ctx['code'] = 200
    request_url=r.var["request"].split(" ")
	#url="http://127.0.0.1"+request_url+":8182"
	#resp = requestsline.get(url)
    conn = httplib.HTTPConnection("127.0.0.1", 8182)
    conn.request('GET', "http://127.0.0.1"+request_url[1])
    #conn.request('GET', "/")
    paramsList=dict()
    params=dict()
    queries =request_url[1].split("?")
    if(len(queries)>1):
        paramsList=queries[1].split('&')
        for p in paramsList:
               pkeyvalue=p.split('=')
               if(len(pkeyvalue)>1):
        	         params[pkeyvalue[0]]=pkeyvalue[1]
               else:
                   params[pkeyvalue[0]]='NULLSTRING'
    resp = conn.getresponse()
    #r.log('access phase', ngx.LOG_INFO)
    r.ctx['ACTresp'] = resp.read()
    r.ctx['ACTrespParams'] = params


def content(r):
    parser=HTMLParser()
    # r.ctx['resp'] = params[0]
    sol=parser.findXSSAttackOneReqNginx(r.ctx['ACTresp'],  r.ctx['ACTrespParams'])
    if(sol):
        r.ctx['code']=sol[0]
        r.ctx['resp']=sol[1]
    else:
        r.ctx['code']=200

    if(r.ctx['code']==404):
        r.ho['X-Out'] =r.ctx['resp']
        r.status = r.ctx['code']
        r.sendHeader()
        r.send('Blocked By Content Auditor');
        # r.send(r.ctx['resp']);
        r.send('!!!!!!', ngx.SEND_LAST)
    else:
         r.status = 200
         # r.ho['X-Out'] =r.ctx['resp']
         r.sendHeader()
         r.send(r.ctx['ACTresp']);
         # r.send(httplib.HTTPResponse, ngx.SEND_FLUSH)
         r.send('!', ngx.SEND_LAST)
