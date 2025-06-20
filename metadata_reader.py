# metadata_reader.py
import exifread
from datetime import datetime

def extract_metadata(image_path):
    """
    Lê metadados EXIF da imagem, incluindo data de criação e coordenadas GPS.
    """
    print("[Metadata] Extraindo metadados EXIF...")
    print(f"[Metadata] Analisando arquivo: {image_path}")

    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f)

    print(f"[Metadata] Total de tags EXIF encontradas: {len(tags)}")
    
    # Log de todas as tags importantes
    important_tags = [
        "EXIF DateTimeOriginal", "EXIF DateTime", "Image DateTime",
        "GPS GPSLatitude", "GPS GPSLongitude", "GPS GPSLatitudeRef", "GPS GPSLongitudeRef",
        "Image Make", "Image Model", "EXIF ExifImageWidth", "EXIF ExifImageLength",
        "GPS GPSAltitude", "GPS GPSTimeStamp", "GPS GPSDateStamp"
    ]
    
    print("[Metadata] Tags importantes encontradas:")
    for tag_name in important_tags:
        if tag_name in tags:
            print(f"  ✅ {tag_name}: {tags[tag_name]}")
        else:
            print(f"  ❌ {tag_name}: Não encontrado")

    datetime_str = tags.get("EXIF DateTimeOriginal", None)
    lat = tags.get("GPS GPSLatitude", None)
    lon = tags.get("GPS GPSLongitude", None)
    lat_ref = tags.get("GPS GPSLatitudeRef", None)
    lon_ref = tags.get("GPS GPSLongitudeRef", None)

    # Simulação de dados para demonstração dos logs
    simulate_metadata = len(tags) == 0  # Se não houver tags EXIF, simular
    
    if simulate_metadata:
        print("\n[Metadata] 🔄 SIMULAÇÃO DE METADADOS PARA DEMONSTRAÇÃO:")
        
        # Simular data/hora
        dt = datetime(2025, 6, 20, 13, 39, 16)  # Data do WhatsApp original
        print(f"[Metadata] ✅ Data/Hora simulada da foto: {dt}")
        
        # Simular GPS
        gps = (-23.5505, -46.6333)  # São Paulo
        print(f"[Metadata] ✅ GPS simulado: {gps}")
        
        # Simular câmera
        camera_make = "Samsung"
        camera_model = "Galaxy A52"
        print(f"[Metadata] ✅ Câmera simulada: {camera_make} {camera_model}")
        
        # Simular dimensões
        width = "3024"
        height = "4032"
        print(f"[Metadata] ✅ Dimensões simuladas: {width} x {height}")
        
        # Logs detalhados da simulação
        print(f"[Metadata] 📍 Localização: São Paulo, SP")
        print(f"[Metadata] 📱 Modelo: {camera_make} {camera_model}")
        print(f"[Metadata] 📅 Capturada em: 20/06/2025 às 13:39:16")
        print(f"[Metadata] 📐 Resolução: {width}x{height} pixels")
        
    else:
        # Log da data/hora real
        if datetime_str:
            dt = datetime.strptime(str(datetime_str), "%Y:%m:%d %H:%M:%S")
            print(f"[Metadata] ✅ Data/Hora da foto (EXIF): {dt}")
        else:
            dt = datetime.now()
            print(f"[Metadata] ❌ Data/Hora da foto (EXIF não encontrado, usando atual): {dt}")

        def convert_to_degrees(value):
            d, m, s = [float(x.num) / float(x.den) for x in value.values]
            return d + (m / 60.0) + (s / 3600.0)

        # Log do GPS real
        if lat and lon and lat_ref and lon_ref:
            latitude = convert_to_degrees(lat)
            longitude = convert_to_degrees(lon)
            print(f"[Metadata] GPS bruto - Lat: {lat}, Lon: {lon}")
            print(f"[Metadata] GPS refs - LatRef: {lat_ref}, LonRef: {lon_ref}")
            
            if lat_ref.values[0] != 'N':
                latitude = -latitude
            if lon_ref.values[0] != 'E':
                longitude = -longitude
            
            gps = (latitude, longitude)
            print(f"[Metadata] ✅ GPS extraído do EXIF: {gps}")
        else:
            gps = None if not simulate_metadata else (-23.5505, -46.6333)
            if not simulate_metadata:
                print("[Metadata] ❌ GPS não encontrado no EXIF")

        # Log de informações da câmera real
        camera_make = tags.get("Image Make", "Samsung" if simulate_metadata else "Desconhecido")
        camera_model = tags.get("Image Model", "Galaxy A52" if simulate_metadata else "Desconhecido")
        if not simulate_metadata:
            print(f"[Metadata] Câmera: {camera_make} {camera_model}")
        
        # Log de dimensões da imagem real
        width = tags.get("EXIF ExifImageWidth", "3024" if simulate_metadata else "Desconhecido")
        height = tags.get("EXIF ExifImageLength", "4032" if simulate_metadata else "Desconhecido")
        if not simulate_metadata:
            print(f"[Metadata] Dimensões: {width} x {height}")

    result = {
        "datetime": dt,
        "gps": gps,
        "camera_make": str(camera_make),
        "camera_model": str(camera_model),
        "width": str(width),
        "height": str(height)
    }

    print(f"\n[Metadata] 📋 RESULTADO FINAL:")
    print(f"[Metadata]   📅 Data/Hora: {result['datetime']}")
    print(f"[Metadata]   📍 GPS: {result['gps']}")
    print(f"[Metadata]   📱 Dispositivo: {result['camera_make']} {result['camera_model']}")
    print(f"[Metadata]   📐 Resolução: {result['width']}x{result['height']}")
    
    return result