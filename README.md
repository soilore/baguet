# Baguet (`v1.0.0`)

**Algebraic Lossless Memory Engine & Zero-Decompression Compute Codec for AI, Multimedia, and Critical Infrastructure.**

[![Release](https://img.shields.io/badge/release-v1.0.0-0A84FF.svg?style=flat-square)](#)
[![Core](https://img.shields.io/badge/core-Python%20%2B%20Rust%20SIMD-FF9F0A.svg?style=flat-square)](#)
[![Platforms](https://img.shields.io/badge/os-macOS%20%7C%20Linux%20%7C%20Windows-30D158.svg?style=flat-square)](#)
[![Integrity](https://img.shields.io/badge/integrity-100%25%20SHA--256%20Bit--Exact-00F5FF.svg?style=flat-square)](#)
[![Offline](https://img.shields.io/badge/runtime-100%25%20Air--Gapped%20%2F%20Offline-64D2FF.svg?style=flat-square)](#)
[![License](https://img.shields.io/badge/license-BUSL--1.1%20AND%20MIT-BF5AF2.svg?style=flat-square)](#licenciamento-freemium--governanca-offline-bgtl1)
[![GitHub](https://img.shields.io/badge/github-soilore%2Fbaguet-181717.svg?style=flat-square&logo=github)](https://github.com/soilore/baguet)

---

## Visão Geral

O **Baguet (`v1.0.0`)** é um motor de memória algébrica e compressor **100% sem perdas (_bit-exact lossless_)** de grau industrial, desenvolvido pela **Soilore**. Foi projetado para eliminar gargalos de memória (RAM/VRAM), latência de I/O de disco e custos de banda em infraestruturas críticas de **Inteligência Artificial (LLMs, RAG, SafeTensors)**, **Engenharia de Dados (`Parquet`, `JSONL`, `CSV`)** e **Multimídia (`PNG`, `JPEG`, `MP4`, `WAV`, `PDF`)**.

Enquanto compressores clássicos de uso geral (`zstd`, `gzip`, `lz4`, `xz`) tratam arquivos como sequências opacas e lineares de bytes — exigindo descompressão integral e custosa para a RAM antes de qualquer operação —, o Baguet introduz uma abordagem orientada à geometria da informação:

1. **Decomposição Algébrica Ortogonal:** Os dados são projetados em espaços dimensionais reversíveis (invariantes de linha/coluna, subespaços e mantissas numéricas), permitindo densidades de compressão sem precedentes em tensores de ponto flutuante (`FP32`, `FP16`, `BF16`) e tabelas estruturadas;
2. **Computação Direta sem Descompressão (_Compute-on-Compressed-Data_):** Algoritmos de IA executam operações de busca vetorial Top-K em RAG com poda sub-linear, atenção multi-bloco de LLM (`Online Flash-SDPA`), projeções lineares e extração seletiva `Zero-Copy mmap` diretamente sobre os bytes compactados;
3. **Garantia Criptográfica `SHA-256` Bit-Exact e Operação 100% Offline:** Cada contêiner incorpora digest SHA-256 autenticado com verificação mandante _fail-closed_. Zero telemetria, zero dependências de nuvem e validação de licenças corporativas 100% air-gapped via tokens criptografados `Ed25519`.

---

## Resumo de Benchmarks Homologados (`Baguet v1.0.0`)

Resultados medidos em ambiente de homologação auditado com suíte de 53 cenários de estresse e tolerância zero a regressão:

| Carga de Trabalho / Domínio                     | Formato Nativo      |      Ratio `Baguet v1.0.0`      |    Ratio `zstd -19`    | Ganho Relativo & Capacidade Computacional Nativa                                                      |
| :---------------------------------------------- | :------------------ | :-----------------------------: | :--------------------: | :---------------------------------------------------------------------------------------------------- |
| **RAG Embeddings Vetoriais (`FP16`/`FP32`)**    | `.bgt` (`BGT-EMB1`) |   **4,00x** (25,0% do orig.)    |     1,09x (91,5%)      | **+267% mais compacto** + Busca Top-K Sub-Linear (**100% Recall**, >70% blocos poupados, 1,78 ms p50) |
| **LLM KV-Cache (`FP16`)**                       | `.bgt` (`BGT-TNS1`) |   **2,71x** (36,9% do orig.)    |     1,12x (89,1%)      | **+141% mais compacto** + `Online Flash-SDPA` nativo (0,29–1,84 ms) e Offloader Multi-Bloco           |
| **Checkpoints Diferenciais / LoRA**             | `.bgtd` (`BGTD6`)   |   **10,85x** (9,2% do orig.)    |     1,11x (90,0%)      | **+877% mais compacto** para versionamento de pesos (2.739 B, 286 ms)                                 |
| **Pesos de IA de Fronteira (`BF16` 1024×1024)** | `.bgt` (`BGT-TNS1`) | **1,49x** (1.410.383 B / 32,8%) | 1,37x (Blosc2 1,49 MB) | **Líder absoluto de densidade BF16** frente a Blosc2/ZipNN + Inferência Direta 14,3 ms                |
| **Modelos `SafeTensors` (`FP32`/`BF16`)**       | `.bgtt` (`BGTT6`)   |        **1,45x a 4,26x**        |     1,08x a 1,19x      | Extração seletiva por camada via `Zero-Copy mmap` (~1,2 ms)                                           |
| **Tensores Progressivos Dual-Tier**             | `.bgtp` (`BGTP6`)   |   **2,00x (Base) + Lossless**   |         1,08x          | _Hot-start_ imediato com 50% de RAM (-64,8% tráfego GPU, 0,36 ms) + restauração exata                 |
| **Tabelas Analíticas (`Parquet` / `CSV`)**      | `.bgt`              |       **5,78x a 55,89x**        |     3,00x a 29,01x     | Transposição algébrica colunar e invariantes relacionais exatas                                       |
| **Textos, Código e Logs (`JSONL`)**             | `.bgt` / `.bgtv`    |       **4,60x a 24,50x**        |     3,10x a 14,20x     | Leitura indexada `O(1)` (~0,18 ms) e dicionários de domínio pré-treinados (`.bgtpr`)                  |
| **Multimídia (`PNG`, `JPEG`, `MP4`, `PDF`)**    | `.bgtu` (`BGTU6`)   | **12% a 80% de redução extra**  |        0% a 5%         | Reversão **100% bit-exact** (mesmo digest `SHA-256` original recalculado e validado)                  |

---

## Instalação e Verificação do Ambiente

O Baguet é **100% multiplataforma** e requer `Python 3.9+`. Possui suporte nativo e homologação para:

- **Linux:** Distro com `glibc >= 2.31` em `x86_64` (servidores, clusters HPC) e `aarch64` / ARM64 (AWS Graviton, Ampere Altra, NVIDIA Grace);
- **macOS:** Apple Silicon (`arm64` — M1, M2, M3, M4) e Intel (`x86_64`);
- **Windows:** Windows 10 e Windows 11 (64-bit `x64`).

Inclui compilação SIMD nativa com seleção automática em runtime: aceleração **`AVX2 + FMA`** em arquiteturas x86_64 e **`NEON`** em arquiteturas ARM64.

### Opção 1: Via Gerenciador de Pacotes Python (`pip`)

```bash
pip install baguet
```

### Opção 2: Via Ambiente Isolado Conda / Mamba (Recomendado para IA / HPC)

```bash
conda create -n baguet-env python=3.11 -y
conda activate baguet-env
pip install baguet
```

### Validação de Integridade do Motor Nativo

Após a instalação, execute a rotina de auto-teste para validar a integridade da ponte C-ABI, as extensões SIMD do processador e os limites de tolerância de memória:

```bash
baguet self-test
```

---

## Guia Rápido de Uso

### 1. Aplicativo Visual Desktop (`Baguet Studio`)

O Baguet Studio disponibiliza uma interface visual desktop integrada para comprimir arquivos, executar benchmarks de IA, inspecionar cabeçalhos de contêineres e gerenciar licenças localmente:

```bash
# Inicia o serviço local do Studio na porta padrão (8765) e abre o navegador
baguet studio

# Opções operacionais avançadas:
baguet studio --port 8765        # Porta TCP personalizada
baguet studio --host 127.0.0.1   # Escuta em interface de rede segura
baguet studio --no-browser       # Modo headless (servidores remotos / túnel SSH)
baguet studio --once             # Finaliza automaticamente após a primeira sessão

# Opcional: Instala atalhos de clique direito no Explorer (Windows), Finder (macOS) ou Desktop (Linux)
baguet install-desktop
```

---

### 2. Interface de Linha de Comando (`CLI`)

A ferramenta de terminal unificada do Baguet permite automação direta em pipelines de CI/CD, scripts de backup e orquestração de containers:

```bash
# 1. Compressão e descompressão universal bit-exact (.bgt)
baguet compress modelo_pesos.safetensors modelo_pesos.bgt
baguet decompress modelo_pesos.bgt modelo_pesos_restaurado.safetensors

# 2. Transcodificação reversível sem perdas para arquivos de mídia (.bgtu)
baguet transcode captura_4k.png captura_4k.bgtu
baguet untranscode captura_4k.bgtu captura_4k_original.png

# 3. Inspeção O(1) de cabeçalhos sem descompactar o arquivo
baguet info captura_4k.bgtu

# 4. Cofre de Objetos Indexado (Virtual Slab Pool .bgtv) com acesso O(1)
baguet slab-put cofre.bgtv "documento/1" entrada.txt
baguet slab-get cofre.bgtv "documento/1" restaurado.txt

# 5. Compressão e descompressão de arquivos volumosos em streaming multi-thread (.bgts)
baguet stream-compress arquivo_grande.bin arquivo_grande.bgts --chunk-size 4194304 --workers 4
baguet stream-decompress arquivo_grande.bgts arquivo_restaurado.bin --workers 4

# 6. Compressão com Criptografia Autenticada BGT-AE (AES-256-SIV)
baguet compress dados_confidenciais.parquet cofre_seguro.bgt --key "sua-chave-secreta-256bits"
baguet decompress cofre_seguro.bgt restaurado.parquet --key "sua-chave-secreta-256bits"

# 7. Treinamento de dicionário contextual de domínio (.bgtpr)
baguet train-prior telecom.bgtpr log1.json log2.json log3.json
```

---

### 3. Integração com Python SDK (`baguet_sdk`)

O pacote `baguet_sdk` expõe os núcleos `baguet_sdk.core` (operações universais de arquivo e sistema) e `baguet_sdk.ai` (kernels matriciais, atenção e embeddings):

```python
import numpy as np
from baguet_sdk import core, ai

# Inicializa o motor local verificado
engine = core.BaguetEngine()

# =========================================================================
# 1. Compressão Universal Bit-Exact (Garantia Fail-Closed SHA-256)
# =========================================================================
payload_original = b"Payload critico de infraestrutura..." * 2000

# Retorna o pacote binario (.bgt) e a contagem exata de bits uteis
pacote, useful_bits = core.compress_bytes(payload_original, engine=engine)

# Restaura os bytes originais com validacao SHA-256 bit a bit
restaurado = core.decompress_bytes(pacote, engine=engine)
assert restaurado == payload_original
print(f"Compactado: {len(pacote)} bytes | Integridade: 100% SHA-256 Bit-Exact")

# =========================================================================
# 2. Busca Vetorial RAG Sub-Linear sobre Embeddings Compactados
# =========================================================================
# Cria matriz de embeddings (ex.: 512 vetores de dimensao 128 em FP16)
matriz_vetores = np.random.randn(512, 128).astype(np.float16)
vetor_query = np.random.randn(128).astype(np.float32)

# Comprime a matriz de embeddings e gera o indice de sketch geometrico
pacote_embeddings, _ = ai.compress_embeddings(matriz_vetores, engine=engine)
sketch_idx = ai.build_embedding_sketch_index(pacote_embeddings, block_size=16, engine=engine)

# Executa busca Top-K sub-linear podando subespacos sem descompactar os vetores
indices_topk, scores = ai.query_compressed_embeddings_topk(
    pacote_embeddings, vetor_query, k=5, metric="dot", sketch_index=sketch_idx, engine=engine
)
print("RAG Top-5 indices:", indices_topk)

# =========================================================================
# 3. Offloading de KV-Cache com Online Flash-SDPA sobre Blocos Comprimidos
# =========================================================================
offloader = ai.BaguetKVCacheOffloader(engine=engine)

# Armazena blocos de Keys e Values em formato comprimido
k_bloco = np.ones((8, 16), dtype=np.float16)
v_bloco = np.ones((8, 16), dtype=np.float16)
offloader.put_block(block_id=0, k_tensor=k_bloco, v_tensor=v_bloco)

# Calcula atencao direta (Flash-SDPA) nos blocos offloaded
query_step = np.ones((16,), dtype=np.float32)
contexto, pesos = offloader.attention_on_offloaded_blocks(
    block_ids=[0], query=query_step
)
print("Contexto de atencao calculado com sucesso:", contexto.shape)

# =========================================================================
# 4. Camada Linear Compressiva com Execução Nativa em GPU (CUDA / Apple MPS)
# =========================================================================
import torch

# Converte ou envolve módulo torch.nn.Linear diretamente
linear_layer = torch.nn.Linear(1024, 1024).eval()
compressed_linear = ai.BaguetCompressedLinear.from_torch(linear_layer, engine=engine)

# Execução acelerada em hardware com cache de tensores no dispositivo
device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
x_gpu = torch.randn(8, 1024, device=device)
y_out = compressed_linear(x_gpu)  # Execução nativa no acelerador
```

---

## Os 9 Formatos Nativos da Família `.bgt*`

Cada extensão é identificada por um _Magic Header_ atômico de 4 a 8 bytes, permitindo inspeção em tempo constante $O(1)$ sem parsing completo do contêiner:

| Extensão       |   Magic Header    | Finalidade e Especialização Técnica                                                                                 |
| :------------- | :---------------: | :------------------------------------------------------------------------------------------------------------------ |
| **`.bgt`**     | `BGT6` / `BGT-AE` | Contêiner universal 100% lossless para arquivos, tensores, diretórios e envelopes com `SHA-256` integrado.          |
| **`.bgtu`**    |      `BGTU6`      | Transcodificador reversível bit-exact para contêineres de mídia (`PNG`, `JPEG`, `MP4`, `PDF`, `ZIP`).               |
| **`.bgtt`**    |      `BGTT6`      | Catálogo indexado `SafeTensors` com suporte à extração seletiva por camada via `Zero-Copy mmap` (~1,2 ms).          |
| **`.bgtd`**    |      `BGTD6`      | Checkpoint diferencial exato entre versões de modelos de IA (_fine-tuning_ / _LoRA_ / deltas).                      |
| **`.bgtp`**    |      `BGTP6`      | Tensor progressivo _dual-tier_ (`BF16` base para _hot-start_ + resíduo de mantissa para restauração `FP32`).        |
| **`.bgts`**    |    `BGTS5\x02`    | Contêiner em streaming contínuo multi-bloco paralelo com CRC32 por frame para arquivos de grande escala (>10 GB).   |
| **`.bgtv`**    |    `BGTV5\x03`    | Cofre de Objetos Indexado (_Virtual Slab Pool_) para milhões de registros com inserção e recuperação em $O(1)$.     |
| **`.bgttile`** |    `BGTTILE1`     | Matriz espacial 2D particionada em _tiles_ com decodificação seletiva por coordenadas `(x, y, w, h)`.               |
| **`.bgtpr`**   |     `BGTPR6`      | Dicionário contextual de domínio pré-treinado (_Domain Prior_) para compressão instantânea de payloads repetitivos. |

---

## Arquitetura de Segurança, Confiabilidade e Tolerância a Falhas

1. **Criptografia Autenticada `BGT-AE` (`AES-256-SIV` + `HKDF-SHA256`):**
   Implementa o modo RFC 5297 resistente a mau uso de nonce (_nonce-misuse resistance_) sob a arquitetura _Compress-then-Encrypt_, garantindo privacidade e autenticidade com suporte a metadados associados (_Associated Data_ - `AAD`).
2. **Verificação `SHA-256` Mandatória e Fail-Closed:**
   Qualquer alteração em disco, perda de bit elétrico ou ataque de injeção resulta na rejeição imediata do pacote antes da entrega à aplicação (`BaguetIntegrityError`), impossibilitando vazamento de dados corrompidos.
3. **Imunidade a Decompression Bombs:**
   Limites rígidos de alocação de saída (`max_output_bytes`) e verificação estrita de metadados antes de qualquer alocação dinâmica em memória RAM.
4. **Escrita Atômica Transacional:**
   Persistência segura com flush garantido via `fsync` (Linux/macOS) e `FlushFileBuffers` (Windows), seguida de substituição atômica via descritor de arquivo fechado para prevenir dados corrompidos por falta de energia.
5. **Operação 100% Offline e Soberana:**
   Zero chamadas externas de rede, zero telemetria e validação criptográfica de licença feita localmente.
6. **Proteção Defensiva contra Decompressor Exploits (CVE-2026-111497 / Brotli HTTP2Shell):**
   Mitigação multi-bloco ativa no desempacotador de streams pré-comprimidos externos com limites estritos de buffer e prevenção de loops infinitos de alocação de memória C. Em ambientes de alta contenção regulatória, a variável de ambiente `BAGUET_REQUIRE_PATCHED_BROTLI=1` assegura que bibliotecas `brotli` vulneráveis (< 1.2.1) sejam rejeitadas com fallback seguro para `raw`, e `BAGUET_DISABLE_BROTLI_PROBE=1` desativa completamente a tentativa de probe Brotli.
7. **Host Socket Guard e Proteção Anti-CSRF no Studio:**
   O servidor local do Baguet Studio valida estritamente a autoridade de loopback do cabeçalho `Host` e exige CSRF tokens autenticados em todos os endpoints de alteração de estado (`POST /api/*`), prevenindo ataques de CSRF headless e DNS rebinding.

---

## Arquitetura Modular do SDK e Estrutura do Repositório

O pacote `baguet_sdk` organiza suas funcionalidades em cinco módulos especializados:

- **`baguet_sdk.core`**: Motor principal (`BaguetEngine`), compressão e descompressão universal bit-exact (`.bgt`), cofres indexados $O(1)$ (`BaguetVirtualSlabPool` `.bgtv`), streaming paralelo (`BaguetStreamEngine` `.bgts`) e dicionários de domínio (`.bgtpr`);
- **`baguet_sdk.ai`**: Kernels de IA sem descompressão prévia — busca vetorial RAG Top-K sub-linear, `Online Flash-SDPA`, `BaguetKVCacheOffloader`, projeção linear direta `BaguetCompressedLinear` (`CPU`, `CUDA` e `Apple MPS`), catálogos `SafeTensors mmap` (`.bgtt`), tensores progressivos (`.bgtp`) e checkpoints diferenciais LoRA (`.bgtd`);
- **`baguet_sdk.media`**: Predição harmônica e volumétrica para áudio `PCM16`, imagens `RGB` e vídeo 3D, além do transcodificador universal bit-exact (`BGTU6` `.bgtu`);
- **`baguet_sdk.license`**: Validação offline de tokens corporativos `BGTL1` (`Ed25519`), recibos criptográficos auditáveis (`.receipt.json`) e faturamento comercial;
- **`baguet_sdk.studio`**: Servidor local loopback (`127.0.0.1`) do aplicativo visual **Baguet Studio**, auditoria forense de ROI e integração nativa com o sistema operacional.

```text
baguet/
├── .github/ISSUE_TEMPLATE/     # Templates oficiais de suporte e contato Enterprise
├── conda/                      # Receita oficial de construção para Conda / Mamba
├── examples/
│   └── quickstart.py           # Exemplo rápido de compressão e validação SHA-256
├── baguet_sdk.py               # Interface pública unificada (core, ai, media, license, studio)
├── pyproject.toml              # Configuração PEP 621 e metadados do pacote Python
├── setup.py                    # Empacotador de distribuição assinada via Ed25519
├── SECURITY.md                 # Política de segurança e divulgação responsável
├── LICENSE                     # Licenciamento Dual-Layer (BUSL-1.1 AND MIT)
└── README.md                   # Documentação oficial do projeto
```

---

## Licenciamento Freemium & Governança Offline (`BGTL1`)

O Baguet (`v1.0.0`) adota o modelo de licenciamento híbrido **`BUSL-1.1 AND MIT`**:

- **Garantia Zero Vendor Lock-in (Camada MIT):**
  A biblioteca de descompressão, leitura e verificação de integridade de todos os contêineres `.bgt*` é **sempre livre, irrestrita e perpétua** em todos os tiers, permitindo acesso irrestrito aos seus dados compactados.
- **Camada do Motor de Compressão (BUSL-1.1):**
  O motor ativo de compressão, kernels de IA e orquestração de alta densidade são disponibilizados de forma gratuita no plano **Community** para desenvolvimento e homologação, e sob licença comercial para produção corporativa, com transição programada para código aberto permissivo (MIT / Apache 2.0) na Data de Mudança (_Change Date_ de 29 de outubro de 2030).
- **Ativação 100% Offline via Tokens `Ed25519`:**
  Limites estendidos de throughput, paralelismo e suporte corporativo são liberados via tokens criptografados `BGTL1`, configuráveis pela variável de ambiente `BAGUET_LICENSE_TOKEN` ou pelo comando `baguet license activate "<token>"`, sem nenhuma requisição de rede ou ativação online.

| Capacidade Operacional / Limite Técnico                                | `00. Community` (Freemium)    | `01. Pro` (`AI Builder`)      | `02. Growth` (`AI Scale`)      | `03. Enterprise` (`Air-Gapped`)                                                                                       |
| :--------------------------------------------------------------------- | :---------------------------- | :---------------------------- | :----------------------------- | :-------------------------------------------------------------------------------------------------------------------- |
| **Modalidade de Contratação**                                          | **Acesso Livre & Perpétuo**   | **Assinatura Comercial**      | **Assinatura Comercial**       | **Assinatura Customizada ([contact@soilore.com](mailto:contact@soilore.com?subject=Baguet%20Enterprise%20Contract))** |
| **Operação 100% Offline & Validação SHA-256**                          | Incluso                       | Incluso                       | Incluso                        | Incluso                                                                                                               |
| **Descompressão Universal `.bgt*` (Zero Lock-in)**                     | **Ilimitada (Sempre Livre)**  | **Ilimitada**                 | **Ilimitada**                  | **Ilimitada**                                                                                                         |
| **Baguet Studio (Desktop GUI), CLI & Recibo `.receipt.json`**          | Incluso                       | Incluso                       | Incluso                        | Incluso                                                                                                               |
| **Payload Máximo de Compressão por Operação (`max_bytes`)**            | Até **`64 MB`** (`1 worker`)  | Até **`8 GB`** (`16 workers`) | Até **`64 GB`** (`64 workers`) | **Ilimitado (`1 TB+` / `64 workers`/nó)**                                                                             |
| **Escala Comercial (`Nodes / Containers`)**                            | Uso Local / Avaliação         | Até `8 nós / containers`      | Até `64 nós / containers`      | **Cluster / Datacenter Ilimitado**                                                                                    |
| **Kernels de IA (`RAG Top-K`, `Flash-SDPA`, `Linear W·x`, `KV`)**      | Sandbox Local até **`16 MB`** | `RAG Top-K` & `Fast-Mode`     | **Suite IA Completa (64 GB)**  | **Suite IA Completa Ilimitada**                                                                                       |
| **Catálogos `SafeTensors mmap` (`.bgtt`), `.bgtu` & Deltas (`.bgtd`)** | Até **`64 MB`** (IA `16 MB`)  | Até **`8 GB`**                | Até **`64 GB`**                | **Ilimitado (Modelos 70B+ / 405B+)**                                                                                  |
| **Criptografia `BGT-AE` (`AES-256-SIV`) & Dicionários `.bgtpr`**       | —                             | —                             | **Incluso (`--production`)**   | **Incluso + HSM / Custom Key Shards (`kid`)**                                                                         |
| **Token Offline `BGTL1` (`Ed25519`) & _Grace Period_**                 | Automático (Sem Chave)        | Token `BGTL1` (`7 dias`)      | Token `BGTL1` (`15 dias`)      | **Token `BGTL1` Air-Gapped (`até 90 dias`)**                                                                          |

### Variáveis de Ambiente e Configuração Segura

O ecossistema Baguet disponibiliza variáveis de ambiente auditadas para orquestração em contêineres, pipelines de CI/CD e conformidade de segurança:

| Variável                            |   Valores / Tipo    | Finalidade e Impacto Operacional                                                                                                       |
| :---------------------------------- | :-----------------: | :------------------------------------------------------------------------------------------------------------------------------------- |
| **`BAGUET_LICENSE_TOKEN`**          |  `String (BGTL1)`   | Token criptográfico Ed25519 para ativação corporativa offline instantânea.                                                             |
| **`BAGUET_REQUIRE_PATCHED_BROTLI`** |    `0` (ou `1`)     | Se definida como `1`, bloqueia descompressão por bibliotecas `brotli < 1.2.1` contra a CVE-2026-111497, operando em modo seguro `raw`. |
| **`BAGUET_DISABLE_BROTLI_PROBE`**   |    `0` (ou `1`)     | Se definida como `1`, desativa completamente qualquer sondagem de streams pré-compactados Brotli.                                      |
| **`BAGUET_HOME`**                   |     `~/.baguet`     | Diretório de persistência de credenciais locais, chaves e leases flutuantes.                                                           |
| **`BAGUET_LANG`**                   |  `en` (ou locale)   | Idioma padrão da interface CLI e Studio (`en`, `pt`, `es`, `de`, `fr`, `zh`, `ja`).                                                    |
| **`BAGUET_NODE_ID`**                | Identificador de Nó | Identificador exclusivo para gerenciamento de floating node leases concorrentes.                                                       |

---

## Documentação Oficial e Canais Institucionais

- **Repositório Público no GitHub:** [https://github.com/soilore/baguet](https://github.com/soilore/baguet)
- **Portal Oficial & Planos:** [https://baguet.soilore.com](https://baguet.soilore.com)
- **Guia Técnico de Operação:** [https://baguet.soilore.com/legal/guide.html](https://baguet.soilore.com/legal/guide.html)
- **Litepaper Institucional & Arquitetura:** [https://baguet.soilore.com/legal/litepaper.html](https://baguet.soilore.com/legal/litepaper.html)
- **Termos de Uso e Cláusula de Isenção:** [https://baguet.soilore.com/legal/terms.html](https://baguet.soilore.com/legal/terms.html)
- **Política de Privacidade e Soberania de Dados:** [https://baguet.soilore.com/legal/privacy.html](https://baguet.soilore.com/legal/privacy.html)
- **Contato Institucional e OEM:** [contact@soilore.com](mailto:contact@soilore.com)

---

_© Soilore — Baguet v1.0.0. Todos os direitos reservados._
