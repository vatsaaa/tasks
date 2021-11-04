## Keep the order of imoprts
from flask_cors import CORS
import logging
import connexion


## TODO: enablße to set from commandline
ALLOW_ALL_FILE_TYPES = True ## True by default
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xlsx'}

logging.basicConfig()
logger = logging.getLogger('waitress')
logger.setLevel(logging.DEBUG)

app = connexion.FlaskApp(__name__, specification_dir='./')
app.add_api('swagger.yml')

CORS(app.app, origins="*", allow_headers="*")

app.app.config['SECRET_KEY'] = 'top-secret!'
app.app.config['UPLOAD_FOLDER'] = '/tmp/'

