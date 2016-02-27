# franca-tools
Misc tools for working with Franca IDL

This project aims to construct some useful tools for working with the Franca IDL language (https://github.com/franca/franca) together with the Common API toolchain(http://git.projects.genivi.org/?p=ipc/common-api-tools.git;a=summary).

The goal is to implement the following tools:
- A code generator that takes Franca (.fidl) files and outputs Python code, compatible with the Common API DBus marshalling, to be used for integration tests of Common API services.
- A documentation generator plugin for doxygen that takes Franca (.fidl) files and generates doxygen documentation.
- A Franca code completion plugin for vim.
- ...

In order to construct these tools, a lexer, parser and AST are needed. The Franca lexer/parser/AST builder is heavily inspired by pycparser(https://github.com/eliben/pycparser).
