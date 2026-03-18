from abc import ABC, abstractmethod


# ─── PASSO 1: Interface base + implementações por tipo ───────────────────────
# O — Open/Closed: novas implementações não alteram as existentes
# L — Liskov: qualquer ProcessadorTipo pode substituir a abstração
# I — Interface Segregation: interface mínima com apenas 2 métodos

class ProcessadorTipo(ABC):
    """Define o contrato para processamento de um tipo específico de valor."""

    @abstractmethod
    def aceita(self, valor: object) -> bool:
        """Retorna True se este processador é responsável pelo tipo do valor."""
        ...

    @abstractmethod
    def processar(self, valor: object) -> object:
        """Aplica a transformação e retorna o resultado."""
        ...


class ProcessadorInt(ProcessadorTipo):
    """
    Regras para inteiros:
    - positivo + par  + < 100  → valor * 2
    - positivo + par  + >= 100 → valor * 3
    - positivo + ímpar + < 50  → valor + 10
    - positivo + ímpar + >= 50 → valor - 10
    - negativo + par           → abs(valor)
    - negativo + ímpar         → 0
    """

    def aceita(self, valor: object) -> bool:
        return isinstance(valor, int) and not isinstance(valor, bool)

    def processar(self, valor: int) -> int:
        if valor > 0:
            return self._processar_positivo(valor)
        return self._processar_negativo(valor)

    def _processar_positivo(self, valor: int) -> int:
        if valor % 2 == 0:
            return valor * 2 if valor < 100 else valor * 3
        return valor + 10 if valor < 50 else valor - 10

    def _processar_negativo(self, valor: int) -> int:
        return abs(valor) if valor % 2 == 0 else 0


class ProcessadorStr(ProcessadorTipo):
    """
    Regras para strings:
    - len > 5 + começa maiúscula → lower()
    - len > 5 + começa minúscula → upper()
    - len <= 5 + só dígitos      → int(valor) * 5
    - len <= 5 + outros          → valor invertido
    """

    def aceita(self, valor: object) -> bool:
        return isinstance(valor, str)

    def processar(self, valor: str) -> object:
        if len(valor) > 5:
            return valor.lower() if valor[0].isupper() else valor.upper()
        return int(valor) * 5 if valor.isdigit() else valor[::-1]


class ProcessadorLista(ProcessadorTipo):
    """Processa listas recursivamente usando o pipeline principal."""

    def __init__(self, pipeline: "PipelineProcessamento") -> None:
        self._pipeline = pipeline

    def aceita(self, valor: object) -> bool:
        return isinstance(valor, list)

    def processar(self, valor: list) -> list:
        return self._pipeline.executar(valor)


# ─── PASSO 2: Enum + Validador + Transformador ───────────────────────────────
# S — Single Responsibility: cada classe tem uma única razão para mudar
# Magic numbers substituídos por Enum legível

from enum import Enum, auto


class ModoTransformacao(Enum):
    """Substitui os magic numbers modo=1, modo=2, modo=3."""
    DOBRAR   = auto()  # multiplica por 2
    FILTRAR  = auto()  # remove valores falsy
    PASSAGEM = auto()  # retorna sem alteração


class Validador:
    """Responsabilidade única: verificar se os dados de entrada são válidos."""

    def validar(self, dados: object) -> bool:
        if not dados:
            return False
        if not isinstance(dados, (list, tuple)):
            return False
        return True


class Transformador:
    """Responsabilidade única: aplicar uma transformação a uma coleção de dados."""

    _transformacoes = {
        ModoTransformacao.DOBRAR: lambda d: [
            v * 2 if isinstance(v, (int, float))
            else v.upper() if isinstance(v, str)
            else v
            for v in d
        ],
        ModoTransformacao.FILTRAR:  lambda d: [v for v in d if v],
        ModoTransformacao.PASSAGEM: lambda d: list(d),
    }

    def transformar(self, dados: list, modo: ModoTransformacao) -> list:
        transformacao = self._transformacoes.get(modo)
        if transformacao is None:
            raise ValueError(f"Modo desconhecido: {modo}")
        return transformacao(dados)


# ─── PASSO 3: Persistidor ────────────────────────────────────────────────────
# S — Single Responsibility: persistência isolada do processamento
# D — Dependency Inversion: código de alto nível depende da abstração,
#     não de open() diretamente
# O — Open/Closed: para salvar em banco ou JSON, basta nova implementação


class Persistidor(ABC):
    """Interface de persistência — desacopla o destino do dado processado."""

    @abstractmethod
    def salvar(self, dados: list, destino: str) -> None: ...


class PersistidorArquivo(Persistidor):
    """Salva o resultado em um arquivo de texto com tratamento de exceção."""

    def salvar(self, dados: list, destino: str) -> None:
        try:
            with open(destino, "w", encoding="utf-8") as arquivo:
                arquivo.write(str(dados))
        except OSError as e:
            raise RuntimeError(f"Falha ao salvar em '{destino}': {e}") from e


# ─── PASSO 4: Processador refatorado ─────────────────────────────────────────
# S — Single Responsibility: só aplica multiplicadores sobre uma coleção
# Magic numbers m=1/2/3 substituídos por ModoProcessamento
# Atributos nomeados: fator_x, fator_y, fator_z, modo, ativo, resultados


class ModoProcessamento(Enum):
    """Substitui os magic numbers 1, 2, 3 do método proc() original."""
    FATOR_X = auto()  # multiplica cada item por fator_x
    FATOR_Y = auto()  # soma fator_y a cada item
    FATOR_Z = auto()  # multiplica cada item por fator_z


class Processador:
    """Aplica um fator numérico a uma coleção conforme o modo configurado."""

    def __init__(
        self,
        fator_x: float,
        fator_y: float | None = None,
        fator_z: float | None = None,
        modo: ModoProcessamento = ModoProcessamento.FATOR_X,
        ativo: bool = True,
    ) -> None:
        self.fator_x = fator_x
        self.fator_y = fator_y if fator_y is not None else fator_x * 2
        self.fator_z = fator_z if fator_z is not None else self.fator_y * 3
        self.modo = modo
        self.ativo = ativo
        self.resultados: list = []

    def processar(self, dados: list) -> list | None:
        if not self.ativo:
            return None

        operacoes = {
            ModoProcessamento.FATOR_X: lambda d: [v * self.fator_x for v in d],
            ModoProcessamento.FATOR_Y: lambda d: [v + self.fator_y for v in d],
            ModoProcessamento.FATOR_Z: lambda d: [v * self.fator_z for v in d],
        }

        self.resultados = operacoes[self.modo](dados)
        return self.resultados

    @property
    def ultimo_resultado(self) -> list:
        return self.resultados

    def alterar_modo(self, novo_modo: ModoProcessamento) -> None:
        self.modo = novo_modo


# ─── PASSO 5: PipelineProcessamento + categorizar + testes ───────────────────
# D — Dependency Inversion: pipeline depende de abstrações injetadas
# S — Single Responsibility: orquestra sem conter lógica de negócio


class PipelineProcessamento:
    """
    Orquestra o processamento delegando cada valor ao ProcessadorTipo correto.
    Recebe dependências via construtor — nunca instancia concretos internamente.
    """

    def __init__(self, processadores: list[ProcessadorTipo]) -> None:
        self._processadores = processadores

    def executar(self, dados: list) -> list:
        return [self._processar_item(item) for item in dados]

    def _processar_item(self, valor: object) -> object:
        for processador in self._processadores:
            if processador.aceita(valor):
                return processador.processar(valor)
        return None  # tipo não suportado → None (equivalente ao original)


# ─── categorizar refatorado ───────────────────────────────────────────────────
# Guard clauses substituem os ifs aninhados; isinstance() no lugar de type()

def categorizar(valor: object) -> str:
    if isinstance(valor, bool):
        return "desconhecido"

    if isinstance(valor, int):
        if valor < 0:   return "negativo"
        if valor == 0:  return "zero"
        if valor < 10:  return "pequeno"
        if valor < 100: return "medio"
        return "grande"

    if isinstance(valor, str):
        if valor.isdigit():
            return categorizar(int(valor))
        return "curto" if len(valor) < 5 else "longo"

    if isinstance(valor, list):
        if len(valor) == 0: return "vazio"
        return "poucos" if len(valor) < 5 else "muitos"

    return "desconhecido"


# ─── Testes equivalentes ao original ─────────────────────────────────────────

if __name__ == "__main__":
    # Monta o pipeline injetando os processadores (ProcessadorLista precisa do pipeline)
    pipeline = PipelineProcessamento.__new__(PipelineProcessamento)
    pipeline._processadores = [
        ProcessadorInt(),
        ProcessadorStr(),
        ProcessadorLista(pipeline),
    ]

    print("=== TESTE 1 ===")
    dados = [1, 2, -3, 4, "hello", "WORLD", "123", [5, 6]]
    print(pipeline.executar(dados))

    print("\n=== TESTE 2 ===")
    transformador = Transformador()
    validador = Validador()
    entrada = [1, 2, 3, "ok", None, 0]
    if validador.validar(entrada):
        print(transformador.transformar(entrada, ModoTransformacao.DOBRAR))
        print(transformador.transformar(entrada, ModoTransformacao.FILTRAR))
        print(transformador.transformar(entrada, ModoTransformacao.PASSAGEM))

    print("\n=== TESTE 3 ===")
    for v in [5, 150, "hello", [1, 2, 3]]:
        print(f"categorizar({v!r}) → {categorizar(v)}")

    print("\n=== TESTE 4 ===")
    p = Processador(fator_x=2, fator_y=4, fator_z=6, modo=ModoProcessamento.FATOR_X)
    print(p.processar([1, 2, 3, 4, 5]))
