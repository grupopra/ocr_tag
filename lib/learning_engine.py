"""
🧠 Motor de Aprendizado Inteligente
Sistema que aprende automaticamente com cada etiqueta processada
"""

import json
import pickle
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import csv
from pathlib import Path

from .tags_patterns import CompanyType, PatternMatch, tags_patterns

@dataclass
class LearningSession:
    timestamp: str
    image_path: str
    ocr_text: str
    company_detected: str
    confidence: float
    extracted_data: Dict
    gps_validation: bool
    route_match: bool
    learning_outcome: str

class LearningEngine:
    """Motor de aprendizado que evolui com cada etiqueta processada"""
    
    def __init__(self, models_dir: str = "models"):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)
        
        # Arquivos de conhecimento
        self.patterns_file = self.models_dir / "learned_patterns.json"
        self.signatures_file = self.models_dir / "company_signatures.pkl"
        self.cache_file = self.models_dir / "pattern_cache.json"
        
        # Carregar conhecimento existente
        self.learned_patterns = self._load_learned_patterns()
        self.company_signatures = self._load_company_signatures()
        self.pattern_cache = self._load_pattern_cache()
        
        # Contadores de aprendizado
        self.session_counter = 0
        self.total_processed = self.learned_patterns.get("statistics", {}).get("total_images", 0)
        
    def _load_learned_patterns(self) -> Dict:
        """Carrega padrões aprendidos do arquivo JSON"""
        if self.patterns_file.exists():
            try:
                with open(self.patterns_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erro ao carregar padrões: {e}")
        
        # Estrutura inicial
        return {
            "version": "1.0",
            "last_updated": datetime.now().isoformat(),
            "statistics": {
                "total_images": 0,
                "successful_recognitions": 0,
                "companies_learned": 0,
                "accuracy_evolution": []
            },
            "companies": {
                "amazon": {
                    "confidence_score": 0.0,
                    "total_samples": 0,
                    "successful_validations": 0,
                    "visual_patterns": {
                        "logo_signatures": [],
                        "text_patterns": [],
                        "color_patterns": []
                    },
                    "shortcuts": {},
                    "evolution_timeline": []
                },
                "correios": {
                    "confidence_score": 0.0,
                    "total_samples": 0,
                    "successful_validations": 0,
                    "visual_patterns": {
                        "logo_signatures": [],
                        "text_patterns": [],
                        "color_patterns": []
                    },
                    "shortcuts": {},
                    "evolution_timeline": []
                },
                "mercado_livre": {
                    "confidence_score": 0.0,
                    "total_samples": 0,
                    "successful_validations": 0,
                    "visual_patterns": {
                        "logo_signatures": [],
                        "text_patterns": [],
                        "color_patterns": []
                    },
                    "shortcuts": {},
                    "evolution_timeline": []
                },
                "jadlog": {
                    "confidence_score": 0.0,
                    "total_samples": 0,
                    "successful_validations": 0,
                    "visual_patterns": {
                        "logo_signatures": [],
                        "text_patterns": [],
                        "color_patterns": []
                    },
                    "shortcuts": {},
                    "evolution_timeline": []
                },
                "unknown": {
                    "confidence_score": 0.0,
                    "total_samples": 0,
                    "patterns_to_investigate": []
                }
            }
        }
    
    def _load_company_signatures(self) -> Dict:
        """Carrega assinaturas visuais das empresas"""
        if self.signatures_file.exists():
            try:
                with open(self.signatures_file, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"Erro ao carregar assinaturas: {e}")
        
        return {
            "visual_hashes": {},
            "color_signatures": {},
            "layout_patterns": {}
        }
    
    def _load_pattern_cache(self) -> Dict:
        """Carrega cache de reconhecimento rápido"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erro ao carregar cache: {e}")
        
        return {
            "quick_recognition": {},
            "text_shortcuts": {},
            "pattern_frequency": {}
        }
    
    def process_learning_session(self, 
                                image_path: str,
                                ocr_text: str,
                                analysis_result: Dict,
                                gps_validation: bool = False,
                                route_match: bool = False) -> LearningSession:
        """Processa uma sessão de aprendizado com uma nova etiqueta"""
        
        self.session_counter += 1
        self.total_processed += 1
        
        # Criar sessão de aprendizado
        session = LearningSession(
            timestamp=datetime.now().isoformat(),
            image_path=image_path,
            ocr_text=ocr_text,
            company_detected=analysis_result["company"].company.value,
            confidence=analysis_result["company"].confidence,
            extracted_data=analysis_result["extracted_data"],
            gps_validation=gps_validation,
            route_match=route_match,
            learning_outcome=""
        )
        
        # Processar aprendizado
        if session.company_detected != "unknown":
            self._learn_from_successful_recognition(session, analysis_result)
        else:
            self._learn_from_unknown_pattern(session, analysis_result)
        
        # Atualizar estatísticas
        self._update_statistics(session)
        
        # Salvar conhecimento
        self._save_all_knowledge()
        
        # Log da sessão
        self._log_learning_session(session)
        
        return session
    
    def _learn_from_successful_recognition(self, session: LearningSession, analysis: Dict):
        """Aprende com reconhecimento bem-sucedido"""
        
        company = session.company_detected
        
        # Verificar se empresa existe, se não, criar dinamicamente
        if company not in self.learned_patterns["companies"]:
            print(f"🆕 [APRENDIZADO] Nova empresa detectada: {company} - Criando estrutura...")
            self.learned_patterns["companies"][company] = {
                "confidence_score": 0.0,
                "total_samples": 0,
                "successful_validations": 0,
                "visual_patterns": {
                    "logo_signatures": [],
                    "text_patterns": [],
                    "color_patterns": []
                },
                "shortcuts": {},
                "evolution_timeline": []
            }
        
        company_data = self.learned_patterns["companies"][company]
        
        # Atualizar contadores
        company_data["total_samples"] += 1
        
        if session.gps_validation and session.route_match:
            company_data["successful_validations"] += 1
            session.learning_outcome = "successful_validation"
        else:
            session.learning_outcome = "recognized_but_not_validated"
        
        # Aprender novos padrões de texto
        self._extract_new_text_patterns(session.ocr_text, company_data)
        
        # Criar shortcuts para reconhecimento rápido
        self._create_shortcuts(session.ocr_text, company, analysis)
        
        # Atualizar score de confiança da empresa
        success_rate = company_data["successful_validations"] / company_data["total_samples"]
        company_data["confidence_score"] = min(99.9, 60 + (success_rate * 35) + (company_data["total_samples"] * 0.05))
        
        # Timeline de evolução
        company_data["evolution_timeline"].append({
            "timestamp": session.timestamp,
            "confidence": company_data["confidence_score"],
            "total_samples": company_data["total_samples"],
            "success_rate": success_rate
        })
        
        print(f"📚 Aprendizado: {company} agora tem {company_data['total_samples']} samples (confiança: {company_data['confidence_score']:.1f}%)")
    
    def _learn_from_unknown_pattern(self, session: LearningSession, analysis: Dict):
        """Aprende com padrão desconhecido para investigação futura"""
        
        unknown_data = self.learned_patterns["companies"]["unknown"]
        unknown_data["total_samples"] += 1
        
        # Salvar padrão para investigação
        pattern_to_investigate = {
            "timestamp": session.timestamp,
            "image_path": session.image_path,
            "ocr_text": session.ocr_text[:200],  # Primeiros 200 chars
            "extracted_data": session.extracted_data,
            "potential_patterns": self._identify_potential_patterns(session.ocr_text)
        }
        
        unknown_data["patterns_to_investigate"].append(pattern_to_investigate)
        
        # Manter apenas últimos 50 padrões desconhecidos
        if len(unknown_data["patterns_to_investigate"]) > 50:
            unknown_data["patterns_to_investigate"] = unknown_data["patterns_to_investigate"][-50:]
        
        session.learning_outcome = "unknown_pattern_logged"
        print(f"🔍 Padrão desconhecido salvo para investigação futura")
    
    def _extract_new_text_patterns(self, ocr_text: str, company_data: Dict):
        """Extrai novos padrões de texto do OCR"""
        
        # Palavras-chave que aparecem frequentemente
        words = ocr_text.lower().split()
        
        for word in words:
            if len(word) > 3 and word.isalpha():  # Palavras significativas
                if word not in company_data["visual_patterns"]["text_patterns"]:
                    company_data["visual_patterns"]["text_patterns"].append(word)
        
        # Manter apenas os 50 padrões mais comuns
        if len(company_data["visual_patterns"]["text_patterns"]) > 50:
            company_data["visual_patterns"]["text_patterns"] = company_data["visual_patterns"]["text_patterns"][-50:]
    
    def _create_shortcuts(self, ocr_text: str, company: str, analysis: Dict):
        """Cria shortcuts para reconhecimento rápido"""
        
        # Shortcuts baseados em texto extraído
        key_phrases = []
        
        # Frases da empresa detectada
        if analysis["company"].matched_text:
            key_phrases.append(analysis["company"].matched_text.lower())
        
        # Dados extraídos importantes
        for data_type, (value, confidence) in analysis["extracted_data"].items():
            if confidence > 0.8 and len(value) > 5:
                key_phrases.append(value.lower())
        
        # Salvar shortcuts no cache
        for phrase in key_phrases:
            if phrase not in self.pattern_cache["quick_recognition"]:
                self.pattern_cache["quick_recognition"][phrase] = company
    
    def _identify_potential_patterns(self, ocr_text: str) -> List[str]:
        """Identifica potenciais padrões em texto desconhecido"""
        
        potential_patterns = []
        
        # Códigos de rastreamento
        tracking_codes = tags_patterns.extract_data(ocr_text, "nf_number")
        if tracking_codes:
            potential_patterns.append(f"tracking_code: {tracking_codes[0][0]}")
        
        # Padrões de URL ou domínio
        import re
        urls = re.findall(r'[\w\.-]+\.com\.br|[\w\.-]+\.com', ocr_text.lower())
        if urls:
            potential_patterns.extend([f"url: {url}" for url in urls])
        
        # Padrões de código postal
        postal_codes = re.findall(r'\d{5}-?\d{3}', ocr_text)
        if postal_codes:
            potential_patterns.extend([f"postal: {code}" for code in postal_codes])
        
        return potential_patterns
    
    def _update_statistics(self, session: LearningSession):
        """Atualiza estatísticas gerais do sistema"""
        
        stats = self.learned_patterns["statistics"]
        stats["total_images"] = self.total_processed
        
        if session.company_detected != "unknown":
            stats["successful_recognitions"] += 1
        
        # Calcular precisão atual
        if stats["total_images"] > 0:
            current_accuracy = (stats["successful_recognitions"] / stats["total_images"]) * 100
            
            # Salvar evolução da precisão
            stats["accuracy_evolution"].append({
                "timestamp": session.timestamp,
                "total_images": stats["total_images"],
                "accuracy": current_accuracy
            })
            
            # Manter apenas últimos 100 pontos de evolução
            if len(stats["accuracy_evolution"]) > 100:
                stats["accuracy_evolution"] = stats["accuracy_evolution"][-100:]
        
        # Contar empresas aprendidas
        companies_with_samples = sum(1 for company, data in self.learned_patterns["companies"].items() 
                                   if company != "unknown" and data["total_samples"] > 0)
        stats["companies_learned"] = companies_with_samples
        
        # Atualizar timestamp
        self.learned_patterns["last_updated"] = datetime.now().isoformat()
    
    def _save_all_knowledge(self):
        """Salva todo o conhecimento adquirido"""
        
        # Salvar padrões aprendidos
        with open(self.patterns_file, 'w', encoding='utf-8') as f:
            json.dump(self.learned_patterns, f, indent=2, ensure_ascii=False)
        
        # Salvar assinaturas visuais
        with open(self.signatures_file, 'wb') as f:
            pickle.dump(self.company_signatures, f)
        
        # Salvar cache de reconhecimento
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.pattern_cache, f, indent=2, ensure_ascii=False)
    
    def _log_learning_session(self, session: LearningSession):
        """Log detalhado da sessão de aprendizado"""
        
        log_dir = Path("data/logs")
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / "learning_progress.csv"
        
        # Criar arquivo se não existir
        if not log_file.exists():
            with open(log_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp", "image_path", "company_detected", "confidence", 
                    "data_fields_found", "gps_validation", "route_match", 
                    "learning_outcome", "total_processed"
                ])
        
        # Adicionar nova linha
        with open(log_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                session.timestamp,
                session.image_path,
                session.company_detected,
                session.confidence,
                len(session.extracted_data),
                session.gps_validation,
                session.route_match,
                session.learning_outcome,
                self.total_processed
            ])
    
    def get_learning_stats(self) -> Dict:
        """Retorna estatísticas de aprendizado"""
        
        stats = self.learned_patterns["statistics"]
        
        return {
            "total_images_processed": stats["total_images"],
            "successful_recognitions": stats["successful_recognitions"],
            "recognition_accuracy": (stats["successful_recognitions"] / max(1, stats["total_images"])) * 100,
            "companies_learned": stats["companies_learned"],
            "session_counter": self.session_counter,
            "companies_detail": {
                company: {
                    "samples": data["total_samples"],
                    "confidence": data["confidence_score"],
                    "success_rate": (data["successful_validations"] / max(1, data["total_samples"])) * 100
                }
                for company, data in self.learned_patterns["companies"].items()
                if company != "unknown"
            }
        }
    
    def quick_recognition(self, text: str) -> Optional[str]:
        """Reconhecimento rápido baseado em cache"""
        
        text_lower = text.lower()
        
        # Verificar shortcuts diretos
        for phrase, company in self.pattern_cache["quick_recognition"].items():
            if phrase in text_lower:
                return company
        
        return None
    
    def suggest_investigation_patterns(self) -> List[Dict]:
        """Sugere padrões desconhecidos que merecem investigação"""
        
        unknown_patterns = self.learned_patterns["companies"]["unknown"]["patterns_to_investigate"]
        
        # Retornar últimos 10 padrões com potencial
        return [
            pattern for pattern in unknown_patterns[-10:]
            if len(pattern["potential_patterns"]) > 0
        ]


# Instância global
learning_engine = LearningEngine() 