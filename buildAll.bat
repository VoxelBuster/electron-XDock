@echo off
del /Q node_modules
call npm i -D electron@beta
call npm i jquery@latest
call npm i paper@latest
call npm i string-format@latest
call npm -g --verbose install
echo Process completed.
