"""Calculadora com operações básicas."""

from typing import Callable


class Calculadora:
    """Calculadora que suporta operações aritméticas básicas."""

    def __init__(self) -> None:
        self._operacoes: dict[str, Callable[[float, float], float]] = {
            "+": self._somar,
            "-": self._subtrair,
            "*": self._multiplicar,
            "/": self._dividir,
        }

    @staticmethod
    def _somar(a: float, b: float) -> float:
        return a + b

    @staticmethod
    def _subtrair(a: float, b: float) -> float:
        return a - b

    @staticmethod
    def _multiplicar(a: float, b: float) -> float:
        return a * b

    @staticmethod
    def _dividir(a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Divisão por zero não é permitida.")
        return a / b

    @property
    def operacoes_disponiveis(self) -> str:
        return ",".join(self._operacoes)

    def calcular(self, a: float, b: float, operacao: str) -> float:
        """Executa a operação entre dois números."""
        if operacao not in self._operacoes:
            raise ValueError(f"Operação inválida: '{operacao}'. Use: {self.operacoes_disponiveis}")
        return self._operacoes[operacao](a, b)


def _ler_numero(prompt: str) -> float:
    """Lê e valida um número do usuário."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Entrada inválida. Digite um número.")


def _deseja_continuar() -> bool:
    """Pergunta se o usuário quer continuar."""
    resposta = input("Continuar? (s/n): ").strip().lower()
    return resposta in ("s", "sim")


def main() -> None:
    """Loop principal da calculadora."""
    calc = Calculadora()
    print("=== CALCULADORA ===")

    while True:
        a = _ler_numero("Número 1: ")
        b = _ler_numero("Número 2: ")
        operacao = input(f"Operação ({calc.operacoes_disponiveis}): ").strip()

        try:
            resultado = calc.calcular(a, b, operacao)
            print(f"Resultado: {resultado}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"Erro: {e}")

        if not _deseja_continuar():
            print("Tchau!")
            break


if __name__ == "__main__":
    main()
