# List of arrays used for parsing
subq_start_array = ["(", "select"]
subq_exists_array = ["select", "in", "not in", "exists", "between", "with", "from"]
subq_alias_start_array = [" ", ")"]
tab_alias_sep_array = [","]
join_start_array = ["where", "and"]
join_sep_array = ["=", "!=", "<>", ">", ">=", "<", "<=", "join on and", "join on where", "join using", "cross join"]
join_type_array = ["inner", "left", "left outer", "right", "right outer", "full", "full outer"]