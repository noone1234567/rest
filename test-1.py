from requests import get, post, delete, put

print(get('http://localhost:8080/news').json())
print(post('http://localhost:8080/news',
           json={'title': 'Заголовок'}).json())
print(get('http://localhost:8080/').json())
print(post('http://localhost:8080/news',
           json={'title': 'Заголовок',
                 'content': 'Текст новости',
                 'user_id': 2}).json())
print(get('http://localhost:8080/').json())
print(get('http://localhost:8080/news').json())
print(get('http://localhost:8080/news/1').json())
print(get('http://localhost:8080/news/hiiiii').json())
print(delete('http://localhost:8080/news/12').json())
print(delete('http://localhost:8080/news/1').json())

