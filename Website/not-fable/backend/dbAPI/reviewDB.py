from models.models import *
from mongoengine import ValidationError

# Some of the error handling here is done by ai.
# It was same thing again and again, so i used ai to do it.

def struct_comment(comment):
    return {
        'id': str(comment.id),
        'content': comment.content,
        'user': {
            'id': str(comment.user.id),
            'username': comment.user.username
        },
        'date': comment.date.strftime('%Y-%m-%d')
    }

def struct_like_dislike(like_dislike):
    return {
        'value': like_dislike.value,
        'user': {
            'id': str(like_dislike.user.id),
            'username': like_dislike.user.username
        }
    }

def struct_review(review):
    return {
        'id': str(review.id),
        'heading': review.heading,
        'content': review.content,
        'rating': review.rating,
        'user': {
            'id': str(review.user.id),
            'username': review.user.username
        },
        'book': {
            'id': str(review.book.id),
            'google_id': review.book.google_id,
            'title': review.book.title
        },
        'comments': [struct_comment(comment) for comment in review.comments],
        'likesDislikes': [struct_like_dislike(ld) for ld in review.likesDislikes],
        'likes': sum(1 for like in review.likesDislikes if like.value == 1),
        'dislikes': sum(1 for dislikes in review.likesDislikes if dislikes.value == -1),
        'date': review.date.strftime('%Y-%m-%d') if review.date else None
    }

def createReview(user_id: str, google_id: str, heading: str, content: str, rating: str | int):
    try:
        if not all([user_id, google_id, content, heading]):
            return False, None, "Missing required fieds"
        
        if len(content.strip()) == 0:
            return False, None, "Review content cannot be empty"
        
        if len(heading.strip()) == 0:
            return False, None, "Heading content cannot be empty"
        
        if len(str(rating).strip()) == 0:
            return False, None, "Rating cannot be empty"
        
        user = User.objects(id=user_id).first()
        if not user:
            return False, None, "User not found"
        
        book = Book.objects(google_id=google_id).first()
        if not book:
            return False, None, "Book not found"
        
        review = Review(user=user, book=book, heading=heading.strip(), content=content.strip(), rating=str(rating))
        review.save()

        book.update(push__reviews=review)
        
        return True, struct_review(review), None
        
    except ValidationError as e:
        return False, None, f"Validation error: {str(e)}"
    except Exception as e:
        return False, None, "Internal server error"

def changeReview(review_id: str, content: str, user_id: str):
    try:
        if not all([review_id, content]):
            return False, None, "Missing required fields"
        
        if len(content.strip()) == 0:
            return False, None, "Review content cannot be empty"
        
        review = Review.objects(id=review_id).first()
        if not review:
            return False, None, "Review not found"
        
        if user_id != str(review.user.id):
            return False, None, "You are not allowed to change this review"
        
        Review.objects(id=review_id).update(set__content=content)
        return True, None, None
        
    except ValidationError as e:
        return False, None, f"Validation error: {str(e)}"
    except Exception as e:
        return False, None, "Internal server error"
    
def getReview(review_id: str):
    try:
        if not review_id:
            return False, None, "Review ID is required"
        
        review = Review.objects(id=review_id).first()
        if not review:
            return False, None, "Review not found"
        
        return True, struct_review(review), None
        
    except Exception as e:
        return False, None, "Internal server error"
    
def getUserReviews(user_id: str):
    try:
        if not user_id:
            return False, None, "User id is required"
        
        user = User.objects(id=user_id).first()
        reviews = Review.objects(user=user)
        res = []
        for review in reviews:
            res.append(struct_review(review))
        
        if len(res) == 0:
            return False, None, "Reviews not found"
        return True, res, None
    except Exception as e:
        print(e)
        return False, None, str(e)
    
def deleteReview(review_id: str, user_id: str):
    try:
        if not review_id:
            return False, None, "Review ID is required"
        
        review = Review.objects(id=review_id).first()
        if not review:
            return False, None, "Review not found"
        
        if user_id != str(review.user.id):
            return False, None, "You are not allowed to delete this review"
        book = review.book
        if book:
            book.update(pull__reviews=review)
        
        Review.objects(id=review_id).delete()
        return True, "Review deleted successfully", None
        
    except Exception as e:
        return False, None, "Internal server error"
    
def addLike(user_id: str, review_id: str):
    try:
        if not all([user_id, review_id]):
            return False, None, "Missing required fields"
        
        user = User.objects(id=user_id).first()
        if not user:
            return False, None, "User not found"
        
        review = Review.objects(id=review_id).first()
        if not review:
            return False, None, "Review not found"
        
        for i, like_dislike in enumerate(review.likesDislikes):
            if str(like_dislike.user.id) == user_id:
                review.likesDislikes[i].value = 1
                review.save()
                return True, "Updated to like", None
        new_like = LikeDislike(value=1, user=user)
        review.likesDislikes.append(new_like)
        review.save()
        return True, "Added like", None
        
    except ValidationError as e:
        return False, None, f"Validation error: {str(e)}"
    except Exception as e:
        return False, None, "Internal server error"
    
def removeLikeDislike(user_id: str, review_id: str):
    try:
        if not all([user_id, review_id]):
            return False, None, "Missing required fields"
        
        review = Review.objects(id=review_id).first()
        if not review:
            return False, None, "Review not found"
        
        for like_dislike in review.likesDislikes:
            if str(like_dislike.user.id) == user_id:
                review.likesDislikes.remove(like_dislike)
                review.save()
                return True, "Removed like/dislike", None
        return False, None, "No like/dislike found to remove"
        
    except Exception as e:
        return False, None, "Internal server error"
    
def addDislike(user_id: str, review_id: str):
    try:
        if not all([user_id, review_id]):
            return False, None, "Missing required fields"
        
        user = User.objects(id=user_id).first()
        if not user:
            return False, None, "User not found"
        
        review = Review.objects(id=review_id).first()
        if not review:
            return False, None, "Review not found"
        
        for i, like_dislike in enumerate(review.likesDislikes):
            if str(like_dislike.user.id) == user_id:
                review.likesDislikes[i].value = -1
                review.save()
                return True, "Updated to dislike", None
            
        new_dislike = LikeDislike(value=-1, user=user)
        review.likesDislikes.append(new_dislike)
        review.save()
        return True, "Added dislike", None
        
    except ValidationError as e:
        return False, None, f"Validation error: {str(e)}"
    except Exception as e:
        return False, None, "Internal server error"

def addComment(user_id: str, review_id: str, content: str):
    try:
        if not all([user_id, review_id, content]):
            return False, None, "Missing required fields"
        if len(content.strip()) == 0:
            return False, None, "Comment content cannot be empty"
        
        user = User.objects(id=user_id).first()
        if not user:
            return False, None, "User not found"
    
        review = Review.objects(id=review_id).first()
        if not review:
            return False, None, "Review not found"
        
        comment = Comment(user=user, content=content)
        review.comments.append(comment)
        review.save()
        return True, None, None
        
    except ValidationError as e:
        return False, None, f"Validation error: {str(e)}"
    except Exception as e:
        return False, None, "Internal server error"
    
def deleteComment(user_id: str, review_id: str, comment_id: str):
    try:
        if not all([user_id, review_id, comment_id]):
            return False, None, "Missing required fields"
        user = User.objects(id=user_id).first()
        if not user:
            return False, None, "User not found"
        
        review = Review.objects(id=review_id).first()
        if not review:
            return False, None, "Review not found"
        comment_to_delete = None
        for comment in review.comments:
            if str(comment.id) == comment_id:
                comment_to_delete = comment
                break
        
        if not comment_to_delete:
            return False, None, "Comment not found"
        if str(comment_to_delete.user.id) != user_id:
            return False, None, "Not authorized to delete this comment"
        review.update(pull__comments=comment_to_delete)
        return True, "Comment deleted successfully", None
    
    except Exception as e:
        return False, None, "Internal server error"