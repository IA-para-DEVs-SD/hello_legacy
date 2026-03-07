# processador de dados confuso

# PROBLEMAS NESTE CÓDIGO:
# 1. Lógica confusa e difícil de entender
# 2. Nomes de variáveis sem significado
# 3. Código "esperto" demais (over-engineering ruim)
# 4. Condicionais aninhados profundamente
# 5. Falta de comentários úteis
# 6. Mistura de português e inglês
# 7. Magic numbers por todo lado

# RUIM: função com nome vago
def processar(data):
    # RUIM: variável com nome sem significado
    r = []

    # RUIM: lógica confusa com múltiplos ifs aninhados
    for item in data:
        if type(item) == int:
            if item > 0:
                if item % 2 == 0:
                    if item < 100:
                        r.append(item * 2)
                    else:
                        r.append(item * 3)
                else:
                    if item < 50:
                        r.append(item + 10)
                    else:
                        r.append(item - 10)
            else:
                if item % 2 == 0:
                    r.append(abs(item))
                else:
                    r.append(0)
        elif type(item) == str:
            if len(item) > 5:
                if item[0].isupper():
                    r.append(item.lower())
                else:
                    r.append(item.upper())
            else:
                if item.isdigit():
                    r.append(int(item) * 5)
                else:
                    r.append(item[::-1])
        elif type(item) == list:
            # RUIM: recursão sem documentação
            r.append(processar(item))
        else:
            r.append(None)

    return r

# RUIM: função com lógica bizarra
def calc(x, y, z=1):
    # RUIM: lógica desnecessariamente complicada
    if z == 1:
        return (x + y) * z if x > y else (x - y) / z if x < y else x * y * z
    elif z == 2:
        return x ** y if x > 0 and y > 0 else x + y if x < 0 else y - x
    else:
        return ((x + y) * z - x) / (y if y != 0 else 1) + z

# RUIM: função que faz muitas coisas diferentes
def validar_e_processar_e_salvar(dados, arquivo=None, modo=1):
    # RUIM: função faz 3 coisas diferentes
    # RUIM: parâmetro modo é magic number

    # validação confusa
    if not dados:
        return False

    if modo == 1:
        resultado = []
        for d in dados:
            if isinstance(d, (int, float)):
                if d > 0:
                    resultado.append(d * 2)
            elif isinstance(d, str):
                if len(d) > 0:
                    resultado.append(d.upper())
    elif modo == 2:
        resultado = [d for d in dados if d]  # RUIM: filtro vago
    else:
        resultado = dados

    # RUIM: salvar opcional confunde responsabilidade
    if arquivo:
        # RUIM: sem tratamento de exceção
        with open(arquivo, "w") as f:
            f.write(str(resultado))

    return resultado

# RUIM: função com muitos return e lógica confusa
def categorizar(valor):
    # RUIM: múltiplos returns tornam difícil seguir o fluxo
    if type(valor) == int:
        if valor < 0:
            return "negativo"
        if valor == 0:
            return "zero"
        if valor < 10:
            return "pequeno"
        if valor < 100:
            return "medio"
        return "grande"

    if type(valor) == str:
        if valor.isdigit():
            return categorizar(int(valor))  # RUIM: recursão confusa
        if len(valor) < 5:
            return "curto"
        return "longo"

    if type(valor) == list:
        if len(valor) == 0:
            return "vazio"
        if len(valor) < 5:
            return "poucos"
        return "muitos"

    return "desconhecido"

# RUIM: classe mal projetada
class Processador:
    # RUIM: construtor confuso
    def __init__(self, x, y=None, z=None, modo=1, ativo=True):
        self.x = x  # RUIM: atributos sem significado
        self.y = y if y else x * 2  # RUIM: lógica no construtor
        self.z = z if z else self.y * 3
        self.m = modo  # RUIM: nome abreviado
        self.a = ativo
        self.r = []  # RUIM: r de que?

    # RUIM: método que modifica estado de forma confusa
    def proc(self, data):
        if not self.a:
            return None

        # RUIM: lógica baseada em magic number
        if self.m == 1:
            self.r = [d * self.x for d in data]
        elif self.m == 2:
            self.r = [d + self.y for d in data]
        else:
            self.r = [d * self.z for d in data]

        return self.r

    # RUIM: getter/setter sem propósito claro
    def get_r(self):
        return self.r

    def set_m(self, m):
        self.m = m

# Testes (também ruins)
print("=== TESTE 1 ===")
d = [1, 2, -3, 4, "hello", "WORLD", "123", [5, 6]]
print(processar(d))

print("\n=== TESTE 2 ===")
print(calc(5, 3, 1))
print(calc(5, 3, 2))
print(calc(5, 3, 3))

print("\n=== TESTE 3 ===")
print(categorizar(5))
print(categorizar(150))
print(categorizar("hello"))
print(categorizar([1, 2, 3]))

print("\n=== TESTE 4 ===")
p = Processador(2, 4, 6, 1)
print(p.proc([1, 2, 3, 4, 5]))

# SUGESTÕES DE REFATORAÇÃO:
# - Renomear variáveis para nomes significativos
# - Extrair condicionais aninhados em funções separadas
# - Criar classes específicas para cada tipo de processamento
# - Usar Strategy Pattern para diferentes modos
# - Substituir magic numbers por Enums ou constantes
# - Aplicar princípio Single Responsibility
# - Adicionar type hints
# - Criar classes especializadas (IntProcessor, StringProcessor, etc)
# - Usar polimorfismo em vez de type checking
# - Documentar lógica complexa adequadamente
# - Simplificar expressões ternárias aninhadas
# - Usar guard clauses para reduzir aninhamento
# - Implementar __repr__ e __str__ adequadamente
# - Separar validação, processamento e persistência
# - Adicionar testes unitários com casos claros
