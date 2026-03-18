import json
import os


def sistema_tarefas():
    t = []

    while True:
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

        o = input("opcao: ")

        if o == "1":
            n = input("titulo: ")
            d = input("descricao: ")
            p = input("prioridade (1-baixa, 2-media, 3-alta): ")

            tarefa = {"titulo": n, "desc": d, "prio": p, "feita": False}
            t.append(tarefa)
            print("tarefa adicionada!")

        elif o == "2":
            if len(t) == 0:
                print("nenhuma tarefa")
            else:
                for i in range(len(t)):
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
            if len(t) == 0:
                print("nenhuma tarefa")
            else:
                for i in range(len(t)):
                    s = "[X]" if t[i]["feita"] else "[ ]"
                    print(f"{i+1}. {s} {t[i]['titulo']}")

                n = input("numero da tarefa: ")
                idx = int(n) - 1

                if idx >= 0 and idx < len(t):
                    t[idx]["feita"] = True
                    print("marcada como feita!")
                else:
                    print("invalido")

        elif o == "4":
            if len(t) == 0:
                print("nenhuma tarefa")
            else:
                for i in range(len(t)):
                    s = "[X]" if t[i]["feita"] else "[ ]"
                    print(f"{i+1}. {s} {t[i]['titulo']}")

                n = input("numero da tarefa: ")
                idx = int(n) - 1

                if idx >= 0 and idx < len(t):
                    t.pop(idx)
                    print("deletada!")
                else:
                    print("invalido")

        elif o == "5":
            if len(t) == 0:
                print("nenhuma tarefa")
            else:
                for i in range(len(t)):
                    print(f"{i+1}. {t[i]['titulo']}")

                n = input("numero da tarefa: ")
                idx = int(n) - 1

                if idx >= 0 and idx < len(t):
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
            arquivo = "tarefas.json"
            with open(arquivo, "w") as f:
                json.dump(t, f)
            print(f"salvo em {arquivo}")

        elif o == "8":
            arquivo = "tarefas.json"
            if os.path.exists(arquivo):
                with open(arquivo, "r") as f:
                    t = json.load(f)
                print("carregado!")
            else:
                print("arquivo nao existe")

        elif o == "0":
            print("tchau!")
            break
        else:
            print("opcao invalida")


sistema_tarefas()
