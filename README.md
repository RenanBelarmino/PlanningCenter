# Projeto de Coleta de Eventos do Planning Center

Este projeto é uma aplicação Python que coleta dados sobre eventos de uma organização usando a API do Planning Center. Ele autentica solicitações, busca eventos em um intervalo de datas específico, e processa as informações dos eventos, incluindo a presença de pessoas e dados dos líderes.

## Funcionalidades

- Autenticação com a API do Planning Center usando um `APP_ID` e uma `SECRET_KEY`.
- Busca eventos em um intervalo de datas especificado.
- Processamento dos dados dos eventos, incluindo:
  - ID do evento
  - Nome do evento
  - Data e hora de início e fim
  - Nome do grupo
  - Total de participantes e número de presentes
  - Informações sobre o líder do grupo
- Exportação dos dados dos eventos para um arquivo CSV chamado `eventos.csv`.

## Pré-requisitos

Antes de começar, verifique se você tem os seguintes itens instalados:

- Python 3.x
- pip (gerenciador de pacotes do Python)

## Instalação

1. Clone este repositório ou faça o download dos arquivos.
2. Navegue até o diretório do projeto:
   ```bash
   cd seu-diretorio

Instale as dependências necessárias usando o requirements.txt:

pip install -r requirements.txt



Crie um arquivo .env no diretório do projeto e adicione suas credenciais:

```bash
APP_ID=seu_app_id
SECRET_KEY=sua_secret_key



```bash
seu-diretorio/
│
├── main.py         # Script principal que busca e processa eventos
├── eventos.csv           # Arquivo CSV onde os eventos são salvos
├── requirements.txt      # Dependências do projeto
├── .env                  # Variáveis de ambiente (credenciais)
└── logger.py             # Módulo para configuração do logger
