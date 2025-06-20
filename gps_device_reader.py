# gps_device_reader.py
def get_device_location():
    """
    Simula a captura da geolocalização atual do dispositivo (como se fosse do celular).
    Em uma aplicação real, isso viria do EXIF da foto, GPS do app, ou sensor do dispositivo.
    """
    print("[GPS-Device] Capturando localização simulada do celular...")
    return (-23.5505, -46.6333)  # Exemplo: São Paulo, SP