# Checking if the keyword is in the text or not

def check(key, text):
    key, text = str.lower(key), str.lower(text)
    val = str.find(text, key)
    if val == -1:
        return False
    else:
        return True

def test_check_with_key_in_text():
    assert check("hi", "Hello, this floor is high") == True

def test_check_with_key_not_in_text():
    assert check("hi", "Hello, the key is not there in the text") == False

def test_check_with_key_in_text_Capitals():
    assert check("HI", "Hello, this floor is high") == True

def test_check_with_key_not_in_text_Capitals():
    assert check("HI", "Hello, the key is not there in the text") == False
