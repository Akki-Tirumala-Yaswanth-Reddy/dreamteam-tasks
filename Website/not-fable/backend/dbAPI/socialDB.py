from models.models import User
from mongoengine import ValidationError

def addFollower(user_id: str, follower_id: str):
    try:
        if user_id == follower_id:
            return False, None, "User can't follow themselves"
        user = User.objects(id=user_id).first()
        psn = User.objects(id=follower_id).first()
        if not all([user, psn]):
            return False, None, 'Could not process.'
        else:
            if psn not in user.followers:
                user.update(push__followers=psn)
                psn.update(push__following=user)
                return True, "Success", None
            else:
                return True, "Already there", None
    except ValidationError as e:
        return False, None, f'Validation error: {str(e)}'

def removeFollower(user_id: str, follower_id: str):
    try:
        user = User.objects(id=user_id).first()
        psn = User.objects(id=follower_id).first()
        if not all([user, psn]):
            return False, None, 'Could not process.'
        else:
            if psn in user.followers:
                user.update(pull__followers=psn)
                psn.update(pull__following=user)
                return True, "Success", None
    except ValidationError as e:
        return False, None, f'Validation error: {str(e)}'
    
def getFollowers(user_id: str):
    try:
        user = User.objects(id=user_id).first()
        if not user:
            return False, None, "Server error"
        followers = []
        for follower in user.followers:
            followers.append(follower.username)
        return True, followers, None
    except ValidationError as e:
        return False, None, f"Validation error: {str(e)}"

def getFollowing(user_id: str):
    try:
        user = User.objects(id=user_id).first()
        if not user:
            return False, None, "Server error"
        arr = []
        for follower in user.following:
            arr.append(follower.username)
        return True, arr, None
    except ValidationError as e:
        return False, None, f"Validation error: {str(e)}"
        