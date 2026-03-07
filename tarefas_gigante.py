# gerenciador de tarefas com funcao gigante

# PROBLEMAS NESTE CÓDIGO:
# 1. Função gigante com 100+ linhas
# 2. Código profundamente aninhado
# 3. Variáveis com nomes de uma letra
# 4. Falta de funções auxiliares
# 5. Lógica duplicada
# 6. Hard-coded valores
# 7. Sem separação de concerns

import json
import os

# RUIM: função gigante que faz TUDO
def sistema_tarefas():
    # RUIM: dados em memória, perdem ao fechar
    t = []  # RUIM: nome de variável ruim

    while True:  # RUIM: loop infinito sem controle adequado
        # RUIM: UI misturada com lógica
        print("\n" + "="*50)
        print("GERENCIADOR DE TAREFAS")
        print("="*50)
        print("1 - adicionar tarefa")
        print("2 - listar tarefas")
        print("3 - marcar como feita")
        print("4 - deletar tarefa")
        print("5 - editar tarefa")
        print("6 - filtrar por prioridade")
        print("7 - salvar em arquivo")
        print("8 - carregar de arquivo")
        print("0 - sair")
        print("="*50)

        o = input("opcao: ")  # RUIM: nome de variável ruim

        # RUIM: if/elif gigante
        if o == "1":
            # RUIM: lógica de adicionar aqui em vez de função separada
            n = input("titulo: ")
            d = input("descricao: ")
            p = input("prioridade (1-baixa, 2-media, 3-alta): ")

            # RUIM: sem validação
            tarefa = {"titulo": n, "desc": d, "prio": p, "feita": False}
            t.append(tarefa)
            print("tarefa adicionada!")

        elif o == "2":
            # RUIM: lógica de listagem aqui
            if len(t) == 0:
                print("nenhuma tarefa")
            else:
                # RUIM: loop complexo com muitos ifs
                for i in range(len(t)):
                    # RUIM: lógica de formatação complicada
                    s = "[X]" if t[i]["feita"] else "[ ]"
                    if t[i]["prio"] == "1":
                        p_txt = "BAIXA"
                    elif t[i]["prio"] == "2":
                        p_txt = "MEDIA"
                    elif t[i]["prio"] == "3":
                        p_txt = "ALTA"
                    else:
                        p_txt = "???"

                    print(f"{i+1}. {s} {t[i]['titulo']} - {p_txt}")
                    print(f"   {t[i]['desc']}")

        elif o == "3":
            # RUIM: código duplicado (mesma lógica de listagem)
            if len(t) == 0:
                print("nenhuma tarefa")
            else:
                for i in range(len(t)):
                    s = "[X]" if t[i]["feita"] else "[ ]"
                    print(f"{i+1}. {s} {t[i]['titulo']}")

                n = input("numero da tarefa: ")
                # RUIM: sem try/except para conversão
                idx = int(n) - 1

                # RUIM: validação básica mas sem mensagem clara
                if idx >= 0 and idx < len(t):
                    t[idx]["feita"] = True
                    print("marcada como feita!")
                else:
                    print("invalido")

        elif o == "4":
            # RUIM: mais código duplicado
            if len(t) == 0:
                print("nenhuma tarefa")
            else:
                for i in range(len(t)):
                    s = "[X]" if t[i]["feita"] else "[ ]"
                    print(f"{i+1}. {s} {t[i]['titulo']}")

                n = input("numero da tarefa: ")
                idx = int(n) - 1

                if idx >= 0 and idx < len(t):
                    # RUIM: sem confirmação antes de deletar
                    t.pop(idx)
                    print("deletada!")
                else:
                    print("invalido")

        elif o == "5":
            # RUIM: ainda mais código duplicado
            if len(t) == 0:
                print("nenhuma tarefa")
            else:
                for i in range(len(t)):
                    print(f"{i+1}. {t[i]['titulo']}")

                n = input("numero da tarefa: ")
                idx = int(n) - 1

                if idx >= 0 and idx < len(t):
                    # RUIM: edição inline, confuso
                    print(f"atual: {t[idx]['titulo']}")
                    novo_t = input("novo titulo (enter para manter): ")
                    if novo_t != "":
                        t[idx]["titulo"] = novo_t

                    print(f"atual: {t[idx]['desc']}")
                    novo_d = input("nova desc (enter para manter): ")
                    if novo_d != "":
                        t[idx]["desc"] = novo_d

                    print(f"atual: {t[idx]['prio']}")
                    novo_p = input("nova prio (enter para manter): ")
                    if novo_p != "":
                        t[idx]["prio"] = novo_p

                    print("atualizada!")

        elif o == "6":
            # RUIM: filtro ineficiente
            p = input("prioridade (1/2/3): ")
            encontrou = False
            for i in range(len(t)):
                if t[i]["prio"] == p:
                    encontrou = True
                    s = "[X]" if t[i]["feita"] else "[ ]"
                    print(f"{i+1}. {s} {t[i]['titulo']}")

            if not encontrou:
                print("nenhuma tarefa com essa prioridade")

        elif o == "7":
            # RUIM: salvamento sem tratamento de erro adequado
            arquivo = "tarefas.json"
            with open(arquivo, "w") as f:
                json.dump(t, f)
            print(f"salvo em {arquivo}")

        elif o == "8":
            # RUIM: carregamento perigoso
            arquivo = "tarefas.json"
            if os.path.exists(arquivo):
                with open(arquivo, "r") as f:
                    t = json.load(f)  # RUIM: sobrescreve sem avisar
                print("carregado!")
            else:
                print("arquivo nao existe")

        elif o == "0":
            # RUIM: sair sem salvar, perde dados
            print("tchau!")
            break
        else:
            print("opcao invalida")

# RUIM: execução direto no módulo
sistema_tarefas()

# SUGESTÕES DE REFATORAÇÃO:
# - Criar classe Tarefa com validações
# - Criar classe GerenciadorTarefas
# - Separar UI (menu) da lógica de negócio
# - Extrair cada operação em método próprio
# - Criar enums para prioridade e status
# - Implementar padrão Command para operações
# - Usar list comprehension para filtros
# - Adicionar confirmação antes de deletar
# - Auto-save periódico
# - Implementar padrão Observer para mudanças
# - Usar biblioteca como Rich para UI melhor
# - Adicionar testes unitários
# - Implementar undo/redo
# - Validar inputs adequadamente
# - Usar dataclasses para Tarefa
