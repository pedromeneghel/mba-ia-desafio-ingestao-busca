from search import search_prompt

def main():
    """
    Interface CLI para interação com o sistema de busca semântica.
    """
    print("=" * 60)
    print("Sistema de Busca Semântica com LangChain e Postgres pgVector")
    print("=" * 60)
    print("Inicializando o sistema...")

    try:
        chain = search_prompt()
        print("Sistema pronto! Digite 'sair' para encerrar.\n")
    except Exception as e:
        print(f"Erro ao inicializar o chat: {e}")
        print("Verifique se:")
        print("1. O banco de dados está rodando (docker compose up -d)")
        print("2. A ingestão foi executada (python3 src/ingest.py)")
        print("3. As variáveis de ambiente estão configuradas corretamente")
        return

    # Loop principal do chat
    while True:
        try:
            # Solicita pergunta do usuário
            print("-" * 60)
            pergunta = input("Faça sua pergunta: ").strip()

            # Verifica se o usuário quer sair
            if pergunta.lower() in ['sair', 'exit', 'quit', 'q']:
                print("\nEncerrando o sistema. Até logo!")
                break

            # Ignora perguntas vazias
            if not pergunta:
                print("Por favor, digite uma pergunta válida.")
                continue

            # Processa a pergunta
            print("\nProcessando...")
            resposta = chain.invoke(pergunta)

            # Exibi a resposta
            print(f"\nPERGUNTA: {pergunta}")
            print(f"RESPOSTA: {resposta}\n")

        except KeyboardInterrupt:
            print("\n\nEncerrando o sistema. Até logo!")
            break
        except Exception as e:
            print(f"\nErro ao processar a pergunta: {e}")
            print("Tente novamente ou digite 'sair' para encerrar.\n")

if __name__ == "__main__":
    main()
