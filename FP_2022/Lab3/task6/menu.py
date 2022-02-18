'''
Created on Sep 2, 2015

@author: Sameer Adhikari
'''
import abc, sys
from task6.book import Notebook
from task6.note import Note

class Menu(object):
    '''Abstract class for the interface that the  
    user has to work with notebooks and notes.
    The interface will vary between a CLI and GUI.
    This class enforces the methods to implement.
    '''
    __metaclass__ = abc.ABCMeta

    def __init__(self, notebook=None, choices={}):
        '''Initializes a menu with an empty task6
        and the options available to work with it.
        '''
        self.notebook = notebook
        self.choices = choices
        
    @abc.abstractmethod
    def display_menu(self):
        '''Displays the menu to the user.
        Returns the choice as string.
        '''
        
    @abc.abstractmethod
    def display_notes(self):
        '''Displays the notes to the user. 
        '''
        
    @abc.abstractmethod
    def search_notes(self):
        '''Asks the user for a search pattern.
        Displays any matching note found.
        '''
        
    @abc.abstractmethod
    def add_new_note(self):
        '''Modifies the text and tags for a note.
        '''
    @abc.abstractmethod
    def modify_note(self):
        '''Modifies the text and tags for a note.
        '''
    
    def run(self):
        '''Display the menu and respond to choices
        '''
        while True:
            choice = self.display_menu()
            if choice in self.choices:
                action = self.choices[choice]
                print('\t{0} is a valid choice'.format(choice))
                action()
            else:
                print('\t{0} is not a valid choice'.format(choice))
            
    def quit(self):
        '''Exit from the task6.
        '''
        print('\tGoodbye!')
        sys.exit(0)