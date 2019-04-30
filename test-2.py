from requests import get, post, delete, put

print(get('http://localhost:8080/news').json())
print(post('http://localhost:8080/news',
           json={'title': '1232444'}).json())
print(post('http://localhost:8080/news',
           json={'title': '68868767',
                 'content': '878787878',
                 'user_id': 1}).json())
print(get('http://localhost:8080/news').json())
print(get('http://localhost:8080/news/1').json())
print(get('http://localhost:8080/news/jhjhjh').json())
print(put('http://localhost:8080/news/1',
          json={'part': 'title',
                'text': 'hi'}).json())
print(put('http://localhost:8080/news/1',
          json={'part': 'title'}).json())
print(delete('http://localhost:8080/news/13').json())
print(delete('http://localhost:8080/news/1').json())

print()

print(get('http://localhost:8080/users').json())
print(post('http://localhost:8080/users',
           json={'login': '1232444'}).json())
print(post('http://localhost:8080/users',
           json={'login': '68868767',
                 'password': '878787878'}).json())
print(get('http://localhost:8080/users').json())
print(get('http://localhost:8080/users/1').json())
print(get('http://localhost:8080/users/jhjhjh').json())
print(put('http://localhost:8080/users/1',
          json={'part': 'user_name',
                'text': 'hi'}).json())
print(put('http://localhost:8080/users/1',
          json={'part': 'login'}).json())
print(delete('http://localhost:8080/users/13').json())
print(delete('http://localhost:8080/users/1').json())

