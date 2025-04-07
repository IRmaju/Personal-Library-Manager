import streamlit as st
import json
import os

class LibraryManager:
    def __init__(self, file_name="library.json"):
        self.file_name = file_name
        self.load_library()

    def load_library(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                self.library = json.load(file)
        else:
            self.library = []

    def save_library(self):
        with open(self.file_name, 'w') as file:
            json.dump(self.library, file, indent=4)

    def add_book(self, title, author, year, progress):
        book = {
            'title': title,
            'author': author,
            'year': year,
            'progress': progress
        }
        self.library.append(book)
        self.save_library()

    def delete_book(self, title):
        for book in self.library:
            if book['title'].lower() == title.lower():
                self.library.remove(book)
                self.save_library()
                return True
        return False

    def search_book(self, title):
        for book in self.library:
            if book['title'].lower() == title.lower():
                return book
        return None

    def update_book(self, title, new_title, new_author, new_year, new_progress):
        for book in self.library:
            if book['title'].lower() == title.lower():
                if new_title:
                    book['title'] = new_title
                if new_author:
                    book['author'] = new_author
                if new_year:
                    book['year'] = new_year
                if new_progress:
                    book['progress'] = new_progress
                self.save_library()
                return True
        return False

    def get_books(self):
        return self.library

    def get_book_progress(self, title):
        for book in self.library:
            if book['title'].lower() == title.lower():
                return book['progress']
        return None


def main():
    st.title("Personal Library Manager")
    
    library_manager = LibraryManager()

    menu = ["Home", "Add Book", "Delete Book", "Search Book", "Update Book", "Show All Books", "Show Progress"]
    choice = st.sidebar.selectbox("Choose an option", menu)

    if choice == "Home":
        st.write("Welcome to the Personal Library Manager")

    elif choice == "Add Book":
        with st.form(key='add_book_form'):
            title = st.text_input("Enter the book title:")
            author = st.text_input("Enter the author's name:")
            year = st.text_input("Enter the publication year:")
            progress = st.text_input("Enter your reading progress (0-100):")
            submit_button = st.form_submit_button("Add Book")
            
            if submit_button:
                library_manager.add_book(title, author, year, progress)
                st.success(f"Book '{title}' added to the library!")

    elif choice == "Delete Book":
        title = st.text_input("Enter the title of the book to delete:")
        if st.button("Delete Book"):
            if library_manager.delete_book(title):
                st.success(f"Book '{title}' deleted from the library!")
            else:
                st.error(f"Book '{title}' not found!")

    elif choice == "Search Book":
        title = st.text_input("Enter the title of the book to search:")
        if st.button("Search"):
            book = library_manager.search_book(title)
            if book:
                st.write(f"Found: {book['title']} by {book['author']} ({book['year']}) - Progress: {book['progress']}%")
            else:
                st.error(f"Book '{title}' not found!")

    elif choice == "Update Book":
        title = st.text_input("Enter the title of the book to update:")
        if title:
            book = library_manager.search_book(title)
            if book:
                new_title = st.text_input(f"New Title (Leave blank to keep '{book['title']}'):", value=book['title'])
                new_author = st.text_input(f"New Author (Leave blank to keep '{book['author']}'):", value=book['author'])
                new_year = st.text_input(f"New Year (Leave blank to keep '{book['year']}'):", value=book['year'])
                new_progress = st.text_input(f"New Progress (Leave blank to keep '{book['progress']}'):", value=book['progress'])
                if st.button("Update Book"):
                    if library_manager.update_book(title, new_title, new_author, new_year, new_progress):
                        st.success(f"Book '{title}' updated!")
                    else:
                        st.error(f"Book '{title}' not found!")
            else:
                st.error(f"Book '{title}' not found!")

    elif choice == "Show All Books":
        books = library_manager.get_books()
        if books:
            for book in books:
                st.write(f"{book['title']} by {book['author']} ({book['year']}) - Progress: {book['progress']}%")
        else:
            st.write("No books in the library.")

    elif choice == "Show Progress":
        title = st.text_input("Enter the title of the book to show progress:")
        if st.button("Show Progress"):
            progress = library_manager.get_book_progress(title)
            if progress is not None:
                st.write(f"Progress of '{title}': {progress}%")
            else:
                st.error(f"Book '{title}' not found!")

if __name__ == "__main__":
    main()
