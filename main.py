import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import csv
from logger import get_logger  # Importando o logger

# Carregar as variáveis do arquivo .env
load_dotenv()

# Configurando o logger
logger = get_logger(__name__)

# Application ID e Secret Key, agora carregados de forma segura do arquivo .env
app_id = os.getenv('APP_ID')
secret_key = os.getenv('SECRET_KEY')

# Verificar se as credenciais foram carregadas corretamente
if not app_id or not secret_key:
    logger.error("As credenciais não foram encontradas. Verifique o arquivo .env.")
    exit()
    
# URL base para listar eventos
base_url = 'https://api.planningcenteronline.com/groups/v2/events'
start_date = '2024-09-01'  # Data de início
end_date = '2024-09-30'  # Data de fim

# Inicializando variáveis para a paginação
events = []
per_page = 25  # Número de eventos por página (pode ser ajustado entre 1 e 100)
offset = 0  # Inicializa o offset

logger.info("Iniciando o processo de busca de eventos.")

while True:
    url = f'{base_url}?include=group&where[starts_at][gte]={start_date}&where[starts_at][lte]={end_date}&per_page={per_page}&offset={offset}'

    response = requests.get(url, auth=HTTPBasicAuth(app_id, secret_key))

    if response.status_code == 200:
        events_data = response.json()
        events.extend(events_data['data'])

        #logger.info(f"Eventos recebidos: {len(events)} até agora (offset: {offset})")

        if len(events_data['data']) < per_page:
            break
        else:
            offset += per_page
    else:
        logger.error(f"Erro ao obter eventos: {response.status_code}, {response.text}")
        break

# Processamento dos eventos
zero_attendance_count = 0

logger.info("Processando os eventos obtidos.")

with open('eventos.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Evento ID', 'Nome do Evento', 'Início', 'Fim', 'Grupo', 'Total de Pessoas', 'Presentes', 'Líder', 'Email do Líder', 'Telefone do Líder', 'Link do Evento'])

    event_counter = 0

    for event in events:
        event_id = event.get('id', 'N/A')
        event_name = event['attributes'].get('name', 'N/A')
        starts_at = event['attributes'].get('starts_at', 'N/A')
        ends_at = event['attributes'].get('ends_at', 'N/A')
        group_id = event['relationships']['group']['data'].get('id', 'N/A')

        group_url = f'https://api.planningcenteronline.com/groups/v2/groups/{group_id}'
        group_response = requests.get(group_url, auth=HTTPBasicAuth(app_id, secret_key))

        if group_response.status_code == 200:
            group_data = group_response.json()
            group_name = group_data['data']['attributes'].get('name', 'N/A')

            people_url = f'https://api.planningcenteronline.com/groups/v2/events/{event_id}/people'
            people_response = requests.get(people_url, auth=HTTPBasicAuth(app_id, secret_key))

            if people_response.status_code == 200:
                people_data = people_response.json()
                present_count = 0
                total_count = people_data['meta']['total_count']

                for person in people_data.get('data', []):
                    if person['attributes'].get('attended', False):
                        present_count += 1

                if present_count == 0:
                    zero_attendance_count += 1

                event_link = f"https://groups.planningcenteronline.com/groups/{group_id}/events/{event_id}"

                members_url = f'https://api.planningcenteronline.com/groups/v2/groups/{group_id}/members?offset=0&order=first_name,last_name&page=1&per_page=25&where[search_term]='
                members_response = requests.get(members_url, auth=HTTPBasicAuth(app_id, secret_key))

                leader_info = None

                if members_response.status_code == 200:
                    members_data = members_response.json()

                    for member in members_data.get('data', []):
                        first_name = member['attributes'].get('first_name', 'N/A')
                        last_name = member['attributes'].get('last_name', 'N/A')
                        role = member['attributes'].get('role', 'N/A')

                        if role.lower() == 'leader':
                            leader_info = {
                                'name': f"{first_name} {last_name}",
                                'email': member['attributes']['email_addresses'][0]['address'] if member['attributes'].get('email_addresses') else 'N/A',
                                'phone': member['attributes']['phone_numbers'][0]['number'] if member['attributes'].get('phone_numbers') else 'N/A'
                            }
                            break

                if leader_info:
                    csv_writer.writerow([event_id, event_name, starts_at, ends_at, group_name, total_count, present_count, leader_info['name'], leader_info['email'], leader_info['phone'], event_link])
                else:
                    csv_writer.writerow([event_id, event_name, starts_at, ends_at, group_name, total_count, present_count, 'N/A', 'N/A', 'N/A', event_link])

                event_counter += 1
                logger.info(f"Processado {event_counter} eventos.")
            else:
                logger.error(f"Erro ao obter pessoas para o evento {event_id}: {people_response.status_code}, {people_response.text}")
        else:
            logger.error(f"Erro ao obter grupo para o evento {event_id}: {group_response.status_code}, {group_response.text}")

logger.info(f"Número total de eventos processados: {len(events)}")
logger.info(f"Número de eventos com 0 pessoas presentes: {zero_attendance_count}")
