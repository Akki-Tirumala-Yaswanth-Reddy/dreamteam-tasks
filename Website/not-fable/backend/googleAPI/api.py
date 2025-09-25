import requests
from dateutil import parser

api_key = "AIzaSyDLPKr1Y6oeCkr9ZEI9rp2MKFkxltf2t6s"
base_url = "https://www.googleapis.com/books/v1/"

def getBooks(**kwargs):
    query = ''
    # The query requires the terms to be like q=intitle:{title}+inauthor:{author}... 
    # So we build the required string, step by step
    if 'title' in kwargs:
         title = kwargs.get('title').replace(' ', '+')
         query += f'intitle:{title}' + '+'
    if 'author' in kwargs:
        author = kwargs.get('author').replace(' ', '+')
        query += f'inauthor:{author}' + '+'

    if 'genre' in kwargs:
         genre = kwargs.get('genre').replace(' ', '+')
         query += f'subject:{genre}' + '+'

    url = base_url + f"volumes?q={query}&key={api_key}&maxResults=4"
    response = requests.get(url)
    print(url)
    if response.status_code == 200:
            data = response.json()
            arr = []
            # When date is invoved we search for the titles with the required date
            if 'date' in kwargs:
                 date = kwargs.get('date')
                 for item in data.get('items', []):
                      info = item.get('volumeInfo', {})
                      if parser.parse(info.get('publishedDate')).year == date:
                           info = item.get('volumeInfo',{})
                           arr.append({"title": info.get('title'),"google_id": item.get('id'), "rating": info.get('averageRating')})
            # When date is not involved
            else:
                for item in data.get('items',[]):
                    info = item.get('volumeInfo',{})
                    arr.append({"title": info.get('title'),"google_id": item.get('id'), "rating": info.get('averageRating')}) 
            return arr
                  

print(getBooks(title='40 laws'))