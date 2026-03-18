import hashlib
import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Usuario:
    nome: str
    idade: int
    email: str
    _senha_hash: str = field(repr=False)
    ativo: bool = True

    def __str__(self) -> str:
        status = "ativo" if self.ativo else "inativo"
        return f"{self.nome} | {self.idade} anos | {self.email} | {status}"

    def __repr__(self) -> str:
        return f"Usuario(nome={self.nome!r}, idade={self.idade}, email={self.email!r})"


class ValidacaoError(Exception):
    pass


def _hash_senha(senha: str) -> str:
    if len(senha) < 8:
        raise ValidacaoError("Senha deve ter no mínimo 8 caracteres.")
    return hashlib.sha256(senha.encode()).hexdigest()


def _validar_idade(idade: int) -> None:
    if not (0 <= idade <= 120):
        raise ValidacaoError(f"Idade inválida: {idade}. Deve estar entre 0 e 120.")


def _validar_email(email: str) -> None:
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email):
        raise ValidacaoError(f"Email inválido: {email}")


class GerenciadorUsuarios:
    def __init__(self) -> None:
        self._usuarios: dict[str, Usuario] = {}

    def cadastrar(self, nome: str, idade: int, email: str, senha: str) -> Usuario:
        if nome in self._usuarios:
            raise ValidacaoError(f"Usuário '{nome}' já existe.")
        _validar_idade(idade)
        _validar_email(email)
        usuario = Usuario(
            nome=nome,
            idade=idade,
            email=email,
            _senha_hash=_hash_senha(senha),
        )
        self._usuarios[nome] = usuario
        return usuario

    def buscar(self, nome: str) -> Optional[Usuario]:
        return self._usuarios.get(nome)

    def _buscar_ou_erro(self, nome: str) -> Usuario:
        usuario = self.buscar(nome)
        if usuario is None:
            raise KeyError(f"Usuário '{nome}' não encontrado.")
        return usuario

    def atualizar_idade(self, nome: str, nova_idade: int) -> None:
        _validar_idade(nova_idade)
        self._buscar_ou_erro(nome).idade = nova_idade

    def atualizar_email(self, nome: str, novo_email: str) -> None:
        _validar_email(novo_email)
        self._buscar_ou_erro(nome).email = novo_email

    def desativar(self, nome: str) -> None:
        self._buscar_ou_erro(nome).ativo = False

    def listar_ativos(self) -> list[Usuario]:
        return [u for u in self._usuarios.values() if u.ativo]


if __name__ == "__main__":
    gerenciador = GerenciadorUsuarios()

    try:
        gerenciador.cadastrar("joao", 25, "joao@email.com", "senha_segura1")
        gerenciador.cadastrar("maria", 30, "maria@email.com", "senha_segura2")
        gerenciador.cadastrar("pedro", -5, "emailinvalido", "p")  # levanta ValidacaoError
    except ValidacaoError as e:
        print(f"Erro ao cadastrar: {e}")

    print("\n=== LISTA DE ATIVOS ===")
    for usuario in gerenciador.listar_ativos():
        print(usuario)

    print("\n=== BUSCA ===")
    usuario = gerenciador.buscar("joao")
    if usuario:
        print(usuario)

    try:
        gerenciador.atualizar_idade("maria", 999)  # levanta ValidacaoError
    except ValidacaoError as e:
        print(f"Erro ao atualizar: {e}")

    gerenciador.desativar("joao")
    print("\n=== LISTA APÓS DESATIVAR JOAO ===")
    for usuario in gerenciador.listar_ativos():
        print(usuario)
