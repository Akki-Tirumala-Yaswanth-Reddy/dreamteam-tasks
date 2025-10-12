import requests
from dateutil import parser

# api_key = "AIzaSyDLPKr1Y6oeCkr9ZEI9rp2MKFkxltf2t6s"
base_url = "https://www.googleapis.com/books/v1/"

def getGoogleBooks(**kwargs):
     try:
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
          if len(kwargs) == 0:
               query += f'spiderman+batman+thanos+superman'

          url = base_url + f"volumes?q={query}&maxResults=40"
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
                              published_date = info.get('publishedDate')
                              
                              # Skip items without published date
                              if not published_date:
                                   continue
                                   
                              try:
                                   parsed_year = str(parser.parse(published_date).year)
                                   photo = info.get("imageLinks", {}).get("thumbnail", "")
                                   if photo == "":
                                        photo = "https://www.scribbler.com/cdn/shop/files/IL103.jpg?v=1748362754"
                                   if parsed_year == date:
                                        arr.append({"title": info.get('title'),
                                                  "google_id": item.get('id'), 
                                                  "rating": info.get('averageRating'), 
                                                  "imageUrl": photo,
                                                  "subtitle": info.get("subtitle", None),
                                                  "description": info.get("description", None),
                                                  "authors": info.get("authors", []),
                                                  "publishedDate": parsed_year
                                                  })
                              except (ValueError, TypeError):
                                   # Skip items with invalid date format
                                   continue
                    # When date is not involved
                    else:
                         for item in data.get('items',[]):
                              info = item.get('volumeInfo',{})
                              published_date = info.get('publishedDate')
                              photo = info.get("imageLinks", {}).get("thumbnail", "")
                              if photo == "":
                                   photo = "https://www.scribbler.com/cdn/shop/files/IL103.jpg?v=1748362754"
                              parsed_date = "Unknown"
                              if published_date:
                                   try:
                                        parsed_date = str(parser.parse(published_date).year)
                                   except (ValueError, TypeError):
                                        parsed_date = "Unknown"
                              
                              arr.append({"title": info.get('title'),
                                        "google_id": item.get('id'), 
                                        "rating": info.get('averageRating'), 
                                        "imageUrl": photo,
                                        "subtitle": info.get("subtitle", None),
                                        "description": info.get("description", None),
                                        "authors": info.get("authors", []),
                                        "publishedDate": parsed_date
                                        }) 
                    return arr
     except Exception as e:
          print(e)
          return []
    
def getGoogleBook(id):
     url = base_url + f"volumes/{str(id)}"
     print(url)
     response = requests.get(url)

     if response.status_code == 200:
          data = response.json()
          info = data.get('volumeInfo',{})
          published_date = info.get('publishedDate')

          photo = info.get("imageLinks", {}).get("thumbnail", "")
          if photo == "":
               photo = "https://www.scribbler.com/cdn/shop/files/IL103.jpg?v=1748362754"
          
          # Handle missing or invalid published date
          parsed_date = "Unknown"
          if published_date:
               try:
                    parsed_date = str(parser.parse(published_date).year)
               except (ValueError, TypeError):
                    parsed_date = "Unknown"
          
          return { "title": info.get('title'),
               "google_id": data.get('id'),
               "rating": info.get('averageRating', None),
               "imageUrl": photo,
               "subtitle": info.get("subtitle", None),
               "description": info.get("description", None),
               "authors": info.get("authors", []),
               "publishedDate": parsed_date }
     
