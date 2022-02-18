'''
Created on Sep 3, 2015

@author: Sameer Adhikari
'''

from task6.menu import Menu
from task6.book import Notebook

class MenuCLI(Menu):
    '''A class that provides a command line interface for the menu.
    '''


    def __init__(self):
        self.notebook = Notebook()
        self.choices = {
            '1': self.display_notes,
            '2': self.search_notes,
            '3': self.add_new_note,
            '4': self.modify_note,
            '5': self.quit
        }
        Menu.__init__(self, self.notebook, self.choices)

    def display_menu(self):
        '''Displays the menu to the user.
        Returns the choice as string.
        '''
        print('''
        Notebook Menu
        
        1. Display Notes
        2. Search Notes
        3. Add Note
        4. Modify Note
        5. Quit
        ''')
        return input('\tEnter a choice: ')

    def display_notes(self):
        '''Displays the notes to the user. 
        '''
        for note in self.notebook.notes_list:
            print('\n\t{0}'.format(note))

    def search_notes(self):
        '''Asks the user for a search pattern.
        Displays any matching note found.
        '''
        search_string = input('\n\tEnter the string to search for: ')
        matching_notes = self.notebook.search_notes(search_string)
        print('\tThere are {0} notes matching the string "{1}":'.format(len(matching_notes), search_string))
        for note in matching_notes:
            print('\n\t{0}'.format(note))

    def add_new_note(self):
        '''Modifies the text and tags for a note.
        '''
        note_text = input('\n\tEnter the text for the note: ')
        note_tags = input('\tEnter tags for the note: ')
        self.notebook.add_new_note(note_text, note_tags)
        print('\tNote has been added')

    def modify_note(self):
        '''Modifies the text and tags for a note.
        '''
        note_id = int(input('\n\tEnter a note id: '))
        note_text = input('\n\tEnter the text for the note: ')
        note_tags = input('\tEnter tags for the note: ')
        if note_text:
            self.notebook.replace_note_text(note_id, note_text)
        if note_tags:
            self.notebook.replace_note_tags(note_id, note_tags)

if __name__ == '__main__':
    menu_cli = MenuCLI()
    menu_cli.run()
