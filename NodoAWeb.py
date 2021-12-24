from flask import Flask, render_template

# Create a Flask Instance
app = Flask(__name__)

# Create a route decorator
@app.route('/')

def index():
    return render_template("index.html")

#localhost:5000/user/John
@app.route('/user/<name>')

def user(name):
    #retorna el valor escrito en el buscador como una pagina
    #return "<h1>Hola {}</h1>".format(name)
    return render_template("user.html", user_name=name)

#Create Custom Error Pages
#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("404.html"), 500



#Con este codigo puedo llamar el archivo desde consola y corre el servidor
if __name__ == '__main__':
    app.run(debug=True)