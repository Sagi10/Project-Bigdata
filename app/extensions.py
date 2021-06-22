from flask_bcrypt import Bcrypt
from flask_login import LoginManager

bcrypt = Bcrypt()                           # Initialize Password Bcrypt object
login_manager = LoginManager()              # Initialize Flask Login Manager for session and auth etc.
login_manager.login_view = "main.login"    # Default view for login
login_manager.login_message_category='info' # Default message class
