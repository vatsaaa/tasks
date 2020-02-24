import connexion

app = connexion.FlaskApp(__name__, specification_dir='./')
app.add_api('swagger.yml')

app.app.config['SECRET_KEY'] = 'top-secret!'
app.app.config['UPLOAD_FOLDER'] = '/tmp/'
