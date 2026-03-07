# sistema de usuarios sem POO

# PROBLEMAS NESTE CÓDIGO:
# 1. Usar listas paralelas em vez de classes/dicionários
# 2. Variáveis globais por todo lado
# 3. Funções com muitos parâmetros
# 4. Sem encapsulamento
# 5. Dados sensíveis (senha) sem proteção
# 6. Código repetitivo
# 7. Lógica de busca ineficiente

# RUIM: variáveis globais
nomes = []
idades = []
emails = []
senhas = []
ativo = []

# RUIM: função com muitos parâmetros e sem validação
def add(n, i, e, s):
    # RUIM: sem validação de dados
    nomes.append(n)
    idades.append(i)
    emails.append(e)
    senhas.append(s)  # RUIM: senha em texto puro
    ativo.append(True)
    print("usuario adicionado!")

# RUIM: lógica de busca O(n) toda vez
def buscar(n):
    for x in range(len(nomes)):  # RUIM: usar range(len()) em vez de enumerate
        if nomes[x] == n:
            # RUIM: código duplicado para exibir dados
            print("Nome:", nomes[x])
            print("Idade:", idades[x])
            print("Email:", emails[x])
            print("Senha:", senhas[x])  # RUIM: expor senha
            print("Ativo:", ativo[x])
            return
    print("nao encontrado")

# RUIM: modificar dados sem validação
def mudar_idade(n, nova):
    for x in range(len(nomes)):
        if nomes[x] == n:
            idades[x] = nova  # RUIM: sem validação de idade
            print("idade alterada")
            return
    print("usuario nao encontrado")

# RUIM: lógica duplicada
def mudar_email(n, novo):
    for x in range(len(nomes)):
        if nomes[x] == n:
            emails[x] = novo  # RUIM: sem validação de email
            return
    print("usuario nao encontrado")

# RUIM: função que faz várias coisas
def listar():
    if len(nomes) == 0:  # RUIM: comparar com 0 em vez de not lista
        print("nenhum usuario")
    else:
        # RUIM: lógica de exibição misturada
        for x in range(len(nomes)):
            if ativo[x]:  # RUIM: if dentro de loop
                print(f"{x+1}. {nomes[x]} - {idades[x]} anos - {emails[x]}")

# RUIM: "deletar" sem realmente deletar
def desativar(n):
    for x in range(len(nomes)):
        if nomes[x] == n:
            ativo[x] = False
            return
    print("usuario nao encontrado")

# Teste
add("joao", 25, "joao@email.com", "123456")  # RUIM: senha fraca
add("maria", 30, "maria@email.com", "senha123")
add("pedro", -5, "emailinvalido", "p")  # RUIM: aceita dados inválidos

print("\n=== LISTA ===")
listar()

print("\n=== BUSCAR ===")
buscar("joao")

mudar_idade("maria", 999)  # RUIM: aceita idade absurda

# SUGESTÕES DE REFATORAÇÃO:
# - Criar classe Usuario com atributos privados
# - Usar lista de objetos ou dicionário em vez de listas paralelas
# - Implementar validações (idade, email, senha forte)
# - Hash de senha em vez de texto puro
# - Usar @property e @setter para encapsulamento
# - Criar classe GerenciadorUsuarios para operações CRUD
# - Implementar __str__ e __repr__ na classe Usuario
# - Usar enumerate em vez de range(len())
# - Extrair lógica de busca para método reutilizável
# - Adicionar tratamento de exceções
# - Implementar padrão Repository para persistência
# - Usar type hints
# - Adicionar logging em vez de prints
