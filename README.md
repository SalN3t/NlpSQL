# NlpSQL
=====

NlpSQL is a question answering system that uses natural language processing to generat SQL statements.
I used `NLTK <http://nltk.org/>` to parse the text and created a parse grammar to build the SQL query.
The goal of the project is to create an easy way for regular to fetch data from the database even if they don't know SQL language.
The database engin used in this project is `MySQL <https://www.mysql.com/>`

License
-------

NlpSQL is free software, released under the MIT
`<https://opensource.org/licenses/MIT>`_.


Requirements
------------
You will need some Python packages

To install dependencies (on a Debian-like GNU/Linux distribution)::
    git clone #project_url#
    cd #project_directory#
    pip install requirements.txt


You will also need to download some NLTK data package. You can do so
executing::

    python -m nltk.downloader genesis maxent_treebank_pos_tagger punkt stopwords averaged_perceptron_tagger

You will also need MySQL database. You can do so if you don't have it by::
    apt-get install mysql

Now you would need to create the databse schema provided. 
A good tutorial `Create a MySQL Database on Linux via Command Line <https://www.liquidweb.com/kb/create-a-mysql-database-on-linux-via-command-line/>`

Please make sure to name the database::
    employees

Ok, Now we will need to papulate the data::
    mysql -u username -p employee < schema.sql

You would need to update the config file to connect to the databse by filling the data::
    nano config.py

Then Change the following::
    db_config = {
        'user': '##username##',
        'passwd': '##password##',
        'host': '##host##',   
        'db': 'employees',
    }

That's it!

Runing
----------
Make sure you filfile the requirements First.

To run::

    python main.py
