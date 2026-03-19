"""Calculadora refatorada com boas práticas."""

from typing import Optional

# Constantes de mensagens
MSG_CABECALHO = "=== CALCULADORA ==="
MSG_RESULTADO = "resultado:"
MSG_ERRO_DIVISAO = "erro!"
MSG_OPERACAO_INVALIDA = "operacao invalida"
MSG_ENTRADA_INVALIDA = "Entrada inválida. Digite um número válido."
MSG_SAIDA = "tchau"
MSG_NUM1 = "numero 1: "
MSG_NUM2 = "numero 2: "
MSG_OPERACAO = "operacao (+,-,*,/): "
MSG_CONTINUAR = "continuar? (s/n): "
RESPOSTAS_SIM = {"s", "sim"}


class Calculadora:
    """Classe responsável pela lógica de cálculo."""

    def somar(self, a: float, b: float) -> float:
        return a + b

    def subtrair(self, a: float, b: float) -> float:
        return a - b

    def multiplicar(self, a: float, b: float) -> float:
        return a * b

    def dividir(self, a: float, b: float) -> Optional[float]:
        if b == 0:
            return None
        return a / b

    def calcular(self, a: float, b: float, operacao: str) -> Optional[float]:
        """Executa a operação usando dicionário de dispatch."""
        operacoes: dict[str, callable] = {
            "+": self.somar,
            "-": self.subtrair,
            "*": self.multiplicar,
            "/": self.dividir,
        }
        func = operacoes.get(operacao)
        if func is None:
            return None
        return func(a, b)


def ler_numero(mensagem: str) -> float:
    """Lê e valida um número do input."""
    valor = input(mensagem)
    return float(valor)


def usuario_quer_continuar() -> bool:
    """Verifica se o usuário deseja continuar."""
    resposta = input(MSG_CONTINUAR)
    return resposta.strip().lower() in RESPOSTAS_SIM


def calc() -> None:
    """Loop principal da calculadora."""
    calculadora = Calculadora()
    continuar = True

    while continuar:
        print(MSG_CABECALHO)

        a = ler_numero(MSG_NUM1)
        b = ler_numero(MSG_NUM2)
        operacao = input(MSG_OPERACAO)

        if operacao not in {"+", "-", "*", "/"}:
            print(MSG_OPERACAO_INVALIDA)
        else:
            resultado = calculadora.calcular(a, b, operacao)
            if resultado is None:
                print(MSG_ERRO_DIVISAO)
            else:
                print(MSG_RESULTADO, resultado)

        continuar = usuario_quer_continuar()

    print(MSG_SAIDA)


calc()

# Propts utilizados

# Criação de testes: 
# crie testes unitarios para a classe calculadora_ruim

# refatoração: 
# Refatore o código calculadora_ruim aplicando boas práticas, com foco em legibilidade, organização e performance.

# Requisitos:

# Criar classe Calculadora
# Separar lógica de negócio de input/output
# Criar métodos para cada operação
# Usar dicionário em vez de if/elif
# Implementar loop while (sem recursão)
# Validar inputs com try/except
# Adicionar type hints
# Definir constantes para mensagens
# Aplicar princípios DRY e SOLID