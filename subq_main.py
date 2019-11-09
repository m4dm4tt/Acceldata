# Main Program for Sub-query parser
import os
from os import path
import sys
import nltk
from collections import deque
subq_start_pos_array = []
subq_end_pos_array = []
g_all_tokens = []
g_subq_start_tokens = []
g_subq_end_tokens = []
g_strsql = ''
	
def temp():
	data = []
	a,b = 3,4
	c,d = 5,6
	data.append([a,b])
	data.append([c,d])
	print(data)

	
def welcome():
	print('\n')
	l_welcome_msg =  'WELCOME to the uber exciting world of sub query trolling!'
	print(l_welcome_msg.center(190, " "))
	print('_' * 190)

def clear_debug_out():
	debug_flnm = 'debug_subq_main.log'
	debug_flobj = open(debug_flnm, 'w')
	debug_flobj.close()	
	
def write_debug_out(line):
	debug_flnm = 'debug_subq_main.log'
	debug_flobj = open(debug_flnm, 'a')
	debug_flobj.write(str(line)+"\n")
	debug_flobj.close()	

def parse_infile(in_flnm):
	# Purpose: read query form input file and tokenize it.
	with open(in_flnm, 'r') as in_flobj:
		l_strsql = in_flobj.read().replace('\n', ' ')
	l_all_tokens = nltk.word_tokenize(l_strsql)
	return(l_strsql, l_all_tokens)
	
def find_all_bracket_pos(l_tokens):
	# Purpose: create 3 lists containing bracket positions
	l_subq_start_tokens = []
	l_stack = deque()
	l_all_bracket_pairs = []
	l_subq_bracket_pairs = []
	for l_index,l_token in enumerate(l_tokens):
		if (l_token =='('):
			l_stack.append(l_index)			
			if (l_tokens[l_index+1]) == 'select':
				l_subq_start_tokens.append(l_index) 
		elif (l_token == ')'):
			l_start_pos = l_stack.pop()
			l_all_bracket_pairs.append([l_start_pos, l_index])
			if l_start_pos in l_subq_start_tokens:
				l_subq_bracket_pairs.append([l_start_pos, l_index])				
				
		write_debug_out(str(l_index)+":"+l_token) 
	write_debug_out("Open and close bracket pairs: ")
	write_debug_out(l_all_bracket_pairs)
	write_debug_out("Subquery Open bracket positions: ")
	write_debug_out(l_subq_start_tokens)
	write_debug_out("Subquery start and end positions: ")
	write_debug_out(l_subq_bracket_pairs)
	return(l_all_bracket_pairs, l_subq_bracket_pairs, l_subq_start_tokens)

def print_subqs(l_all_tokens, l_subq_bracket_pairs):
	# Purpose: To print the sub-queries.
	l_subquery = ''
	print("Number of Sub-Queries : " + str(len(l_subq_bracket_pairs)))
	print("List of Sub-Queries   : " )
	for i in l_subq_bracket_pairs:
		l_subquery = ''
		for k in range(i[0], i[1]):
			l_subquery = l_subquery + ' ' + str(l_all_tokens[k])
		print(l_subquery)
	
if __name__== "__main__":
	clear_debug_out()
	welcome()
	g_strsql, g_all_tokens = parse_infile('myquery.txt')
	g_all_bracket_pairs, g_subq_bracket_pairs, g_subq_start_tokens = find_all_bracket_pos(g_all_tokens)
	print_subqs(g_all_tokens, g_subq_bracket_pairs)