import json
import os
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional

ARQUIVO_PADRAO = "tarefas.json"

MENU = """
==================================================
GERENCIADOR DE TAREFAS
==================================================
1 - adicionar tarefa
2 - listar tarefas
3 - marcar como feita
4 - deletar tarefa
5 - editar tarefa
6 - filtrar por prioridade
7 - salvar em arquivo
8 - carregar de arquivo
0 - sair
=================================================="""


class Prioridade(str, Enum):
    BAIXA = "1"
    MEDIA = "2"
    ALTA  = "3"

    @property
    def label(self) -> str:
        return self.name

    @classmethod
    def valida(cls, valor: str) -> bool:
        return valor in {p.value for p in cls}


@dataclass
class Tarefa:
    titulo: str
    desc: str
    prio: str
    feita: bool = False

    @property
    def status(self) -> str:
        return "[X]" if self.feita else "[ ]"

    @property
    def prioridade_label(self) -> str:
        try:
            return Prioridade(self.prio).label
        except ValueError:
            return "???"

    def exibir(self, numero: int, mostrar_desc: bool = True) -> None:
        print(f"{numero}. {self.status} {self.titulo} - {self.prioridade_label}")
        if mostrar_desc:
            print(f"   {self.desc}")

    @classmethod
    def from_dict(cls, dados: dict) -> "Tarefa":
        return cls(**dados)

    def to_dict(self) -> dict:
        return asdict(self)


class GerenciadorTarefas:
    def __init__(self) -> None:
        self.tarefas: list[Tarefa] = []

    # --- helpers internos ---

    def _listar_resumido(self) -> None:
        for i, tarefa in enumerate(self.tarefas, start=1):
            print(f"{i}. {tarefa.status} {tarefa.titulo}")

    def _selecionar_indice(self, prompt: str = "numero da tarefa: ") -> Optional[int]:
        entrada = input(prompt)
        try:
            idx = int(entrada) - 1
        except ValueError:
            print("entrada invalida")
            return None
        if not (0 <= idx < len(self.tarefas)):
            print("numero fora do intervalo")
            return None
        return idx

    def _requer_tarefas(self) -> bool:
        if not self.tarefas:
            print("nenhuma tarefa")
            return False
        return True

    # --- operações de negócio ---

    def adicionar(self) -> None:
        titulo = input("titulo: ").strip()
        desc   = input("descricao: ").strip()
        prio   = input("prioridade (1-baixa, 2-media, 3-alta): ").strip()

        if not titulo:
            print("titulo nao pode ser vazio")
            return
        if not Prioridade.valida(prio):
            print("prioridade invalida, use 1, 2 ou 3")
            return

        self.tarefas.append(Tarefa(titulo=titulo, desc=desc, prio=prio))
        print("tarefa adicionada!")

    def listar(self) -> None:
        if not self._requer_tarefas():
            return
        for i, tarefa in enumerate(self.tarefas, start=1):
            tarefa.exibir(i, mostrar_desc=True)

    def marcar_feita(self) -> None:
        if not self._requer_tarefas():
            return
        self._listar_resumido()
        idx = self._selecionar_indice()
        if idx is None:
            return
        self.tarefas[idx].feita = True
        print("marcada como feita!")

    def deletar(self) -> None:
        if not self._requer_tarefas():
            return
        self._listar_resumido()
        idx = self._selecionar_indice()
        if idx is None:
            return
        confirmacao = input(f"deletar '{self.tarefas[idx].titulo}'? (s/n): ").strip().lower()
        if confirmacao == "s":
            self.tarefas.pop(idx)
            print("deletada!")
        else:
            print("cancelado")

    def editar(self) -> None:
        if not self._requer_tarefas():
            return
        self._listar_resumido()
        idx = self._selecionar_indice()
        if idx is None:
            return

        tarefa = self.tarefas[idx]
        campos = [
            ("titulo", "novo titulo"),
            ("desc",   "nova desc"),
            ("prio",   "nova prio"),
        ]
        for atributo, prompt in campos:
            atual = getattr(tarefa, atributo)
            novo  = input(f"{prompt} (atual: '{atual}', enter para manter): ").strip()
            if novo:
                if atributo == "prio" and not Prioridade.valida(novo):
                    print("prioridade invalida, mantendo valor atual")
                    continue
                setattr(tarefa, atributo, novo)

        print("atualizada!")

    def filtrar_por_prioridade(self) -> None:
        prio = input("prioridade (1/2/3): ").strip()
        resultado = [
            (i + 1, tarefa)
            for i, tarefa in enumerate(self.tarefas)
            if tarefa.prio == prio
        ]
        if not resultado:
            print("nenhuma tarefa com essa prioridade")
            return
        for numero, tarefa in resultado:
            tarefa.exibir(numero, mostrar_desc=False)

    def salvar(self, arquivo: str = ARQUIVO_PADRAO) -> None:
        try:
            with open(arquivo, "w", encoding="utf-8") as f:
                json.dump([t.to_dict() for t in self.tarefas], f, ensure_ascii=False, indent=2)
            print(f"salvo em {arquivo}")
        except OSError as e:
            print(f"erro ao salvar: {e}")

    def carregar(self, arquivo: str = ARQUIVO_PADRAO) -> None:
        if not os.path.exists(arquivo):
            print("arquivo nao existe")
            return
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
            self.tarefas = [Tarefa.from_dict(d) for d in dados]
            print("carregado!")
        except (OSError, json.JSONDecodeError, TypeError) as e:
            print(f"erro ao carregar: {e}")


def sistema_tarefas() -> None:
    gerenciador = GerenciadorTarefas()

    acoes = {
        "1": gerenciador.adicionar,
        "2": gerenciador.listar,
        "3": gerenciador.marcar_feita,
        "4": gerenciador.deletar,
        "5": gerenciador.editar,
        "6": gerenciador.filtrar_por_prioridade,
        "7": gerenciador.salvar,
        "8": gerenciador.carregar,
    }

    while True:
        print(MENU)
        opcao = input("opcao: ").strip()

        if opcao == "0":
            print("tchau!")
            break
        elif opcao in acoes:
            acoes[opcao]()
        else:
            print("opcao invalida")


if __name__ == "__main__":
    sistema_tarefas()
