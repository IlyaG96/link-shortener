from link_shortener import bp
from app_factory import create_app

app = create_app()
app.register_blueprint(bp, name="bp")

if __name__ == '__main__':
    app.run()