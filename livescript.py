from livereload import Server
from appFlask import app

server = Server(app.wsgi_app)
# server.watch("templates/*.html")

if __name__ == '__main__':
    server.serve()
