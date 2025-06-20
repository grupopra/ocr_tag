# ocr_extractor.py
import pytesseract
from PIL import Image
import numpy as np
import re
import io
import tempfile
import os

def extract_ocr_data(image_path):
    """
    Aplica OCR real na imagem usando pytesseract para extrair texto livre.
    """
    print("[OCR] Usando Tesseract para extrair texto da imagem...")
    print(f"[OCR] Processando arquivo: {image_path}")

    try:
        # Abrir a imagem
        image = Image.open(image_path)
        print(f"[OCR] Imagem carregada: {image.format}, {image.size}, {image.mode}")
        
        # 🔧 CONVERSÃO MPO → JPEG se necessário
        if image.format == 'MPO':
            print("[OCR] ⚠️ Formato MPO detectado - convertendo para JPEG...")
            
            # Converter para RGB se necessário
            if image.mode != 'RGB':
                print(f"[OCR] Convertendo de {image.mode} para RGB")
                image = image.convert('RGB')
            
            # Criar arquivo temporário JPEG
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                temp_path = temp_file.name
                image.save(temp_path, 'JPEG', quality=95)
                print(f"[OCR] ✅ MPO convertido para JPEG temporário: {temp_path}")
            
            # Reabrir como JPEG
            image = Image.open(temp_path)
            print(f"[OCR] ✅ Imagem recarregada: {image.format}, {image.size}, {image.mode}")
            
            # Usar o arquivo temporário para OCR
            ocr_image_path = temp_path
        else:
            # Converter para RGB se necessário (para compatibilidade)
            if image.mode != 'RGB':
                print(f"[OCR] Convertendo de {image.mode} para RGB")
                image = image.convert('RGB')
            ocr_image_path = image_path
        
        # Tentar OCR com diferentes configurações
        try:
            # Primeira tentativa com configuração padrão
            print(f"[OCR] Info da imagem: {image.info}")
            raw_text = pytesseract.image_to_string(image, lang='por+eng', config='--psm 6')
            print("[OCR] ✅ OCR executado com sucesso (por+eng)")
        except Exception as e1:
            print(f"[OCR] ⚠️ Primeira tentativa falhou: {e1}")
            try:
                # Segunda tentativa apenas com inglês
                raw_text = pytesseract.image_to_string(image, lang='eng')
                print("[OCR] ✅ OCR executado com sucesso (eng)")
            except Exception as e2:
                print(f"[OCR] ⚠️ Segunda tentativa falhou: {e2}")
                try:
                    # Terceira tentativa sem especificar idioma
                    raw_text = pytesseract.image_to_string(image)
                    print("[OCR] ✅ OCR executado com sucesso (padrão)")
                except Exception as e3:
                    print(f"[OCR] ❌ Todas as tentativas falharam: {e3}")
                    raw_text = "[ERRO] Não foi possível extrair texto da imagem"

        print("[OCR] Texto extraído:")
        print(raw_text)
        print("-" * 50)

        # Regex para NF, rota e endereço
        nf_match = re.search(r'(NF\d{6,})', raw_text, re.IGNORECASE)
        rota_match = re.search(r'(R\d{3,})', raw_text, re.IGNORECASE)
        endereco_match = re.search(r'Rua\s+[\w\s]+,\s*\d+.*', raw_text)

        # Aqui você pode usar regex para extrair NF, endereço, etc.
        result = {
            "nf_number": nf_match.group(1) if nf_match else "NF_NOT_FOUND",
            "route_number": rota_match.group(1) if rota_match else "R_NOT_FOUND",
            "address": endereco_match.group(0) if endereco_match else "ADDRESS_NOT_FOUND",
            "raw_text": raw_text
        }
        
        # 🗑️ Limpar arquivo temporário se foi criado
        if image.format == 'JPEG' and 'temp_path' in locals():
            try:
                os.unlink(temp_path)
                print(f"[OCR] 🗑️ Arquivo temporário removido: {temp_path}")
            except:
                pass
        
        return result
        
    except Exception as e:
        print(f"[OCR] ❌ Erro ao processar imagem: {e}")
        return {
            "nf_number": "NF_ERROR",
            "route_number": "R_ERROR",
            "address": "Erro ao processar imagem",
            "raw_text": f"[ERRO] {str(e)}"
        }