"""Sistema de gerenciamento de usuários com boas práticas de programação."""

import hashlib
import logging
import re
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class ValidacaoError(Exception):
    """Exceção para erros de validação de dados."""


def _hash_senha(senha: str) -> str:
    """Gera hash SHA-256 da senha."""
    return hashlib.sha256(senha.encode()).hexdigest()


def _validar_email(email: str) -> str:
    padrao = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"
    if not re.match(padrao, email):
        raise ValidacaoError(f"Email inválido: {email}")
    return email


def _validar_idade(idade: int) -> int:
    if not (0 <= idade <= 150):
        raise ValidacaoError(f"Idade inválida: {idade}. Deve ser entre 0 e 150.")
    return idade


def _validar_senha(senha: str) -> str:
    if len(senha) < 6:
        raise ValidacaoError("Senha deve ter no mínimo 6 caracteres.")
    return senha


@dataclass
class Usuario:
    """Representa um usuário do sistema."""

    nome: str
    idade: int
    email: str
    ativo: bool = True
    _senha_hash: str = field(repr=False, default="")

    def __post_init__(self) -> None:
        self.idade = _validar_idade(self.idade)
        self.email = _validar_email(self.email)

    @property
    def senha_hash(self) -> str:
        return self._senha_hash

    @senha_hash.setter
    def senha_hash(self, senha: str) -> None:
        _validar_senha(senha)
        self._senha_hash = _hash_senha(senha)

    def verificar_senha(self, senha: str) -> bool:
        return self._senha_hash == _hash_senha(senha)

    def __str__(self) -> str:
        status = "ativo" if self.ativo else "inativo"
        return f"{self.nome} ({self.idade} anos) - {self.email} [{status}]"


class GerenciadorUsuarios:
    """Gerencia operações CRUD de usuários."""

    def __init__(self) -> None:
        self._usuarios: dict[str, Usuario] = {}

    def adicionar(self, nome: str, idade: int, email: str, senha: str) -> Usuario:
        if nome in self._usuarios:
            raise ValidacaoError(f"Usuário '{nome}' já existe.")

        usuario = Usuario(nome=nome, idade=idade, email=email)
        usuario.senha_hash = senha
        self._usuarios[nome] = usuario
        logger.info("Usuário '%s' adicionado.", nome)
        return usuario

    def buscar(self, nome: str) -> Usuario | None:
        return self._usuarios.get(nome)

    def atualizar_idade(self, nome: str, nova_idade: int) -> None:
        usuario = self._obter_ou_erro(nome)
        usuario.idade = _validar_idade(nova_idade)
        logger.info("Idade de '%s' atualizada para %d.", nome, nova_idade)

    def atualizar_email(self, nome: str, novo_email: str) -> None:
        usuario = self._obter_ou_erro(nome)
        usuario.email = _validar_email(novo_email)
        logger.info("Email de '%s' atualizado.", nome)

    def desativar(self, nome: str) -> None:
        usuario = self._obter_ou_erro(nome)
        usuario.ativo = False
        logger.info("Usuário '%s' desativado.", nome)

    def listar_ativos(self) -> list[Usuario]:
        return [u for u in self._usuarios.values() if u.ativo]

    def listar_todos(self) -> list[Usuario]:
        return list(self._usuarios.values())

    def _obter_ou_erro(self, nome: str) -> Usuario:
        usuario = self.buscar(nome)
        if usuario is None:
            raise ValidacaoError(f"Usuário '{nome}' não encontrado.")
        return usuario


# --- Demo ---
if __name__ == "__main__":
    gerenciador = GerenciadorUsuarios()

    # Adicionando usuários válidos
    gerenciador.adicionar("joao", 25, "joao@email.com", "senha_segura_123")
    gerenciador.adicionar("maria", 30, "maria@email.com", "outra_senha_456")

    # Tentando adicionar dados inválidos (capturados pela validação)
    for nome, idade, email, senha in [
        ("pedro", -5, "emailinvalido", "p"),
        ("ana", 200, "ana@email.com", "123456"),
        ("carlos", 20, "carlos@email.com", "abc"),
    ]:
        try:
            gerenciador.adicionar(nome, idade, email, senha)
        except ValidacaoError as e:
            logger.warning("Falha ao adicionar '%s': %s", nome, e)

    print("\n=== LISTA DE ATIVOS ===")
    for i, usuario in enumerate(gerenciador.listar_ativos(), 1):
        print(f"{i}. {usuario}")

    print("\n=== BUSCAR ===")
    if usuario_encontrado := gerenciador.buscar("joao"):
        print(usuario_encontrado)
    else:
        print("Usuário não encontrado.")

    # Atualizar idade com validação
    try:
        gerenciador.atualizar_idade("maria", 31)
    except ValidacaoError as e:
        logger.warning("Falha: %s", e)

    # Verificar senha (sem expor o hash)
    if usuario_encontrado := gerenciador.buscar("joao"):
        print(f"\nSenha correta? {usuario_encontrado.verificar_senha('senha_segura_123')}")
        print(f"Senha errada?  {usuario_encontrado.verificar_senha('tentativa')}")
