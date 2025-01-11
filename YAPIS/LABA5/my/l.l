%{
#include "tab.h"
#include <stdio.h>
#include <stdlib.h>
%}

%%

[0-9]+(\.[0-9]+)?    { yylval.num = atof(yytext); return NUMBER; }
"sin"                { return SIN; }
"cos"                { return COS; }
"+"                  { return PLUS; }
"-"                  { return MINUS; }
"*"                  { return MUL; }
"/"                  { return DIV; }
"("                  { return LPAREN; }
")"                  { return RPAREN; }
";"                  { return SEMICOLON; }
[a-zA-Z][a-zA-Z0-9]* { yylval.id = strdup(yytext); return ID; }
[ \t\n]             ; /* Игнорируем пробелы, табуляцию и переносы строк */
.                    { return yytext[0]; }

%%

int yywrap() {
    return 1;
}