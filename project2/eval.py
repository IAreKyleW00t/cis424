#!/usr/bin/env python
import sys

# Global vars
var_map = dict()
tokens = list()
token = None
token_index = -1

class Variable:
    def __init__(self, id=None, value=None, type=None):
        self.id = id
        self.value = value
        self.type = type

class Node:
    def __init__(self, data=None):
        self.data = data
        self.children = list()

    def add_child(self, child):
        self.children.append(child)

    def remove_child(self, child=0):
        self.children.remove(child)

    def eval(self):
        if self.data == '+': # Addition
            return self.children[0].eval() + self.children[1].eval()
        elif self.data == '-': # Subtraction
            return self.children[0].eval() - self.children[1].eval()
        elif self.data == '*': # Multiplication
            return self.children[0].eval() * self.children[1].eval()
        elif self.data == '/': # Division
            return self.children[0].eval() / self.children[1].eval()
        elif self.data == '^': # Factorization
            return self.children[0].eval() ** self.children[1].eval()
        elif self.data in var_map: # Variable
            var = var_map[self.data] # Save variable Object
            if var.type == 'int': # Integer type
                return int(var.value)
            elif var.type == 'real': # Real (float) type
                return float(var.value)
        else: # Number
            # Attempt to parse the number as an Integer, then Float
            try:
                return int(self.data)
            except ValueError:
                return float(self.data)

def perror(expected, got):
    print("Syntax error: Expected %s, but got %s" % (expected, got))
    print("Token index: %d" % token_index)
    print("Tokens: %s" % tokens)
    sys.exit(1)

def lexeme():
    global token, token_index

    token_index += 1 # Move to next token
    if token_index >= len(tokens): # EOF
        token = None
        return

    # Set token pointer to new index
    token = tokens[token_index]

def prog():
    lexeme() # Read first token
    decl_list() # Evaluate each variable declaration
    stmt_list() # Evaluate each statement

def decl_list():
    # Loop until we don't reach a valid variable type
    while token == 'int' or token == 'real':
        decl()

def decl():
    var_type = type() # Get variable type
    var_list = id_list() # List of all variable with this type

    # Add each variable to the global var_map
    for var in var_list:
        var_map[var] = Variable(var, None, var_type)

    # Check for an ending ';'
    if token != ';':
        perror(';', token)
    lexeme() # token -> <next declaration>

def type():
    if token == 'int' or token == 'real': # Valid types
        var_type = token # Save token as type
        lexeme() # token -> <identifier>
        return var_type
    else: # Invalid type
        perror('int or real', var_type)

def id_list():
    vars = [token] # Save current token as variable identifier
    lexeme() # token -> <next token>

    # Check if there are more identifiers
    if token == ',':
        lexeme() # token -> <next identifier>
        vars.extend(id_list())

    # Return a list of all variable identifiers of a single type
    return vars

def stmt_list():
    # Loop until we reach the end of our tokens
    while token is not None:
        stmt()

def stmt():
    global var_map

    if token in var_map: # Variable = <expr>
        var = var_map[token] # Save variable
        lexeme() # token -> '='

        # Check if variable identifier is followed by an '=' sign
        if token != '=':
            perror('=', token)
        lexeme() # token -> <expr>

        # Evaluate the expression
        right = expr()

        # Check if statement ends in ';'
        if token != ';':
            perror(';', token)
        lexeme() # token -> <next statement>

        # Update the value stored in the variable
        var_map[var.id] = Variable(var.id, right.eval(), var.type)
    elif token == 'iprint': # Integer print statement
        lexeme() # token -> <expr>

        # Evaluate the expression
        right = expr()

        # Check if statement ends in ';'
        if token != ';':
            perror(';', token)
        lexeme() # token -> <next statement>

        # Display the fully evaluated expression as a Integer number
        print(int(right.eval()))
    elif token == 'rprint': # Real (float) print statement
        lexeme() # token -> <expr>

        # Evaluate the expression
        right = expr()

        # Check if statement ends in ';'
        if token != ';':
            perror(';', token)
        lexeme() # token -> <next statement>

        # Display the fully evaluated expression as a real (float) number
        print(float(right.eval()))
    else: # Invalid statement
        perror('variable or print-statement', token)

def expr():
    # Evaluate the left-hand expression
    left = term()

    # Check if the next token is a '+' or '-'
    if token == '+' or token == '-':
        op = Node(token) # Save operator Node
        lexeme() # token -> <right-hand expr>

        # Evaluate the right-hand expression
        right = expr()

        # Set the left and right Nodes as children to the operator Node and
        # return then final operator Node
        op.add_child(left)
        op.add_child(right)
        return op

    # Return only the "left" Node if there is not a '+' or '-' after it
    return left

def term():
    # Evaluate the left-hand expression
    left = factor()

    # Check if the next token is a '*' or '/'
    if token == '*' or token == '/':
        op = Node(token) # Save operator Node
        lexeme() # token -> <right-hand expr>

        # Evaluate the right-hand expression
        right = expr()

        # Set the left and right Nodes as children to the operator Node and
        # return then final operator Node
        op.add_child(left)
        op.add_child(right)
        return op

    # Return only the "left" Node if there is not a '*' or '/' after it
    return left

def factor():
    # Evaluate the left-hand expression
    left = base()

    # Check if the next token is a '^'
    if token == '^':
        op = Node(token) # Save operator Node
        lexeme() # token -> <right-hand expr>

        # Evaluate the right-hand expression
        right = expr()

        # Set the left and right Nodes as children to the operator Node and
        # return then final operator Node
        op.add_child(left)
        op.add_child(right)
        return op

    # Return only the "left" Node if there is not a '^'
    return left

def base():
    if token == "(": # Parenthesis
        lexeme() # token -> <expr>

        # Evaluate the left-hand expression
        left = expr()

        # Check if there is a closing parenthesis
        if token != ")":
            op = Node(token) # Save operator Node
            lexeme() # token -> <right-hand expr>

            # Evaluate the right-hand expression
            right = expr()

            # Set the left and right Nodes as children to the operator Node and
            # set the operator Node as the new left Node
            op.add_child(left)
            op.add_child(right)
            left = op
        lexeme() # token -> <next token>

        # Return only the final "left" Node
        return left
    else: # Number or variable
        base = Node(token) # Save token Node
        lexeme() # token -> <next token>

        # Return the final "base" Node
        return base

def main():
    global tokens

    # Check for valid command line arguments
    if (len(sys.argv) != 2):
        print("Usage: %s filename" % sys.argv[0])
        sys.exit(1)

    # Save input file
    filename = sys.argv[1]

    # Read all tokens from file
    with open(filename, 'r') as f:
        tokens = [word for line in f for word in line.split()]

    # "Run" the provided program
    prog()

if __name__ == "__main__":
  main()
