import datetime
import json
import os

class Library:
    def __init__(self):
       
        self.books = self.load_books()
        self.lent_books = self.load_lent_books()

    def load_books(self):
      
        if os.path.exists("books.json"):
            with open("books.json", "r") as file:
                return json.load(file)
        else:
          
            return {
                "Harry Potter": {"quantity": 5},
                "The Great Gatsby": {"quantity": 3},
                "1984": {"quantity": 2}
            }

    def load_lent_books(self):
        """Load the lent books data from a JSON file"""
        if os.path.exists("lent_books.json"):
            with open("lent_books.json", "r") as file:
                return json.load(file)
        else:
            return {}

    def save_books(self):
        
        with open("books.json", "w") as file:
            json.dump(self.books, file, indent=4)

    def save_lent_books(self):
        """Save lent books data to file"""
        with open("lent_books.json", "w") as file:
            json.dump(self.lent_books, file, indent=4)

    def lend_book(self):
  
        print("Available Books:")
        for book, details in self.books.items():
            print(f"{book}: {details['quantity']} available")
        
        book_title = input("Enter the title of the book you want to borrow: ").strip()
        
        if book_title not in self.books:
            print("This book is not available in our library.")
            return
        
        if self.books[book_title]["quantity"] <= 0:
            print("There are not enough books available to lend.")
            return


        borrower_name = input("Enter your name: ").strip()
        borrower_phone = input("Enter your phone number: ").strip()
        
        due_date_str = input("Enter the due date for the return (yyyy-mm-dd): ").strip()
        try:
            due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use yyyy-mm-dd.")
            return
        
    
        self.books[book_title]["quantity"] -= 1
        self.lent_books[borrower_name] = {
            "phone": borrower_phone,
            "book_title": book_title,
            "due_date": due_date.strftime("%Y-%m-%d")
        }
        
        self.save_books()
        self.save_lent_books()
        print(f"The book '{book_title}' has been lent to {borrower_name}. Due date: {due_date.strftime('%Y-%m-%d')}")

    def return_book(self):
        """Handle the book return operation"""
        borrower_name = input("Enter your name to return a book: ").strip()

        if borrower_name not in self.lent_books:
            print(f"No borrow record found for {borrower_name}.")
            return
        
        lend_info = self.lent_books[borrower_name]
        book_title = lend_info["book_title"]
        
        del self.lent_books[borrower_name]
        self.books[book_title]["quantity"] += 1
        
        self.save_books()
        self.save_lent_books()
        print(f"The book '{book_title}' has been returned. Thank you!")

    def display_menu(self):
        """Display the menu and handle user input"""
        while True:
            print("\nLibrary Management CLI")
            print("1. Lend Book")
            print("2. Return Book")
            print("3. Exit")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.lend_book()
            elif choice == "2":
                self.return_book()
            elif choice == "3":
                print("Exiting the Library Management System.")
                break
            else:
                print("Invalid choice. Please try again.")
