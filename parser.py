from nltk import load_parser
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, state_union

import re

supported_questions_str_list = ['what','which','how','who']
sen_words = ['between', 'not', 'do']

stop_words = set(stopwords.words("english"))


def parse_sentence(parser_grammer, sent, trace = 0):
    try:
        # 1- if it's a sentence else throw exceptions
        if is_question(sent) < 1:
            return  Exception("Only one questions is allowed, and should be asked using ",supported_questions_str_list,", questions types")
        # 2- senitize it
        sent = senitize_question(sent)
        # More Senitize by removing stop words
        words = word_tokenize(sent)
        sent = ' '.join([w for w in words if not w in stop_words or w in supported_questions_str_list or w in sen_words])

        # 3- parse it
        cp = load_parser(parser_grammer, trace)
        trees = list(cp.parse(sent.split()))

        answer = trees[0].label()['SEM']
        answer = [s for s in answer if s ]

        q = ' '.join(answer)
    except IndexError as e:
        raise e
    return q    # string return 



def organize_sql_statment(sent):
    try:
        sent = sent.replace(" (","(") # Fix min max indexing i.e. MAX (value) raise error.. should be MAX(value)
    except ValueError as e:
        raise e
    qq = re.split("(BREAK_S | BREAK_F | BREAK_W)", sent)


    sen_s = 'SELECT '
    sen_f = 'FROM '
    sen_w = 'WHERE '
    bool_w = False # To check if there is a where clause or not
    
    for item in qq:
        if 'select' in item.lower():
            sen_s += item.lower().replace('select','')+', '
        elif 'from' in item.lower():
            sen_f += str(item.lower().replace('from',''))+', '
        elif 'where' in item.lower():
            bool_w = True
            sen_w += str(item.lower().replace('where',''))+' and '
    if bool_w:
        sql_query = sen_s[:-2]+' '+sen_f[:-2]+' '+sen_w[:-4]
        if 'TMP_1'.lower() in sql_query.lower():
            sql_query = sql_query.replace('TMP_1'.lower(), filter(None, sen_f.split(' '))[1].replace(',','') )
    else:
        sql_query = sen_s[:-2]+' '+sen_f[:-2]
    if 'max' in sql_query.lower():
        tmp = re.split('(\(|\))', sql_query)
        value = tmp[2]
        tmp = tmp[0] +''+tmp[-1]
        if ',' in tmp:
            comma = ','
        else:
            comma = ''
        sql_query = tmp.lower().replace('max', value+comma) + ' order by '+value+' DESC limit 1'
    if 'min' in sql_query.lower():
        tmp = re.split('(\(|\))', sql_query)
        value = tmp[2]
        tmp = tmp[0] +''+tmp[-1]
        if ',' in tmp:
            comma = ','
        else:
            comma = ''
        sql_query = tmp.lower().replace('min', value+comma)+ ' order by '+value+' ASC limit 1'

    return sql_query

    # '''
    # Senitize question from:
    #     * 's clauses
    #     * ?
    # Takes WH sentense and return the sentense after stripping off unwanted charcters
    # # Note only support the supported questions strings
    # SELECT  salary, first_name, last_name, employees.emp_no FROM  salaries,  employees WHERE   employees.emp_no = salaries.emp_no  order by salary desc limit 1
    # '''
def senitize_question(sent):
    sent = sent.replace('?', '').replace("\'s","").replace("\'re","").replace("\n't"," not ")
    return sent

def is_question(sent):
    words = word_tokenize(sent)
    is_q = [w for w in words if w.lower() in supported_questions_str_list ]
    number_of_questions = len(is_q)
    if number_of_questions < 1: # Not a question.. Should start with the supported questions format only
        return -1
    elif number_of_questions > 1: # More than one question
        return 0
    return 1




# Main

parser_grammer = 'grammars/extends.fcfg'


def parse_sent(sent):
    try:
        output = organize_sql_statment(parse_sentence(parser_grammer ,sent))
    except Exception  as e:
        # print '*'*30
        # print str(e)
        raise e
    return output




#######################################################
#     Brain Storming to land into this structure
#                  Some General notes
#######################################################
## MySQL 
## Note: Nested Queries are not supported


## Base Form
# SELECT (Columns names)* FROM (Table names)*

## WHERE Form
# SELECT (Columns names)* FROM (Table names)* [WHERE [Conditions] ]

## Average Form
# SELECT AVG( (Column name) )(Columns names)* FROM (Table names)*
# SELECT AVG( (Column name) )(Columns names)* FROM (Table names)* [WHERE [Conditions] ] ...


## GROUP By Forms
# SELECT (Columns names)* FROM (Table names)* [WHERE [Conditions] ] [GROUP BY (Colmns name)]
# SELECT (Columns names)* FROM (Table names)* [GROUP BY (Colmns name)]

## ORDER BY Forms
# SELECT (Columns names)* FROM (Table names)* [WHERE [Conditions] ] [ORDER BY (Colmns name) (ASC/DESC)]
# SELECT (Columns names)* FROM (Table names)* [WHERE [Conditions] ] [GROUP BY (Colmns name)] [ORDER BY (Colmns name) (ASC/DESC)]

# SELECT (Columns names)* FROM (Table names)* [WHERE [Conditions] ] [GROUP BY (Colmns name)] [ORDER BY (Colmns name) (ASC/DESC)]

###############################
### Conditions

# Col_name (> , =>, <, <=, =) value
# Col_name (> , =>, <, <=, =) value (AND/OR) Col_name (> , =>, <, <=, =) value

#  Col_name LIKE value

#  Col_name IN (value, value, ...)




# sen_words['between', 'not', 'do']
# stop_word

# # Salary qeustions
# What is the average salary?
# ['What', 'average', 'salary', '?']

# What is the average salary in development departments?
# ['What', 'average', 'salary', 'development', 'deparments', '?'

# What is the salary in acending order? 
# ['What', 'salary', 'acending', 'order', '?']

# What is the salary in development deparments in decsinding order?
# ['What', ''salary', 'development', 'deparments', 'decsinding', 'order', '?']

# What is the (maximum/minimum, max/min) salary being paid [in department][using accending/decsinding order]?
# What is the maximum salary being paid ?
# ['What', 'maximum', 'salary', 'paid', '?']

# What is the max salary?
# ['What', 'max', 'salary', 'paid', '?']

# What is the minimum salary?
# ['What', 'minimum', 'salary', 'paid', '?']


# What is the min salary being paid ?
# ['What', 'min', 'salary', 'paid', '?']


# (Skip) what is the highest average salary between departments? (SELECT MAX(avg_sal), dept_no , dept_name  FROM (SELECT AVG(salary) as avg_sal, dept_emp.dept_no  , departments.dept_name FROM salaries, dept_emp, departments where salaries.emp_no = dept_emp.emp_no group by departments.dept_no) as table1)
# ['what', 'highest', 'average', 'salary', 'between', 'departments', '?']

# ------------
# # Departments questions

# (Skip) Which departmnets has the most employees?
# ['Which', 'departmnets', 'most', 'employees', '?']

# (skip) Which departmnets does not have the most employees?
# ['Which', 'departmnets', 'not', 'most', 'employees', '?']

# (skip) Which departments has most paying salaries?
# ['Which', 'departments', 'most', 'paying', 'salaries', '?']

# (skip) Which departments has least paying salaries?
# ['Which', 'departments', 'least', 'paying', 'salaries', '?']

# How many employees in development department?
# (SELECT COUNT(employees.emp_no), dept_name  FROM employees, dept_emp, departments WHERE dept_emp.emp_no = employees.emp_no and departments.dept_name = 'development')
# ['How', 'many', 'employees', 'development', 'department', '?']

# ------------
# # employees questions
# Who is the highest paid employee?
# ['Who', 'highest', 'paid', 'employee', '?']
# (SELECT MAX(salary), first_name, last_name, employees.emp_no FROM salaries, employees where employees.emp_no = salaries.emp_no)

# Who is the highest paid employee in Engeering deparment?
# ['Who', 'highest', 'paid', 'employee', 'Engeering', 'deparment', '?']
# SELECT MAX(salary), first_name, last_name, employees.emp_no, dept_name FROM salaries, employees, departments, dept_emp where employees.emp_no = salaries.emp_no and departments.dept_no = dept_emp.dept_no and dept_emp.emp_no = salaries.emp_no and departments.dept_name= "development"

# Who is the highest paid person?
# ['Who', 'highest', 'paid', 'person', '?'

# Who is the highest paid person in Engeering deparment?
# ['Who', 'highest', 'paid', 'person', 'Engeering', 'deparment', '?']

# (Skip) Which employee has last name ending in stu?
# ['Which', 'employee', 'last', 'name', 'ending', 'stu', '?']

# Which employee has last name Guana?
# ['Which', 'employee', 'last', 'name', 'Guana', '?']
# select * from employees where last_name='Facello'


# Which employee has first name Guana?
# ['Which', 'employee', 'last', 'name', 'Guana', '?']
# select * from employees where first_name='Rimon'

# Which employee has fisrt name starting in stu?
# ['Which', 'employee', 'fisrt', 'name', 'starting', 'stu', '?']


# Which employee has id number 1001?
# ['Which', 'employee', 'id', 'number', '1001', '?']


# what is the first and last name of an employee with id number 1001?
# ['what', 'first', 'last', 'name', 'employee', 'id', 'number', '1001']

# Which department does John Du works at(under)?
# ['Which', 'department', 'John', 'Du', 'works', '(', ')', '?']

# How much does John Du make?
# ['How', 'much', 'John', 'Du', 'make', '?']


# What is John Du title?
# ['What', 'John', 'Du', 'title', '?']

# What does John du do?
# ['What', 'John', 'du', 'do', '?']

# Which employee has CEO title?
# ['Which', 'employee', 'CEO', 'title', '?']


# How many employee has staff title?
# ['How', 'many', 'employee', 'staff', 'title', '?']



# ------------ Type of Q:
# 	- Qantitive
# 	- Singulartive
# 	- Avergeing
# 	- Max/Min


# ------------ SQL operations supported
# 	- SELECT
# 	- FROM
# 	- WHERE
# 	- AVG
# 	- ORDER BY ASC/DESC
# 	- LIKE  (SKIP)
# 	- IN    (SKIP)
# 	- operations(> , < , = )
