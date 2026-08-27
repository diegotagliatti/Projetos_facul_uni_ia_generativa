from gpt4all import GPT4All
from pathlib import Path
import sys
import os
import time
import urllib.request

# 1. Configuração Automática de Pastas e Caminhos
pasta_modelos = Path("models").resolve()
pasta_modelos.mkdir(exist_ok=True)
nome_modelo = "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
caminho_completo_modelo = pasta_modelos / nome_modelo
url_download = "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"

print("=" * 60)
print("INICIANDO ASSISTENTE UNIVERSAL")
print(f"Pasta de modelos: {pasta_modelos}")
print(f"Modelo selecionado: {nome_modelo}")
print("=" * 60)

# 2. Sistema Próprio de Download
if not caminho_completo_modelo.exists():
    print("\nModelo não encontrado localmente.")
    print("Iniciando download direto do Hugging Face (~638 MB)...")
    print("Por favor, aguarde. O tempo depende da velocidade da sua internet.")
    try:
        urllib.request.urlretrieve(url_download, caminho_completo_modelo)
        print("Download concluído com sucesso!\n")
    except Exception as erro:
        print(f"Erro crítico durante o download do modelo: {erro}")
        if caminho_completo_modelo.exists():
            caminho_completo_modelo.unlink()
        sys.exit(1)

# 3. Inicialização da IA
try:
    print("Carregando o motor da Inteligência Artificial...")
    Ia = GPT4All(
        model_name=nome_modelo,
        model_path=str(pasta_modelos),
        allow_download=False,
        device="cpu",
        n_ctx=1024
    )
    print("Modelo carregado com sucesso!")
except Exception as erro:
    print(f"\nErro crítico na inicialização da IA: {erro}")
    sys.exit(1)

# 4. Função para Ler (ou Criar) a Base de Conhecimento
def ler_base_conhecimento(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        print(f"\nAviso: Arquivo '{caminho_arquivo}' não encontrado no computador.")
        print("Criando uma base de conhecimento geral automática para teste...")
        conteudo_padrao = (
            "Informações Gerais de Referência:\n"
            "- A água ferve a 100 graus Celsius ao nível do mar e congela a 0 grau Celsius.\n"
            "- A velocidade da luz no vácuo é de aproximadamente 300.000 quilômetros por segundo.\n"
            "- Para manter uma boa produtividade, é recomendável fazer pausas regulares durante os estudos ou trabalho.\n"
            "- O Linux é um sistema operacional de código aberto amplamente utilizado em servidores e desenvolvimento de software.\n"
        )
        try:
            with open(caminho_arquivo, 'w', encoding='utf-8') as ficheiro:
                ficheiro.write(conteudo_padrao)
            print(f"Arquivo '{caminho_arquivo}' criado com sucesso!\n")
            return conteudo_padrao
        except Exception as erro:
            print(f"Erro ao tentar criar o arquivo base: {erro}")
            sys.exit(1)
        
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as ficheiro:
            conteudo = ficheiro.read()
            
            if not conteudo.strip():
                print("O arquivo de conhecimento está vazio.")
                sys.exit(1)
                
            print("Base de conhecimento carregada!")
            return conteudo      
    except Exception as erro:
        print(f"Erro ao tentar ler a base: {erro}")
        sys.exit(1)

# 5. Execução Principal do Chatbot
if __name__ == "__main__":
    arquivo_base = "base_geral.txt"
    texto_da_base = ler_base_conhecimento(arquivo_base)

    print('\n' + '=' * 60)
    print('BEM-VINDO AO ASSISTENTE VIRTUAL'.center(60))
    print('=' * 60)
    
    nome_usuario = input("\nPor favor, digite o seu nome: ").strip()
    if not nome_usuario:
        nome_usuario = "Usuário"

    print(f"\nOlá, {nome_usuario}! Pergunte qualquer coisa ou digite 'sair' para encerrar.")

    prompt_sistema = (
        "Você é um assistente virtual educado, prestativo e com conhecimentos gerais.\n"
        "RESPONDA SEMPRE EM PORTUGUÊS.\n"    
        f"Informações de referência:\n{texto_da_base}\n"
    )
    with Ia.chat_session(system_prompt=prompt_sistema):
        while True:
            try:
                pergunta = input(f'\n{nome_usuario}: ').strip()
            except (KeyboardInterrupt, EOFError):
                print("\n\nChat encerrado pelo usuário. Tchau!")
                break

            if pergunta.lower() == "sair":
                print("\nAssistente: Foi um prazer ajudar! Tchau!")
                break        
            
            if not pergunta:
                continue

            print("Assistente: ", end="", flush=True)
            resposta_completa = ""
            tempo_inicio = time.time()
            

            for token in Ia.generate(prompt=pergunta, max_tokens=1100, temp=0.7, streaming=True):
                resposta_completa += token
                
                if f"{nome_usuario}:" in resposta_completa or "Usuário:" in resposta_completa:
                    break
                    
                print(token, end="", flush=True)
                
            tempo_gasto = time.time() - tempo_inicio
            print(f"\n\n[Tempo de resposta: {tempo_gasto:.2f} segundos]")