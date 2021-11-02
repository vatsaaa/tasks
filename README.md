# How to run
## Setup the development environment
### Clone from repository
```shell
> mkdir projects
> cd projects
> git clone https://github.com/vatsaaa/tasks.git
```

### Setup virtual environment
#### macOS/Linux
```shell
> cd tasks
> python3 -m venv .venv
```

#### Windows
```shell
> cd tasks
> python -m venv .venv
```

### Get the code working
#### Activate the virtual environment and Install requirements
```shell
> ./.venv/bin/activate
> pip3 install -r requirements.txt
```

#### Run the code
```shell
> python3 app.py
```

#### Test Successful running API
- Open link http://127.0.0.1:5454/api/v1/ui
- Operate with Swagger UI 

# How to code
## Add more functionality
### Add definition to config/swagger.yml file
```yml
paths:
  /ping:
    get:
      summary: Health check url
      operationId: controllers.controllers.ping
      parameters:
        - in: query
          name: suffix
          required: false
          schema:
            type: string
          description: suffix is appended to response from the service 
      tags:
      - Health Check
      responses:
        200:
          description: ping( ) services responds to user's ping with pong and the time at which the srvice was invoked. e.g. 
```
### Add corresponding code to controllers/controllers.py
```python
def ping(suffix=None):
    resp_str = "User ping, tasks pong / " + dt.now().strftime("%Y-%m-%d, %H:%M:%S")
    resp = resp_str if suffix is None else resp_str + " / " + suffix
    return resp
```
### Run and test from Swagger-UI
```shell
> python3 app.py
INFO:waitress:Serving on http://127.0.0.1:5454
```
Open the browser to visit page http://127.0.0.1:5454/api/v1/ui to launch the swagger ui and to test the service just added

Alternatively, one could use the cUrl utility as well:
```shell
curl -X 'GET' \
  'http://127.0.0.1:5454/api/v1/ping?suffix=suffix01' \
  -H 'accept: */*'
```
