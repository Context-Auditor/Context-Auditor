# Context-Auditor in a Chrome extension

In this deployment, we used [Tamper](https://github.com/dutzi/tamper) extension that uses [mitmproxy](https://mitmproxy.org/).
It is a similar use case to the mitmproxy deployment that we had [here](../mitmproxy-config) except that this extension does not block HTTP responses marked to include a content injection.
This extension only logs those indications of content injections in the console.

In order for the Context-Auditor to perform a parsing analysis on sets of HTTP requests/responses in an extension, do the following:
  
  1- Clone the Tamper extension's source code from ``https://github.com/dutzi/tamper`` repository.

  2- To integrate the parsing analysis capability of Context-Auditor into Tamper extension,
  we should modify https://github.com/dutzi/tamper/blob/master/mitmproxy-extension/tamper/tamper.py.
  For such aim you can replace it with ``tamper.py`` file in this directory.


*** Note: Tamper extension in the https://chrome.google.com/webstore/detail/tamper/mabhojhgigkmnkppkncbkblecnnanfmd?hl=en URL does not install properly now and it seems that also the developers of the above repo have stopped maintaining extension & code for a while. It's very hard to make this settings work as of now.
