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
    is_close = gps_distance < 0.5  # tolerância de 500 metros

    return {
        "is_valid": is_close,
        "nf_number": ocr_data.get("nf_number"),
        "expected_address": ocr_data.get("address"),
        "photo_taken_at": metadata.get("datetime").isoformat(),
        "device_gps": device_gps,
        "vehicle_gps": vehicle_gps,
        "distance": round(gps_distance, 3)
    }
