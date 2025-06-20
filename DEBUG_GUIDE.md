# 🐛 Guia de Debug - Sistema OCR

## 📋 Configurações de Launch Disponíveis

### 🚀 Configurações Principais:
1. **🚀 Debug Main - Imagem Padrão** - Debug básico com imagem padrão
2. **🔍 Debug OCR - Teste Photo** - Debug com imagem que funciona bem
3. **📱 Debug iPhone EXIF - test_001.jpg** - Debug com imagem real do iPhone (EXIF completo)
4. **🍎 Debug HEIC - test_iphone.HEIC** - Debug com formato HEIC (problemas conhecidos)

### 🧪 Configurações Específicas:
5. **🧪 Debug OCR Extractor** - Debug apenas do módulo OCR
6. **📋 Debug Metadata Reader** - Debug apenas do leitor de metadados
7. **🔧 Debug Current File** - Debug do arquivo atualmente aberto
8. **🐍 Python: Debug with Arguments** - Debug com argumentos de linha de comando

## 🎯 Breakpoints Sugeridos

### 📍 Breakpoints Principais:

#### 1. **main.py linha ~20** (início de process_delivery)
```python
def process_delivery(photo_path):
    print("\n[INFO] Iniciando validação da entrega...")
    # 🔴 BREAKPOINT AQUI - Verificar photo_path
```

#### 2. **main.py linha ~30** (após OCR)
```python
ocr_data = extract_ocr_data(photo_path)
# 🔴 BREAKPOINT AQUI - Verificar resultado do OCR
```

#### 3. **metadata_reader.py linha ~15** (leitura de tags EXIF)
```python
tags = exifread.process_file(f)
# 🔴 BREAKPOINT AQUI - Verificar tags extraídas
```

#### 4. **validator.py linha ~15** (cálculo de distância)
```python
gps_distance = geodesic(device_gps, vehicle_gps).km
# 🔴 BREAKPOINT AQUI - Verificar cálculo GPS
```

### 🔍 Breakpoints para Problemas Específicos:

#### Problema OCR (formato de imagem):
- **ocr_extractor.py linha ~15** - Verificar image.format
- **ocr_extractor.py linha ~22** - Verificar conversão RGB

#### Problema EXIF:
- **metadata_reader.py linha ~25** - Verificar tags importantes
- **metadata_reader.py linha ~45** - Verificar conversão GPS

## 🛠️ Como Usar

### 1. **Configurar Breakpoints:**
- Clique na margem esquerda do código (bolinha vermelha)
- Ou pressione `F9` na linha desejada

### 2. **Iniciar Debug:**
- Pressione `F5` ou `Ctrl+Shift+D`
- Escolha uma das configurações do dropdown

### 3. **Controles de Debug:**
- `F10` - Step Over (próxima linha)
- `F11` - Step Into (entrar na função)
- `Shift+F11` - Step Out (sair da função)
- `F5` - Continue

### 4. **Variáveis de Ambiente:**
- `DEBUG_MODE=1` - Ativa breakpoints automáticos com pdb
- `DEBUG_IMAGE=caminho` - Especifica imagem para debug

## 📊 Inspeção de Variáveis

### Variáveis Importantes para Inspecionar:

#### Durante OCR:
```python
image.format    # Formato da imagem (JPEG, MPO, etc.)
image.size      # Dimensões (width, height)
image.mode      # Modo de cor (RGB, RGBA, etc.)
raw_text        # Texto extraído pelo OCR
```

#### Durante EXIF:
```python
tags            # Todas as tags EXIF
len(tags)       # Quantidade de tags encontradas
lat, lon        # Coordenadas GPS brutas
gps             # GPS convertido (latitude, longitude)
```

#### Durante Validação:
```python
device_gps      # GPS do dispositivo
vehicle_gps     # GPS do veículo
gps_distance    # Distância calculada em km
is_close        # Boolean da validação
```

## 🚨 Cenários de Teste

### ✅ Teste com Sucesso:
- Imagem: `samples/_test_photo.jpeg`
- Expectativa: OCR funciona, EXIF simulado, validação OK

### ❌ Teste com Erro OCR:
- Imagem: `samples/test_001.jpg`
- Expectativa: OCR falha (formato MPO), EXIF real do iPhone

### ⚠️ Teste com Distância Inválida:
- Imagem: `samples/test_001.jpg`
- Expectativa: GPS real (RJ) vs simulado (SP) = ~330km

## 💡 Dicas de Debug

1. **Watch Expressions:** Adicione expressões como `len(tags)`, `gps_distance`, `result['is_valid']`

2. **Call Stack:** Observe a pilha de chamadas para entender o fluxo

3. **Console:** Use o console integrado para executar código Python durante o debug

4. **Conditional Breakpoints:** Clique direito no breakpoint para adicionar condições

5. **Log Points:** Adicione log points em vez de breakpoints para não parar a execução

## 🎯 Objetivos de Debug

- [ ] Verificar extração correta de EXIF
- [ ] Validar conversão de GPS
- [ ] Testar diferentes formatos de imagem
- [ ] Analisar fluxo de validação
- [ ] Debugar problemas de OCR 