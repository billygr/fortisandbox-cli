# fortisandbox-cli
A tiny-lightweight python script to interact with Fortisandbox :) via JSON-RPC


## Setup

Copy the config.py.example as config.py and change the below variables.

```
FORTISANDBOX_URL = ""
API_TOKEN = ""
```


Set the values:

- FORTISANDBOX_URL: Your FortiSandbox instance URL (e.g., https://fortisandbox.example.com).
- API_TOKEN: Your API token for authentication in fortisandbox, to grab one you need to do this:

    In FortiSandbox, open the CLI console by clicking the CLI icon at the top-right of the page.
    In the CLI console, run the following CLI command to generate a new token.

    ```
    login-token -g
    ```

**Important Note**: https encryption is enforced 

## Requirements

- Python 3.7+
- Python virtual environment is preferable 
- Access to your FortiSandbox URL
- A valid API token

## Python Virtual Enviroment
```
python3 -mvenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Syntax

Example 1:
```
python3 fortisandbox-cli.py <file>
```

Example 2:
```
python3 fortisandbox-cli.py <file> --forcedvm 1 --comments "testing"
```


## Options
At the moment the script only scans files smaller than 200mb with or without VM.

```
usage: fortisandbox-cli.py [-h] [--forcedvm FORCEDVM] [--comments COMMENTS] file_path

Upload a file to FortiSandbox for analysis.

positional arguments:
  file_path            Ruta completa al archivo a subir

options:
  -h, --help           show this help message and exit
  --forcedvm FORCEDVM  Force scan using Virtual Machine (0 = No, 1 = Yes)
  --comments COMMENTS  Comment for the file
```

