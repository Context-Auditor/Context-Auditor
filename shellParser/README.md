# Context-Auditor as Shell Parsing module

To prove the extensibility of our approach, we have also implemented a simple 2PDA for parsing analysis of Bash language.

You can test this module by calling ``shellParser.py  <BASH COMMAND>  <UNTRUSTED INPUT BYTES>`` and in case there is a command injection in the input it will print `0`.

Or

In  a test environment (please do not test it on your real OS since I am afraid you might mess up with your ``\bin\sh``):
1. make a copy of ``\bin\sh`` in another executable called ``\bin\shh``,
2. configure an apache webserver so that it would save URL query parameters of an incoming HTTP request in an environment variable called
``QUERY_STR``
3. then use ``pybash.py`` as a wrapper around `\bin\sh` to prevent requests triggering a command injection exploitation from reaching the actual ``bin\sh``.
