'''
Created on Aug 31, 2015

@author: Sameer Adhikari
'''
from task6.note import Note

class Notebook(object):
    '''
    A collection that allows user to:
    1. Create a new note
    2. Modify the text of an existing note
    3. Tag a note
    4. Search inside the note text and tags
    '''    

    def __init__(self):
        '''
        Initialize a task6 with an empty list of notes
        '''
        self.notes_list = []
        
    def add_new_note(self, note_text, note_tags=''):
        '''Create a new note and add to task6.
        '''
        self.notes_list.append(Note(note_text=note_text, note_tags=note_tags))
        
    def _find_note(self, note_id):
        '''Returns the note with id that matches given one.  
        Currently performs an inefficient linear scan.
        '''
        for note in self.notes_list:
            if note.note_id == note_id:
                return note
        return None

    def get_num_notes(self):
        '''Return the number of notes
        '''
        return len(self.notes_list)
    
    def get_note_text(self, note_id):
        '''Find note with the given id and 
        return its text
        '''
        note = self._find_note(note_id=note_id)  
        return note.note_text
    
    def replace_note_text(self, note_id, note_text):
        '''Find note with the given id and replace
        its text with the given text
        '''
        note = self._find_note(note_id=note_id)  
        note.note_text = note_text
        
    def get_note_tags(self, note_id):
        '''Find note with the given id and 
        return its text
        '''
        note = self._find_note(note_id=note_id)  
        return note.note_tags
    
    def replace_note_tags(self, note_id, note_tags):
        '''Find note with the given id and replace
        its tags with the given tags
        '''
        note = self._find_note(note_id=note_id)  
        note.note_tags = note_tags
    
    def search_notes(self, search_string):
        '''Find all the notes that contain the search string
        '''
        return [note for note in self.notes_list if note.contains(search_string)]
    
    def __str__(self):
        '''Print the task6
        '''
        result = ''
        for note in self.notes_list:
            result += str(note)
            result += '\n'
        return result

    __repr__ = __str__
    
if __name__ == '__main__':
    nb = Notebook()
    nb.add_new_note('hello world', '')
    nb.add_new_note('hello again', '')
    # This for loop assumes that the note ids are 0..N-1
    # Not really top-shelf code, but that is not the aim
    for note_id in range(nb.get_num_notes()):
        note_text = nb.get_note_text(note_id)
        print('Note = {0}, Text = {1}'.format(note_id, note_text))

    notes = nb.search_notes('hello')
    for note in notes:
        print(note.note_text)

    nb.replace_note_text(0, 'hi world')
    print(nb.get_note_text(0))
    
    nb.replace_note_tags(1, 'message, greeting')
    print(nb.get_note_tags(1))
    
    print(64*'=')
    print(nb)
