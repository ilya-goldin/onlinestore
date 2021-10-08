# Online Store
## Installation
```shell
  git clone https://github.com/ilya-goldin/onlinestore.git
  cd onlinestore/
```
Set up dependencies  
```shell
pip install -r requirements.txt
```
Create PostgreSQL DB
```shell
  createdb onlinestore_products
```
Run migration
```shell
  python manage.py migrate
```
Load data in DB
```shell
  python manage.py loaddata
```
Run server
```shell
  python manage.py runserver
```
    
## Tests coverage

![Tests coverage screenshot](htmlcov/Screenshot%20from%202021-10-08.png)
