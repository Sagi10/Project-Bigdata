from flask import Flask
from config import Config
import dash_bootstrap_components as dbc
import dash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
dask_apps = []


def create_app(config_class=Config):
    server = Flask(__name__, instance_relative_config=False)  # Initialize the Flask app
    server.config.from_object(
        'config.Config')  # Set the configuration of the Flask app 'app' equal to the the Config class in config.py

    register_blueprints(server)  # Blueprints like @routes

    # Import layout and callbacks of dash app and create it and register it to flask app/server
    from app.dashapp.layout import get_Layout as layout1
    from app.dashapp.callbacks import register_callbacks as register_callbacks1
    register_dashapp(server, 'IDO-LAAD Reporting', 'dashboard', layout1, register_callbacks1)

    return server


# Create and Register Dash App to FLask
def register_dashapp(app, title, base_pathname, layout, register_callbacks_fun):
    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    # Stylesheets for dash app
    external_stylesheets = [
        '/static/style/main.css',
        '/static/style/tabs.css',
        dbc.themes.BOOTSTRAP
    ]

    # Create dash App with Flask server as parameter
    my_dashapp = dash.Dash(__name__,
                           server=app,
                           url_base_pathname=f'/{base_pathname}/',
                           external_stylesheets=external_stylesheets,
                           #  assets_folder=get_root_path(__name__) + f'/{base_pathname}/assets/',
                           meta_tags=[meta_viewport])

    # Register Callbacks and set Layout
    with app.app_context():
        db.init_app(app)  # Initialze db with flask app
        register_extensions(app)  # Register rest of extensions like flask_login with flask app

        my_dashapp.title = title  # Set title of Dash App
        my_dashapp.layout = layout(db)  # Set layout of Dash App
        register_callbacks_fun(my_dashapp, db)  # Register the callbacks for the dashapp and layout

    dask_apps.append(my_dashapp)  # Append to to list of all dashApps


#  Register Blueprints / Routes to FLask
def register_blueprints(server):
    from app.webapp import server_bp
    # Import all Routes/ View functions
    server.register_blueprint(server_bp)


# Method for Register/Init Extensions
def register_extensions(app):
    import app.extensions as ex
    ex.bcrypt.init_app(app)
    ex.login_manager.init_app(app)
