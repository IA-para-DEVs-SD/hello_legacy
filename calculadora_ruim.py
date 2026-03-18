from abc import ABC, abstractmethod


# ─── S: Single Responsibility ────────────────────────────────────────────────
# Cada classe tem uma única responsabilidade.

class Operacao(ABC):
    """Interface base para operações — OCP + LSP."""

    @abstractmethod
    def executar(self, a: float, b: float) -> float: ...

    @abstractmethod
    def simbolo(self) -> str: ...


# ─── O: Open/Closed ──────────────────────────────────────────────────────────
# Novas operações são adicionadas criando novas classes, sem alterar as existentes.

class Soma(Operacao):
    def executar(self, a: float, b: float) -> float:
        return a + b

    def simbolo(self) -> str:
        return "+"


class Subtracao(Operacao):
    def executar(self, a: float, b: float) -> float:
        return a - b

    def simbolo(self) -> str:
        return "-"


class Multiplicacao(Operacao):
    def executar(self, a: float, b: float) -> float:
        return a * b

    def simbolo(self) -> str:
        return "*"


class Divisao(Operacao):
    def executar(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Divisão por zero não é permitida.")
        return a / b

    def simbolo(self) -> str:
        return "/"


# ─── D: Dependency Inversion ─────────────────────────────────────────────────
# Calculadora depende da abstração Operacao, não de implementações concretas.

class Calculadora:
    """Executa operações registradas. Não sabe nada de I/O."""

    def __init__(self) -> None:
        self._operacoes: dict[str, Operacao] = {}

    def registrar(self, operacao: Operacao) -> None:
        self._operacoes[operacao.simbolo()] = operacao

    def calcular(self, simbolo: str, a: float, b: float) -> float:
        if simbolo not in self._operacoes:
            raise KeyError(f"Operação '{simbolo}' não suportada.")
        return self._operacoes[simbolo].executar(a, b)

    def operacoes_disponiveis(self) -> list[str]:
        return list(self._operacoes.keys())


# ─── I: Interface Segregation ────────────────────────────────────────────────
# Leitor e Exibidor são interfaces separadas; nenhum cliente é forçado a
# depender de métodos que não usa.

class LeitorEntrada(ABC):
    @abstractmethod
    def ler_numero(self, mensagem: str) -> float: ...

    @abstractmethod
    def ler_operacao(self, opcoes: list[str]) -> str: ...

    @abstractmethod
    def ler_continuar(self) -> bool: ...


class ExibidorResultado(ABC):
    @abstractmethod
    def mostrar_resultado(self, resultado: float) -> None: ...

    @abstractmethod
    def mostrar_erro(self, mensagem: str) -> None: ...

    @abstractmethod
    def mostrar_boas_vindas(self) -> None: ...

    @abstractmethod
    def mostrar_despedida(self) -> None: ...


# ─── L: Liskov Substitution ──────────────────────────────────────────────────
# ConsoleLeitor e ConsoleExibidor podem substituir suas abstrações sem quebrar
# o comportamento esperado.

class ConsoleLeitor(LeitorEntrada):
    def ler_numero(self, mensagem: str) -> float:
        while True:
            try:
                return float(input(mensagem))
            except ValueError:
                print("Entrada inválida. Digite um número.")

    def ler_operacao(self, opcoes: list[str]) -> str:
        opcoes_str = "/".join(opcoes)
        while True:
            op = input(f"Operação ({opcoes_str}): ").strip()
            if op in opcoes:
                return op
            print(f"Operação inválida. Escolha entre: {opcoes_str}")

    def ler_continuar(self) -> bool:
        resposta = input("Continuar? (s/n): ").strip().lower()
        return resposta in ("s", "sim")


class ConsoleExibidor(ExibidorResultado):
    def mostrar_resultado(self, resultado: float) -> None:
        print(f"Resultado: {resultado}")

    def mostrar_erro(self, mensagem: str) -> None:
        print(f"Erro: {mensagem}")

    def mostrar_boas_vindas(self) -> None:
        print("=== CALCULADORA ===")

    def mostrar_despedida(self) -> None:
        print("Tchau!")


# ─── Orquestrador ────────────────────────────────────────────────────────────

class AplicacaoCalculadora:
    def __init__(
        self,
        calculadora: Calculadora,
        leitor: LeitorEntrada,
        exibidor: ExibidorResultado,
    ) -> None:
        self._calc = calculadora
        self._leitor = leitor
        self._exibidor = exibidor

    def executar(self) -> None:
        self._exibidor.mostrar_boas_vindas()
        while True:
            a = self._leitor.ler_numero("Número 1: ")
            b = self._leitor.ler_numero("Número 2: ")
            op = self._leitor.ler_operacao(self._calc.operacoes_disponiveis())

            try:
                resultado = self._calc.calcular(op, a, b)
                self._exibidor.mostrar_resultado(resultado)
            except (ValueError, KeyError) as e:
                self._exibidor.mostrar_erro(str(e))

            if not self._leitor.ler_continuar():
                break

        self._exibidor.mostrar_despedida()


# ─── Composição e execução ───────────────────────────────────────────────────

if __name__ == "__main__":
    calc = Calculadora()
    for op in (Soma(), Subtracao(), Multiplicacao(), Divisao()):
        calc.registrar(op)

    app = AplicacaoCalculadora(calc, ConsoleLeitor(), ConsoleExibidor())
    app.executar()
