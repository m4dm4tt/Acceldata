Mail as received from Acceldata:
--------------------------------

We at Acceldata want to optimize SQL queries on the fly. 
We would like to implement a minimal query parser that allows us to apply simple optimization rules for auto-tuning queries.

Given a SQL query, Your query parser/analyzer should be able to

Count number of Subqueries
List of Subqueries with their Aliases.
Get a list of Tables used in each Subquery along with table aliases
Get a list of any Between clauses, order by clauses and limit clauses
Get a List of Joins used Per sub query along with the join types


Requirement & Progress
----------------------

Given a SQL Query,

1) Count number of sub-queries.
	DONE
2) List of sub-queries with their aliases.
	DONE
3) List of tables used in each sub-query along with table aliases.
	DONE
4) List of BETWEEN, ORDER BY and LIMIT clauses.
	DONE			
5) List of joins per sub-query along with join type.
	DONE

Language of choice
------------------

Bash is out since this project involves much more than simple text search. There is need for regexp/tokenization.
We also need positional traversal of queuing/stack to arrive at index positions of sub-queries. 
Therefore, Python is the language of choice.

Setup
-----

1) Install python 3.8 for windows and ensure it is added to the PATH
2) To Install nltk: type: pip install nltk
3) In python shell, type: import nltk
4) In python shell, type: nltk.download('all')
5) myquery.txt is the input file for parsing. Please input only one valid SQL at a time into this file.
   Sample queries used for testing are available in query_database.sql
6) Ensure myquery.txt, subq_main.py and subq_lib.py are available in the same directory.

Logic
-----

The algorithm for the program is captured in 'Algorithm.txt'.
   
Execution
---------

cd <working_dir_containing_scripts>
python subq_main.py

Output
------

1) Output is directed to terminal.
2) debug_subq_main.log is a debug log which can be ignored.



Limitations
-----------

There are known bugs which have been documented in the header of the main program(subq_main.py)
