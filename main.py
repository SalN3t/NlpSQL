# Natural Language Toolkit: Form Completion
#
# Copyright (C) 2001-2017 NLTK Project
# Authors: Salah Alarfaj <salah01@gmail.com>
# URL: <http://nltk.org/>

# a translation table used to convert things you say into things the
# computer says back, e.g. "I am" --> "you are"

from __future__ import print_function
from chatbot_util import Chat, reflections

# a table of response pairs, where each pair consists of a
# regular expression, and a list of possible responses,
# with group-macros labelled as %1, %2.

pairs = (

    (r'name (.*)',
   ('Hello##username##! type your question.. or type help',
   'Hey there##username##! type your question.. or type help for options')),

  (r'(\bwhat|\bwhich|\bhow|\bwho|\bhow|\bwhat\'s|\bwhich|\'s\bhow\'s|\bwho\'s|\bhow\'s) (.*)',
   ('Ok ##username##! Let me think ... \n Cool! your sql statment is: \n\n ##sql_statment## \n\n ##sql_result##',
   'Cool! your sql statment is: \n\n ##sql_statment## \n\n.. hmm here is the result for that: \n\n ##sql_result##')),

 (r'help',
  ( "You can ask me questions like:"
        "\n\t * What is the average salary?"
        "\n\t * What is the average salary in development departments?"
        "\n\t * What is the minimum salary?"
        "\n\t * How many employees in development department?"
        "\n\t * Who is the highest paid employee?"
        "\n\t * Who is the highest paid employee in development department?"
        "\n\t * Which employee has last name Facello?",
    "I could help you with:" 
        "\n\t * What is the average salary?"
        "\n\t * What is the average salary in development departments?"
        "\n\t * What is the max salary?"
        "\n\t * How many employees in development department?"
        "\n\t * Who is the highest paid employee?"
        "\n\t * Who is the highest paid employee in development department?"
        "\n\t * Which employee with first name Guana?",
        )),

  (r'quit',
  ( "Thank you for talking with me##username##.",
    "Good-bye##username##.",
    "Thank you, Have a good day!")),

  (r'(.*)',
  ( "##username## I didn\'t understand! Please ask a question!",
    "##username## That seems off topic. Please ask a question with which, what, who or how.",
    "I see, I don\'t have that in my database, can you make sure to use the correct format as directed."))
)

form_chat = Chat(pairs, reflections)

def form_chatbot():
    form_chat.converse()


def demo():
  form_chatbot()


if __name__ == "__main__":
    demo()
