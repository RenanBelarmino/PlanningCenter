import requests
from requests.auth import HTTPBasicAuth

# URL para o tipo de grupo (ID: 418098)
url = "https://api.planningcenteronline.com/groups/v2/group_types/418098" #grupos

# Application ID e Secret Key (substitua pelos seus)
app_id = 'bdfe520a26cf305885955700289877f380c7182d28cf64adc81c9dfe330f2d3b'  # Substitua pelo seu Application IDurl = f'https://api.planningcenteronline.com/groups/v2/groups/{group_id}/events'
secret_key = 'pco_pat_470869a8e80661de19aff2757d935ea1ddcb8096395ff850587aeeb603f78ba4ac5b0da4'  # Substitua pela sua Secret Key

# Fazendo a requisição GET com autenticação Basic
response = requests.get(url, auth=HTTPBasicAuth(app_id, secret_key))
print(response.text)

# Verificando se a resposta foi bem-sucedida
if response.status_code == 200:
    group_type_data = response.json()
    print(group_type_data)  # Exibindo os dados do tipo de grupo
else:
    print(f"Erro: {response.status_code}, {response.text}")




