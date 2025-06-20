"""
🚚 Sistema Inteligente de Validação de Entregas - Main com Aprendizado
Versão 2.0 com IA, aprendizado automático e validação multi-camadas
"""

import os
from datetime import datetime
from typing import Dict, Any

# Importações do sistema base (mantidas para compatibilidade)
from ocr_extractor import extract_ocr_data
from metadata_reader import extract_metadata
from gps_device_reader import get_device_location
from gps_vehicle_fetcher import get_vehicle_location
from notifier import send_alert

# 🧠 Importações do novo sistema inteligente
from lib import tags_patterns, learning_engine, enhanced_validators
from lib.tags_patterns import CompanyType
from lib.validators import ValidationResult


def process_intelligent_delivery(photo_path: str) -> Dict[str, Any]:
    """
    🧠 Processamento inteligente de entrega com aprendizado automático
    
    Args:
        photo_path: Caminho para o arquivo de imagem
        
    Returns:
        dict: Resultado completo da validação inteligente
    """
    print("\n🚚 [INFO] Iniciando validação INTELIGENTE da entrega...")
    print(f"📸 [DEBUG] Arquivo de imagem: {photo_path}")
    
    # Breakpoint para debug se necessário
    if os.getenv('DEBUG_MODE'):
        print(f"🔧 [DEBUG] Modo debug ativado")
        import pdb; pdb.set_trace()

    # ===========================================
    # ETAPA 1: OCR TRADICIONAL (Sistema Base)
    # ===========================================
    print("🔍 [DEBUG] Etapa 1: Extração OCR básica")
    ocr_data = extract_ocr_data(photo_path)
    ocr_text = ocr_data.get("raw_text", "")
    
    print(f"📝 [OCR] Texto extraído: {len(ocr_text)} caracteres")
    if len(ocr_text) > 100:
        print(f"📝 [OCR] Preview: {ocr_text[:100]}...")
    else:
        print(f"📝 [OCR] Texto completo: {ocr_text}")

    # ===========================================
    # ETAPA 2: ANÁLISE INTELIGENTE DE PADRÕES
    # ===========================================
    print("🧠 [DEBUG] Etapa 2: Análise inteligente de padrões")
    
    # Verificar cache de reconhecimento rápido primeiro
    quick_company = learning_engine.quick_recognition(ocr_text)
    if quick_company:
        print(f"⚡ [CACHE] Reconhecimento instantâneo: {quick_company}")
    
    # Análise completa dos padrões
    analysis_result = tags_patterns.analyze_full_text(ocr_text)
    
    print(f"🏢 [IA] Empresa detectada: {analysis_result['company'].company.value}")
    print(f"🎯 [IA] Confiança da empresa: {analysis_result['company'].confidence:.2f}")
    print(f"📊 [IA] Dados extraídos: {len(analysis_result['extracted_data'])} campos")
    print(f"💯 [IA] Confiança geral: {analysis_result['overall_confidence']:.2f}")
    print(f"💡 [IA] Recomendação: {analysis_result['analysis_summary']['recommendation']}")
    
    # Mostrar dados extraídos
    for data_type, (value, confidence) in analysis_result['extracted_data'].items():
        print(f"   📋 {data_type}: {value} (confiança: {confidence:.2f})")

    # ===========================================
    # ETAPA 3: METADADOS E GPS (Sistema Base)
    # ===========================================
    print("📱 [DEBUG] Etapa 3: Extração de metadados")
    metadata = extract_metadata(photo_path)
    
    print("🗺️ [DEBUG] Etapa 4: GPS do dispositivo")
    device_gps = metadata.get("gps") or get_device_location()
    
    if device_gps:
        print(f"📍 [GPS] Localização do dispositivo: {device_gps[0]:.6f}, {device_gps[1]:.6f}")
    else:
        print("⚠️ [GPS] Não foi possível obter localização do dispositivo")
        device_gps = (0.0, 0.0)  # Fallback
    
    print("🚗 [DEBUG] Etapa 5: GPS do veículo")
    vehicle_gps = get_vehicle_location(timestamp=metadata.get("datetime") or datetime.now())
    
    if vehicle_gps:
        print(f"🚛 [GPS] Localização do veículo: {vehicle_gps[0]:.6f}, {vehicle_gps[1]:.6f}")

    # ===========================================
    # ETAPA 4: VALIDAÇÃO MULTI-CAMADAS INTELIGENTE
    # ===========================================
    print("🎯 [DEBUG] Etapa 6: Validação inteligente multi-camadas")
    
    # Usar timestamp da imagem ou atual
    validation_timestamp = metadata.get("datetime") or datetime.now()
    
    # Validação abrangente
    validation_result: ValidationResult = enhanced_validators.comprehensive_validation(
        analysis_result=analysis_result,
        device_gps=device_gps,
        timestamp=validation_timestamp
    )
    
    print(f"✅ [VALIDAÇÃO] Entrega válida: {validation_result.is_valid}")
    print(f"📊 [VALIDAÇÃO] Score de confiança: {validation_result.confidence_score:.2f}")
    print(f"📏 [VALIDAÇÃO] Distância GPS: {validation_result.gps_distance:.3f}km")
    
    # Mostrar detalhes de validação
    for component, details in validation_result.validation_details.items():
        status = "✅" if details["valid"] else "❌"
        print(f"   {status} {component}: {details['score']:.2f} - {details['details']}")
    
    # Mostrar recomendações
    for rec in validation_result.recommendations:
        print(f"💡 [RECOMENDAÇÃO] {rec}")
    
    # Mostrar warnings se houver
    for warning in validation_result.warnings:
        print(f"⚠️ [WARNING] {warning}")

    # ===========================================
    # ETAPA 5: APRENDIZADO AUTOMÁTICO
    # ===========================================
    print("📚 [DEBUG] Etapa 7: Sessão de aprendizado automático")
    
    # Determinar se GPS e rota estão válidos para aprendizado
    gps_validation = device_gps != (0.0, 0.0) and validation_result.gps_distance < 0.5
    route_match = validation_result.matched_route is not None
    
    # Processar sessão de aprendizado
    learning_session = learning_engine.process_learning_session(
        image_path=photo_path,
        ocr_text=ocr_text,
        analysis_result=analysis_result,
        gps_validation=gps_validation,
        route_match=route_match
    )
    
    print(f"🧠 [APRENDIZADO] Empresa: {learning_session.company_detected}")
    print(f"🧠 [APRENDIZADO] Resultado: {learning_session.learning_outcome}")
    
    # Mostrar estatísticas de aprendizado
    learning_stats = learning_engine.get_learning_stats()
    print(f"📈 [ESTATÍSTICAS] Total processado: {learning_stats['total_images_processed']}")
    print(f"📈 [ESTATÍSTICAS] Precisão atual: {learning_stats['recognition_accuracy']:.1f}%")
    print(f"📈 [ESTATÍSTICAS] Empresas aprendidas: {learning_stats['companies_learned']}")

    # ===========================================
    # ETAPA 6: ALERTAS E NOTIFICAÇÕES
    # ===========================================
    print("🔔 [DEBUG] Etapa 8: Verificação de alertas")
    
    # Usar validação tradicional como fallback para alertas
    traditional_result = {
        'is_valid': validation_result.is_valid,
        'confidence': validation_result.confidence_score,
        'reason': ', '.join(validation_result.warnings) if validation_result.warnings else 'Validação OK',
        'gps_distance': validation_result.gps_distance,
        'company_detected': analysis_result['company'].company.value,
        'data_quality': len(analysis_result['extracted_data'])
    }
    
    if not validation_result.is_valid:
        print("🚨 [ALERTA] Enviando notificação de entrega suspeita")
        send_alert(traditional_result)
    else:
        print("✅ [ALERTA] Nenhum alerta necessário - Entrega válida")

    # ===========================================
    # RESULTADO FINAL CONSOLIDADO
    # ===========================================
    
    return {
        # Dados básicos
        "image_path": photo_path,
        "timestamp": validation_timestamp.isoformat(),
        
        # OCR e análise
        "ocr_text_length": len(ocr_text),
        "ocr_preview": ocr_text[:100] + "..." if len(ocr_text) > 100 else ocr_text,
        
        # IA e reconhecimento
        "company_detected": analysis_result['company'].company.value,
        "company_confidence": analysis_result['company'].confidence,
        "pattern_used": analysis_result['company'].pattern_used,
        "data_fields_extracted": len(analysis_result['extracted_data']),
        "extracted_data": dict(analysis_result['extracted_data']),
        "overall_ai_confidence": analysis_result['overall_confidence'],
        
        # Validação
        "is_valid": validation_result.is_valid,
        "validation_score": validation_result.confidence_score,
        "gps_distance_km": validation_result.gps_distance,
        "matched_route_id": validation_result.matched_route.get("route_id") if validation_result.matched_route else None,
        "validation_details": validation_result.validation_details,
        
        # Aprendizado
        "learning_outcome": learning_session.learning_outcome,
        "total_images_processed": learning_stats['total_images_processed'],
        "current_accuracy": learning_stats['recognition_accuracy'],
        "companies_learned": learning_stats['companies_learned'],
        
        # Recomendações e warnings
        "recommendations": validation_result.recommendations,
        "warnings": validation_result.warnings,
        
        # Compatibilidade com sistema antigo
        "legacy_ocr_data": ocr_data,
        "legacy_metadata": metadata,
        "device_gps": device_gps,
        "vehicle_gps": vehicle_gps
    }


def main():
    """Função principal do sistema inteligente"""
    
    print("="*60)
    print("🚚 SISTEMA INTELIGENTE DE VALIDAÇÃO DE ENTREGAS v2.0")
    print("🧠 Com aprendizado automático e IA de reconhecimento")
    print("="*60)
    
    # Verificar imagem de debug ou usar padrão
    debug_image = os.getenv('DEBUG_IMAGE')
    
    if debug_image:
        path = debug_image
        print(f"🔧 [DEBUG] Usando imagem de debug: {path}")
    else:
        # Usar imagem real do iPhone para teste
        path = 'samples/test_001.jpg'
        print(f"📱 [INFO] Usando imagem real do iPhone: {path}")
    
    if not os.path.exists(path):
        print(f"❌ [ERRO] Arquivo não encontrado: {path}")
        return
    
    print(f"🚀 [INFO] Processando com sistema inteligente...")
    
    # Breakpoint principal para debug
    if os.getenv('DEBUG_MODE'):
        print("🔧 [DEBUG] Modo debug do main ativado")
        import pdb; pdb.set_trace()
    
    # Processar com sistema inteligente
    result = process_intelligent_delivery(path)
    
    # ===========================================
    # EXIBIÇÃO DOS RESULTADOS
    # ===========================================
    
    print("\n" + "="*60)
    print("📊 RESULTADO FINAL DO SISTEMA INTELIGENTE")
    print("="*60)
    
    # Seção: Reconhecimento IA
    print("🧠 RECONHECIMENTO INTELIGENTE:")
    print(f"   🏢 Empresa: {result['company_detected']}")
    print(f"   🎯 Confiança: {result['company_confidence']:.2f}")
    print(f"   📋 Dados extraídos: {result['data_fields_extracted']} campos")
    print(f"   💯 IA Geral: {result['overall_ai_confidence']:.2f}")
    
    # Seção: Validação
    print("\n🎯 VALIDAÇÃO MULTI-CAMADAS:")
    print(f"   ✅ Válida: {result['is_valid']}")
    print(f"   📊 Score: {result['validation_score']:.2f}")
    print(f"   📏 Distância GPS: {result['gps_distance_km']:.3f}km")
    print(f"   🗺️ Rota: {result['matched_route_id'] or 'Não encontrada'}")
    
    # Seção: Aprendizado
    print("\n📚 APRENDIZADO AUTOMÁTICO:")
    print(f"   🧠 Resultado: {result['learning_outcome']}")
    print(f"   📈 Total processado: {result['total_images_processed']}")
    print(f"   🎯 Precisão atual: {result['current_accuracy']:.1f}%")
    print(f"   🏢 Empresas aprendidas: {result['companies_learned']}")
    
    # Seção: Dados extraídos
    if result['extracted_data']:
        print("\n📋 DADOS EXTRAÍDOS:")
        for data_type, (value, confidence) in result['extracted_data'].items():
            print(f"   📝 {data_type}: {value} ({confidence:.2f})")
    
    # Seção: Recomendações
    if result['recommendations']:
        print("\n💡 RECOMENDAÇÕES:")
        for rec in result['recommendations']:
            print(f"   {rec}")
    
    # Seção: Warnings
    if result['warnings']:
        print("\n⚠️ WARNINGS:")
        for warning in result['warnings']:
            print(f"   {warning}")
    
    print("="*60)
    print("🎉 PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
    print("📚 Sistema aprendeu com esta imagem e evoluiu automaticamente")
    print("="*60)


if __name__ == '__main__':
    main() 