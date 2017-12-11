# Natural Language Toolkit: Chatbot Utilities
#
# Copyright (C) 2001-2017 NLTK Project
# Authors: Steven Bird <stevenbird1@gmail.com>
#          Salah Alarfaj <salah01@gmail.com>
# URL: <http://nltk.org/>

from __future__ import print_function

import re
import random

from six.moves import input
from tkinter import *
from ScrolledText import *

import parser
import mySql_demon 

reflections = {
  "i am"       : "you are",
  "i was"      : "you were",
  "i"          : "you",
  "i'm"        : "you are",
  "i'd"        : "you would",
  "i've"       : "you have",
  "i'll"       : "you will",
  "my"         : "your",
  "you are"    : "I am",
  "you were"   : "I was",
  "you've"     : "I have",
  "you'll"     : "I will",
  "your"       : "my",
  "yours"      : "mine",
  "you"        : "me",
  "me"         : "you"
}

class Chat(object): 
    def __init__(self, pairs, reflections={}):
        """
        Initialize the chatbot.  Pairs is a list of patterns and responses.  Each
        pattern is a regular expression matching the user's statement or question,
        e.g. r'I like (.*)'.  For each such pattern a list of possible responses
        is given, e.g. ['Why do you like %1', 'Did you ever dislike %1'].  Material
        which is matched by parenthesized sections of the patterns (e.g. .*) is mapped to
        the numbered positions in the responses, e.g. %1.

        :type pairs: list of tuple
        :param pairs: The patterns and responses
        :type reflections: dict
        :param reflections: A mapping between first and second person expressions
        :rtype: None
        """
        # DB Connection
        self.db = mySql_demon.DB()
        self._keywords = ['name']
        self._data_arr = []
        self._pairs = [(re.compile(x, re.IGNORECASE),y) for (x,y) in pairs]
        self._reflections = reflections
        self._regex = self._compile_reflections()


    def _compile_reflections(self):
        sorted_refl = sorted(self._reflections.keys(), key=len,
                reverse=True)
        return  re.compile(r"\b({0})\b".format("|".join(map(re.escape,
            sorted_refl))), re.IGNORECASE)

    def _substitute(self, str):
        """
        Substitute words in the string, according to the specified reflections,
        e.g. "I'm" -> "you are"

        :type str: str
        :param str: The string to be mapped
        :rtype: str
        """

        return self._regex.sub(lambda mo:
                self._reflections[mo.string[mo.start():mo.end()]],
                    str.lower())

    def _wildcards(self, response, match, sent = ''):
        pos = response.find('%')
        while pos >= 0:
            num = int(response[pos+1:pos+2])
            response = response[:pos] + \
                self._substitute(match.group(num)) + \
                response[pos+2:]
            pos = response.find('%')
        if len(self._data_arr) > 0:
            response = response.replace('##username##', self._data_arr[0])
            if parser.is_question(sent) > 0:
                try:
                    sql_statment = parser.parse_sent(sent)
                    response = response.replace('##sql_statment##', sql_statment)
                    response = response.replace('##sql_result##', self.db.query_pretty(sql_statment))
                    
                except Exception as e:
                   # response = str('That seems off topic! Please type help to see some questions that I can help with.')
                    response = str(e)
            
        else:
            response = "Please Enter your name using the format name {your name}. Example: name John Due"
        return response

    def respond(self, str):
        """
        Generate a response to the user input.

        :type str: str
        :param str: The string to be mapped
        :rtype: str
        """
        # Store user input
        if any(x in str for x in self._keywords):
            self._data_arr.append(str.replace('name', ''))
        # check each pattern
        for (pattern, response) in self._pairs:
            match = pattern.match(str)

            # did the pattern match?
            if match:
                resp = random.choice(response)    # pick a random response
                resp = self._wildcards(resp, match, str) # process wildcards

                # fix munged punctuation at the end
                if resp[-2:] == '?.': resp = resp[:-2] + '.'
                if resp[-2:] == '??': resp = resp[:-2] + '?'
                return resp

    # Hold a conversation with a chatbot -- USING GUI Interface
    def get_input(self, event):
        try: user_input = self.entry.get()
        except EOFError:
            print(user_input)
        if user_input.lower() == "quit":
            sys.exit(0)
        elif user_input:
                while user_input[-1] in "!.": user_input = user_input[:-1]
                response = self.respond(user_input)
                self.textPad.insert(INSERT, "\nYou > "+user_input+"\nChatbot > " + str(response) + "\n")
                self.textPad.see(END)
                self.entry.delete(0, 'end')
                response = ''
                user_input = ''

       
    def converse(self, quit="quit"):
        self.root = Tk(className=" NLP To SQL (QA)")
  
        # --- put frame in canvas ---
        width_window, height_window = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry('%dx%d+0+0' % (width_window,height_window))

        # Scroll text Model
        self.entry = Entry(self.root,  width=width_window)
        
        self.entry.bind("<Return>", self.get_input)
        self.entry.pack(side = BOTTOM, ipady=10 )

        self.textPad = ScrolledText(self.root, width=width_window, height = height_window)
        self.textPad.pack(side="left", fill="both", expand=True)

        self.textPad.insert(INSERT, "NLP Chatbot database QA System\n--------")
        self.textPad.insert(INSERT, "\nTalk to the program by typing in plain English, using normal upper-")
        self.textPad.insert(INSERT, "\nand lower-case letters and punctuation.  Enter 'quit' when done.\n")
        self.textPad.insert(INSERT, '='*72)
        self.textPad.insert(INSERT, "\n\nChatbot >Please Enter your name using the format name {your name}. Example: name John Due")

        self.root.mainloop()

