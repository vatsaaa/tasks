"""
Copyright (C) 2021  <Ankur Vatsa>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

## Keep the order of imports
import sys

## Project modules
from config.config import app
from utils.project.cli_args import process_args, usage

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        exit(-1)
    
    ## No app_host because the app runs on localhost
    ## One could do a gethostbyname() to get the hostname, though
    print('Starting the app with config:', sys.argv[1:])
    config = process_args(sys.argv[1:])

    app.run(host=config["app"]["host"], port=config["app"]["port"])