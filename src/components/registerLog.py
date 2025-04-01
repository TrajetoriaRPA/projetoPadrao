import logging
import os
import requests
from datetime import datetime

def setup_logger():
    """
    Configura o logger para salvar logs com nome baseado na data (ano/mês/dia).
    Exemplo: logs20230220.txt (formato logsYYYYMMDD.txt)
    """
    try:
        # Obtém a data atual para o nome do arquivo
        now = datetime.now()
        log_dir = f"outputs/{now.strftime('%Y')}/{now.strftime('%m')}/{now.strftime('%d')}"
        os.makedirs(log_dir, exist_ok=True)  # Garante que a pasta exista

        log_file = os.path.join(log_dir, f"logs{now.strftime('%Y%m%d')}.txt")

        # Configuração do logger
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )

    except Exception as e:
        print(f"❌ Erro ao configurar o logger: {e}")

def register_log(message, level="info", company_name="Desconhecido", robot_name="Desconhecido"):
    """
    Registra mensagens de log e envia os dados para a API REST.
    """
    setup_logger()

    levels = {
        "info": logging.info,
        "error": logging.error,
        "critical": logging.critical,
        "debug": logging.debug,
    }

    # Mapeamento do status conforme o nível do log
    status_map = {
        "info": "1",
        "error": "2",
        "critical": "3",
        "debug": "4"
    }

    log_entry = {
        "cliente": company_name,
        "id_robo": robot_name,
        "nivel": level.upper(),
        "status": status_map.get(level, "1"),  # Se o nível não for encontrado, assume "1" (info)
        "message": message
    }

    log_function = levels.get(level, logging.info)
    log_function(message)
    print(log_entry)

    # Enviar o log para a API REST via webhook
    try:
        webhook_url = "http://177.39.21.61:3009/logs" 
        response = requests.post(webhook_url, json=log_entry)

        # Verificar a resposta da API
        if response.status_code == 201:
            print("Log enviado com sucesso para a API!")
        else:
            print(f"Erro ao enviar log para a API. Status: {response.status_code}")
            print(f"Resposta da API: {response.text}")  # Exibe o corpo da resposta da API para debugging
    
    except Exception as e:
        print(f"Erro ao enviar log para a API: {e}")


register_log("teste", "debug", "trajetoria", "apilogs")
