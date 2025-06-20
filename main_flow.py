# ocr_extractor.py
def extract_ocr_data(image_path):
    """
    Aplica OCR na imagem para extrair dados como número da nota fiscal, rota e endereço.
    Substituir implementação real com Vista-OCR, LOCR ou LongFin.
    """
    print("[OCR] Extraindo dados OCR da imagem...")
    return {
        "nf_number": "NF123456",
        "route_number": "R001",
        "address": "Rua Exemplo, 123 - SP"
    }


# metadata_reader.py
from datetime import datetime

def extract_metadata(image_path):
    """
    Lê metadados EXIF da imagem: data de captura, GPS (se houver).
    """
    print("[Metadata] Lendo metadados da imagem...")
    return {
        "datetime": datetime.now(),
        "camera_model": "MotoG20",
        "gps": (-23.5505, -46.6333)  # Exemplo: São Paulo
    }


# gps_device_reader.py
def get_device_location():
    """
    Simula a captura da geolocalização atual do dispositivo.
    """
    print("[GPS-Device] Capturando localização do celular...")
    return (-23.5505, -46.6333)  # Exemplo: São Paulo


# gps_vehicle_fetcher.py
def get_vehicle_location(timestamp):
    """
    Consulta a localização do veículo com base no timestamp da foto.
    Aqui está simulado. Em produção, conecta à API do rastreador.
    """
    print("[GPS-Vehicle] Consultando localização do veículo...")
    return (-23.5510, -46.6340)


# validator.py
from geopy.distance import geodesic

def validate_delivery(ocr_data, metadata, device_gps, vehicle_gps):
    """
    Valida se os dados extraídos são consistentes:
    - Endereço OCR vs GPS
    - Hora coerente
    - Proximidade veículo vs dispositivo
    """
    print("[Validator] Validando consistência da entrega...")

    gps_distance = geodesic(device_gps, vehicle_gps).km
    is_close = gps_distance < 0.5  # tolerância de 500m

    return {
        "is_valid": is_close,
        "nf_number": ocr_data["nf_number"],
        "expected_address": ocr_data["address"],
        "photo_taken_at": metadata["datetime"].isoformat(),
        "device_gps": device_gps,
        "vehicle_gps": vehicle_gps,
        "distance": round(gps_distance, 3)
    }


# notifier.py
def send_alert(data):
    """
    Envia alerta para o motorista sobre possível entrega errada.
    Em produção, usar push notification ou WhatsApp API.
    """
    print("[ALERTA] Entrega possivelmente errada detectada!")
    print(f" - NF: {data['nf_number']}")
    print(f" - Distância entre dispositivo e veículo: {data['distance']} km")
    print(f" - Endereço esperado: {data['expected_address']}")


def main():
    """
    Função principal que executa o fluxo completo de validação de entrega
    """
    print("=== Sistema de Validação de Entrega ===\n")
    
    # Caminho da imagem de exemplo
    # image_path = "samples/WhatsApp Image 2025-06-20 at 13.39.16.jpeg"
    image_path = "samples/test_iphone.HEIC"
    # image_path = "samples/test_photo.jpg"
    
    
    # 1. Extrair dados OCR
    ocr_data = extract_ocr_data(image_path)
    
    # 2. Extrair metadados da imagem
    metadata = extract_metadata(image_path)
    
    # 3. Obter localização do dispositivo
    device_gps = get_device_location()
    
    # 4. Obter localização do veículo
    vehicle_gps = get_vehicle_location(metadata["datetime"])
    
    # 5. Validar entrega
    validation_result = validate_delivery(ocr_data, metadata, device_gps, vehicle_gps)
    
    # 6. Mostrar resultado
    print("\n=== Resultado da Validação ===")
    print(f"Entrega válida: {'✅ SIM' if validation_result['is_valid'] else '❌ NÃO'}")
    print(f"Nota Fiscal: {validation_result['nf_number']}")
    print(f"Endereço esperado: {validation_result['expected_address']}")
    print(f"Data/Hora da foto: {validation_result['photo_taken_at']}")
    print(f"GPS do dispositivo: {validation_result['device_gps']}")
    print(f"GPS do veículo: {validation_result['vehicle_gps']}")
    print(f"Distância: {validation_result['distance']} km")
    
    # 7. Enviar alerta se necessário
    if not validation_result['is_valid']:
        print()
        send_alert(validation_result)
    else:
        print("\n✅ Entrega validada com sucesso!")


if __name__ == "__main__":
    main()