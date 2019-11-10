# List of arrays used for parsing
compressed_tokens_array = ['right join', 'inner join', 'left outer join', 'right outer join', 'full outer join', 'cross join', 'natural join', 'order by', 'group by']
joins_tokens_array = ['right join', 'inner join', 'left outer join', 'right outer join', 'full outer join', 'cross join', 'natural join']
between_clause_end_array = ['group by', 'and', ')', 'order by']
alias_end_array = ['group by', 'and', ')', 'order by', 'limit']
order_by_clause_end_array = [';', 'limit', ')']
table_list_eliminate_array = ['join', 'left', 'outer']
join_sep_array = ['=', '!=', '<>', '>', '>=', '<', '<=', 'join on and', 'join on where', 'join using', 'cross join']
join_type_array = ['inner', 'left', 'left outer', 'right', 'right outer', 'full', 'full outer']
subq_start_array = ['(', 'select']
subq_exists_array = ['select', 'in', 'not in', 'exists', 'between', 'with', 'from']
subq_alias_start_array = [' ', ')']
tab_alias_sep_array = [',']
join_start_array = ['where', 'and']
