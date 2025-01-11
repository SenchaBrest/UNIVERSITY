bison -d y.y -o tab.c
flex -o lex.c l.l 
gcc lex.c tab.c -o app ./libfl.a