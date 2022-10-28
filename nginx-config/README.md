# Context-Auditor as an Nginx module



First of all, set up your environment so that an apache webserver hosts your web application on any port other than port 80, and it is only accessible for local traffic.
Then, configure your Nginx webserver in the reverse proxy mode;
it should receive web traffic on port 80 and act as a proxy between the web client and the actual web application hosted on apache webserver.


In order for the Context-Auditor to perform a parsing analysis on sets of HTTP requests/responses on the Nginx webserver, do the following:
  1- Run ``python generateCode.py`` in this directory and the copy the generated ``detector.py`` file into the parent directory of your ``nginx.conf`` file. 

  2- Since our implementation of Context-Auditor is in Python language, Nginx requires to load [Nginx Python Module](https://github.com/arut/nginx-python-module). Follow instructions in the github repository to load the [Nginx Python Module](https://github.com/arut/nginx-python-module) in Nginx.

  3- Insert ``load_module modules/ngx_python_module.so;`` at the top of ``nginx.conf`` file.

  4- Insert following lines to your of ``nginx.conf`` to activate Context-Auditor:

  ``http {
      python_include detector.py;
      server {
          /*...YOUR OWN CONFIG HERE...*/
          location / {
          python_access "access(r)";
          python_content "content(r)";
          /*...YOUR OWN CONFIG HERE...*/
          }
        }
      }``
