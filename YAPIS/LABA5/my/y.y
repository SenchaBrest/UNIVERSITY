%{
#include <stdio.h>
#include <stdlib.h>
void yyerror(const char *s);
int yylex();
%}

%union {
    double num;
    char* id;
}

%token <num> NUMBER
%token <id> ID
%token PLUS MINUS MUL DIV
%token LPAREN RPAREN
%token SEMICOLON
%token SIN COS
%type <num> expr term factor func

%%

program: 
    statement_list
    ;

statement_list:
    statement_list SEMICOLON statement
    | statement
    ;

statement:
    expr    { printf("Expression evaluated\n"); }
    ;

expr:
    expr PLUS term   { printf("Operation: Addition\n"); }
    | expr MINUS term { printf("Operation: Subtraction\n"); }
    | term
    ;

term:
    term MUL factor  { printf("Operation: Multiplication\n"); }
    | term DIV factor { printf("Operation: Division\n"); }
    | factor
    ;

factor:
    NUMBER          { printf("Number constant\n"); }
    | ID            { printf("Identifier: %s\n", $1); }
    | LPAREN expr RPAREN
    | func
    ;

func:
    SIN LPAREN expr RPAREN  { printf("Function: sin()\n"); }
    | COS LPAREN expr RPAREN { printf("Function: cos()\n"); }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main() {
    return yyparse();
}