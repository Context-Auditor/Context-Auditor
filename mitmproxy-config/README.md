# Context-Auditor as a web proxy


To run an instance of Context-Auditor inside mitmproxy, you need to do the following: 


  1- Install [mitmproxy](https://mitmproxy.org/).


  2- Send your network's traffic throgh ``localhost:8080``.


  3- Run ``mitmproxy --scripts \<PATH to mitmScript.py\>`` in the command line.
