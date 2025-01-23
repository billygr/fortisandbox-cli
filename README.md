# fortisandbox-cli
A tiny-lightweight python script to interact with Fortisandbox :) via JSON-RPC


## Setup

Edit Variables:

Open the script file in your text editor or IDE.
Locate the following variables at the beginning of the script:

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

**Important Note**: I'm using a valid certificate with my Fortisandbox, so you need to replace the "**verify=True**" to "**verify=False**" in the **requests** if you don't have one.

## Requirements

- Python 3.7+
- Access to your FortiSandbox URL
- A valid API token

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

Sube un archivo a FortiSandbox para su análisis.

positional arguments:
  file_path            Ruta completa al archivo a subir

options:
  -h, --help           show this help message and exit
  --forcedvm FORCEDVM  Forzar escaneo mediante Virtual Machine (0 = No, 1 = Si)
  --comments COMMENTS  Comentario para el archivo
```

