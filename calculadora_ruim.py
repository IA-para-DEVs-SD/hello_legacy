"""Calculadora interativa com separação de responsabilidades."""

from typing import Callable


class Calculadora:
    """Encapsula as operações matemáticas da calculadora."""

    OPERACOES: dict[str, Callable[[float, float], float]] = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b,
    }

    def calcular(self, a: float, b: float, operacao: str) -> float:
        """Executa a operação entre dois números.

        Raises:
            ValueError: se a operação for inválida.
            ZeroDivisionError: se houver divisão por zero.
        """
        if operacao not in self.OPERACOES:
            raise ValueError(f"Operação inválida: '{operacao}'")
        if operacao == "/" and b == 0:
            raise ZeroDivisionError("Divisão por zero não é permitida.")
        return self.OPERACOES[operacao](a, b)


def ler_numero(prompt: str) -> float:
    """Lê e valida um número do usuário."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Entrada inválida. Digite um número.")


def ler_operacao() -> str:
    """Lê e valida a operação do usuário."""
    operacoes_validas = {"+", "-", "*", "/"}
    while True:
        op = input("Operação (+, -, *, /): ").strip()
        if op in operacoes_validas:
            return op
        print(f"Operação inválida. Escolha entre: {', '.join(operacoes_validas)}")


def continuar() -> bool:
    """Pergunta ao usuário se deseja continuar."""
    resposta = input("Continuar? (s/n): ").strip().lower()
    return resposta in {"s", "sim"}


def main() -> None:
    """Loop principal da calculadora."""
    calc = Calculadora()
    print("=== CALCULADORA ===")

    while True:
        a = ler_numero("Número 1: ")
        b = ler_numero("Número 2: ")
        operacao = ler_operacao()

        try:
            resultado = calc.calcular(a, b, operacao)
            print(f"Resultado: {resultado}")
        except ZeroDivisionError as e:
            print(f"Erro: {e}")

        if not continuar():
            print("Tchau!")
            break


if __name__ == "__main__":
    main()
