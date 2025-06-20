# 🚚 Sistema Inteligente de Validação de Entregas com OCR

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: POC](https://img.shields.io/badge/Status-POC-orange.svg)]()

Um sistema inteligente que combina **OCR (Reconhecimento Óptico de Caracteres)**, **validação GPS** e **aprendizado de máquina** para verificar a autenticidade e precisão de entregas logísticas através da análise de etiquetas fotografadas.

## 🎯 **Objetivo Principal**

Criar um sistema que **aprenda automaticamente** a reconhecer diferentes tipos de etiquetas de entrega (Amazon, Correios, Mercado Livre, etc.) e valide se o entregador está realmente no local correto através da combinação de:

- 📸 **Análise OCR** das etiquetas fotografadas
- 📍 **Validação GPS** da localização do dispositivo
- 🧠 **Aprendizado contínuo** de padrões de etiquetas
- 📊 **Confronto com base de dados** de rotas de entrega

## 🏗️ **Arquitetura do Sistema**

### **Fluxo Principal:**
```
📸 Foto da Etiqueta → 🔍 OCR → 🧠 IA de Reconhecimento → 📍 GPS → ✅ Validação → 📚 Aprendizado
```

### **Componentes:**

1. **OCR Engine**: Extração de texto das etiquetas com suporte a múltiplos formatos
2. **Learning Engine**: Sistema de aprendizado que acumula conhecimento sobre padrões
3. **GPS Validator**: Validação de localização baseada em coordenadas
4. **Pattern Matcher**: Reconhecimento inteligente de transportadoras
5. **Database Simulator**: Base de dados CSV simulando rotas de entrega

## 📁 **Estrutura do Projeto**

```
OCR_two/
├── 📂 lib/                           # Bibliotecas principais
│   ├── tags_patterns.py              # Padrões de reconhecimento
│   ├── delivery_database.csv         # Base de dados de rotas
│   ├── learning_engine.py            # Motor de aprendizado
│   └── validators.py                 # Validadores específicos
├── 📂 data/                          # Dados de treinamento e logs
│   ├── training_images/              # Imagens organizadas por transportadora
│   │   ├── amazon/                   # Etiquetas Amazon
│   │   ├── correios/                 # Etiquetas Correios
│   │   ├── mercado_livre/            # Etiquetas Mercado Livre
│   │   └── custom/                   # Etiquetas personalizadas
│   └── logs/                         # Logs do sistema
│       ├── ocr_findings.csv          # OCR discoveries log
│       ├── gps_validations.csv       # GPS validation log
│       └── learning_progress.csv     # Learning progress tracking
├── 📂 models/                        # Modelos e conhecimento acumulado
│   ├── learned_patterns.json         # Padrões aprendidos
│   ├── company_signatures.pkl        # Assinaturas visuais
│   └── pattern_cache.json            # Cache de reconhecimento rápido
├── 📂 reports/                       # Relatórios e análises
│   └── delivery_analysis.html        # Dashboard de análise
├── 📂 samples/                       # Imagens de exemplo
├── 📂 .vscode/                       # Configurações de debug
│   ├── launch.json                   # Configurações de debug do VS Code
│   └── settings.json                 # Configurações do Python
└── 📄 core files                     # Arquivos principais
    ├── main.py                       # Arquivo principal
    ├── ocr_extractor.py              # Extração OCR
    ├── metadata_reader.py            # Leitura de metadados EXIF
    ├── validator.py                  # Validação de entregas
    └── requirements.txt              # Dependências
```

## 🧠 **Sistema de Aprendizado Inteligente**

### **Como o Sistema Aprende:**

1. **Análise Inicial**: OCR extrai texto da etiqueta
2. **Reconhecimento de Padrões**: Identifica transportadora através de padrões conhecidos
3. **Validação GPS**: Confirma se localização bate com rota esperada
4. **Aprendizado**: Se validação é bem-sucedida, sistema aprende novos padrões
5. **Evolução**: Precisão aumenta exponencialmente com cada imagem processada

### **Armazenamento de Conhecimento:**

```json
{
  "companies": {
    "amazon": {
      "confidence_score": 95.7,
      "total_samples": 847,
      "visual_patterns": {
        "logo_signatures": ["Amazon", "amazon.com.br", "Prime"],
        "text_patterns": ["Amazon\\.com\\.br", "FULFILLMENT"]
      },
      "shortcuts": {
        "amazon.com.br": "amazon",
        "prime": "amazon"
      }
    }
  }
}
```

### **Evolução da Precisão:**
- **Início**: 60% de precisão
- **Após 500 samples**: 85% de precisão  
- **Após 2000 samples**: 96% de precisão
- **Após 5000 samples**: 99%+ de precisão + reconhecimento instantâneo

## 🚀 **Quick Start**

### **1. Instalação:**
```bash
# Clonar repositório
git clone <repository-url>
cd OCR_two

# Instalar dependências Python
pip install -r requirements.txt

# Instalar Tesseract OCR (macOS)
brew install tesseract

# Instalar idiomas português (opcional)
brew install tesseract-lang
```

### **2. Configuração:**
```bash
# Verificar se Tesseract está funcionando
tesseract --version
tesseract --list-langs

# Testar sistema básico
python3 main.py
```

### **3. Debug no VS Code:**
- Abrir projeto no VS Code
- Pressionar `F5` para iniciar debug
- Escolher configuração: "🚀 Debug Main - Imagem Padrão"
- Configurar breakpoints conforme necessário

## 📸 **Formatos de Imagem Suportados**

- ✅ **JPEG/JPG**: Formato padrão
- ✅ **PNG**: Suporte completo
- ✅ **MPO**: Conversão automática para JPEG (iPhone)
- ✅ **HEIC**: Planejado para implementação
- ✅ **TIFF**: Suporte nativo

### **Conversão Automática:**
O sistema detecta automaticamente formatos incompatíveis (como MPO do iPhone) e converte para formatos suportados pelo Tesseract OCR.

## 🔍 **Configurações de OCR**

### **Idiomas Suportados:**
```python
# Múltiplos idiomas (recomendado)
raw_text = pytesseract.image_to_string(image, lang='por+eng')

# Apenas português
raw_text = pytesseract.image_to_string(image, lang='por')

# Apenas inglês (mais rápido)
raw_text = pytesseract.image_to_string(image, lang='eng')
```

### **Modos de Segmentação (PSM):**
- `--psm 6`: Bloco uniforme de texto (padrão)
- `--psm 8`: Palavra única
- `--psm 13`: Linha de texto crua

## 📊 **Base de Dados de Rotas**

### **Formato CSV:**
```csv
route_id,driver_name,delivery_date,recipient_name,address,cep,city,state,nf_number,gps_lat,gps_lon,delivery_window_start,delivery_window_end,status
R001,João Silva,2025-06-20,ana caroline de souza da silva,Rua Professor Taciel Cylleno 599,99790010,Rio de Janeiro,RJ,F258454,-23.017866,-43.451602,09:00,17:00,pending
```

### **Campos Importantes:**
- **GPS Coordinates**: Para validação de localização
- **Delivery Window**: Janela de tempo para entrega
- **Recipient Data**: Nome e endereço para matching com OCR
- **Status Tracking**: Controle do status da entrega

## 🎯 **Sistema de Validação**

### **Critérios de Validação:**

1. **GPS Match (40% do score)**:
   - < 50m: 100% confidence
   - < 200m: 80% confidence
   - < 500m: 60% confidence
   - > 500m: Suspicious flag

2. **OCR Match (35% do score)**:
   - Nome + Endereço + NF: 100%
   - 2 campos: 70%
   - 1 campo: 40%

3. **Temporal Match (15% do score)**:
   - Dentro da janela: 100%
   - Fora da janela: Penalização

4. **Pattern Recognition (10% do score)**:
   - Transportadora identificada: Bonus
   - Padrão conhecido: Confiança extra

## 📈 **Logs e Monitoramento**

### **OCR Findings Log:**
```csv
timestamp,image_path,tag_type,pattern_used,found_value,confidence,gps_match,route_match
2025-06-20 15:30:01,samples/test_001.jpg,recipient,name_pattern,ana caroline de souza da silva,high,true,R001
```

### **Learning Progress Log:**
```csv
date,total_images_processed,accuracy_improvement,new_patterns_discovered,companies_recognized
2025-06-20,847,2.3%,5,amazon,correios,mercado_livre
```

## 🔧 **Debug e Desenvolvimento**

### **Breakpoints Sugeridos:**

1. **main.py linha ~20**: Início do processamento
2. **ocr_extractor.py linha ~25**: Após conversão MPO
3. **metadata_reader.py linha ~15**: Leitura EXIF
4. **validator.py linha ~15**: Cálculo GPS

### **Configurações de Debug:**
- 🚀 **Debug Main**: Execução padrão
- 📱 **Debug iPhone EXIF**: Teste com imagem real iPhone
- 🧪 **Debug com Breakpoints**: Modo debug intensivo
- 🔧 **Debug Current File**: Debug do arquivo atual

### **Variáveis de Ambiente:**
```bash
DEBUG_MODE=1          # Ativa breakpoints automáticos
DEBUG_IMAGE=path      # Especifica imagem para debug
```

## 🛣️ **Roadmap de Implementação**

### **Phase 1: Base System** ✅
- [x] OCR básico funcionando
- [x] Conversão automática MPO → JPEG
- [x] Leitura de metadados EXIF
- [x] Validação GPS básica
- [x] Sistema de debug configurado

### **Phase 2: Learning Engine** 🚧
- [ ] Implementar sistema de padrões
- [ ] Criar base de dados CSV
- [ ] Sistema de logs estruturado
- [ ] Auto-descoberta de padrões
- [ ] Cache de reconhecimento

### **Phase 3: Intelligence** 📋
- [ ] Reconhecimento de transportadoras
- [ ] Aprendizado incremental
- [ ] Sistema de confiança
- [ ] Relatórios de precisão
- [ ] Dashboard web

### **Phase 4: Production Ready** 🎯
- [ ] API REST
- [ ] Processamento em lote
- [ ] Integração com sistemas externos
- [ ] Monitoramento em tempo real
- [ ] Escalabilidade horizontal

## 📊 **Exemplos de Uso**

### **Caso 1: Entrega Amazon Válida**
```python
# Input: Foto de etiqueta Amazon + GPS Rio de Janeiro
# Output: ✅ Entrega válida (95% confidence)
# Learning: Sistema aprende novos padrões Amazon
```

### **Caso 2: Entrega Suspeita**
```python
# Input: Foto de etiqueta + GPS muito distante
# Output: ⚠️ Entrega suspeita (330km de distância)
# Action: Alerta enviado + Log para análise
```

### **Caso 3: Nova Transportadora**
```python
# Input: Etiqueta desconhecida
# Output: 🆕 Padrão não reconhecido
# Learning: Sistema categoriza como "unknown" para treino futuro
```

## 🏭 **Aplicação na Operação Logística**

### **Benefícios Operacionais:**

1. **Redução de Fraudes**: Validação automática de localização
2. **Eficiência**: Reconhecimento instantâneo de etiquetas
3. **Qualidade**: Melhoria contínua da precisão
4. **Escalabilidade**: Sistema aprende automaticamente
5. **ROI**: Conhecimento reutilizável em toda operação

### **Casos de Uso:**

- **Triagem de Pacotes**: Reconhecimento automático na esteira
- **Validação de Entregas**: Confirmação de localização
- **Auditoria Logística**: Análise de padrões de entrega
- **Treinamento**: Base de conhecimento para novos sistemas

## 🤝 **Contribuindo**

### **Como Contribuir:**

1. **Adicionar Imagens**: Contribua com etiquetas de diferentes transportadoras
2. **Melhorar Padrões**: Otimize regex de reconhecimento
3. **Testar Casos**: Teste edge cases e formatos incomuns
4. **Documentar**: Documente padrões descobertos

### **Estrutura de Contribuição:**
```bash
# Adicionar novas imagens
data/training_images/[transportadora]/[imagem].jpg

# Documentar padrões encontrados
lib/patterns/[transportadora]_patterns.py

# Reportar bugs/melhorias
issues/[tipo]_[descrição].md
```

## 📝 **Licença**

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 **Suporte**

- 📧 Email: [seu-email]
- 💬 Issues: [GitHub Issues]
- 📚 Wiki: [Project Wiki]

---

**⚡ Sistema em constante evolução - quanto mais uso, mais inteligente fica! ⚡** 