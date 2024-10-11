import requests
from requests.auth import HTTPBasicAuth

# Application ID e Secret Key (substitua pelos seus)
app_id = 'bdfe520a26cf305885955700289877f380c7182d28cf64adc81c9dfe330f2d3b'  # Substitua pelo seu Application ID
secret_key = 'pco_pat_470869a8e80661de19aff2757d935ea1ddcb8096395ff850587aeeb603f78ba4ac5b0da4'  # Substitua pela sua Secret Key

# URL base para listar eventos
base_url = 'https://api.planningcenteronline.com/groups/v2/events'
start_date = '2024-09-01'  # Data de início
end_date = '2024-09-30'  # Data de fim

# Inicializando variáveis para a paginação
events = []
per_page = 25  # Número de eventos por página (pode ser ajustado entre 1 e 100)
offset = 0  # Inicializa o offset

while True:
    # Montando a URL com os parâmetros de filtragem e paginação
    url = f'{base_url}?include=group&where[starts_at][gte]={start_date}&where[starts_at][lte]={end_date}&per_page={per_page}&offset={offset}'

    # Fazendo a requisição GET com autenticação Basic para obter eventos
    response = requests.get(url, auth=HTTPBasicAuth(app_id, secret_key))

    # Verificando se a resposta foi bem-sucedida
    if response.status_code == 200:
        events_data = response.json()
        events.extend(events_data['data'])  # Adiciona os eventos recebidos à lista

        # Exibe o número atual da página e o número total de eventos recebidos
        print(f"Eventos recebidos: {len(events)} até agora (offset: {offset})")

        # Verifica se há mais eventos para buscar
        if len(events_data['data']) < per_page:
            break  # Sai do loop se não houver mais eventos
        else:
            offset += per_page  # Atualiza o offset para a próxima página
    else:
        print(f"Erro ao obter eventos: {response.status_code}, {response.text}")
        break

# Processando os eventos obtidos
for event in events:
    # Exibindo os dados relevantes de cada evento
    event_id = event.get('id', 'N/A')  # Pega o ID do evento
    event_name = event['attributes'].get('name', 'N/A')
    starts_at = event['attributes'].get('starts_at', 'N/A')
    ends_at = event['attributes'].get('ends_at', 'N/A')
    group_id = event['relationships']['group']['data'].get('id', 'N/A')

    # Fazendo a requisição GET para obter o grupo do evento
    group_url = f'https://api.planningcenteronline.com/groups/v2/groups/{group_id}'
    group_response = requests.get(group_url, auth=HTTPBasicAuth(app_id, secret_key))

    if group_response.status_code == 200:
        group_data = group_response.json()
        group_name = group_data['data']['attributes'].get('name', 'N/A')  # Nome do grupo

        # Fazendo a requisição GET para obter pessoas do evento
        people_url = f'https://api.planningcenteronline.com/groups/v2/events/{event_id}/people'
        people_response = requests.get(people_url, auth=HTTPBasicAuth(app_id, secret_key))

        if people_response.status_code == 200:
            people_data = people_response.json()
            present_count = 0
            total_count = people_data['meta']['total_count']  # Total de pessoas no grupo

            # Contando presença
            for person in people_data.get('data', []):
                if person['attributes'].get('attended', False):  # Verifica se a pessoa esteve presente
                    present_count += 1

            # Link para o evento
            event_link = f"https://groups.planningcenteronline.com/groups/{group_id}/events/{event_id}"

            # Fazendo a requisição GET para listar os membros do grupo
            members_url = f'https://api.planningcenteronline.com/groups/v2/groups/{group_id}/members?offset=0&order=first_name,last_name&page=1&per_page=25&where[search_term]='
            members_response = requests.get(members_url, auth=HTTPBasicAuth(app_id, secret_key))

            # Inicializando informações do líder
            leader_info = None  # Variável para armazenar informações do líder, se encontrado

            # Verificando se a resposta dos membros foi bem-sucedida
            if members_response.status_code == 200:
                members_data = members_response.json()

                # Iterando sobre os membros para encontrar o líder
                for member in members_data.get('data', []):
                    first_name = member['attributes'].get('first_name', 'N/A')
                    last_name = member['attributes'].get('last_name', 'N/A')
                    role = member['attributes'].get('role', 'N/A')

                    # Verificando se o membro é um líder
                    if role.lower() == 'leader':
                        leader_info = {
                            'name': f"{first_name} {last_name}",
                            'email': member['attributes']['email_addresses'][0]['address'] if member['attributes'].get('email_addresses') else 'N/A',
                            'phone': member['attributes']['phone_numbers'][0]['number'] if member['attributes'].get('phone_numbers') else 'N/A',
                            'avatar_url': member['attributes'].get('avatar_url', 'N/A'),
                            'joined_at': member['attributes'].get('joined_at', 'N/A')
                        }
                        break  # Saia do loop após encontrar o líder

            # Exibindo todas as informações relevantes do evento
            print(f"Evento: {event_name} ({event_id})")
            print(f"Grupo: {group_name}")  # Nome do grupo
            print(f"Início: {starts_at} | Fim: {ends_at}")
            print(f"Número total de pessoas no GC: {total_count}")
            
            if present_count == 0:
                print("############# ALERTA #############")
            print(f"Número de pessoas marcadas como presentes: {present_count} de {total_count}")
            if present_count == 0:
                print("############# ALERTA #############")
            
            print(f"Link do Evento: {event_link}")

            # Exibindo informações do líder
            if leader_info:
                print(f"Líder do grupo: {leader_info['name']}")
                print(f"Email: {leader_info['email']}")
                print(f"Telefone: {leader_info['phone']}")
                print(f"URL do Avatar: {leader_info['avatar_url']}")
                print(f"Data de entrada: {leader_info['joined_at']}")
            else:
                print("Não foi encontrado nenhum líder no grupo.")

            print('---')
        else:
            print(f"Erro ao obter pessoas para o evento {event_id}: {people_response.status_code}, {people_response.text}")
    else:
        print(f"Erro ao obter grupo para o evento {event_id}: {group_response.status_code}, {group_response.text}")

# Exibindo o número total de eventos processados
print(f"Número total de eventos processados: {len(events)}")
