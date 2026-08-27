------------------------------------
ARQUIVO: CHATBOTS_COMPLETOS.txt
------------------------------------

------------------------------------
Este arquivo contém:
------------------------------------

  - README com instruções detalhadas para instalação e execução
  - Código fonte de BOT_700mb.py
  - Código fonte de botQ2.py
  - Código fonte de chatbot_ollana.py
------------------------------------
LEIA-ME – INSTRUÇÕES PARA RODAR OS CHATBOTS
------------------------------------

Os três bots utilizam modelos de linguagem diferentes e são
independentes. Escolha o que melhor atende sua necessidade.

PRÉ‑REQUISITOS GERAIS:
  - Python 3.8 ou superior instalado
  - pip (gerenciador de pacotes Python)
  - (Opcional) venv para ambiente virtual

DEPENDÊNCIAS COMUNS (instalar com pip):
  pip install gpt4all ollama

(Obs: ollama só é necessário para o chatbot_ollana.py)

------------------------------------
1. BOT_700mb.py
------------------------------------
  - Baixa automaticamente o modelo TinyLlama (~638 MB) do Hugging Face.
  - Cria um arquivo base_geral.txt com conhecimento geral, caso não exista.
  - Inicia um chat interativo em português.

  Como rodar:
    python BOT_700mb.py

  Na primeira execução, o download pode demorar alguns minutos.
  Depois, o chat estará pronto.

------------------------------------
2. botQ2.py (modelo culinário)
------------------------------------
  - Utiliza o modelo stackexchange_cooking.Q2_K.gguf (especializado em culinária).
  - Necessita que o modelo seja baixado manualmente e colocado na pasta models/.
  - Espera um arquivo base.txt com conhecimentos adicionais (criado automaticamente se não existir? Não, ele só lê; se não existir, encerra. Por isso, crie um base.txt com conteúdo relevante ou use o gerado pelo BOT_700mb? Melhor criar um manualmente).

  COMO BAIXAR O MODELO:
    mkdir -p models
    curl -L -o models/stackexchange_cooking.Q2_K.gguf https://huggingface.co/mradermacher/stackexchange_cooking-GGUF/resolve/main/stackexchange_cooking.Q2_K.gguf

  OBSERVAÇÃO IMPORTANTE: no código fornecido, a extensão do arquivo está escrita como .guff (com dois 'f'). Corrija para .gguf no script (ou renomeie o arquivo baixado para .guff). Recomenda-se corrigir o script para .gguf.

  Crie um arquivo base.txt (exemplo):
    "Dicas de culinária: Use sal a gosto, etc."

  Como rodar:
    python botQ2.py

------------------------------------
3. chatbot_ollana.py (Ollama)
------------------------------------
  - Usa o modelo llama3.2:3b via Ollama (requer instalação do Ollama).
  - Cria um arquivo base.txt com receitas básicas, se não existir.
  - Inicia chat interativo focado em culinária.

  INSTALAR OLLAMA:
    Linux (Debian/Ubuntu): curl -fsSL https://ollama.com/install.sh | sh
    macOS/Windows: siga instruções em https://ollama.com

  PUXAR O MODELO:
    ollama pull llama3.2:3b

  Como rodar:
    python chatbot_ollana.py

------------------------------------
COMANDOS RÁPIDOS POR SISTEMA OPERACIONAL
------------------------------------

  Debian/Ubuntu (primeira vez):
    sudo apt update && sudo apt install python3-venv python3-pip curl -y
    curl -fsSL https://ollama.com/install.sh | sh   # se for usar ollama
    python3 -m venv meu_ambiente
    source meu_ambiente/bin/activate
    pip install gpt4all ollama

  Para rodar no dia a dia (com ambiente ativado):
    source meu_ambiente/bin/activate
    python BOT_700mb.py
    # ou
    python botQ2.py
    # ou
    python chatbot_ollana.py

  macOS (primeira vez):
    python3 -m venv meu_ambiente
    source meu_ambiente/bin/activate
    pip install gpt4all ollama

  Arch Linux (primeira vez):
    sudo pacman -S python
    python -m venv meu_ambiente
    source meu_ambiente/bin/activate
    pip install gpt4all ollama

  Windows 11 (PowerShell):
    # Primeira vez:
    python -m venv meu_ambiente
    .\meu_ambiente\Scripts\activate
    pip install gpt4all ollama

    # Rodar (ambiente ativado):
    python BOT_700mb.py

    # Rodar sem ativar (direto):
    .\meu_ambiente\Scripts\python.exe BOT_700mb.py

------------------------------------
ESTRUTURA DE ARQUIVOS ESPERADA
------------------------------------
  ├── BOT_700mb.py
  ├── botQ2.py
  ├── chatbot_ollana.py
  ├── models/
  │   └── stackexchange_cooking.Q2_K.gguf   (para botQ2)
  ├── base.txt          (usado por botQ2 e chatbot_ollana, criado automaticamente pelo último)
  └── base_geral.txt    (criado automaticamente pelo BOT_700mb)

============================================================
FIM DO README
============================================================
