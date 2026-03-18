from typing import Optional
import unittest

MSG_TITULO = "=== CALCULADORA ==="
MSG_RESULTADO = "Resultado: {}"
MSG_DIVISAO_ZERO = "Erro: divisão por zero não é permitida."
MSG_OPERACAO_INVALIDA = "Erro: operação inválida. Use +, -, * ou /."
MSG_NUMERO_INVALIDO = "Erro: entrada inválida. Digite um número válido."
MSG_CONTINUAR = "Continuar? (s/n): "
MSG_TCHAU = "Encerrando a calculadora. Até mais!"
MSG_OPCAO_INVALIDA = "Opção inválida. Digite 's' ou 'n'."


class Calculadora:
    def somar(self, a: float, b: float) -> float:
        return a + b

    def subtrair(self, a: float, b: float) -> float:
        return a - b

    def multiplicar(self, a: float, b: float) -> float:
        return a * b

    def dividir(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError(MSG_DIVISAO_ZERO)
        return a / b

    def calcular(self, a: float, b: float, operacao: str) -> float:
        operacoes = {
            "+": self.somar,
            "-": self.subtrair,
            "*": self.multiplicar,
            "/": self.dividir,
        }
        if operacao not in operacoes:
            raise ValueError(MSG_OPERACAO_INVALIDA)
        return operacoes[operacao](a, b)


def ler_numero(prompt: str) -> Optional[float]:
    try:
        return float(input(prompt))
    except ValueError:
        print(MSG_NUMERO_INVALIDO)
        return None


def ler_operacao() -> Optional[str]:
    operacao = input("Operação (+, -, *, /): ").strip()
    if operacao not in ("+", "-", "*", "/"):
        print(MSG_OPERACAO_INVALIDA)
        return None
    return operacao


def ler_continuar() -> bool:
    while True:
        resposta = input(MSG_CONTINUAR).strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print(MSG_OPCAO_INVALIDA)


def executar():
    calc = Calculadora()
    print(MSG_TITULO)

    while True:
        a = ler_numero("Número 1: ")
        if a is None:
            continue

        b = ler_numero("Número 2: ")
        if b is None:
            continue

        operacao = ler_operacao()
        if operacao is None:
            continue

        try:
            resultado = calc.calcular(a, b, operacao)
            print(MSG_RESULTADO.format(resultado))
        except ZeroDivisionError as e:
            print(e)

        if not ler_continuar():
            print(MSG_TCHAU)
            break


class TestCalculadora(unittest.TestCase):
    def setUp(self):
        self.calc = Calculadora()

    def test_somar(self):
        self.assertEqual(self.calc.somar(2, 3), 5)
        self.assertEqual(self.calc.somar(-1, 1), 0)

    def test_subtrair(self):
        self.assertEqual(self.calc.subtrair(5, 3), 2)
        self.assertEqual(self.calc.subtrair(0, 5), -5)

    def test_multiplicar(self):
        self.assertEqual(self.calc.multiplicar(3, 4), 12)
        self.assertEqual(self.calc.multiplicar(-2, 3), -6)

    def test_dividir(self):
        self.assertEqual(self.calc.dividir(10, 2), 5)
        self.assertAlmostEqual(self.calc.dividir(1, 3), 0.3333, places=4)

    def test_dividir_por_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calc.dividir(5, 0)

    def test_operacao_invalida(self):
        with self.assertRaises(ValueError):
            self.calc.calcular(1, 2, "%")

    def test_calcular_todas_operacoes(self):
        self.assertEqual(self.calc.calcular(4, 2, "+"), 6)
        self.assertEqual(self.calc.calcular(4, 2, "-"), 2)
        self.assertEqual(self.calc.calcular(4, 2, "*"), 8)
        self.assertEqual(self.calc.calcular(4, 2, "/"), 2)


if __name__ == "__main__":
    import sys
    if "--test" in sys.argv:
        sys.argv.remove("--test")
        unittest.main()
    else:
        executar()
