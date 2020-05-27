import re

class Token:
	def __init__(self, token, lexeme , line_num):
		self.__token = token
		self.__lexeme = lexeme
		self.__line_num = line_num

	def getToken(self):
		return self.__token

	def getLexeme(self):
		return self.__lexeme

	def getLineNum(self):
		return self.__line_num


	def __str__(self):
		return "On line number " + str(self.__line_num) + ":\nTOKEN: " + self.__token + "\t LEXEME: " +  self.__lexeme + "\n" 


class Lexer:

	def __init__(self,line, line_num):
		self.__line = line
		self.__line_num = line_num


	#matches the lexeme to a token
	def lex(self):

		token_codes = {
		"^#" : "COMMENT",
		"\\b^prog\\b" : "KEYWORD_PROG",
		"\\b^start\\b" : "KEYWORD_START",
		"\\b^end\\b" : "KEYWORD_END",
		"\\b^then\\b" : "KEYWORD_THEN",
		"\\b^if\\b" : "KEYWORD_IF",
		"\\b^else\\b" : "KEYWORD_ELSE",
		"\\b^while\\b" : "KEYWORD_WHILE",
		"\\b^do\\b" : "KEYWORD_DO",
		"\\b^save\\b" : "KEYWORD_SAVE",
		"\\b^finish\\b" : "KEYWORD_FINISH",
		"\\b^load\\b" : "KEYWORD_LOAD",
		"^[A-Za-z]([A-Za-z0-9])*" : "VARIABLE",
		"^[A-Z]([A-Za-z0-9])*" : "PROGNAME",
		"^[0-9]+" : "INT_LITERAL",
		"^(<>|<=|>=|=|<|>)" : "RELATIONAL_OPERATOR",
		"^[\+\-]" : "SIGN",
		"^\*" : "MULTI_OP",
		"^\/" : "DIV_OP",
		"^:=" : "ASSIGN_OP",
		"^;": "SEMICOLON",
		"^\(" : "LEFT_PAREN",
		"^\)" : "RIGHT_PAREN",
		"^," : "COMMA",
		" " : "WHITESPACE"
		}

		tokens = []

		#remove all white spaces
		#self.__line = "".join(self.__line.split())

		#remove all the leading and ending white spaces
		self.__line = self.__line.strip()

		#loop through each lexeme in a line until there are no more lexemes in the line
		while(len(self.__line) > 0):
			#reset matched to false
			matched = False

			#loop through the dictionary
			for regex in token_codes:
				#if there is a match between one of the regexes and the lexeme in the line
				if re.match(regex,self.__line) != None:

					#set matched to true
					matched = True

					#Match the string with the regex to get the lexeme
					match= re.findall("\'.+\'",str(re.match(regex,self.__line)))
					
					#Since the lexeme is in the first element of the list, store it into a separate variable
					lexeme = match[0]

					#remove the single quotes to get the lexeme by itself
					lexeme = lexeme[1:len(lexeme) -1]
					
					#store the lexeme's token value
					token =  token_codes[regex]

					#if the length of the tokens list is greater than 1 (there are at least two lexemes in it)
					if len(tokens) > 0 :
						#get the token value of the previous lexeme
						prevToken = tokens[len(tokens) - 1].getToken()

						#get the the line number of the previous lexeme
						prevLine = tokens[len(tokens) - 1].getLineNum()

						#if the token value is equal to the reserved keyword PROGNAME
						if prevToken == "KEYWORD_PROG" and token == "VARIABLE" :
							#make the token value of the current lexeme "PROGNAME"
							token = "PROGNAME"

						#if there was a number before this lexeme and the current lexeme's token is SIGN
						elif ( prevToken == "INT_LITERAL" or prevToken == "RIGHT_PAREN"  or prevToken == "VARIABLE" ) and token == "SIGN"  :
							#and if the current lexeme is a plus sign
							if lexeme == "+":	
								#make the token an addition operator
								token = "ADD_OP"
							#and if the current lexeme is a minus sign
							else:
								#make the token a subtraction operator
								token = "SUB_OP"

					#if the token isn't a whitespace					
					if token != "WHITESPACE":
						#add the token object to the list of token objects
						tokens.append(Token(token,lexeme, self.__line_num))

					#if it's a comment, make the line empty
					if lexeme == "#":
						self.__line = ""

					#if it's any other lexeme
					else:
						#remove the current lexeme and keep the rest of the line
						self.__line = self.__line[len(lexeme):]
						
					#break out of the inner loop
					break

			#if the lexeme hasn't been matched
			if matched == False:
				#create a token object with the unidentified lexeme
				tokens.append(Token("UNIDENTIFIED",self.__line[0:1],self.__line_num))	
				#cut off the unidentified lexeme and keep the rest of the line
				self.__line = self.__line[1:]
				
		return tokens
