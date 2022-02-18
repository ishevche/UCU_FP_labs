'''
Created on Aug 30, 2015

@author: Sameer Adhikari
'''
import datetime

# the id available for the next note
available_id = 0

class Note(object):
    '''Represent a note in the task6.
    Match against a string in searches.
    Store tags for each note.
    '''
    def __init__(self, note_text, note_tags=''):
        '''Initialize a note with a note_text and optional note_tags.
        Automatically assign an id and creation date.
        '''
        global available_id
        self.note_text = note_text
        self.note_tags = note_tags
        self.note_id = available_id
        available_id += 1
        self.creation_date = datetime.date.today()
        return
    
    def contains(self, search_string):
        '''Determines if the note contains the search_string.
        Check both the note_text and note_tags for the presence 
        of the search_string as a sub string in the note.
        The search is case-sensitive.
        '''
        return search_string in self.note_text or search_string in self.note_tags
    
    def __str__(self):
        '''String representation of the object
        '''
        return('Note Id = {0}, Date = {1}, Text = {2}, Tags = {3}'
              .format(self.note_id, self.creation_date, self.note_text, self.note_tags))    
        
    __repr__ = __str__

if __name__ == '__main__':
    n1 = Note('first hello')
    n2 = Note('second_hello') 
    print('n1 id = {0}'.format(n1.note_id))       
    print('n2 id = {0}'.format(n2.note_id))      
    print(n1.contains('hello')) 
    print(n2.contains('again')) 
