from LexicalAnalysis import *
from SyntaxAnalysis import *

import re
#list of token objects
tokens = []

#create a variable that stores the file name
file_name = "eacosta1-p5.txt"
 

def printTokens():
	for lexeme in tokens:
		if lexeme.getToken() == "UNIDENTIFIED":
			print("<LEXICAL ERROR> Illegal character " + lexeme.getLexeme() + " on line " + str(lexeme.getLineNum()))
		print(lexeme.__str__())

#reads the file
def lexAnalysis():
	my_file = open(file_name, "r")

	if my_file.mode == "r":
		data = my_file.readlines()
		line_num = 0

		#takes each line of code
		for line in data:
			#keep track of how many lines are in the file
			line_num = line_num + 1
			#Create a Lexer object that takes the line number and the line as parameters
			lexer = Lexer(line,line_num)
			#call lex on the object and return a table full of lexemes and their associated token value
			tokens.extend(lexer.lex())

		#closes file
		my_file.close()

	else:
		print("ERROR: Failed to open file for reading")


def syntaxAnalysis():
	#give the syntac object a list of tokens
	syntax = Syntax(tokens)
	#run the syntax analyzer
	syntax.run()

lexAnalysis()
#printTokens()
syntaxAnalysis()






