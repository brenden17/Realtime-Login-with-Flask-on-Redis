# Real Login status with redis and mongodb on Flask 

This is Flask extension which implements user's friend login status with Redis and mongodb.


## Reqirements

* Redis server
* mongodb
* Python library

~~~
pip install flask-script
pip install flask-mongoengine
pip install flask-sqlalchemy
pip install flask-login
pip install redis
~~~

* Bootsrap

## How to use

This extension uses three different databases such as MySQL(SQL), Mongodb(NoSQL) and Redis for performance. 
SQL database supports data entity relations, NoSQL also saves only friend's names and Redis manages their status on memory.

~~~
python manage.py server # for running server
# go to http://127.0.0.1:5000/user/
python manage.py shell # for shell
~~~

