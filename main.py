# main.py
import os
from ocr_extractor import extract_ocr_data
from metadata_reader import extract_metadata
from gps_device_reader import get_device_location
from gps_vehicle_fetcher import get_vehicle_location
from validator import validate_delivery
from notifier import send_alert

def process_delivery(photo_path):
    """
    Processa uma entrega com base na foto fornecida.
    
    Args:
        photo_path: Caminho para o arquivo de imagem
        
    Returns:
        dict: Resultado da validação da entrega
    """
    print("\n[INFO] Iniciando validação da entrega com base na imagem...")
    print(f"[DEBUG] Arquivo de imagem: {photo_path}")
    
    # Breakpoint sugerido aqui para debug inicial
    if os.getenv('DEBUG_MODE'):
        print(f"[DEBUG] Modo debug ativado")
        import pdb; pdb.set_trace()

    # 1. OCR
    print("[DEBUG] Etapa 1: Extração OCR")
    ocr_data = extract_ocr_data(photo_path)

    # 2. Metadados (data e GPS da imagem)
    print("[DEBUG] Etapa 2: Extração de metadados")
    metadata = extract_metadata(photo_path)

    # 3. GPS atual do celular (poderia ser via EXIF também)
    print("[DEBUG] Etapa 3: GPS do dispositivo")
    device_gps = metadata.get("gps") or get_device_location()

    # 4. Localização do veículo no momento da imagem
    print("[DEBUG] Etapa 4: GPS do veículo")
    vehicle_gps = get_vehicle_location(timestamp=metadata["datetime"])

    # 5. Validação dos dados
    print("[DEBUG] Etapa 5: Validação")
    result = validate_delivery(
        ocr_data=ocr_data,
        metadata=metadata,
        device_gps=device_gps,
        vehicle_gps=vehicle_gps
    )

    # 6. Alerta se for inconsistente
    print("[DEBUG] Etapa 6: Verificação de alertas")
    if not result['is_valid']:
        send_alert(result)

    return result


if __name__ == '__main__':
    # Verificar se há uma imagem especificada via variável de ambiente (para debug)
    debug_image = os.getenv('DEBUG_IMAGE')
    
    if debug_image:
        path = debug_image
        print(f"[DEBUG] Usando imagem de debug: {path}")
    else:
        # Imagens disponíveis para teste
        # path = 'samples/_test_photo.jpeg'  # ✅ Funciona
        # path = 'samples/test_photo.jpg'    # Vamos testar
        path = 'samples/test_001.jpg'        # iPhone com EXIF real
        # path = 'samples/test_iphone.HEIC'  # Formato HEIC pode ter problemas
    
    print(f"[INFO] Processando imagem: {path}")
    
    # Breakpoint sugerido aqui para debug do main
    if os.getenv('DEBUG_MODE'):
        print("[DEBUG] Modo debug do main ativado")
        import pdb; pdb.set_trace()
    
    output = process_delivery(path)
    
    print("\n" + "="*50)
    print("RESULTADO FINAL:")
    print("="*50)
    for k, v in output.items():
        print(f"{k:20}: {v}")
    print("="*50)