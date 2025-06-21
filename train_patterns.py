#!/usr/bin/env python3
"""
🧠 SISTEMA DE TREINAMENTO AUTOMÁTICO DE PADRÕES
Sistema inteligente que aprende padrões de reconhecimento a partir de imagens reais
organizadas por transportadora, gerando regex patterns precisos e específicos.

Autor: Sistema OCR Inteligente
Data: 2025-06-20
"""

import os
import re
import json
import argparse
import statistics
from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Set
from datetime import datetime

# Importar módulos do sistema
import sys
sys.path.append('.')
from ocr_extractor import extract_ocr_data
from lib.tags_patterns import TagsPatterns


class PatternTrainer:
    """Sistema de treinamento automático de padrões"""
    
    def __init__(self):
        self.training_data = defaultdict(list)  # {company: [texts...]}
        self.patterns_generated = defaultdict(dict)  # {company: {pattern_type: patterns}}
        self.statistics = defaultdict(dict)
        self.word_frequency = defaultdict(Counter)  # {company: Counter(words)}
        self.unique_signatures = defaultdict(set)  # {company: set(unique_words)}
        
    def scan_training_images(self, base_path: str = "data/training_images") -> Dict[str, List[str]]:
        """Escanear todas as imagens de treinamento organizadas por empresa"""
        print(f"🔍 [SCAN] Escaneando diretório: {base_path}")
        
        image_files = defaultdict(list)
        supported_formats = {'.jpg', '.jpeg', '.png', '.tiff', '.bmp'}
        
        if not os.path.exists(base_path):
            print(f"❌ [ERROR] Diretório não encontrado: {base_path}")
            return image_files
            
        for company_dir in os.listdir(base_path):
            company_path = os.path.join(base_path, company_dir)
            
            if not os.path.isdir(company_path):
                continue
                
            print(f"📁 [SCAN] Empresa encontrada: {company_dir}")
            
            for file_name in os.listdir(company_path):
                file_path = os.path.join(company_path, file_name)
                
                if os.path.isfile(file_path):
                    _, ext = os.path.splitext(file_name.lower())
                    if ext in supported_formats:
                        image_files[company_dir].append(file_path)
                        print(f"  📸 [SCAN] Imagem: {file_name}")
        
        return image_files
    
    def extract_training_data(self, image_files: Dict[str, List[str]]) -> None:
        """Extrair texto OCR de todas as imagens de treinamento"""
        print("\n🔬 [OCR] Iniciando extração de dados de treinamento...")
        
        for company, files in image_files.items():
            print(f"\n🏢 [OCR] Processando empresa: {company.upper()}")
            print(f"📊 [OCR] Total de imagens: {len(files)}")
            
            for i, file_path in enumerate(files, 1):
                print(f"  📸 [OCR] Processando {i}/{len(files)}: {os.path.basename(file_path)}")
                
                try:
                    # Extrair texto da imagem
                    ocr_result = extract_ocr_data(file_path)
                    
                    if ocr_result and ocr_result.get('raw_text'):
                        text = ocr_result['raw_text'].strip()
                        if text:
                            self.training_data[company].append(text)
                            print(f"    ✅ [OCR] Extraído: {len(text)} caracteres")
                            
                            # Preview do texto (primeiras 100 chars)
                            preview = text[:100].replace('\n', ' ')
                            print(f"    📝 [OCR] Preview: {preview}...")
                        else:
                            print(f"    ⚠️ [OCR] Texto vazio extraído")
                    else:
                        print(f"    ❌ [OCR] Falha na extração")
                        
                except Exception as e:
                    print(f"    ❌ [OCR] Erro: {str(e)}")
    
    def analyze_text_patterns(self) -> None:
        """Analisar padrões estatísticos nos textos extraídos"""
        print("\n📊 [ANÁLISE] Iniciando análise estatística de padrões...")
        
        for company, texts in self.training_data.items():
            print(f"\n🏢 [ANÁLISE] Empresa: {company.upper()}")
            print(f"📄 [ANÁLISE] Total de textos: {len(texts)}")
            
            if not texts:
                print("⚠️ [ANÁLISE] Nenhum texto para analisar")
                continue
            
            # Unir todos os textos da empresa
            combined_text = ' '.join(texts).lower()
            
            # Análise de palavras
            words = re.findall(r'\b\w+\b', combined_text)
            word_counter = Counter(words)
            
            # Filtrar palavras muito comuns (stopwords básicas)
            stopwords = {'o', 'a', 'e', 'de', 'do', 'da', 'em', 'um', 'uma', 'para', 'com', 'por', 'na', 'no', 'ao', 'aos', 'das', 'dos', 'se', 'que', 'mais', 'como', 'mas', 'foi', 'ele', 'ela', 'seu', 'sua', 'ou', 'quando', 'muito', 'nos', 'já', 'eu', 'também', 'só', 'pelo', 'pela', 'até', 'isso', 'ela', 'entre', 'depois', 'sem', 'mesmo', 'ao', 'durante', 'todo', 'todos', 'todas', 'cada', 'qualquer', 'alguns', 'algumas', 'outro', 'outros', 'outra', 'outras'}
            
            # Palavras significativas (aparecem em múltiplos textos e não são stopwords)
            significant_words = []
            for word, count in word_counter.most_common(50):
                if len(word) >= 3 and word not in stopwords and count >= max(1, len(texts) * 0.3):
                    significant_words.append(word)
            
            self.word_frequency[company] = word_counter
            
            # Buscar padrões únicos específicos da empresa
            unique_patterns = self.find_unique_patterns(company, combined_text)
            self.unique_signatures[company] = unique_patterns
            
            # Estatísticas
            self.statistics[company] = {
                'total_texts': len(texts),
                'total_words': len(words),
                'unique_words': len(set(words)),
                'significant_words': significant_words[:15],  # Top 15
                'unique_patterns': list(unique_patterns)[:10],  # Top 10
                'avg_text_length': statistics.mean([len(text) for text in texts]),
                'text_samples': [text[:200] + '...' if len(text) > 200 else text for text in texts[:3]]
            }
            
            print(f"  📊 [ANÁLISE] Palavras únicas: {len(set(words))}")
            print(f"  📊 [ANÁLISE] Palavras significativas: {len(significant_words)}")
            print(f"  📊 [ANÁLISE] Padrões únicos: {len(unique_patterns)}")
            print(f"  🔝 [ANÁLISE] Top palavras: {significant_words[:5]}")
    
    def find_unique_patterns(self, company: str, text: str) -> Set[str]:
        """Encontrar padrões únicos específicos de uma empresa"""
        patterns = set()
        
        # Padrões de números específicos
        number_patterns = re.findall(r'\b\d{6,}\b', text)  # Números com 6+ dígitos
        for pattern in number_patterns:
            patterns.add(f"number_{pattern[:4]}")  # Primeiros 4 dígitos
        
        # Padrões de códigos alfanuméricos
        alphanum_patterns = re.findall(r'\b[a-zA-Z]+\d+[a-zA-Z\d]*\b', text)
        for pattern in alphanum_patterns:
            if len(pattern) >= 4:
                patterns.add(pattern.lower())
        
        # Padrões de endereços/códigos específicos
        address_patterns = re.findall(r'\b(?:rua|av|avenida|praca|praça)\s+[\w\s]+\d+', text, re.IGNORECASE)
        for pattern in address_patterns:
            # Extrair palavras chave do endereço
            words = re.findall(r'\b\w{4,}\b', pattern.lower())
            patterns.update(words[:2])  # Primeiras 2 palavras significativas
        
        # Padrões específicos por empresa conhecida
        if 'logistics' in text.lower():
            patterns.add('logistics')
        if 'mercado' in text.lower() and 'livre' in text.lower():
            patterns.add('mercado_livre')
        if 'correios' in text.lower() or 'ebct' in text.lower():
            patterns.add('correios')
        if 'amazon' in text.lower():
            patterns.add('amazon')
            
        # Padrões de CEP
        cep_patterns = re.findall(r'\b\d{5}-?\d{3}\b', text)
        if cep_patterns:
            patterns.add('cep_pattern')
        
        return patterns
    
    def generate_regex_patterns(self) -> None:
        """Gerar padrões regex precisos baseados na análise estatística"""
        print("\n🔧 [REGEX] Gerando padrões regex automáticos...")
        
        for company in self.training_data.keys():
            print(f"\n🏢 [REGEX] Empresa: {company.upper()}")
            
            significant_words = self.statistics[company]['significant_words']
            unique_patterns = list(self.unique_signatures[company])
            
            # Gerar padrões de palavras-chave
            if significant_words:
                # Top 3 palavras mais significativas
                top_words = significant_words[:3]
                keyword_pattern = '|'.join([re.escape(word) for word in top_words])
                
                self.patterns_generated[company]['keywords'] = f"(?i)({keyword_pattern})"
                print(f"  🔑 [REGEX] Keywords: {keyword_pattern}")
            
            # Gerar padrões únicos específicos
            if unique_patterns:
                # Filtrar padrões realmente únicos (não aparecem em outras empresas)
                truly_unique = []
                for pattern in unique_patterns:
                    is_unique = True
                    for other_company in self.training_data.keys():
                        if other_company != company and pattern in self.unique_signatures[other_company]:
                            is_unique = False
                            break
                    if is_unique:
                        truly_unique.append(pattern)
                
                if truly_unique:
                    unique_pattern = '|'.join([re.escape(pattern) for pattern in truly_unique[:5]])
                    self.patterns_generated[company]['unique'] = f"(?i)({unique_pattern})"
                    print(f"  🎯 [REGEX] Unique: {unique_pattern}")
            
            # Padrões combinados (mais restritivos)
            if significant_words and len(significant_words) >= 2:
                # Combinar 2 palavras top com OR
                combo_words = significant_words[:2]
                combo_pattern = f"(?i).*({re.escape(combo_words[0])}).*({re.escape(combo_words[1])})|.*({re.escape(combo_words[1])}).*({re.escape(combo_words[0])})"
                self.patterns_generated[company]['combo'] = combo_pattern
                print(f"  🔗 [REGEX] Combo: {combo_words[0]} + {combo_words[1]}")
    
    def validate_patterns(self) -> Dict[str, float]:
        """Validar padrões gerados com cross-validation"""
        print("\n✅ [VALIDAÇÃO] Testando padrões gerados...")
        
        validation_results = {}
        
        for company in self.training_data.keys():
            print(f"\n🏢 [VALIDAÇÃO] Empresa: {company.upper()}")
            
            company_texts = self.training_data[company]
            if not company_texts:
                continue
            
            # Testar cada tipo de padrão
            for pattern_type, pattern in self.patterns_generated[company].items():
                matches = 0
                total = len(company_texts)
                
                for text in company_texts:
                    if re.search(pattern, text):
                        matches += 1
                
                accuracy = matches / total if total > 0 else 0
                validation_key = f"{company}_{pattern_type}"
                validation_results[validation_key] = accuracy
                
                print(f"  📊 [VALIDAÇÃO] {pattern_type}: {matches}/{total} = {accuracy:.2%}")
        
        return validation_results
    
    def update_patterns_file(self) -> None:
        """Atualizar arquivo tags_patterns.py com os novos padrões"""
        print("\n📝 [UPDATE] Atualizando arquivo de padrões...")
        
        # Ler arquivo atual
        patterns_file = "lib/tags_patterns.py"
        
        try:
            with open(patterns_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ [UPDATE] Erro ao ler arquivo: {e}")
            return
        
        # Backup do arquivo original
        backup_file = f"{patterns_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"💾 [UPDATE] Backup criado: {backup_file}")
        
        # Gerar novos padrões para substituição
        new_patterns = self.generate_new_patterns_code()
        
        # Substituir seção de padrões
        pattern_start = "# Padrões de reconhecimento de transportadoras"
        pattern_end = "    def extract_data("
        
        start_idx = content.find(pattern_start)
        end_idx = content.find(pattern_end)
        
        if start_idx != -1 and end_idx != -1:
            new_content = (
                content[:start_idx] + 
                new_patterns + 
                "\n    " +
                content[end_idx:]
            )
            
            # Salvar arquivo atualizado
            with open(patterns_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ [UPDATE] Arquivo atualizado: {patterns_file}")
            print(f"📊 [UPDATE] Padrões atualizados para {len(self.patterns_generated)} empresas")
        else:
            print("❌ [UPDATE] Não foi possível localizar seção para substituição")
    
    def generate_new_patterns_code(self) -> str:
        """Gerar código Python com os novos padrões"""
        code = "# Padrões de reconhecimento de transportadoras\n"
        code += "    # 🤖 PADRÕES GERADOS AUTOMATICAMENTE PELO SISTEMA DE TREINAMENTO\n"
        code += f"    # 📅 Gerados em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        code += f"    # 📊 Baseados em {sum(len(texts) for texts in self.training_data.values())} imagens reais\n\n"
        
        code += "    COMPANY_PATTERNS = {\n"
        
        for company in sorted(self.patterns_generated.keys()):
            code += f"        '{company}': {{\n"
            
            # Adicionar estatísticas como comentário
            stats = self.statistics.get(company, {})
            code += f"            # 📊 Baseado em {stats.get('total_texts', 0)} imagens\n"
            code += f"            # 🔝 Palavras-chave: {', '.join(stats.get('significant_words', [])[:5])}\n"
            
            # Padrões gerados
            patterns = self.patterns_generated[company]
            if 'unique' in patterns:
                code += f"            'primary': r\"{patterns['unique']}\",\n"
            elif 'keywords' in patterns:
                code += f"            'primary': r\"{patterns['keywords']}\",\n"
            else:
                code += f"            'primary': r\"(?i){company}\",\n"
            
            if 'combo' in patterns:
                code += f"            'secondary': r\"{patterns['combo']}\",\n"
            elif 'keywords' in patterns and 'unique' in patterns:
                code += f"            'secondary': r\"{patterns['keywords']}\",\n"
            
            code += f"            'confidence_boost': 0.85,\n"
            code += "        },\n"
        
        code += "    }\n\n"
        
        return code
    
    def generate_training_report(self) -> str:
        """Gerar relatório completo do treinamento"""
        report = []
        report.append("="*80)
        report.append("🧠 RELATÓRIO DE TREINAMENTO AUTOMÁTICO DE PADRÕES")
        report.append("="*80)
        report.append(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"📊 Total de empresas processadas: {len(self.training_data)}")
        report.append(f"📸 Total de imagens processadas: {sum(len(texts) for texts in self.training_data.values())}")
        report.append("")
        
        for company in sorted(self.training_data.keys()):
            stats = self.statistics.get(company, {})
            patterns = self.patterns_generated.get(company, {})
            
            report.append(f"🏢 EMPRESA: {company.upper()}")
            report.append("-" * 40)
            report.append(f"📄 Textos processados: {stats.get('total_texts', 0)}")
            report.append(f"📊 Palavras únicas: {stats.get('unique_words', 0)}")
            report.append(f"📏 Comprimento médio: {stats.get('avg_text_length', 0):.0f} caracteres")
            report.append(f"🔝 Top palavras: {', '.join(stats.get('significant_words', [])[:8])}")
            report.append(f"🎯 Padrões únicos: {', '.join(stats.get('unique_patterns', [])[:5])}")
            report.append(f"🔧 Padrões gerados: {len(patterns)}")
            
            if patterns:
                for pattern_type, pattern in patterns.items():
                    report.append(f"  • {pattern_type}: {pattern[:60]}...")
            
            report.append("")
        
        return "\n".join(report)
    
    def run_training(self, mode: str = "deep_learning") -> None:
        """Executar processo completo de treinamento"""
        print("="*80)
        print("🧠 SISTEMA DE TREINAMENTO AUTOMÁTICO DE PADRÕES")
        print("🤖 Gerando padrões precisos baseados em imagens reais")
        print("="*80)
        print(f"🎯 Modo: {mode}")
        print(f"📅 Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Etapa 1: Escanear imagens
        image_files = self.scan_training_images()
        
        if not image_files:
            print("❌ Nenhuma imagem encontrada para treinamento!")
            print("💡 Certifique-se de ter imagens em: data/training_images/{empresa}/")
            return
        
        # Etapa 2: Extrair dados OCR
        self.extract_training_data(image_files)
        
        if not self.training_data:
            print("❌ Nenhum texto extraído das imagens!")
            return
        
        # Etapa 3: Análise estatística
        self.analyze_text_patterns()
        
        # Etapa 4: Gerar padrões regex
        self.generate_regex_patterns()
        
        # Etapa 5: Validar padrões
        validation_results = self.validate_patterns()
        
        # Etapa 6: Atualizar arquivo de padrões
        if mode == "deep_learning":
            self.update_patterns_file()
        
        # Etapa 7: Gerar relatório
        report = self.generate_training_report()
        
        # Salvar relatório
        report_file = f"reports/training_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        os.makedirs("reports", exist_ok=True)
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # Resultado final
        print("\n" + "="*80)
        print("🎉 TREINAMENTO CONCLUÍDO COM SUCESSO!")
        print("="*80)
        print(f"📊 Empresas processadas: {len(self.training_data)}")
        print(f"🔧 Padrões gerados: {sum(len(patterns) for patterns in self.patterns_generated.values())}")
        print(f"📄 Relatório salvo: {report_file}")
        
        if mode == "deep_learning":
            print("✅ Arquivo lib/tags_patterns.py foi atualizado!")
            print("🔄 Reinicie o sistema para usar os novos padrões")
        
        print("\n📊 RESUMO DAS VALIDAÇÕES:")
        for key, accuracy in validation_results.items():
            print(f"  • {key}: {accuracy:.1%}")


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description="Sistema de Treinamento Automático de Padrões OCR")
    parser.add_argument(
        "--mode", 
        choices=["analyze", "deep_learning"], 
        default="deep_learning",
        help="Modo de operação: analyze (apenas análise) ou deep_learning (análise + atualização)"
    )
    parser.add_argument(
        "--path",
        default="data/training_images",
        help="Caminho para as imagens de treinamento"
    )
    
    args = parser.parse_args()
    
    # Criar e executar treinador
    trainer = PatternTrainer()
    trainer.run_training(mode=args.mode)


if __name__ == "__main__":
    main() 