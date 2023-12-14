from flask import Flask, Response, request
from sqlalchemy import exc

from crud import get_note, create_note
from models import create_tables, drop_tables

app = Flask(__name__)

drop_tables()
create_tables()

@app.route("/", methods=["GET"])
def home_page_view():
    return "<h1>Hello, World!</h1>"

@app.route("/create_note", methods=["GET"])
def get_create_notes():
    return (
        "<h1> Создать анонимную запись </h1>"
        '<form action="/create_note" method="post">' 
        '   <p> title: <input type="text" name="title"> </p>'  
        '   <p> content: <input type="text" name="content"> </p>'  
        '   <p> <input type="submit"> </p>' 
        '</form>'
    )

@app.route("/create_note", methods=["POST"])
def create_note_view():
    note_data = request.form

    note = create_note(
            title=note_data["title"],
            content=note_data["content"],
        )

    return f"""
    <h1>Ваша запись успешно создана !</h1>
    <p>ID: {note.uuid}</p>"""


@app.route("/<uuid>", methods=["GET"])
def note_view(uuid: str):
    try:
        note = get_note(uuid)
    except exc.NoResultFound:
        return Response("Note not found.", status=404)

    return f"""
        <h1>Ваша запись  {note.uuid}</h1>
        <p>title: {note.title} </p>
        <p>content: {note.content}</p>
        <p>created at: {note.created_at} </p>

    """

