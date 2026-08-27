from gpt4all import GPT4All
from pathlib import Path
import sys
import os
import time

caminho_modelo = Path("models/stackexchange_cooking.Q2_K.gguf").resolve()

print("Carregando o modelo: stackexchange_cooking...")

try:
    Ia = GPT4All(model_name=str(caminho_modelo), device="cpu", n_ctx=2048)
except Exception as erro:
    print(f'Erro na inicialização da IA: {erro}')
    sys.exit(1)


# Função para ler o arquivo de contexto
def ler_base_conhecimento(Conhecimento_basico):
    if not os.path.exists(Conhecimento_basico):
        print('Erro: Arquivo base de conhecimento não encontrado.')
        sys.exit(1)

    try:
        with open(Conhecimento_basico, 'r', encoding='utf-8') as ficheiro:
            conteudo = ficheiro.read()

            if not conteudo.strip():
                print("O arquivo está vazio ou não pôde ser lido corretamente.")
                sys.exit(1)

            print("Base carregada")
            return conteudo
    except Exception as erro:
        print(f"Erro ao tentar ler a base: {erro}")
        sys.exit(1)


# Execução principal do Chatbot
if __name__ == "__main__":
    Conhecimento = "base.txt"
    texto_da_base = ler_base_conhecimento(Conhecimento)
    print('Bot iniciando...')

    print('\n                              Bem vindo ao chatbot de Culinária                              ')
    nome_usuario = input("Por favor, digite o seu nome: ").strip()

    if not nome_usuario:
        nome_usuario = "Usuário"

    prompt_base = (
        "Você é um chef de cozinha educado.\n"
        "RESPONDA SEMPRE NA MESMA LÍNGUA.\n"
        f"Informações:\n{texto_da_base}\n\n"
    )

    # AQUI ESTÁ A CORREÇÃO PRINCIPAL: Abrindo a sessão de chat!
    with Ia.chat_session(system_prompt=prompt_base):
        while True:
            pergunta = input(f'\n{nome_usuario}: ').strip()

            if not pergunta:
                continue

            if pergunta.lower() == "sair":
                print("Chat encerrado, tchau.")
                break

            print("ChefBot: ", end="", flush=True)

            resposta_completa = ""
            tempo_inicio = time.time()


            for token in Ia.generate(prompt=pergunta, max_tokens=1355, temp=0.7, streaming=True):
                resposta_completa += token

                if "Usuário:" in resposta_completa or f"{nome_usuario}:" in resposta_completa:
                    break

                print(token, end="", flush=True)

            tempo_fim = time.time()
            tempo_gasto = tempo_fim - tempo_inicio

            print(f"\n\n[ Tempo de resposta: {tempo_gasto:.2f} segundos]\n")
