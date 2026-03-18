nomes = []
idades = []
emails = []
senhas = []
ativo = []


def add(n, i, e, s):
    nomes.append(n)
    idades.append(i)
    emails.append(e)
    senhas.append(s)
    ativo.append(True)
    print("usuario adicionado!")


def buscar(n):
    for x in range(len(nomes)):
        if nomes[x] == n:
            print("Nome:", nomes[x])
            print("Idade:", idades[x])
            print("Email:", emails[x])
            print("Senha:", senhas[x])
            print("Ativo:", ativo[x])
            return
    print("nao encontrado")


def mudar_idade(n, nova):
    for x in range(len(nomes)):
        if nomes[x] == n:
            idades[x] = nova
            print("idade alterada")
            return
    print("usuario nao encontrado")


def mudar_email(n, novo):
    for x in range(len(nomes)):
        if nomes[x] == n:
            emails[x] = novo
            return
    print("usuario nao encontrado")


def listar():
    if len(nomes) == 0:
        print("nenhum usuario")
    else:
        for x in range(len(nomes)):
            if ativo[x]:
                print(f"{x+1}. {nomes[x]} - {idades[x]} anos - {emails[x]}")


def desativar(n):
    for x in range(len(nomes)):
        if nomes[x] == n:
            ativo[x] = False
            return
    print("usuario nao encontrado")


add("joao", 25, "joao@email.com", "123456")
add("maria", 30, "maria@email.com", "senha123")
add("pedro", -5, "emailinvalido", "p")

print("\n=== LISTA ===")
listar()

print("\n=== BUSCAR ===")
buscar("joao")

mudar_idade("maria", 999)
