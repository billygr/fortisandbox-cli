import requests
import base64
import json
import time
import argparse
import os 
import sys 

# Configuración
FORTISANDBOX_URL = "https://<CHANGE_ME>/jsonrpc"
API_TOKEN = '<YOU API TOKEN>'
#Hey, ten ojo con el Verify=True en las requests, dejalo en False si no tienes un certificado válido.

def login(api_token):
    payload = {
        "method": "get",
        "params": [
            {
                "url" : "/sys/login/token",
                "token" : api_token
            }
        ],
        "session": "",
        "id": 53,
        "ver": "5.0"
    }

    response = requests.post(FORTISANDBOX_URL, json=payload, verify=True)
    if response.status_code == 200:
        result = response.json()
        if result.get("result"):
            return result["session"]
    print("Error al autenticar:", response.text)
    return None

def upload_big_file(session, file_path, forcedvm, comments):
    data_json = {
        "url": "/alert/ondemand/submit-file",
        "type": "file",
        "skip_steps": "",
        "overwrite_vm_list": "",
        "malpkg": 0,
        "vrecord": "0",
        "forcedvm": forcedvm,
        "comments": comments,  
        "enable_ai": 0,
        "archive_password": "",
        "timeout": "3600",
        "meta_url": "",
        "meta_filename": "",
        "session": session
    }

    with open(file_path, "rb") as file:
        files = {
            "file": (file_path, file, "multipart/form-data"),
            "data": (None, json.dumps(data_json), "application/json")
        }

        response = requests.post(FORTISANDBOX_URL, files=files, verify=True) 
        if response.status_code == 200:
            result = response.json()
            if result.get("result"):
                return result["result"]["data"]["sid"]
        print("Error al subir archivo:", response.text)
        return None

def upload_file(session, file_path, filename, forcedvm, comments):
   
    with open(file_path, "rb") as file:
        file_data = base64.b64encode(file.read()).decode()

    payload = {
        "method": "set",
        "session": session,
        "params": [
            {
                "file": file_data,
                "filename": base64.b64encode(filename.encode('utf-8')).decode('utf-8'),
                "url": "/alert/ondemand/submit-file",
                "type": "file",
                "overwrite_vm_list": "",
                "archive_password": "",
                "malpkg": "1",
                "meta": {"meta_filename": "", "meta_url": ""},
                "timeout": "3600",
                "vrecord": '0',
                "enable_ai": '0',
                "forcedvm": forcedvm, 
                "comments": comments
            }
        ],
       "id": 11,
        "ver": "5.0"
    }

    response = requests.post(FORTISANDBOX_URL, json=payload, verify=True)
    if response.status_code == 200:
        result = response.json()
        if result.get("result"):
            return result["result"]["data"]["sid"]
    print("Error al subir archivo:", response.text)
    return None



def get_submission_jobs(session, submission_id):
    payload = {
        "method": "get",
        "params": [
            {
                "url": "/scan/result/get-jobs-of-submission",
                "sid": submission_id
            }
        ],
        "session": session,
        "id": 17,
        "ver": "5.0"
    }
    response = requests.post(FORTISANDBOX_URL, json=payload, verify=True)
    if response.status_code == 200:
        return response.json()["result"]["data"]["jids"]
    print("Error al obtener estado:", response.text)
    return None


def get_analysis_status(session, submission_id):
    jids = get_submission_jobs(session, submission_id)

    for jid in jids:
        payload = {
            "method": "get",
            "params": [
                {
                    "url": "/scan/result/job",
                    "jid": jid
                }
            ],
            "session": session,
            "id": 15,
            "ver": "5.0"
        }
        response = requests.post(FORTISANDBOX_URL, json=payload, verify=True)
        if response.status_code == 200:
            return response.json()
        print("Error al obtener estado:", response.text)
    return None

def main():

    parser = argparse.ArgumentParser(description="Sube un archivo a FortiSandbox para su análisis.")
    parser.add_argument("file_path", help="Ruta completa al archivo a subir")
    parser.add_argument("--forcedvm", help="Forzar escaneo mediante Virtual Machine (0 = No, 1 = Si)?")
    parser.add_argument("--comments", help="Comentario para el archivo")
    args = parser.parse_args()

    session = login(API_TOKEN)
    if not session:
        return

    if args.forcedvm:
        if args.forcedvm in ["0","1"]:
            forcedvm = args.forcedvm
        else:
            print("[!] Valor '--forcedvm' debe ser 0 o 1, se forza o no el scan VM.")
            forcedvm = 0
    else:
        forcedvm = 0

    if not args.comments:
        comments = ""
    else:
        comments = args.comments


    if os.path.exists(args.file_path):
        tamanio_archivo = os.path.getsize(args.file_path)
        
        limite_min = 20 * 1024 * 1024   # 20 MB
        limite_max = 200 * 1024 * 1024  # 200 MB

        if limite_min <= tamanio_archivo <= limite_max:
            print(f"El archivo pesa más de 20 MB ({tamanio_archivo / (1024 * 1024):.2f} MB).")
            filename = args.file_path.split("/")[-1]
            submission_id = upload_big_file(session, args.file_path, forcedvm, comments)
            if not submission_id:
                return
            print(f"Archivo subido exitosamente. ID de envío: {submission_id}")

        elif tamanio_archivo < limite_min:
            print(f"El archivo pesa menos de 20 MB ({tamanio_archivo / (1024 * 1024):.2f} MB).")
            filename = args.file_path.split("/")[-1]
            submission_id = upload_file(session, args.file_path, filename, forcedvm, comments)
            if not submission_id:
                return
            print(f"Archivo subido exitosamente. ID de envío: {submission_id}")
        else:
            print(f"El archivo es demasiado grande: {tamanio_archivo / (1024 * 1024):.2f} MB. (Máximo permitido: 200 MB)")
            sys.exit()

    else:
        print("Error, el archivo no existe.")
        sys.exit()

    while True:
        status = get_analysis_status(session, submission_id)
        if status:
            analysis_status = status["result"]["status"]["message"]
            if analysis_status == "OK":
                print("Análisis completado:", status["result"]["status"]["message"])
                print("Veredicto:", status["result"]["data"]["rating"])
                print("Detalles:", status["result"]["data"]["detail_url"])
                break
            else:
                print("El análisis está en progreso...")
        time.sleep(10)

if __name__ == "__main__":
    main()
