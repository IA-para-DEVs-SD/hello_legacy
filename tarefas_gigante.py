"""
Gerenciador de Tarefas - Refatorado com princípios SOLID

S - Single Responsibility: Tarefa, GerenciadorTarefas, JsonTarefaRepository e MenuCLI
    têm responsabilidades únicas e bem definidas.
O - Open/Closed: Novos comandos podem ser adicionados sem modificar MenuCLI.
    Novo storage basta implementar TarefaRepository.
L - Liskov Substitution: JsonTarefaRepository pode ser trocado por qualquer
    implementação de TarefaRepository sem quebrar o sistema.
I - Interface Segregation: TarefaRepository expõe apenas o contrato necessário.
D - Dependency Inversion: GerenciadorTarefas depende da abstração TarefaRepository,
    não de uma implementação concreta.
"""

from __future__ import annotations

import json
import os
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Callable, Optional


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Prioridade(Enum):
    BAIXA = "1"
    MEDIA = "2"
    ALTA  = "3"

    @classmethod
    def from_valor(cls, valor: str) -> "Prioridade":
        for membro in cls:
            if membro.value == valor:
                return membro
        raise ValueError(f"Prioridade inválida: '{valor}'. Use 1, 2 ou 3.")

    def __str__(self) -> str:
        return self.name


# ---------------------------------------------------------------------------
# Entidade  (SRP: só representa dados de uma tarefa + validações básicas)
# ---------------------------------------------------------------------------

@dataclass
class Tarefa:
    titulo: str
    descricao: str
    prioridade: Prioridade
    concluida: bool = False

    def __post_init__(self) -> None:
        if not self.titulo.strip():
            raise ValueError("Título não pode ser vazio.")

    def concluir(self) -> None:
        self.concluida = True

    def atualizar(
        self,
        titulo: Optional[str] = None,
        descricao: Optional[str] = None,
        prioridade: Optional[Prioridade] = None,
    ) -> None:
        if titulo:
            self.titulo = titulo
        if descricao:
            self.descricao = descricao
        if prioridade:
            self.prioridade = prioridade

    # helpers de serialização
    def to_dict(self) -> dict:
        d = asdict(self)
        d["prioridade"] = self.prioridade.value
        return d

    @classmethod
    def from_dict(cls, dados: dict) -> "Tarefa":
        return cls(
            titulo=dados["titulo"],
            descricao=dados["descricao"],
            prioridade=Prioridade.from_valor(dados["prioridade"]),
            concluida=dados.get("concluida", False),
        )


# ---------------------------------------------------------------------------
# Repository  (DIP: abstração que o gerenciador depende)
# ---------------------------------------------------------------------------

class TarefaRepository(ABC):
    """Interface de persistência — qualquer storage implementa isso."""

    @abstractmethod
    def salvar(self, tarefas: list[Tarefa]) -> None: ...

    @abstractmethod
    def carregar(self) -> list[Tarefa]: ...


class JsonTarefaRepository(TarefaRepository):
    """Implementação concreta: persiste em JSON. (OCP: troque sem mexer no resto)"""

    ARQUIVO_PADRAO = "tarefas.json"

    def __init__(self, caminho: str = ARQUIVO_PADRAO) -> None:
        self._caminho = caminho

    def salvar(self, tarefas: list[Tarefa]) -> None:
        with open(self._caminho, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in tarefas], f, ensure_ascii=False, indent=2)

    def carregar(self) -> list[Tarefa]:
        if not os.path.exists(self._caminho):
            raise FileNotFoundError(f"Arquivo '{self._caminho}' não encontrado.")
        with open(self._caminho, "r", encoding="utf-8") as f:
            return [Tarefa.from_dict(d) for d in json.load(f)]


# ---------------------------------------------------------------------------
# Gerenciador  (SRP: lógica de negócio; DIP: usa abstração do repository)
# ---------------------------------------------------------------------------

class GerenciadorTarefas:
    """Orquestra operações sobre tarefas. Não sabe nada de UI nem de storage."""

    def __init__(self, repository: TarefaRepository) -> None:
        self._repository = repository
        self._tarefas: list[Tarefa] = []

    # --- CRUD ---------------------------------------------------------------

    def adicionar(self, titulo: str, descricao: str, prioridade: Prioridade) -> Tarefa:
        tarefa = Tarefa(titulo=titulo, descricao=descricao, prioridade=prioridade)
        self._tarefas.append(tarefa)
        return tarefa

    def listar(self, prioridade: Optional[Prioridade] = None) -> list[tuple[int, Tarefa]]:
        tarefas = self._tarefas
        if prioridade:
            tarefas = [t for t in tarefas if t.prioridade == prioridade]
        return list(enumerate(tarefas, start=1))

    def buscar_por_indice(self, indice: int) -> Tarefa:
        """indice começa em 1 (como exibido ao usuário)."""
        if not (1 <= indice <= len(self._tarefas)):
            raise IndexError(f"Índice {indice} fora do intervalo.")
        return self._tarefas[indice - 1]

    def concluir(self, indice: int) -> Tarefa:
        tarefa = self.buscar_por_indice(indice)
        tarefa.concluir()
        return tarefa

    def editar(
        self,
        indice: int,
        titulo: Optional[str] = None,
        descricao: Optional[str] = None,
        prioridade: Optional[Prioridade] = None,
    ) -> Tarefa:
        tarefa = self.buscar_por_indice(indice)
        tarefa.atualizar(titulo=titulo, descricao=descricao, prioridade=prioridade)
        return tarefa

    def deletar(self, indice: int) -> Tarefa:
        tarefa = self.buscar_por_indice(indice)
        self._tarefas.pop(indice - 1)
        return tarefa

    # --- Persistência -------------------------------------------------------

    def salvar(self) -> None:
        self._repository.salvar(self._tarefas)

    def carregar(self) -> None:
        self._tarefas = self._repository.carregar()

    @property
    def total(self) -> int:
        return len(self._tarefas)


# ---------------------------------------------------------------------------
# Comandos  (OCP + SRP: cada operação de menu é uma classe independente)
# ---------------------------------------------------------------------------

class Comando(ABC):
    """Interface base para todos os comandos do menu."""

    @property
    @abstractmethod
    def descricao(self) -> str: ...

    @abstractmethod
    def executar(self, gerenciador: GerenciadorTarefas) -> None: ...


# helpers de UI reutilizáveis (ISP: funções pequenas e focadas)

def _formatar_tarefa(indice: int, tarefa: Tarefa) -> str:
    status = "[X]" if tarefa.concluida else "[ ]"
    return f"{indice:>2}. {status} {tarefa.titulo} [{tarefa.prioridade}]\n     {tarefa.descricao}"


def _exibir_lista(pares: list[tuple[int, Tarefa]]) -> None:
    if not pares:
        print("  Nenhuma tarefa encontrada.")
        return
    for indice, tarefa in pares:
        print(_formatar_tarefa(indice, tarefa))


def _ler_indice(gerenciador: GerenciadorTarefas, prompt: str = "Número da tarefa: ") -> Optional[int]:
    try:
        return int(input(prompt))
    except ValueError:
        print("  Entrada inválida — informe um número.")
        return None


def _ler_prioridade(prompt: str = "Prioridade (1-baixa, 2-media, 3-alta): ") -> Optional[Prioridade]:
    try:
        return Prioridade.from_valor(input(prompt).strip())
    except ValueError as exc:
        print(f"  {exc}")
        return None


class ComandoAdicionar(Comando):
    descricao = "Adicionar tarefa"

    def executar(self, gerenciador: GerenciadorTarefas) -> None:
        titulo    = input("Título: ").strip()
        descricao = input("Descrição: ").strip()
        prioridade = _ler_prioridade()
        if not prioridade:
            return
        try:
            tarefa = gerenciador.adicionar(titulo, descricao, prioridade)
            print(f"  Tarefa '{tarefa.titulo}' adicionada.")
        except ValueError as exc:
            print(f"  Erro: {exc}")


class ComandoListar(Comando):
    descricao = "Listar tarefas"

    def executar(self, gerenciador: GerenciadorTarefas) -> None:
        _exibir_lista(gerenciador.listar())


class ComandoConcluir(Comando):
    descricao = "Marcar como concluída"

    def executar(self, gerenciador: GerenciadorTarefas) -> None:
        _exibir_lista(gerenciador.listar())
        indice = _ler_indice(gerenciador)
        if indice is None:
            return
        try:
            tarefa = gerenciador.concluir(indice)
            print(f"  '{tarefa.titulo}' marcada como concluída.")
        except IndexError as exc:
            print(f"  {exc}")


class ComandoDeletar(Comando):
    descricao = "Deletar tarefa"

    def executar(self, gerenciador: GerenciadorTarefas) -> None:
        _exibir_lista(gerenciador.listar())
        indice = _ler_indice(gerenciador)
        if indice is None:
            return
        try:
            confirmacao = input(f"  Confirmar exclusão? (s/N): ").strip().lower()
            if confirmacao != "s":
                print("  Cancelado.")
                return
            tarefa = gerenciador.deletar(indice)
            print(f"  '{tarefa.titulo}' deletada.")
        except IndexError as exc:
            print(f"  {exc}")


class ComandoEditar(Comando):
    descricao = "Editar tarefa"

    def executar(self, gerenciador: GerenciadorTarefas) -> None:
        _exibir_lista(gerenciador.listar())
        indice = _ler_indice(gerenciador)
        if indice is None:
            return
        try:
            tarefa = gerenciador.buscar_por_indice(indice)
        except IndexError as exc:
            print(f"  {exc}")
            return

        titulo    = input(f"  Título [{tarefa.titulo}]: ").strip() or None
        descricao = input(f"  Descrição [{tarefa.descricao}]: ").strip() or None
        prio_raw  = input(f"  Prioridade [{tarefa.prioridade}] (enter para manter): ").strip()
        prioridade: Optional[Prioridade] = None
        if prio_raw:
            try:
                prioridade = Prioridade.from_valor(prio_raw)
            except ValueError as exc:
                print(f"  {exc}")
                return

        gerenciador.editar(indice, titulo=titulo, descricao=descricao, prioridade=prioridade)
        print("  Tarefa atualizada.")


class ComandoFiltrar(Comando):
    descricao = "Filtrar por prioridade"

    def executar(self, gerenciador: GerenciadorTarefas) -> None:
        prioridade = _ler_prioridade()
        if not prioridade:
            return
        _exibir_lista(gerenciador.listar(prioridade=prioridade))


class ComandoSalvar(Comando):
    descricao = "Salvar em arquivo"

    def executar(self, gerenciador: GerenciadorTarefas) -> None:
        try:
            gerenciador.salvar()
            print("  Tarefas salvas.")
        except OSError as exc:
            print(f"  Erro ao salvar: {exc}")


class ComandoCarregar(Comando):
    descricao = "Carregar de arquivo"

    def executar(self, gerenciador: GerenciadorTarefas) -> None:
        if gerenciador.total > 0:
            confirmacao = input("  Isso substituirá as tarefas atuais. Continuar? (s/N): ").strip().lower()
            if confirmacao != "s":
                print("  Cancelado.")
                return
        try:
            gerenciador.carregar()
            print(f"  {gerenciador.total} tarefa(s) carregada(s).")
        except (FileNotFoundError, ValueError) as exc:
            print(f"  Erro ao carregar: {exc}")


# ---------------------------------------------------------------------------
# UI / Menu  (SRP: só cuida de apresentação e roteamento de comandos)
# ---------------------------------------------------------------------------

class MenuCLI:
    """
    Registra comandos dinamicamente — adicionar um novo comando não exige
    modificar esta classe (OCP).
    """

    SEPARADOR = "=" * 50

    def __init__(self, gerenciador: GerenciadorTarefas) -> None:
        self._gerenciador = gerenciador
        self._comandos: dict[str, Comando] = {}
        self._registrar_comandos_padrao()

    def _registrar_comandos_padrao(self) -> None:
        comandos = [
            ComandoAdicionar(),
            ComandoListar(),
            ComandoConcluir(),
            ComandoDeletar(),
            ComandoEditar(),
            ComandoFiltrar(),
            ComandoSalvar(),
            ComandoCarregar(),
        ]
        for i, comando in enumerate(comandos, start=1):
            self._comandos[str(i)] = comando

    def registrar(self, tecla: str, comando: Comando) -> None:
        """Permite estender o menu sem modificar esta classe (OCP)."""
        self._comandos[tecla] = comando

    def _exibir_menu(self) -> None:
        print(f"\n{self.SEPARADOR}")
        print("  GERENCIADOR DE TAREFAS")
        print(self.SEPARADOR)
        for tecla, comando in self._comandos.items():
            print(f"  {tecla} - {comando.descricao}")
        print("  0 - Sair")
        print(self.SEPARADOR)

    def executar(self) -> None:
        while True:
            self._exibir_menu()
            opcao = input("Opção: ").strip()

            if opcao == "0":
                print("Até logo!")
                break
            elif opcao in self._comandos:
                self._comandos[opcao].executar(self._gerenciador)
            else:
                print("  Opção inválida.")


# ---------------------------------------------------------------------------
# Entry point  (DIP: injeta dependências concretas aqui, na borda do sistema)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    repository  = JsonTarefaRepository()
    gerenciador = GerenciadorTarefas(repository)
    menu        = MenuCLI(gerenciador)
    menu.executar()
