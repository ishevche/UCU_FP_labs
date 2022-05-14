"""
Palindrome class realization.
"""

from arraystack import ArrayStack


class Palindrome:
    """
    Finds palindromes in files
    """

    @staticmethod
    def read_file(path: str):
        """
        Reads file with words
        """
        words = []
        with open(path, 'r') as input_file:
            for word in input_file:
                word = word.replace('\n', '')\
                    .replace(' +cs=', '').split()[0]
                if not word:
                    continue
                words += [word]
        return words

    @staticmethod
    def write_to_file(path: str, words: list):
        """
        Writes words in file
        """
        with open(path, 'w') as output_file:
            output_file.write('\n'.join(words))

    @staticmethod
    def find_palindromes(input_path: str, output_path: str):
        """
        Search palindromes words in dictionaries
        """
        all_words = Palindrome.read_file(input_path)
        palindrome_words = []
        for word in all_words:
            if Palindrome.is_palindrome(word):
                palindrome_words.append(word)
        Palindrome.write_to_file(output_path, palindrome_words)
        return palindrome_words

    @staticmethod
    def is_palindrome(word: str):
        """
        Checks is word a palindrome
        """
        stack = ArrayStack(word)
        while not stack.isEmpty():
            if stack.pop() != word[0]:
                return False
            word = word[1:]
        return True
