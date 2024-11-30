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

#### Run the app
The config file should be in ini format.
```shell
> python3 app.py -c config/secrets.ini
```

#### Run celery
```shell
> pip3 install eventlet
```
celery -A taskqueue.tasks.celery_app worker --loglevel=DEBUG --pool=eventlet --purge 

#### Test Successful running API
- Open link http://127.0.0.1:7665/api/v1/ui
- Operate with Swagger UI 

# How to contribute to the project
- Before starting to contribute, one may find it useful to go through this page - [How to contribute to Open Source](https://opensource.guide/how-to-contribute/).
- The recommended IDE is Visual Studio Code. [Here] is a good tutorial to follow and setup the IDE(https://realpython.com/advanced-visual-studio-code-python/).
- PyCharm is as good as VS Code, with a few specific differences. Update README.md file with instructions to setup PyCharm - [Issue #8].
## Code
### Add more functionality
#### Add definition to config/swagger.yml file
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


### Code reviews and walkthroughs

### Testing
#### Unit testing
Need to add unit testing for each module which should run nightly - for every branch
Successful tests is the first criteria for accepting a merge request

#### Automated testing
Need to create automated functional tests which should run nightly - for every branch
Successful tets is the first criteria for accepting a merge request

### Documentation
#### Improve README.md
#### Improve wiki
#### Contribute to discussions


#### How to use redis-cli correctlyc
https://lightrun.com/dev-tools/using-the-redis-command-line/

https://redis.io/topics/data-types-intro

https://www.digitalocean.com/community/cheatsheets/how-to-manage-redis-databases-and-keys

https://github.com/github/copilot-docs/blob/main/docs/visualstudiocode/gettingstarted.md#getting-started-with-github-copilot-in-visual-studio-code

https://www.fast.ai/2021/07/19/copilot/
