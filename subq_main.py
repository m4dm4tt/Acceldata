"""subq_main.py: SQL Query Parser to apply optimization rules for auto-tuning queries."""

__author__      = "Mridul Mathew"
__copyright__   = "Copyright 2019, mridulmathew@gmail.com"
__assumptions__ = "The SQL construct is well formed. E.g., A SQL query should always end with a ';' or '/'"
__known_bugs__ = "(1) Will not print full table list for multiple ANSI joins (2) Will not print the last closing bracket of the second expression of between clauses."

import os
from os import path
import sys
import nltk
from collections import deque
import subq_lib
subq_start_pos_array = []
subq_end_pos_array = []
g_strsql = ''
	

def clearscreen(): 
	# Purpose: clears the screen based on OS.
	if os.name == 'nt': 
		os.system('cls') 
	else: 
		os.system('clear')
	
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
	l_all_words = nltk.word_tokenize(l_strsql)
	l_word_count = len(l_all_words)-1
	
	l_all_tokens = []
	i = 0
	while i <=  l_word_count:
		if i+1 <= l_word_count:
		
			l_2_str = str(l_all_words[i]) + " " + str(l_all_words[i+1])
			if i+2  <= l_word_count:
				l_3_str = str(l_all_words[i]) + " " + str(l_all_words[i+1]) + " " + str(l_all_words[i+2])
			else: 
				l_3_str = ''
				
			if (l_3_str.lower() != '') and (l_3_str.lower() in subq_lib.compressed_tokens_array):		
				l_all_tokens.append(l_3_str)
				i = i + 3
			elif l_2_str.lower()  in subq_lib.compressed_tokens_array:		
				l_all_tokens.append(l_2_str)
				i = i + 2
			else:
				l_all_tokens.append(l_all_words[i])
				i = i + 1					
		else:
			l_all_tokens.append(l_all_words[i])
			i = i + 1			
						
	return(l_strsql, l_all_tokens)
	
def find_all_bracket_pos():
	# Purpose: create 3 lists containing bracket positions
	l_subq_start_tokens = []
	l_stack = deque()
	l_all_bracket_pairs = []
	l_subq_bracket_pairs = []
	for l_index,l_token in enumerate(g_all_tokens):
		if (l_token =='('):
			l_stack.append(l_index)			
			if str((g_all_tokens[l_index+1])).lower() == 'select':
				l_subq_start_tokens.append(l_index) 
		elif (l_token == ')'):
			l_start_pos = l_stack.pop()
			l_end_pos = l_index
			l_all_bracket_pairs.append([l_start_pos, l_end_pos])
			if l_start_pos in l_subq_start_tokens:
				l_alias = ''
				if str(g_all_tokens[l_end_pos+1]).lower() == 'as':
					l_alias = g_all_tokens[l_end_pos+2]
				elif str(g_all_tokens[l_end_pos+1]).lower() not in subq_lib.alias_end_array:
					l_alias = g_all_tokens[l_end_pos+1]
					
				l_subq_bracket_pairs.append([l_start_pos, l_end_pos, l_alias])				
				
		write_debug_out(str(l_index)+":"+l_token) 
	write_debug_out("Open and close bracket pairs: ")
	write_debug_out(l_all_bracket_pairs)
	write_debug_out("Subquery Open bracket positions: ")
	write_debug_out(l_subq_start_tokens)
	write_debug_out("Subquery start and end positions: ")
	write_debug_out(l_subq_bracket_pairs)
	return(l_all_bracket_pairs, l_subq_bracket_pairs, l_subq_start_tokens)

def find_clauses_start_end_pos():
	l_between_clause_pairs = []
	l_end_pos = len(g_all_tokens)
	for l_index,l_token in enumerate(g_all_tokens):
		if str(g_all_tokens[l_index]).lower() == 'between':
			l_between_pos = l_index
			for k in range(l_between_pos+1, l_end_pos):
				if str(g_all_tokens[k]).lower() == 'and':
					l_separator_and_pos = k
					break
			for m in range(l_separator_and_pos+1, l_end_pos):
				if str(g_all_tokens[m]).lower() in subq_lib.between_clause_end_array:
					l_between_clause_end_pos = m-1
					break
			l_between_clause_pairs.append([l_between_pos, l_between_clause_end_pos])
	write_debug_out("Between clause positions: ")
	write_debug_out(l_between_clause_pairs)
	l_order_by_clause_pairs = []
	for l_index,l_token in enumerate(g_all_tokens):
		if (str(l_token).lower() == 'order by') :
			l_order_by_pos = l_index
			for m in range(l_order_by_pos+1, l_end_pos):
				if str(g_all_tokens[m]).lower() in subq_lib.order_by_clause_end_array:
					l_order_by_end_pos = m-1
					break
			l_order_by_clause_pairs.append([l_order_by_pos, l_order_by_end_pos])
	write_debug_out("Order by clause positions: ")
	write_debug_out(l_order_by_clause_pairs)
	l_join_clause_pairs = []
	for l_index,l_token in enumerate(g_all_tokens):
		if (str(l_token).lower() in subq_lib.joins_tokens_array) :
			l_join_type = l_token
			l_join_pos = l_index
			for k in range(l_join_pos, -1, -1):
				if (str(g_all_tokens[k]).lower() == 'from') :
					l_join_start = k+1
					break
			for m in range(l_join_pos, l_end_pos+1):
				if (g_all_tokens[m]).lower() in subq_lib.join_clause_end_array:
					l_join_end = m-1
					break
			l_join_clause_pairs.append([l_join_start, l_join_end, l_join_type])	
			break
	write_debug_out("Join clause positions: ")
	write_debug_out(l_join_clause_pairs)					

	return(l_between_clause_pairs, l_order_by_clause_pairs, l_join_clause_pairs)

def print_join_list(l_start_pos, l_end_pos):
	# Purpose: To print the join clauses and their types.
	l_join_str = "\t"+"JOIN CLAUSE: "
	for k in g_join_clause_pairs:
		if (k[0] >= l_start_pos) and (k[1] <= l_end_pos):
			n1=k[0]
			n2=k[1]
			for m in range(n1, n2+1):
				l_join_str = l_join_str + " " + g_all_tokens[m]
			print(l_join_str)
			print("\t"+"JOIN TYPE: "+k[2])			

def print_table_list(l_start_pos, l_end_pos):
	# Purpose: To print the list of tables inside subqueries along with their aliases.
	for k in range(l_start_pos, l_end_pos+1):
		if str(g_all_tokens[k]).lower() == 'from':
			l_from_pos = k
			break
	l_table_list = '\t'
	for j in range(l_from_pos+1, l_end_pos):
		#if (str(g_all_tokens[j]).lower() == 'where') or ((str(g_all_tokens[j]).lower() == 'on')) or (l_from_pos+1 == l_end_pos) or (g_all_tokens[j] =';'):
		if (str(g_all_tokens[j]).lower() == 'where') or ((str(g_all_tokens[j]).lower() == 'on')) or (l_from_pos+1 == l_end_pos) or (g_all_tokens[j] ==';'):
			break
			#?? bug. what about multiple string of joins
			# SELECT v.name , c.name , p.lastname FROM vehicle v INNER JOIN color c ON v.color_id = c.id INNER JOIN person p ON v.person_id = p.id
		else:
			if str(g_all_tokens[j]).lower() in subq_lib.joins_tokens_array:
				l_table_list = l_table_list + ","		
			else:
				l_table_list = l_table_list + " " + g_all_tokens[j]		
	print('\t'+ "TABLE list along with ALIAS: " + l_table_list )

def print_subqs():
	# Purpose: To print the sub-queries.
	l_subquery = '\t'
	print("Number of SUB QUERIES : " + str(len(g_subq_bracket_pairs)))
	print('\n')
	print("SUB QUERY list: " )
	l_subq_counter = 1;
	for i in g_subq_bracket_pairs:
		l_subquery = ''
		for k in range(i[0], i[1]+1):
			l_subquery = l_subquery + ' ' + str(g_all_tokens[k])
			
		print(str(l_subq_counter) + ".")
		print("\t"+"SUB QUERY TEXT:" + l_subquery)		
		l_subq_counter = l_subq_counter + 1
		if (i[2] != ''):
			print("\t"+"SUB QUERY ALIAS: " + i[2])
		print_table_list(i[0], i[1])
		print_join_list(i[0], i[1])
		print('-' * 100)

def print_between_clauses():
	# Purpose: To print the list of between clauses.	
	print("BETWEEN clause list: " )
	for k in g_between_clause_pairs:
		n1 = k[0]
		n2 = k[1]
		l_between_str = '\t'
		for m in range(n1, n2+1):
			l_between_str = l_between_str + " " + g_all_tokens[m]
		print(l_between_str)
				
def print_orderby_clauses():
	# Purpose: To print the list of between clauses.	
	print("ORDER BY clause list: " )
	for k in g_order_by_clause_pairs:
		n1 = k[0]
		n2 = k[1]
		l_order_by_str = '\t'
		for m in range(n1, n2+1):
			l_order_by_str = l_order_by_str + " " + g_all_tokens[m]
		print(l_order_by_str)

def print_limit_clause():
	# Purpose: To print the sub-queries.
	l_limit_clause = ' '
	l_limit_exists = 0
	print('\n')
	print("LIMIT clause list : " )
	for k in range(len(g_all_tokens)-1, len(g_all_tokens)-4, -1):
		if (g_all_tokens[k] != ';' and g_all_tokens[k] != '/'):
			l_limit_clause =   g_all_tokens[k] + " " + l_limit_clause 
		if str(g_all_tokens[k]).lower() == 'limit':
			l_limit_exists = 1
	if (l_limit_exists == 1):
		print(("\t" + l_limit_clause))
				
if __name__== "__main__":
	clearscreen()
	clear_debug_out()
	welcome()
	g_strsql, g_all_tokens = parse_infile('myquery.txt')
	g_all_bracket_pairs, g_subq_bracket_pairs, g_subq_start_tokens = find_all_bracket_pos()
	g_between_clause_pairs, g_order_by_clause_pairs, g_join_clause_pairs =  find_clauses_start_end_pos()
	print_subqs()
	print_limit_clause()
	print_between_clauses()
	print_orderby_clauses()
