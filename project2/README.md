Project 1
---------
#### Description
  A basic interpreter which uses a top-down recursive-descent method and inherited/synthesized attributes to parse and evaluate a very simple programming language. The grammar for the language is given below:
  
  ```
  <prog>        ::= <decl_list> <stmt_list>
  <decl_list>   ::= <decl> | <decl> <decl_list>
  <decl>        ::= <type> <id_list> ;
  <type>        ::= int | real
  <id_list>     ::= id | id {, <id_list>}
  <stmt_list>   ::= <stmt> | <stmt> <stmt_list>
  <stmt>        ::= id = <expr> ; |
                    iprint <expr> ; |
                    rprint <expr> ;
  <expr>        ::= <term> {+ <term> | - <term>}
  <term>        ::= <factor> {* <factor> | / <factor>}
  <factor>      ::= <base> ^ <factor> | <base>
  <base>        ::= (<expr>) | id | number
  ```
  
  `iprint` will display the expression as an `int`, while `rprint` will display the expression as a real (`float`).

#### Example
  ```
  kyle@arch cis424/project2 » cat sample.tiny
  int s , t ;
  real r , pi ;
  iprint 2 + 3 * 4 ;
  s = 3 + 4 ;
  t = 6 - 2 ;
  iprint s * t ^ 2 ;
  iprint ( s + t ) * ( s - t ) ;
  r = 7.0 ;
  pi = 3.1416 ;
  rprint 4.0 * pi * r ;
  kyle@arch cis424/project2 » ./eval.py sample.tiny
  14
  112
  33
  87.9648
  ```
