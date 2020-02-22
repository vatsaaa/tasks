import connexion

app = connexion.FlaskApp(__name__, specification_dir='./')
app.app.config['UPLOAD_FOLDER'] = '/tmp/'
app.add_api('swagger.yml')

