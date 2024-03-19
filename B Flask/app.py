# Tomando Esta app modificar y lo entregado en del CRUD de Tareas, realizar :

# 1 - Crear o modifcar las rutas del CRUD de Tares para Guadar o ver los datos desde una BD. DONE
# 2 - Hacer que en el index pida el usuario y contraseña para poder ingresar y ver las tareas. DONE
# 3 - Cuando se crea, elimina, modifica o consulta una Tarea deben ser del usuario actualmente logueado. DONE

# NOTA: usar el usuario admin, con la clave admin, para crear usuario, solo él puede ver el crud de usuarios. DONE

from flask import Flask, render_template, request, redirect
from uuid import uuid4
from models.models import db, User, Task, History
from sqlalchemy_utils import database_exists
from flask import session,flash, get_flashed_messages
from flask_session import Session
from cryptography.fernet import Fernet
from functions import load_config_from_json
 
#borrarrrr
import requests, json
from flask import jsonify


app = Flask(__name__)

# Cargar la configuración desde el archivo JSON
load_config_from_json(app, 'config.json')
Session(app)

title = app.config.get('TITLE')
if not app.config.get('SECRET_KEY'):
    secret_key = Fernet.generate_key()
else:
    secret_key = app.config.get('SECRET_KEY')


app.secret_key=secret_key


# Le decimos cual va ha ser la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
# Asocio la App con la Base de Datos en la variable "db"
db.init_app(app)


# Verificacion de la si la base de datos no Existe es la primera ejecucion, entonces debemos crear la base y el User Admin
with app.app_context():
    if not database_exists(db.engine.url):
        db.create_all()
        user = User(id=str(uuid4()), username='admin', password='admin', email='admin@nose.com')
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            print(f'Error: {e}')

#------------------------- BORRAR ---------------------------


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            payload = {
                "Username": username,
                "Password": password
            }
            response = requests.post('http://127.0.0.1:8000/users/login', json=payload)
            response.raise_for_status()

            return redirect('/albums')

        except requests.exceptions.RequestException as e:
            return render_template('index.html', error="Nombre de usuario o contraseña incorrectos")
    else:
        return render_template('index.html', error=None)

@app.route('/register', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        fullname = request.form['fullname']
        password = request.form['password']

        try:
            payload = {
                "Username": username,
                "Fullname": fullname,
                "Password": password
            }
            response = requests.post('http://127.0.0.1:8000/users', json=payload)
            response.raise_for_status()

            return redirect('/login')

        except requests.exceptions.RequestException as e:
            return render_template('register.html', error="Error en el registro. Inténtalo de nuevo.")
    else:
        return render_template('register.html', error=None)

@app.route("/users") #sin uso
def getUsers():
    fastapi_url = 'http://127.0.0.1:8000/users'  # URL del endpoint FastAPI
    response = requests.get(fastapi_url)

    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return jsonify({'error': 'No se pudo obtener los datos del endpoint FastAPI'})


@app.route("/artist") #sin uso
def getArtists():
    fastapi_url = 'http://127.0.0.1:8000/artist'  # URL del endpoint FastAPI
    response = requests.get(fastapi_url)

    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return jsonify({'error': 'No se pudo obtener los datos del endpoint FastAPI'})


@app.route("/albums")
def get_albums():
    fastapi_albums_url = 'http://127.0.0.1:8000/album'
    fastapi_artists_url = 'http://127.0.0.1:8000/artist'

    albums_response = requests.get(fastapi_albums_url)
    artists_response = requests.get(fastapi_artists_url)

    if albums_response.status_code == 200 and artists_response.status_code == 200:
        albums = albums_response.json()
        artists = {artist['ArtistId']: artist['Name'] for artist in artists_response.json()}
        
        # Aplicamos el filtro si se selecciona un artista
        selected_artist_id = request.args.get('artist_filter')
        if selected_artist_id:
            filtered_albums = [album for album in albums if album['ArtistId'] == int(selected_artist_id)]
        else:
            filtered_albums = albums
        
        return render_template('album/albums.html', albums=albums, artists=artists, filtered_albums=filtered_albums)
    else:
        error_message = "Error desconocido al obtener álbumes o artistas."
        return jsonify({'error': error_message}), 500



@app.route("/albums/create", methods=['GET', 'POST'])
def create_album():
    if request.method == 'POST':
        data = request.form
        new_album = {
            "Title": data['Title'],
            "ArtistId": data['ArtistId'],
            "Column1": data['Column1']
        }

        fastapi_create_url = 'http://127.0.0.1:8000/album/'  # URL del endpoint FastAPI para crear álbumes
        response = requests.post(fastapi_create_url, json=new_album)

        if response.status_code == 200:
            return redirect('/albums')
        else:
            error_message = response.json().get('error', 'Error desconocido al crear álbum.')
            return jsonify({'error': error_message}), response.status_code
    elif request.method == 'GET':
        return render_template('album/createAlbum.html')
    else:
        return jsonify({'error': 'Método no permitido'}), 405
    




@app.route('/albums/update/<int:AlbumId>', methods=['GET', 'POST'])
def update_album(AlbumId):
    if request.method == 'GET':
        response = requests.get(f"http://127.0.0.1:8000/album/{AlbumId}")
        album_data = response.json()
        return render_template('album/updateAlbum.html', album=album_data)
    elif request.method == 'POST':
        album_data = {
            "Title": request.form['Title'],
            "ArtistId": request.form['ArtistId'],
            "Column1": request.form['Column1']
        }
        response = requests.put(f"http://127.0.0.1:8000/album/{AlbumId}", json=album_data)
        if response.status_code == 200:
            return redirect('/albums')
        else:
            return "Hubo un error al actualizar el álbum", 500





#-----------------------------------------------------------


#------------____________ARREGLARR___________-------------


@app.route('/albums/delete/<int:AlbumId>', methods=['POST'])
def borrar_album(AlbumId):
    try:
        response = requests.delete(f"http://127.0.0.1:8000/album/{AlbumId}")
        if response.status_code == 200:
            return redirect('/albums')  
        else:
            return "Hubo un error al eliminar el álbum", response.status_code
    except Exception as e:
        return f"Error interno del servidor: {str(e)}", 500  







#-----------HOME-------------

@app.route("/login")
@app.route("/home", methods=['GET','POST'])
def index():
    error=None
    tasks = Task.query.all()
    if request.method=='POST':
        

        if request.args.get('logout') == 'salir': #LOGOUT
            session['user'] = None
            session.clear()
            return redirect('/')
        
        email = request.form.get('email') #obtener datos del formulario
        pwd = request.form.get('password')
        user_bd = User.query.filter_by(email=email).first() #obtener datos de la BD


        if user_bd is not None and email==user_bd.email:
            if pwd==user_bd.password :
                session['user']=user_bd.id
                session['email']=user_bd.email
            else:
                flash("Contraseña incorrecta",'password')
                
        else:
            flash("Email incorrecto",'user')

    return render_template("index.html", title=title, tasks=tasks, session=session)


#------------CREAR TAREA----------

@app.route("/create", methods=["GET", "POST"])
def create():

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]

        task = Task(id = str(uuid4()), title=title,description=description,user_id=session['user'])

        db.session.add(task)
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f'Error: {e}'

        return redirect("/")
    else:
        return render_template("create.html")


#----------EDITAR TAREA-----------

@app.route("/edit/<task_id>", methods=["GET", "POST"])
def edit(task_id):

    task2 = Task.query.filter_by(id=task_id).first()
    if request.method == "POST":
        if not task2:
            return 'Tarea NO Existe', 404
        task2.title = request.form["title"]
        task2.description = request.form["description"]

        try:
            db.session.commit()
        except Exception as e:
            return f'Error: {e}'
        return redirect("/")
    
    else:
        return render_template("edit.html", task=task2)


#---------ELIMINAR TAREA-------------

@app.route("/delete/<task_id>")
def delete(task_id):
    print(request.method)
    task2 = Task.query.get(task_id)

    if not task2:
        return 'Tarea NO Existe', 404

    try:
        db.session.delete(task2)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f'Error: {e}'

    return redirect("/")

#------------CREAR USUARIO----------

@app.route('/addUser', methods=['GET', 'POST'])
def addUser():
    if request.method == 'POST':
        username=request.form['username']
        password = request.form['password']
        email = request.form['email']
        user= User(id = str(uuid4()), username=username,password=password,email=email)
        
        db.session.add(user)
        try:
            db.session.commit()
            return redirect('/getAllUsers')
        except Exception as e:
            return f'Error: {e}'
    else:
        return render_template('users/addUser.html')


#------------ACTUALIZAR USUARIO----------

@app.route('/updateUser/<user_id>', methods=['GET', 'POST']) 
def updateUser(user_id):

    if 'email' in session and session['email'] != 'admin@nose.com':
        return 'No tiene permisos para acceder a esta página'

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return 'Usuario NO Existe', 404
    

    user = User.query.get(user_id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.password = request.form['password']
        user.email = request.form['email']


        try:
            db.session.commit()
            users = User.query.all()
            return render_template('users/getAllUsers.html',users=users)
        except Exception as e:
            return f'Error: {e}'
    
    return render_template('users/updateUser.html', user=user)


#-------------ELIMINAR USUARIO----------

@app.route('/deleteUser/<user_id>')
def deleteUser(user_id):
    user = User.query.get(user_id)

    if not user:
        return 'Usuario NO Existe', 404

    try:
        db.session.delete(user)
        db.session.commit()
        return redirect('/getAllUsers')
    except Exception as e:
        return f'Error: No puede eliminar el Usuario, intente eliminar todas las Tareas del mismo'
    

#------------OBTENER USUARIOS----------

@app.route('/getAllUsers')
def getAllUsers():
    
    
    if session['email']!="admin@nose.com":
        return "No tiene permisos para acceder a esta página"
    
    users = User.query.all()
    if not users:
        return 'No Existen Usuarios'
    
    return render_template("users/getAllUsers.html", users=users,session=session)




if __name__ == "__main__":
    app.run(debug=True)