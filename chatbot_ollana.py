import os
import sys
import time
import ollama

# 1. Funcao Inteligente para Ler (ou Criar) a Base de Conhecimento
def ler_base_conhecimento(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        print(f"Aviso: Arquivo '{caminho_arquivo}' nao encontrado no computador.")
        print("Criando uma base de receitas automatica para teste...")
        conteudo_padrao = (
            "Dicas e Receitas Basicas do Chef:\n"
            "- Para o arroz ficar soltinho, lave os graos antes de cozinhar e use agua quente.\n"
            "- Sempre sele a carne em fogo alto para manter a suculencia antes de cozinhar no molho.\n"
            "- O segredo de um bom refogado e colocar o alho logo depois da cebola, pois o alho queima mais rapido.\n"
            "- Para tirar a acidez do molho de tomate, adicione uma cenoura inteira no cozimento ou uma pitada de acucar.\n"
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
                print("O arquivo de conhecimento esta vazio.")
                sys.exit(1)
                
            print("Base de receitas carregada com sucesso!")
            return conteudo      
    except Exception as erro:
        print(f"Erro ao tentar ler a base: {erro}")
        sys.exit(1)

# 2. Execucao Principal do Chatbot
if __name__ == "__main__":
    arquivo_base = "base.txt"
    texto_da_base = ler_base_conhecimento(arquivo_base)
    
    print('\n' + '=' * 60)
    print('BEM-VINDO AO CHATBOT DE CULINARIA'.center(60))
    print('=' * 60)
    
    try:
        nome_usuario = input("\nPor favor, digite o seu nome: ").strip()
        if not nome_usuario:
            nome_usuario = "Usuario"
    except (KeyboardInterrupt, EOFError):
        print("\n\nChat encerrado pelo usuario. Tchau!")
        sys.exit(0)

    print(f"\nOla, {nome_usuario}! Pergunte qualquer coisa sobre culinaria ou digite 'sair' para encerrar.")
    
    while True:
        try:
            pergunta = input(f'\n{nome_usuario}: ').strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nChat encerrado pelo usuario. Tchau!")
            break
            
        if pergunta.lower() == "sair":
            print("\nChefBot: Foi um prazer ajudar na cozinha! Tchau!")
            break        

        if not pergunta:
            continue

        prompt_base = (
            "Voce e um chef de cozinha educado, prestativo e especialista em culinaria.\n"
            "RESPONDA SEMPRE EM PORTUGUES.\n"
            f"Informacoes de referencia:\n{texto_da_base}\n\n"
        )

        prompt = f"{prompt_base}{nome_usuario}: {pergunta}\nChefBot:"
        
        try:
            tempo_inicio = time.time()
            stream_response = ollama.generate(model='llama3.2:3b', prompt=prompt, stream=True)            
            print("ChefBot: ", end="", flush=True)
            resposta_completa = ""
            
            for chunk in stream_response:
                pedaco = chunk['response']
                resposta_temporaria = resposta_completa + pedaco

                if f"{nome_usuario}:" in resposta_temporaria or "Usuario:" in resposta_temporaria:
                    break
                
                resposta_completa += pedaco
                print(pedaco, end='', flush=True)
                
                # CAPTURA EXATA DOS TOKENS POR SEGUNDO NO ÚLTIMO PACOTE
                if chunk.get('done'):
                    tokens_gerados = chunk.get('eval_count', 0)
                    tempo_segundos = chunk.get('eval_duration', 1) / 1e9
                    taxa_tks = tokens_gerados / tempo_segundos
                    print(f"\n\n[Métrica: {tokens_gerados} tokens gerados a {taxa_tks:.2f} TK/S]")
                    
        # AQUI ESTÁ O BLOCO QUE FALTAVA PARA FECHAR O TRY ACIMA:
        except Exception as erro_geracao:
            print(f"\nErro critico ao comunicar com o Ollama: {erro_geracao}")
            print("Verifique se o servico do Ollama esta rodando no seu sistema e se o modelo foi criado.")