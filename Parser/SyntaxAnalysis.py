from LexicalAnalysis import *

#helps us move from token to token in the list of tokens
position = 0

#gives us the next token in the list of tokens
nextToken = ""

#declares the varibale that is going to store the length of the list 
length = -1

#global variable for depth
depth = 0

class Syntax:
	def __init__(self,tokens):
		self.__tokens = tokens

	def run(self):
		#call this fucntion to get the first token
		self.__getLex()

		#call this function to start parsing
		self.__program()

	#program - parses strings in the language generated by the rule:
	#<program> ::= prog <progname> <compound stmt>
	def __program(self):
		global nextToken

		s = "<program> (enter)"
		#helps indent every time we move onto the next function
		#prints the function that the program is currently in
		self.__indentdepth(1,s)

		#if the token is prog
		if nextToken == "KEYWORD_PROG":
			#get the next token
			self.__getLex()
			#check to see if the next token is progname
			if nextToken == "PROGNAME":
				#get the next token
				self.__getLex()
				#call the function compound statement
				self.__compound_stmt()
			#if the next token isn't progname
			else:
				#print an error message about a missing PROGNAME
				self.__error("PROGNAME")

		#if the next token isn't prog
		else:
			#print an error message about the keyword prog
			self.__error("KEYWORD_PROG")


		s = "<program> (exit)"
		# indents one less every time the program moves to the last function that called it
		#prints the function that the function it just exited
		self.__indentdepth(-1,s)


	#compound_stmt - parses strings in the language generated by the rule:
	#<compound stmt> ::= start <stmt> {; <stmt>} finish
	def __compound_stmt(self):
	#helps indent every time we move onto the next function
		#prints the function that the program is currently in
		s= "<compound stmt> (enter)"
		self.__indentdepth(1,s)

		#if the next token is the keyword start
		if nextToken == "KEYWORD_START":
			#get the next token
			self.__getLex()
			#call the statement function
			self.__stmt()

			#while the next token is a semicolon, continue looping
			while nextToken  == "SEMICOLON":
				#get the next token
				self.__getLex()
				#call the statement function
				self.__stmt()

			#if the next token is the keyword finish
			if nextToken == "KEYWORD_FINISH":
				#get the next token
				self.__getLex()

			#if it isn't the keyword finish
			else:
				#print an error message about a missing finish keyword
				self.__error("KEYWORD_FINISH")

		#if the next token isn't start
		else:
			#print an error message about a missing start keyword
			self.__error("KEYWORD_START")


		s = "<compound stmt> (exit)"
		# indents one less every time the program moves to the last function that called it
		#prints the function that the function it just exited
		self.__indentdepth(-1,s)
		
	#smt - parses strings in the language generated by the rule:
	#<stmt> ::= <simple stmt> | <structured stmt>
	def __stmt(self):
		#helps indent every time we move onto the next function
		#prints the function that the program is currently in
		s = "<stmt> (enter)"
		self.__indentdepth(1,s)

		#if the next token is a variable, a load statement or a save statement
		if nextToken == "VARIABLE" or nextToken == "KEYWORD_LOAD" or nextToken == "KEYWORD_SAVE":
			#call the function simple statement
			self.__simple_stmt()

		#if the next token is a start, an if statement or a while statement
		elif nextToken == "KEYWORD_IF" or nextToken == "KEYWORD_WHILE" or nextToken == "KEYWORD_START":
			#call the function structured statement
			self.__structured_stmt()

		# indents one less every time the program moves to the last function that called it
		#prints the function that the function it just exited
		s = "<stmt> (exit)"
		self.__indentdepth(-1,s)



	#simple_stmt - parses strings in the language generated by the rule:	
	#<simple stmt> ::= <assignment stmt> | <load stmt> | <save stmt>
	def __simple_stmt(self):
		#helps indent every time we move onto the next function
		#prints the function that the program is currently in
		s= "<simple stmt> (enter)"
		self.__indentdepth(1,s)

		if nextToken == "VARIABLE":
			self.__assignment_stmt()

		elif nextToken == "KEYWORD_LOAD":
			self.__load_stmt()

		elif nextToken == "KEYWORD_SAVE":
			self.__save_stmt()

		# indents one less every time the program moves to the last function that called it
		#prints the function that the function it just exited
		s= "<simple stmt> (exit)"
		self.__indentdepth(-1,s)


	#assignment_stmt - parses strings in the language generated by the rule:
	#<assignment stmt> ::= <variable> := <expression>
	def __assignment_stmt(self):
		#helps indent every time we move onto the next function
		#prints the function that the program is currently in
		s= "<assign stmt> (enter)"
		self.__indentdepth(1,s)

		#if  the next token is a vriable
		if nextToken == "VARIABLE":
			#get the next token
			self.__getLex()
			if nextToken == "ASSIGN_OP":
				#get the next token
				self.__getLex()
				#call the function expression
				self.__expression()
			#print an error message if the next token is not an assignment operator
			else:
				self.__error("ASSIGNMENT OPERATOR")

		#print an error message if the next token isn't a variable
		else:
			self.__error("VARIABLE")

		# indents one less every time the program moves to the last function that called it
		#prints the function that the function it just exited
		s = "<assign stmt> (exit)"
		self.__indentdepth(-1,s)

	#load_stmt - parses strings in the language generated by the rule:
	#<load stmt> ::= load ( <variable> { , <variable> } )
	def __load_stmt(self):
		#helps indent every time we move onto the next function
		#prints the function that the program is currently in
		s= "<load stmt> (enter)"
		self.__indentdepth(1,s)

		#if the next token is load
		if nextToken == "KEYWORD_LOAD":
			#get the next token
			self.__getLex()

			#if the next token is left parenthesis
			if nextToken == "LEFT_PAREN":
				#get the next token
				self.__getLex()

				#if the next token is a variable
				if nextToken == "VARIABLE":
					#get the next token
					self.__getLex()

					#while the next token is a comma, continue looping
					while nextToken == "COMMA":
						#get the next token
						self.__getLex()

						#if the next token is a variable
						if nextToken == "VARIABLE":
							#get the next token
							self.__getLex()
						#if the next token isn't a variable
						else:
							#print an error message about a missing variable
							self.__error("VARIABLE")
					#if the next token is a right parenthesis
					if nextToken == "RIGHT_PAREN":
						#get the next token
						self.__getLex()
					#if the next token isn't a right parenthesis
					else:
						#print an error message about a missing right parenthesis
						self.__error("RIGHT PARENTHESIS")
				#if the next token isn't a variable
				else:
					#print an error message about a missing variable
					self.__error("VARIABLE")
			#if the next token isn't a left parenthesis
			else:
				#print an error message about a missing left parenthesis
				self.__error("LEFT PARENTHESIS")
				
		# indents one less every time the program moves to the last function that called it
		#prints the function that the function it just exited
		s = "<load stmt> (exit)"
		self.__indentdepth(-1,s)


	#save_stmt - parses strings in the language generated by the rule:
	#<save stmt> ::= save ( <expression> { , <expression> } )
	def __save_stmt(self):
		#helps indent every time we move onto the next function
		#prints the function that the program is currently in
		s= "<save stmt> (enter)"
		self.__indentdepth(1,s)

		#if the next token is the save keyword
		if nextToken == "KEYWORD_SAVE":
			#get the next token
			self.__getLex()
			#if the next token is a left parenthesis
			if nextToken == "LEFT_PAREN":
				#get the next token
				self.__getLex()
				self.__expression()
				#continue looping if the next token is a comma
				while nextToken == "COMMA":
					#get the next token
					self.__getLex()
					self.__expression()
				#if the next token is a right parenthesis
				if nextToken == "RIGHT_PAREN":
					#get the next token
					self.__getLex()
				#if the next token isn't a right parenthesis
				else:
					#print an error message about a right parenthesis
					self.__error("RIGHT PARENTHESIS")
			#if the next token isn't a left parenthesis
			else:
				#print an error message about a left parenthesis
				self.__error("LEFT PARENTHESIS")

		# indents one less every time the program moves to the last function that called it
		#prints the function that the function it just exited
		s = "<save stmt> (exit)"
		self.__indentdepth(-1,s)


	#structured_stmt- parses strings in the language generated by the rule:
	#<structured stmt> ::= <compound stmt> | <if stmt> | <while stmt>
	def __structured_stmt(self):
		 #helps indent every time we move onto the next function
		#prints the function that the program is currently in
		 s= "<structured stmt> (enter)"
		 self.__indentdepth(1,s)

		 #if the next token is the if keyword
		 if nextToken == "KEYWORD_IF":
		 	#call the function if_statement
		 	self.__if_stmt()

		 #if the next token is the  while keyword
		 elif nextToken == "KEYWORD_WHILE":	
		 	#call the function while_statement
		 	self.__while_stmt()

		 #if it's none of the above tokens
		 else:
		 	#this has to be a compound statement
		 	self.__compound_stmt()
		
		# indents one less every time the program moves to the last function that called it
		#prints the function that the function it just exited
		 s = "<structured stmt> (exit)"
		 self.__indentdepth(-1,s)

	#if_stmt - parses strings in the language generated by the rule:
	#<if stmt> ::= if <expression> then <stmt> | if <expression> then <stmt> else <stmt>
	def __if_stmt(self):
		#helps indent every time we move onto the next function
		#prints the function that the program is currently in
		s = "<if stmt> (enter)"
		self.__indentdepth(1,s)

		#if the next token is the if keyword
		if nextToken == "KEYWORD_IF":
			#get the next token
			self.__getLex()
			#call the expression function
			self.__expression()

			#if the next token is the then keyword
			if nextToken == "KEYWORD_THEN":
				#get the next token
				self.__getLex()
				#call the function statement
				self.__stmt()

				#if the next token is the else keyword
				if nextToken == "KEYWORD_ELSE":
					#get the next token
					self.__getLex()
					#call the function statement
					self.__stmt()
			#if there is no then keyword
			else:
				#print an error message about a missing then keyword
				self.__error("KEYWORD_THEN")

		# indents one less every time the program moves to the last function that called it
		#prints the function that the function it just exited
		s = "<if stmt> (exit)"
		self.__indentdepth(-1,s)


	#while_stmt - parses strings in the language generated by the rule:
	#<while stmt> ::= while <expression> do <stmt>
	def __while_stmt(self):
		#helps indent every time we move onto the next function
		#prints the function that the program is currently in
		s = "<while stmt> (enter)"
		self.__indentdepth(1,s)

		##if the next token is the while keyword
		if nextToken == "KEYWORD_WHILE":
			#get the next token
			self.__getLex()
			#call the expression function
			self.__expression()

			#if the next token is the do keyword
			if nextToken == "KEYWORD_DO":
				#get the next token
				self.__getLex()
				#call the statement function
				self.__stmt()
			#if there is a missing do keyword
			else:
				#print an error message about a missing do keyword
				self.__error("KEYWORD_DO")

		# indents one less every time the program moves to the last function that called it
		#prints the function that the function it just exited
		s = "<while stmt> (exit)"
		self.__indentdepth(-1,s)

	#expression - parses strings in the language generated by the rule:
	# <expression> ::= <simple expr> | <simple expr> <relational_operator> <simple expr>
	def __expression(self):
		#helps indent every time we move onto the next function
		#prints the function that the program is currently in
		s = "<expression> (enter)"
		self.__indentdepth(1,s)

		#call the simple expression function
		self.__simple_expr()

		#if the next token is the relational operator keyword
		if nextToken == "RELATIONAL_OPERATOR":
			#get the next token
			self.__getLex()
			#call the simple expression function
			self.__simple_expr()	
		
		# indents one less every time the program moves to the last function that called it
		#prints the function that the function it just exited
		s = "<expression> (exit)"
		self.__indentdepth(-1,s)


	#simple_expr - parses strings in the language generated by the rule:
	#<simple expr> ::= [ <sign> ] <term> { <adding_operator> <term> }
	def __simple_expr(self):
		#helps indent every time we move onto the next function
		#prints the function that the program is currently in
		s = "<simple expr> (enter)"
		self.__indentdepth(1,s)

		if nextToken == "SIGN":
			#get the next token
			self.__getLex()

		self.__term()

		while nextToken == "ADD_OP" or nextToken == "SUB_OP":
			#get the next token
			self.__getLex()
			self.__term()

		# indents one less every time the program moves to the last function that called it
		#prints the function that the function it just exited		
		s = "<simple expr> (exit)"
		self.__indentdepth(-1,s)


	#term - parses strings in the language generated by the rule:
	#<term> ::= <factor> { <multiplying_operator> <factor> }
	def __term(self):
		#helps indent every time we move onto the next function
		#prints the function that the program is currently in
		s = "<term> (enter)"
		self.__indentdepth(1,s)

		#call the factor function
		self.__factor()

		#continue looping if the next keyword is a multiplcation symbol or a division symbol
		while nextToken == "MULTI_OP" or nextToken == "DIV_OP":
			#get the next token
			self.__getLex()
			#call the factor function
			self.__factor()
		
		# indents one less every time the program moves to the last function that called it
		#prints the function that the function it just exited
		s = "<term> (exit)"
		self.__indentdepth(-1,s)

	#factor - parses strings in the language generated by the rule:
	#<factor> ::= <variable> | <int_literal> | ( <expression> )
	def __factor(self):
		#helps indent every time we move onto the next function
		#prints the function that the program is currently in
		s = "<factor> (enter)"
		self.__indentdepth(1,s)

		#if the next token is a variable or an int
		if nextToken == "VARIABLE" or nextToken == "INT_LITERAL" :
			#get the next token
			self.__getLex()

		# If the RHS is '('<expr>')', call lex to pass over the
		# left parenthesis, call expr, and check for the right
		# parenthesis 

		else:
			if nextToken == "LEFT_PAREN":
				#get the next token
				self.__getLex()

				#call the function expression
				self.__expression()

				if nextToken == "RIGHT_PAREN":
					#get the next token
					self.__getLex()
				#if the next token isn't a right parenthesis
				else:
					#print an error message about a missing right parenthesis
					self.__error("RIGHT PARENTHESIS")
			#if the next token isn't a left parenthesis
			else:
				#print an error message about a missing left parenthesis
				self.__error("LEFT PARENTHESIS")
	
		# indents one less every time the program moves to the last function that called it
		#prints the function that the function it just exited	
		s = "<factor> (exit)"
		self.__indentdepth(-1,s)
	
	#Every time this method is called, we move to the next position in the tokens list to get the next token
	def __getLex(self):
		#global variables
		global position
		global nextToken
		global length

		#store the length of the tokens list
		length = len(self.__tokens)

		#if we have reached the end of the tokens list(or the end of the program)
		if position == length:
			#make the next token a -1
			nextToken = -1
			print("Next token is: " +  str(nextToken) + ", Next lexeme is: EOF")

		else:
			#store the token in nextToken
			nextToken = self.__tokens[position].getToken()
			
			#if the next token is a comment
			if nextToken == "COMMENT":
				#print the token and its lexeme
				print("Next token is: " +  nextToken + ", Next lexeme is: " + self.__tokens[position].getLexeme() )
				#and skip this token
				position = position + 1
				#store the token in nextToken
				nextToken = self.__tokens[position].getToken()


			print("Next token is: " +  nextToken + ", Next lexeme is: " + self.__tokens[position].getLexeme() )

			# for i in self.__tokens:
			# 	print(i)

			#update position
			#add one to the position of a the token list
			position = position + 1

	
	#displays error message
	def __error(self,s):
		#if the error happens after the last line of code, point the error the last line of code
		print("<SYNTAX ERROR>: saw " + " \" " + self.__tokens[position - 1].getToken() + " \" " "but expected " + s + " on line " + str(self.__tokens[position -1].getLineNum()) + "\n")


	#indents when a new depth is reached
	def __indentdepth(self, change, sentence):
		global depth

		if change < 0:
			depth = depth + change

			if depth < 0:
			 	depth = 0

		if depth >= 0:
			temp = depth * 2
			#print temp number of spaces and print the depth level we have reached
			print(" "*temp + sentence)

		if 	change > 0:
			depth = depth + change;

