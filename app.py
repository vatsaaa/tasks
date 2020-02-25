from config import app


if __name__ == '__main__':
    app.run(port=8080, extra_files=["./swagger.yml"])

