import os

# GroundScratch Configuration file

# This value is for the upload folder. We do not recommand modifying it, because it can break things.
UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/uploads/'

# The secret key. Change it from the default and keep it secret!
SECRET_KEY = 'secret key'

# The SQLAlchemy Database URL. Please, do not change that if you don't know what you are doing!
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'

# The url of your GroudScratch instance. Please make it https, because it can break the Scratch file player!
ROOT_URL = 'http://localhost:6060/'

# !!!! NOT FOR PRODUCTION !!!!
# Enable development mode
TESTING = False

# !!!! ONLY FOR DEVELOPMENT ENVIRONNEMENT, NOT PRODUCTION !!! 
# The port of your GroudScratch instance.
PORT = 8080