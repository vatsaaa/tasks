# How to run
## Setup the development environment
### Clone from repository
```bash
> mkdir projects
> cd projects
> git clone https://github.com/vatsaaa/tasks.git
```

### Setup virtual environment
#### macOS/Linux
```
> cd tasks
> python3 -m venv .venv
```

#### Windows
```
> cd tasks
> python -m venv .venv
```

### Get the code working
#### Activate the virtual environment and Install requirements
```
> ./.venv/bin/activate
> pip3 install -r requirements.txt
```

#### Run the code
```
python3 app.py
```

#### Test Successful running API
- Open link http://127.0.0.1:5454/api/v1/ui
- Operate with Swagger UI 

# How to code
## Add more functionality
### Add definition to swagger.yml file
### Add corresponding code to controllers
### Run and test from Swagger-UI
