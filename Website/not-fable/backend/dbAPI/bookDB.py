from models.models import *
from mongoengine import ValidationError

def createBook(google_id: str, title: str):
    try:
        if len(title.strip()) == 0:
            return False, None, "Title cannot be empty"
        existing_book = Book.objects(google_id=google_id).first()
        if existing_book:
            return False, None, "Book already exists"
        
        book = Book(google_id=google_id, title=title)
        book.save()
        return True, str(book.id), None
    except ValidationError as e:
        return False, None, f"Validation error: {str(e)}"
    except Exception as e:
        return False, None, "Internal server error"
    
def addBookRating(google_id: str, user_id: str, rating: int):
    try:
        if rating is None:
            return False, None, "Missing required fields"
        user = User.objects(id=user_id).first()
        if not user:
            return False, None, "User not found"
        
        book = Book.objects(google_id=google_id).first()
        if not book:
            return False, None, "Book not found"
    
        existing_rating = Rating.objects(google_id=google_id, user=user).first()
        if existing_rating:
            existing_rating.update(set__rating=rating)
            rating_obj = existing_rating
        else:
            rating_obj = Rating(google_id=google_id, user=user, rating=rating)
            rating_obj.save()
            Book.objects(google_id=google_id).update(push__ratings=rating_obj)
        return True, str(rating_obj.id), None
    except ValidationError as e:
        return False, None, f"Validation error: {str(e)}"
    except Exception as e:
        return False, None, "Internal server error"
    
def removeBookRating(google_id: str, user_id: str):
    try:
        user = User.objects(id=user_id).first()
        if not user:
            return False, None, "User not found"
        book = Book.objects(google_id=google_id).first()
        if not book:
            return False, None, "Book not found"
        rating_obj = Rating.objects(google_id=google_id, user=user).first()
        if not rating_obj:
            return False, None, "No rating found to remove"
        Book.objects(google_id=google_id).update(pull__ratings=rating_obj)
        rating_obj.delete()
        return True, None, None
    except Exception as e:
        return False, None, "Internal server error"
    
def getBook(google_id: str):
    try:
        book = Book.objects(google_id=google_id).first()
        if not book:
            return False, None, "Book not found"
        return True, book, None
    except Exception as e:
        return False, None, "Internal server error"
    
def getBookRatings(google_id: str):
    try:
        book = Book.objects(google_id=google_id).first()
        if not book:
            return False, None, "Book not found"
        avg = 0
        for review in book.reviews:
            avg = (avg + int(review.rating))
        if len(book.reviews) == 0:
            pass
        else:
            avg = avg / len(book.reviews)
        return True, avg, None
    except Exception as e:
        return False, None, "Internal server error"

def getBookReviews(google_id: str):
    try:
        book = Book.objects(google_id=google_id).first()
        if not book:
            return False, None, "Book not found"
        
        reviews_data = []
        for review in book.reviews:
            reviews_data.append({
                "id": str(review.id),
                "user": {
                    "id": str(review.user.id),
                    "username": review.user.username
                },
                "heading": review.heading,
                "content": review.content,
                "rating": review.rating,
                "date": review.date.strftime('%Y-%m-%d') if review.date else None
            })
        
        return True, reviews_data, None
    except Exception as e:
        print(f"Error in getBookReviews: {str(e)}")
        return False, None, "Internal server error"

def getUserBookRating(google_id: str, user_id: str):
    try:
        user = User.objects(id=user_id).first()
        if not user:
            return False, None, "User not found"
            
        rating = Rating.objects(google_id=google_id, user=user).first()
        if not rating:
            return False, None, "No rating found of this user"
            
        rating_data = {
            "rating": rating.rating,
            "user_id": str(user.id),
            "google_id": rating.google_id
        }
        return True, rating_data, None
    except Exception as e:
        print(f"Error in getUserBookRating: {str(e)}")
        return False, None, "Internal server error"

def getUserBookReview(google_id: str, user_id: str):
    try:
        user = User.objects(id=user_id).first()
        if not user:
            return False, None, "User not found"
            
        book = Book.objects(google_id=google_id).first()
        if not book:
            return False, None, "Book not found"
            
        user_review = None
        for review in book.reviews:
            if str(review.user.id) == user_id:
                user_review = review
                break
                
        if not user_review:
            return False, None, "No review found for this user"
            
        review_data = {
            "id": str(user_review.id),
            "heading": user_review.heading,
            "content": user_review.content,
            "rating": user_review.rating,
            "date": user_review.date.strftime('%Y-%m-%d') if user_review.date else None
        }
        return True, review_data, None
    except Exception as e:
        print(f"Error in getUserBookReview: {str(e)}")
        return False, None, "Internal server error"