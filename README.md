# Тестовое задание:
## Микросервис для электронного магазина
##### Стек: FastAPI, SQLAlchemy

### Шаги для инсталляции и запуска проекта:

- Склонировать репозиторий
- Создать виртуальное окружение и активировать его
- Установить пакеты из _requirements.txt_
- Поднять докер контейнер командой
```sh
docker run -d --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres 
```
(если контейнер поднят, но достучаться до него не получается, то поменяйте порт хоста 5432 на 5431 или любой свободный, непрослушиваемый порт, также необходимо будет изменить порт в файле переменных окружения _.env.example_)
- Внутри дериктории _e-shop_microservice_, с помощью терминала, запустить сервер командой
```sh
python main.py --insert-start-data true
```

(--insert-start-data - это флаг, при истинности которого, на старте инициализируются данные из _start_data.json_)

--------------------------
### Curl команды с нужными параметрами для прохождения тестового сценария:
- Создать товар
```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/api/products/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Smartphone Samsung Galaxy Note 10+",
  "brand": "Samsung",
  "manufacturer": "China",
  "price": 23900
}'
```
- Найти его по названию
```sh
curl -X 'GET' \
  'http://127.0.0.1:8000/api/products/?name=Smartphone%20Samsung%20Galaxy%20Note%2010%2B&desc=false' \
  -H 'accept: application/json'
```
- Получить детали найденного товара
```sh
curl -X 'GET' \
  'http://127.0.0.1:8000/api/products/9' \
  -H 'accept: application/json'
```
 --------------------------
### Документация к API доступна по эндпоинту /docs, например:
##### http://127.0.0.1:8000/docs

