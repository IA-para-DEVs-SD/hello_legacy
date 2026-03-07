# calculadora mal feita

# PROBLEMAS NESTE CÓDIGO:
# 1. Nomes de variáveis ruins (a, b, x, y, z)
# 2. Função gigante fazendo tudo
# 3. Sem tratamento de erros
# 4. Código duplicado
# 5. Magic numbers espalhados
# 6. Sem separação de responsabilidades
# 7. Print dentro da lógica de negócio
# 8. Falta de documentação
# 9. Não usa POO quando deveria

def calc():
    # RUIM: função gigante que faz tudo
    print("=== CALCULADORA ===")
    x = input("numero 1: ")
    y = input("numero 2: ")
    z = input("operacao (+,-,*,/): ")

    # RUIM: sem validação, vai quebrar com input inválido
    a = float(x)
    b = float(y)

    # RUIM: if/elif gigante, difícil de manter
    if z == "+":
        r = a + b
        print("resultado:", r)
    elif z == "-":
        r = a - b
        print("resultado:", r)
    elif z == "*":
        r = a * b
        print("resultado:", r)
    elif z == "/":
        # RUIM: divisão por zero não é tratada adequadamente
        if b == 0:
            print("erro!")
        else:
            r = a / b
            print("resultado:", r)
    else:
        print("operacao invalida")

    # RUIM: código duplicado
    c = input("continuar? (s/n): ")
    if c == "s" or c == "S" or c == "sim" or c == "SIM":
        calc()  # RUIM: recursão sem limite
    else:
        print("tchau")

# RUIM: lógica misturada com execução
calc()

# SUGESTÕES DE REFATORAÇÃO:
# - Criar classe Calculadora
# - Separar input/output da lógica
# - Usar try/except para validação
# - Criar métodos separados para cada operação
# - Usar dicionário em vez de if/elif
# - Implementar loop while em vez de recursão
# - Adicionar type hints
# - Criar constantes para mensagens
# - Validar inputs adequadamente
# - Implementar testes unitários
