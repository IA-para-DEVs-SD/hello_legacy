def processar(data):
    r = []

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
            r.append(processar(item))
        else:
            r.append(None)

    return r


def calc(x, y, z=1):
    if z == 1:
        return (x + y) * z if x > y else (x - y) / z if x < y else x * y * z
    elif z == 2:
        return x ** y if x > 0 and y > 0 else x + y if x < 0 else y - x
    else:
        return ((x + y) * z - x) / (y if y != 0 else 1) + z


def validar_e_processar_e_salvar(dados, arquivo=None, modo=1):
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
        resultado = [d for d in dados if d]
    else:
        resultado = dados

    if arquivo:
        with open(arquivo, "w") as f:
            f.write(str(resultado))

    return resultado


def categorizar(valor):
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
            return categorizar(int(valor))
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


class Processador:
    def __init__(self, x, y=None, z=None, modo=1, ativo=True):
        self.x = x
        self.y = y if y else x * 2
        self.z = z if z else self.y * 3
        self.m = modo
        self.a = ativo
        self.r = []

    def proc(self, data):
        if not self.a:
            return None

        if self.m == 1:
            self.r = [d * self.x for d in data]
        elif self.m == 2:
            self.r = [d + self.y for d in data]
        else:
            self.r = [d * self.z for d in data]

        return self.r

    def get_r(self):
        return self.r

    def set_m(self, m):
        self.m = m


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
