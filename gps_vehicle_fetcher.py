# gps_vehicle_fetcher.py
from datetime import datetime

def get_vehicle_location(timestamp: datetime):
    """
    Simula a consulta de localização do veículo com base no timestamp da imagem.
    Em uma aplicação real, essa função consultaria a API do sistema de rastreamento veicular.
    """
    print("[GPS-Vehicle] Consultando localização do veículo com base no timestamp...")
    # Simula leve desvio de localização
    return (-23.5510, -46.6340)