# notifier.py
def send_alert(data):
    """
    Simula o envio de alerta ao motorista ou sistema de gestão
    informando que há possível inconsistência na entrega.
    """
    print("\n[ALERTA] Entrega possivelmente inconsistente detectada!")
    print(f" - NF: {data.get('nf_number')}")
    print(f" - Endereço esperado (OCR): {data.get('expected_address')}")
    print(f" - GPS do dispositivo: {data.get('device_gps')}")
    print(f" - GPS do veículo: {data.get('vehicle_gps')}")
    print(f" - Distância entre dispositivo e veículo: {data.get('distance')} km")
    print(" - Ação sugerida: verificar com o motorista ou reprocessar a entrega.")