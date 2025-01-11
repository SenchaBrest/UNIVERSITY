/* Калькулятор для выражени в инфиксной нотации -- calc */

%{
#define YYSTYPE double
#include <math.h>

#include <ctype.h>
#include <stdio.h>
#include <malloc.h>

%}

/* Объявления BISON */
%token NUM
%left '-' '+'
%left '*' '/'
%left NEG     /* обращение -- унарный минус */
%right '^'    /* возведение в степень       */

/* Далее следует грамматика */

%%
input:    /* пустая строка */
        | input line
;

line:     '\n'
        | exp '\n'  { printf ("\t%.10g\n", $1); }
;

exp:      NUM                { $$ = $1;         }
        | exp '+' exp        { $$ = $1 + $3;    }
        | exp '-' exp        { $$ = $1 - $3;    }
        | exp '*' exp        { $$ = $1 * $3;    }
        | exp '/' exp        { $$ = $1 / $3;    }
        | '-' exp  %prec NEG { $$ = -$2;        }
        | exp '^' exp        { $$ = pow ((double)$1, (double)$3); }
        | '(' exp ')'        { $$ = $2;         }
;
%%


int
yylex (void)
{
	int c;

	/* пропустить промежутки  */
	while ((c = getchar ()) == ' ' || c == '\t')
		;
	/* обработка чисел       */
	if (c == '.' || isdigit (c))
	{
		ungetc (c, stdin);
		scanf ("%lf", &yylval);
		return NUM;
	}
	/* вернуть конец файла  */
	if (c == EOF)
		return 0;
	/* вернуть одну литеру */
	return c;
}


void
yyerror (const char *s)  /* вызывается yyparse в случае ошибки */
{
	printf ("%s\n", s);
}


int
main (void)
{
	return yyparse ();
}




