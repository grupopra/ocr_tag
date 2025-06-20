"""
🎯 Validadores Específicos para Sistema de Aprendizado
Validação inteligente que considera contexto e histórico de aprendizado
"""

import csv
import math
from datetime import datetime, time
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import re

from .tags_patterns import PatternMatch, CompanyType
from .learning_engine import LearningEngine

class ValidationResult:
    """Resultado detalhado de validação"""
    
    def __init__(self):
        self.is_valid = False
        self.confidence_score = 0.0
        self.validation_details = {}
        self.warnings = []
        self.recommendations = []
        self.matched_route = None
        self.gps_distance = 0.0
        
    def add_validation(self, component: str, is_valid: bool, score: float, details: str = ""):
        """Adiciona resultado de validação de um componente"""
        self.validation_details[component] = {
            "valid": is_valid,
            "score": score,
            "details": details
        }
    
    def calculate_overall_score(self, weights: Optional[Dict[str, float]] = None):
        """Calcula score geral baseado nos pesos dos componentes"""
        if weights is None:
            weights = {
                "gps_match": 0.40,
                "ocr_match": 0.35,
                "temporal_match": 0.15,
                "pattern_recognition": 0.10
            }
        
        total_score = 0.0
        total_weight = 0.0
        
        for component, weight in weights.items():
            if component in self.validation_details:
                total_score += self.validation_details[component]["score"] * weight
                total_weight += weight
        
        self.confidence_score = total_score / max(total_weight, 1.0) if total_weight > 0 else 0.0
        self.is_valid = self.confidence_score >= 0.7  # Threshold de 70%
        
        return self.confidence_score

class EnhancedValidators:
    """Sistema de validação melhorado com aprendizado"""
    
    def __init__(self, database_path: str = "lib/delivery_database.csv"):
        self.database_path = Path(database_path)
        self.delivery_routes = self._load_delivery_database()
        
    def _load_delivery_database(self) -> List[Dict]:
        """Carrega base de dados de rotas de entrega"""
        routes = []
        
        if not self.database_path.exists():
            print(f"⚠️ Base de dados não encontrada: {self.database_path}")
            return routes
        
        try:
            with open(self.database_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                routes = list(reader)
                
            print(f"📊 Carregadas {len(routes)} rotas da base de dados")
            
        except Exception as e:
            print(f"❌ Erro ao carregar base de dados: {e}")
        
        return routes
    
    def comprehensive_validation(self, 
                               analysis_result: Dict,
                               device_gps: Tuple[float, float],
                               timestamp: Optional[datetime] = None) -> ValidationResult:
        """Validação abrangente integrando todos os componentes"""
        
        result = ValidationResult()
        
        if timestamp is None:
            timestamp = datetime.now()
        
        # 1. Validação GPS
        gps_validation = self._validate_gps_location(analysis_result, device_gps)
        result.add_validation("gps_match", gps_validation["valid"], gps_validation["score"], gps_validation["details"])
        result.gps_distance = gps_validation.get("distance", 0.0)
        result.matched_route = gps_validation.get("matched_route")
        
        # 2. Validação OCR/Dados
        ocr_validation = self._validate_ocr_data(analysis_result)
        result.add_validation("ocr_match", ocr_validation["valid"], ocr_validation["score"], ocr_validation["details"])
        
        # 3. Validação Temporal
        if result.matched_route:
            temporal_validation = self._validate_delivery_time(result.matched_route, timestamp)
            result.add_validation("temporal_match", temporal_validation["valid"], temporal_validation["score"], temporal_validation["details"])
        
        # 4. Reconhecimento de Padrões
        pattern_validation = self._validate_pattern_recognition(analysis_result)
        result.add_validation("pattern_recognition", pattern_validation["valid"], pattern_validation["score"], pattern_validation["details"])
        
        # 5. Calcular score final
        result.calculate_overall_score()
        
        # 6. Gerar recomendações
        self._generate_recommendations(result, analysis_result)
        
        return result
    
    def _validate_gps_location(self, analysis_result: Dict, device_gps: Tuple[float, float]) -> Dict:
        """Validação inteligente de localização GPS"""
        
        device_lat, device_lon = device_gps
        best_match = None
        min_distance = float('inf')
        
        # Buscar rota mais próxima
        for route in self.delivery_routes:
            try:
                route_lat = float(route['gps_lat'])
                route_lon = float(route['gps_lon'])
                
                distance = self._calculate_distance(device_lat, device_lon, route_lat, route_lon)
                
                if distance < min_distance:
                    min_distance = distance
                    best_match = route
                    
            except (ValueError, KeyError):
                continue
        
        # Determinar validade baseada na distância
        if min_distance <= 0.05:  # 50m
            score = 1.0
            valid = True
            details = f"GPS exato - distância: {min_distance*1000:.0f}m"
        elif min_distance <= 0.2:  # 200m
            score = 0.8
            valid = True
            details = f"GPS próximo - distância: {min_distance*1000:.0f}m"
        elif min_distance <= 0.5:  # 500m
            score = 0.6
            valid = True
            details = f"GPS aceitável - distância: {min_distance*1000:.0f}m"
        else:
            score = max(0.0, 0.5 - (min_distance * 0.1))  # Penalidade por distância
            valid = False
            details = f"GPS suspeito - distância: {min_distance:.1f}km"
        
        return {
            "valid": valid,
            "score": score,
            "details": details,
            "distance": min_distance,
            "matched_route": best_match
        }
    
    def _validate_ocr_data(self, analysis_result: Dict) -> Dict:
        """Validação dos dados extraídos por OCR"""
        
        extracted_data = analysis_result.get("extracted_data", {})
        company_confidence = analysis_result.get("company", {}).confidence
        
        # Pontuação baseada em dados encontrados
        data_score = 0.0
        data_count = 0
        
        # Verificar cada tipo de dado
        for data_type, (value, confidence) in extracted_data.items():
            if confidence > 0.5:
                data_count += 1
                data_score += confidence
        
        # Normalizar score
        if data_count > 0:
            avg_data_score = data_score / data_count
        else:
            avg_data_score = 0.0
        
        # Combinar com confiança da empresa
        combined_score = (avg_data_score * 0.7) + (company_confidence * 0.3)
        
        valid = combined_score >= 0.6 and data_count >= 2
        
        details = f"Dados extraídos: {data_count} campos (confiança média: {avg_data_score:.2f})"
        
        return {
            "valid": valid,
            "score": combined_score,
            "details": details
        }
    
    def _validate_delivery_time(self, route: Dict, current_time: datetime) -> Dict:
        """Validação da janela de tempo de entrega"""
        
        try:
            # Parse da janela de entrega
            start_time = time.fromisoformat(route['delivery_window_start'])
            end_time = time.fromisoformat(route['delivery_window_end'])
            
            current_time_only = current_time.time()
            
            # Verificar se está dentro da janela
            if start_time <= current_time_only <= end_time:
                score = 1.0
                valid = True
                details = f"Dentro da janela: {start_time}-{end_time}"
            else:
                # Calcular penalidade por estar fora da janela
                if current_time_only < start_time:
                    # Muito cedo
                    minutes_early = (datetime.combine(datetime.today(), start_time) - 
                                   datetime.combine(datetime.today(), current_time_only)).seconds // 60
                    score = max(0.3, 1.0 - (minutes_early * 0.01))  # -1% por minuto
                    details = f"Muito cedo: {minutes_early}min antes da janela"
                else:
                    # Muito tarde
                    minutes_late = (datetime.combine(datetime.today(), current_time_only) - 
                                  datetime.combine(datetime.today(), end_time)).seconds // 60
                    score = max(0.2, 1.0 - (minutes_late * 0.02))  # -2% por minuto
                    details = f"Atrasado: {minutes_late}min após janela"
                
                valid = score >= 0.5
            
        except (ValueError, KeyError) as e:
            score = 0.5  # Score neutro se não conseguir validar
            valid = True
            details = f"Não foi possível validar horário: {e}"
        
        return {
            "valid": valid,
            "score": score,
            "details": details
        }
    
    def _validate_pattern_recognition(self, analysis_result: Dict) -> Dict:
        """Validação do reconhecimento de padrões"""
        
        company_match = analysis_result.get("company")
        
        if not company_match:
            return {"valid": False, "score": 0.0, "details": "Nenhuma empresa detectada"}
        
        # Score baseado na confiança da detecção
        company_confidence = company_match.confidence
        
        if company_match.company != CompanyType.UNKNOWN:
            # Empresa conhecida detectada
            if company_confidence >= 0.8:
                score = 1.0
                details = f"Empresa bem reconhecida: {company_match.company.value} ({company_confidence:.2f})"
            elif company_confidence >= 0.6:
                score = 0.7
                details = f"Empresa reconhecida: {company_match.company.value} ({company_confidence:.2f})"
            else:
                score = 0.4
                details = f"Reconhecimento fraco: {company_match.company.value} ({company_confidence:.2f})"
            
            valid = company_confidence >= 0.5
        else:
            # Empresa desconhecida
            score = 0.3
            valid = False
            details = "Padrão desconhecido - requer investigação"
        
        return {
            "valid": valid,
            "score": score,
            "details": details
        }
    
    def _generate_recommendations(self, result: ValidationResult, analysis_result: Dict):
        """Gera recomendações baseadas nos resultados de validação"""
        
        result.recommendations = []
        result.warnings = []
        
        # Recomendações baseadas no score geral
        if result.confidence_score >= 0.9:
            result.recommendations.append("✅ Entrega totalmente válida - Prosseguir normalmente")
        elif result.confidence_score >= 0.7:
            result.recommendations.append("✅ Entrega válida - Algumas verificações menores")
        elif result.confidence_score >= 0.5:
            result.recommendations.append("⚠️ Entrega questionável - Verificação manual recomendada")
        else:
            result.recommendations.append("❌ Entrega inválida - Investigação necessária")
        
        # Warnings específicos
        if result.gps_distance > 0.5:
            result.warnings.append(f"🚨 GPS muito distante: {result.gps_distance:.1f}km da rota esperada")
        
        if "ocr_match" in result.validation_details and not result.validation_details["ocr_match"]["valid"]:
            result.warnings.append("🔍 Dados OCR insuficientes ou de baixa qualidade")
        
        if "pattern_recognition" in result.validation_details and not result.validation_details["pattern_recognition"]["valid"]:
            result.warnings.append("🆕 Transportadora não reconhecida - Possível novo padrão")
        
        # Recomendações de aprendizado
        company_match = analysis_result.get("company")
        if company_match and company_match.company != CompanyType.UNKNOWN:
            if result.is_valid:
                result.recommendations.append(f"📚 Dados válidos para aprendizado: {company_match.company.value}")
            else:
                result.recommendations.append("❓ Validar manualmente antes de usar para aprendizado")
        
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calcula distância em km entre duas coordenadas usando fórmula de Haversine"""
        
        R = 6371  # Raio da Terra em km
        
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    def find_route_by_data(self, extracted_data: Dict) -> Optional[Dict]:
        """Encontra rota baseada nos dados extraídos"""
        
        for route in self.delivery_routes:
            matches = 0
            
            # Verificar nome do destinatário
            if "recipient_name" in extracted_data:
                ocr_name = extracted_data["recipient_name"][0].lower()
                route_name = route["recipient_name"].lower()
                
                # Verificação fuzzy de nome
                if self._fuzzy_match(ocr_name, route_name, threshold=0.8):
                    matches += 2  # Nome vale mais
            
            # Verificar CEP
            if "cep" in extracted_data:
                ocr_cep = re.sub(r"[^0-9]", "", extracted_data["cep"][0])
                route_cep = re.sub(r"[^0-9]", "", route["cep"])
                
                if ocr_cep == route_cep:
                    matches += 2
            
            # Verificar nota fiscal
            if "nf_number" in extracted_data:
                ocr_nf = extracted_data["nf_number"][0].upper()
                route_nf = route["nf_number"].upper()
                
                if ocr_nf == route_nf:
                    matches += 3  # NF vale mais ainda
            
            # Se tiver pelo menos 2 matches, considerar como rota encontrada
            if matches >= 2:
                return route
        
        return None
    
    def _fuzzy_match(self, text1: str, text2: str, threshold: float = 0.8) -> bool:
        """Verificação fuzzy simples entre dois textos"""
        
        # Remover espaços e converter para minúsculo
        text1_clean = ''.join(text1.split()).lower()
        text2_clean = ''.join(text2.split()).lower()
        
        # Calcular similaridade simples
        if len(text1_clean) == 0 or len(text2_clean) == 0:
            return False
        
        # Usar Levenshtein distance simplificado
        max_len = max(len(text1_clean), len(text2_clean))
        
        if text1_clean in text2_clean or text2_clean in text1_clean:
            return True
        
        # Verificar palavras em comum
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if len(words1) == 0 or len(words2) == 0:
            return False
        
        common_words = words1.intersection(words2)
        similarity = len(common_words) / max(len(words1), len(words2))
        
        return similarity >= threshold


# Instância global
enhanced_validators = EnhancedValidators() 