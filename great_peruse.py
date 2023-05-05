import re
from typing import IO, Tuple, List, Dict


class Book:
    def __init__(self, title: str,
                 author: str,
                 my_rating: int,
                 avg_rating: float,
                 tags: [],
                 shelf: str,
                 percent_read: int,
                 my_review: str,):
        self.title = title
        self.author = author
        self.my_rating = my_rating
        self.avg_rating = avg_rating
        self.tags = tags
        self.shelf = shelf
        self.percent_read = percent_read
        self.my_review = my_review


def main_menu() -> str:
    print("\n1. Add a book to your collection")
    print("2. Search your collection")
    print("3. Done")
    return input("\nWhat would you like to do? ")


def book_error() -> None:
    print("Oops! That is not one of the provided options.")
    print("Please answer using one of the provided options.")


def num_error() -> None:
    print("Please select a number from the menu.")


def yn_error() -> None:
    print("Please select one of the given options (y for yes, n for no).")


def print_book_info(book: Book) -> None:
    print("\nHere's the information we have on " + book.title)
    print("Author: " + book.author)
    print("Shelf: " + book.shelf)
    if book.shelf == "currently-reading":
        print("Percent read: " + str(book.percent_read) + "%")
    print("Tags (e.g. ya, chick lit, horror): " + ''.join(map(str, book.tags)))
    # print("Tags (e.g. ya, chick lit, horror): " + str(book.tags))
    print("Rating (1-5): " + str(book.my_rating))
    print("Review: " + book.my_review)

def update_book_info(book: Book) -> None:
    select = input("\nWould you like to update information about the book? (y for yes, n for no) ")
    while select:
        if select.upper() == "Y" or select.upper() == "N":
            if select.upper() == "Y":
                print("\n1. Tags")
                print("2. Rating")
                print("3. Review")
                print("4. Exclusive Shelf")
                print("5. Percentage Read")
                choice = input("\nWhat would you like to update? ")
                while choice:
                    if choice == "1" or "2" or "3" or "4" or "5":
                        if choice == "1":
                            # add functions for adding & removing tags
                            book.tags = (input("Tags (e.g. young adult, chick lit, horror): ")).split(', ')
                        elif choice == "2":
                            rating = input("Rating (1-5): ")
                            while not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
                                print("Please input a value within in the range of 1-5.")
                                rating = input("Rating (1-5): ")
                            book.my_rating = rating
                        elif choice == "3":
                            book.my_review = input("Review: ")
                        elif choice == "4":
                            shelf = input("Shelf (to-read, currently-reading, or read): ")
                            while shelf:
                                if shelf.lower() == "to-read" or "currently-reading" or "read":
                                    book.shelf = shelf.lower()
                                    break
                                else:
                                    print("Please input one of the provided options.")
                                    shelf = input("Shelf (to-read, currently-reading, or read): ")
                        elif choice == "5":
                            percent_read = input("Percentage Read: ")
                            while not percent_read.isdigit() or int(percent_read) < 0 or int(percent_read) > 100:
                                print("Please input an integer within in the range of 0-100.")
                                percent_read = input("Percentage Read: ")
                            book.percent_read = int(percent_read)
                        break
                    else:
                        num_error()
                        choice = input("\nWhat would you like to update? ")
                select = input("\nWould you like to update information about the book? (y for yes, n for no) ")
            else:
                break
        else:
            yn_error()
            select = input("\nWould you like to update information about the book? (y for yes, n for no) ")

    print_book_info(book)

def num_select_action(library_list: List[Book]) -> str:
    response = main_menu()
    while response:
        if response == "1":
            # Add a book to your collection
            add_book(library_list)
            break
        elif response == "2":
            # Search your collection
            search_book(library_list)
            break
        elif response == "3":
            return "Exit"
        else:
            num_error()
            response = input("What would you like to do? ")
    return "Continue"


def anything_else() -> str:
    select = input("Anything else I can do for you? (y for yes, n for no) ")
    while select:
        if select.upper() == "Y" or select.upper() == "N":
            return select
        else:
            yn_error()


def add_book(library_list: List[Book]) -> None:
    print("\n1. To-read")
    print("2. Currently-reading")
    print("3. Read")
    select = input("\nWhich shelf would you like to add a book to? ")

    overwrite_flag = 1

    while select:
        if (select == "1") or (select == "2") or (select == "3"):
            print("Please input the following information: ")
            book_title = input("Book Title: ")
            author = input("Author: ")
            tags = input("Tags (e.g. young adult, chick lit, horror): ").split()
            ind = 0
            for book in library_list:
                if book.author.upper() == author.upper() and book.title.upper() == book_title.upper():
                    print("\nOops! That book is already in your library!")
                    update_book_info(library_list[ind])
                    overwrite_flag = 0
                ind += 1
            break
        else:
            num_error()
            select = input("\nWhich shelf would you like to add a book to? ")

    if overwrite_flag:
        if select == "1":
            new = Book(book_title, author, 0.0, 0.0, tags, "to-read", 0, "")
        elif select == "2":
            percent_read = input("What percentage of the book have you read so far? ")
            while not percent_read.isdigit() or int(percent_read) < 0 or int(percent_read) > 100:
                print("Please input an integer within in the range of 0-100.")
                percent_read = input("What percentage of the book have you read so far? ")
            new = Book(book_title, author, 0.0, 0.0, tags, "currently-reading", int(percent_read), "")
        elif select == "3":
            rating = input("Rating (1-5): ")
            while not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
                print("Please input a value within in the range of 1-5.")
                rating = input("Rating (1-5): ")
            review = input("Review: ")
            new = Book(book_title, author, int(rating), 0.0, tags, "read", 100, review)

        library_list.append(new)
        print_book_info(new)
    # save_changes(library_list)


def search_book(library_list: List[Book]) -> None:
    search = input("Search: ")
    count = 0
    print("\nHere's what we found: ")
    search_dict = {}
    ind = 0
    for book in library_list:
        if book.author.upper() == search.upper() or book.title.upper() == search.upper():
            count += 1
            search_dict[count] = ind
            print(f"{count}. {book.title} by {book.author}")
        ind += 1

    # print(search_dict)
    choice = input("\nWhich book would you like to look at? ")
    while choice:
        if int(choice) in search_dict:
            break
        else:
            num_error()
            choice = input("Which book would you like to look at? ")

    print_book_info(library_list[search_dict[int(choice)]])
    update_book_info(library_list[search_dict[int(choice)]])


def open_file() -> IO:
    file_name = "greatperuse_library_read.csv"
    file_pointer = None
    while file_pointer is None:
        try:
            file_pointer = open(file_name, 'r')
        except IOError:
            print(f"An error occurred while opening the file {file_name}.\n"
                  f"Make sure the file path and name are correct \nand that "
                  f"the file exist and is readable.")

    return file_pointer


def create_library_list(library_fp: IO) -> List[Book]:
    library = []
    # library_fp.readline()
    line = library_fp.readline()

    # splits string by comma delimiter unless delimiter is in quotation marks
    library_list = [[]]
    quote = None
    for c in line:
        if c == "'" or c == '"':
            if c == quote:
                quote = None
            elif quote is None:
                quote = c
        elif c == ',':
            if quote is None:
                library_list.append([])
                continue
        library_list[-1].append(c)
    library_list = [''.join(line) for line in library_list]

    while line is not None and len(library_list) > 6:
        title = library_list[0]
        author = (library_list[1])
        my_rating = library_list[2]
        avg_rating = library_list[3]
        bookshelves = library_list[4]
        exclusive_shelf = library_list[5]
        percent_read = library_list[6]
        try:
            my_review = library_list[7]
        except IndexError:
            my_review = ""

        library.append(Book(title, author, my_rating, avg_rating, bookshelves, exclusive_shelf, percent_read, my_review))
        line = library_fp.readline()

        # splits string by comma delimiter unless delimiter is in quotation marks
        library_list = [[]]
        quote = None
        for c in line:
            if c == "'" or c == '"':
                if c == quote:
                    quote = None
                elif quote is None:
                    quote = c
            elif c == ',':
                if quote is None:
                    library_list.append([])
                    continue
            library_list[-1].append(c)
        library_list = [''.join(line) for line in library_list]

    return library


def save_changes(library_list: List[Book]) -> None:
    file_name = "greatperuse_library_write.csv"
    with open(file_name, "w") as file_pointer:
        for book in library_list:
            file_pointer.write(f"{book.title},{book.author},{book.my_rating},{book.avg_rating},{book.tags},"
                               f"{book.shelf},{book.percent_read},{book.my_review}")
    print("All changes have been saved.")
    file_pointer.close()


def initialization() -> Tuple[List[Book]]:
    library_fp = open_file()
    library_list = create_library_list(library_fp)

    library_fp.close()
    return library_list


def main():
    print("Welcome to GreatPeruse!")
    library_list = initialization()

    action = "Continue"
    more = "Y"
    while action != "Exit" and more.upper() == "Y":
        action = num_select_action(library_list)
        more = anything_else()

    save_changes(library_list)
    print("Thanks for choosing GreatPeruse! Have a great day!")


if __name__ == "__main__":
    main()