from flask import Flask, render_template, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de la base de datos
class Posteo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario = db.Column(db.String(100), nullable=False)
    titulo = db.Column(db.String(255), nullable=False)
    texto = db.Column(db.Text, nullable=False)

# Inicialización de la base de datos
with app.app_context():
    db.create_all()
    print("Base de datos generada")

# Endpoint para la página de login
@app.route('/login')
def login():
    return render_template('login.html')

# Endpoint para la página principal con los posteos
@app.route('/')
def index():
    posteos = Posteo.query.order_by(Posteo.id.desc()).all()  # Obtener todos los posteos en orden descendente
    return render_template('blog.html', posteos=posteos)

# Endpoint para manejar los posteos con el usuario en la URL
@app.route('/posteos/<usuario>', methods=['GET', 'POST'])
def manejar_posteos(usuario):
    if request.method == 'GET':
        # Obtener los últimos 3 posteos de un usuario
        posteos = Posteo.query.filter_by(usuario=usuario).order_by(Posteo.id.desc()).limit(3).all()
        datos = [{"titulo": post.titulo, "texto": post.texto} for post in posteos]
        return jsonify(datos)
    
    elif request.method == 'POST':
        # Crear un nuevo posteo
        titulo = request.form.get('titulo')
        texto = request.form.get('texto')
        if not titulo or not texto:
            return Response("Faltan datos", status=400)
        nuevo_post = Posteo(usuario=usuario, titulo=titulo, texto=texto)
        db.session.add(nuevo_post)
        db.session.commit()
        return Response(status=201)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
