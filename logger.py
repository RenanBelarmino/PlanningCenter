import logging
import os
from datetime import datetime

# Função para configurar e retornar um logger
def get_logger(name, level=logging.INFO):
    # Gerar o nome do arquivo de log com a data atual
    log_file = f"app_{datetime.now().strftime('%Y-%m-%d')}.log"
    
    # Se o arquivo já existir, excluí-lo
    if os.path.exists(log_file):
        os.remove(log_file)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Criar um formatador de log
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Criar um manipulador para o arquivo de log
    file_handler = logging.FileHandler(log_file, mode='w')  # 'w' para sobrescrever o arquivo
    file_handler.setFormatter(formatter)

    # Adicionar o manipulador ao logger
    if not logger.handlers:
        logger.addHandler(file_handler)

    return logger
