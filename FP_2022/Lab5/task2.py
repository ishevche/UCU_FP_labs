class Book:
    """
    Represents a book
    """

    def __init__(self, name, author, pages):
        self.name = name
        self.author = author
        self.pages = pages
        self.cur_page = 1
        self.bookmark = None

    def turn_page(self, amount: int):
        """
        Turns current page amount times
        """
        if amount > 0:
            self.cur_page = min(self.cur_page + amount, self.pages)
        else:
            self.cur_page = max(self.cur_page + amount, 1)

    def get_current_page(self):
        """
        Returns current page
        """
        return self.cur_page

    def get_bookmarked_page(self):
        """
        Returns bookmarked page
        """
        return self.bookmark

    def place_bookmark(self):
        """
        Places bookmark on current page
        """
        self.bookmark = self.cur_page

    def turn_to_bookmark(self):
        """
        Turns to bookmarked page
        """
        if self.bookmark is not None:
            self.cur_page = self.bookmark

    def remove_bookmark(self):
        """
        Removes bookmark
        """
        self.bookmark = None

    def __str__(self):
        bookmark = '' if self.bookmark is None \
            else f", page {self.bookmark} bookmarked"
        pages = 'pages' if self.pages > 1 else 'page'

        return f'Book<{self.name} by {self.author}: {self.pages} {pages}, ' \
               f'currently on page {self.cur_page}{bookmark}>'

    def __eq__(self, other):
        return (self.name == other.name and
                self.author == other.author and
                self.pages == other.pages and
                self.cur_page == other.cur_page and
                self.bookmark == other.bookmark)


def test_book_class():
    print("Testing Book class...", end="")
    # A Book has a title, and author, and a number of pages.
    # It also has a current page, which always starts at 1. There is no page 0!
    book1 = Book("Harry Potter and the Sorcerer's Stone",
                 "J. K. Rowling", 309)
    assert (str(book1) == "Book<Harry Potter and the Sorcerer's Stone by " +
            "J. K. Rowling: 309 pages, currently on page 1>")
    book2 = Book("Carnegie Mellon Motto", "Andrew Carnegie", 1)
    assert (str(book2) == "Book<Carnegie Mellon Motto by Andrew Carnegie: " +
            "1 page, currently on page 1>")

    # You can turn pages in a book. Turning a positive number of pages moves
    # forward; turning a negative number moves backwards. You can't move past
    # the first page going backwards or the last page going forwards
    book1.turn_page(4)  # turning pages does not return
    assert (book1.get_current_page() == 5)
    book1.turn_page(-1)
    assert (book1.get_current_page() == 4)
    book1.turn_page(400)
    assert (book1.get_current_page() == 309)
    assert (str(book1) == "Book<Harry Potter and the Sorcerer's Stone by " +
            "J. K. Rowling: 309 pages, currently on page 309>")
    book2.turn_page(-1)
    assert (book2.get_current_page() == 1)
    book2.turn_page(1)
    assert (book2.get_current_page() == 1)

    # You can also put a bookmark on the current page. This lets you turn
    # back to it easily. The book starts out without a bookmark.
    book3 = Book("The Name of the Wind", "Patrick Rothfuss", 662)
    assert (str(book3) == "Book<The Name of the Wind by Patrick Rothfuss: " + \
            "662 pages, currently on page 1>")
    assert (book3.get_bookmarked_page() is None)
    book3.turn_page(9)
    book3.place_bookmark()  # does not return
    assert (book3.get_bookmarked_page() == 10)
    book3.turn_page(7)
    assert (book3.get_bookmarked_page() == 10)
    assert (book3.get_current_page() == 17)
    assert (str(book3) == "Book<The Name of the Wind by Patrick Rothfuss: " + \
            "662 pages, currently on page 17, page 10 bookmarked>")
    book3.turn_to_bookmark()
    assert (book3.get_current_page() == 10)
    book3.remove_bookmark()
    assert (book3.get_bookmarked_page() == None)
    book3.turn_page(25)
    assert (book3.get_current_page() == 35)
    book3.turn_to_bookmark()  # if there's no bookmark, don't turn to a page
    assert (book3.get_current_page() == 35)
    assert (str(book3) == "Book<The Name of the Wind by Patrick Rothfuss: " + \
            "662 pages, currently on page 35>")

    # Finally, you should be able to compare two books directly
    book5 = Book("A Game of Thrones", "George R.R. Martin", 807)
    book6 = Book("A Game of Thrones", "George R.R. Martin", 807)
    book7 = Book("A Natural History of Dragons", "Marie Brennan", 334)
    book8 = Book("A Game of Spoofs", "George R.R. Martin", 807)
    assert (book5 == book6)
    assert (book5 != book7)
    assert (book5 != book8)
    book5.turn_page(1)
    assert (book5 != book6)
    book5.turn_page(-1)
    assert (book5 == book6)
    book6.place_bookmark()
    assert (book5 != book6)
    print("Done!")

#
# if __name__ == '__main__':
#     test_book_class()
