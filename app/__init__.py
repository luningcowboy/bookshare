from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
import click
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
from app import views, models

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop')
def initDB(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
@click.option('--config', default='./book.json', help='Add books from json')
def addBook(config):
    click.echo('add Book from config file:%s'% config)
    """
    "name": "book3",
    "author": "author3",
    "pic": "wwww.baidu.com",
    "desc": "This is description",
    "contents": "描\n述\n文\n本",
    "type": "type",
    "download": "www.baidu.com,www.baidu.com"
    """
    import json as js
    bookConfig = open(config).read()
    bookConfig = js.loads(bookConfig)
    click.echo(bookConfig['books'])
    for book in bookConfig['books']:
        click.echo(book['name'])
        bookData = models.Book(name=book['name'],
                author=book['author'],
                booktype=book['type'],
                pic=book['pic'],
                contents=book['contents'],
                download=book['download'])
        db.session.add(bookData)
        db.session.commit()

@app.cli.command()
def listAllBooks():
    books = db.session.query(models.Book)
    for book in books:
        print(book.name, book.author, book.booktype)
