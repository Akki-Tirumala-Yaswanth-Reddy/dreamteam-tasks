from models.models import *
from dbAPI.bookDB import *


# These functions are used to properly format the return data.
def struct_book(book):
    return {
        'id': str(book.id),
        'google_id': book.google_id,
        'title': book.title
    }

def struct_list(reading_list):
    return {
        'id': str(reading_list.id),
        'name': reading_list.name,
        'user': {
            'id': str(reading_list.user.id),
            'username': reading_list.user.username
        },
        'books': [struct_book(book) for book in reading_list.books],
        'book_count': len(reading_list.books)
    }

def createList(name: str, user_id: str):
    try:
        if not all([name, user_id]):
            return False, None, "Name and user_id cant be empty"
        
        user = User.objects(id=user_id).first()
        if not user:
            return False, None, "User not found"
        
        existing_list = ReadingList.objects(name=name, user=user).first()
        if existing_list:
            return False, None, "List with this name already exists"
        
        reading_list = ReadingList(name=name, user=user)
        reading_list.save()

        return True, struct_list(reading_list), None
        
    except Exception as e:
        return False, None, f"Server error: {str(e)}"
      

def addBookToList(list_id: str, google_id: str, title: str):
    try:
        if not all([list_id, google_id, title]):
            return False, None, "Required fields are empty"
        
        reading_list = ReadingList.objects(id=list_id).first()
        if not reading_list:
            return False, None, "Could not find the list"

        book = Book.objects(google_id=google_id).first()
        if not book:
            ok, book_data, err = createBook(google_id=google_id, title=title)
            if not ok:
                return False, None, f"Could not create the book: {err}"
            book = Book.objects(google_id=google_id).first()
        
        if book in reading_list.books:
            return False, None, "Book is already in the list"
        
        reading_list.update(push__books=book)
        updated_list = ReadingList.objects(id=list_id).first()
        
        return True, struct_list(updated_list), None
    
    except Exception as e:
        return False, None, f"Server error: {str(e)}"
      

def removeBookFromList(list_id: str, google_id: str):
    try:
        if not all([list_id, google_id]):
            return False, None, "Required fields are empty"

        reading_list = ReadingList.objects(id=list_id).first()
        book = Book.objects(google_id=google_id).first()

        if not book:
            return False, None, "Book not found"
        if not reading_list:
            return False, None, "List not found"
        
        reading_list.update(pull__books=book)
        updated_list = ReadingList.objects(id=list_id).first()
        
        return True, struct_list(updated_list), None
        
    except Exception as e:
        return False, None, f"Server error: {str(e)}"
      
def getUserLists(user_id: str):
    try:
        if not user_id:
            return False, None, "User ID is required"
            
        user = User.objects(id=user_id).first()
        if not user:
            return False, None, "Could not find the user"
        
        reading_lists = ReadingList.objects(user=user)
        
        serialized_lists = []
        for reading_list in reading_lists:
            serialized_lists.append(struct_list(reading_list))
        
        return True, serialized_lists, None
            
    except Exception as e:
        print(e)
        return False, None, "Server error"

def getListById(list_id: str):
    try:
        if not list_id:
            return False, None, "Required fields are empty"
            
        reading_list = ReadingList.objects(id=list_id).first()
        if not reading_list:
            return False, None, "Reading list not found"
        
        return True, struct_list(reading_list), None
        
    except Exception as e:
        return False, None, f"Server error: {str(e)}"
    
def deleteList(list_id: str, user_id: str):
    try:
        if not all([list_id, user_id]):
            return False, None, "Required fields are empty"
            
        reading_list = ReadingList.objects(id=list_id).first()
        if not reading_list:
            return False, None, "Could not find reading list"
        
        if str(reading_list.user.id) != user_id:
            return False, None, "Not allowed to delete this list"
        
        reading_list.delete()
        return True, "List deleted successfully", None
        
    except Exception as e:
        return False, None, f"Server error: {str(e)}"