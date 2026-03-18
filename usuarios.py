"""
Sistema de gerenciamento de usuários refatorado.
Aplica boas práticas: POO, encapsulamento, validações,
hash de senha, type hints, logging e padrão Repository.
"""

import hashlib
import json
import logging
import re
from dataclasses import field
from pathlib import Path
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# ── Exceções personalizadas ──────────────────────────────────────────

class UsuarioError(Exception):
    """Erro base do domínio de usuários."""


class ValidacaoError(UsuarioError):
    """Dados inválidos fornecidos."""


class UsuarioNaoEncontradoError(UsuarioError):
    """Usuário não existe no repositório."""


class EmailDuplicadoError(UsuarioError):
    """Já existe um usuário com este e-mail."""


# ── Modelo ───────────────────────────────────────────────────────────

class Usuario:
    """Representa um usuário do sistema com atributos protegidos."""

    _IDADE_MIN = 0
    _IDADE_MAX = 150
    _EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")
    _SENHA_MIN_LEN = 8

    def __init__(self, nome: str, idade: int, email: str, senha: str) -> None:
        self.nome = nome          # usa o setter com validação
        self.idade = idade        # usa o setter com validação
        self.email = email        # usa o setter com validação
        self._senha_hash = self._hash_senha(self._validar_senha(senha))
        self._ativo: bool = True

    # ── Properties ───────────────────────────────────────────────

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValidacaoError("Nome não pode ser vazio.")
        self._nome = valor.strip()

    @property
    def idade(self) -> int:
        return self._idade

    @idade.setter
    def idade(self, valor: int) -> None:
        if not isinstance(valor, int) or not (self._IDADE_MIN <= valor <= self._IDADE_MAX):
            raise ValidacaoError(
                f"Idade deve ser inteiro entre {self._IDADE_MIN} e {self._IDADE_MAX}."
            )
        self._idade = valor

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        if not self._EMAIL_RE.match(valor):
            raise ValidacaoError(f"E-mail inválido: {valor}")
        self._email = valor.lower()

    @property
    def ativo(self) -> bool:
        return self._ativo

    # ── Senha ────────────────────────────────────────────────────

    def _validar_senha(self, senha: str) -> str:
        if len(senha) < self._SENHA_MIN_LEN:
            raise ValidacaoError(
                f"Senha deve ter no mínimo {self._SENHA_MIN_LEN} caracteres."
            )
        if not re.search(r"[A-Z]", senha):
            raise ValidacaoError("Senha deve conter ao menos uma letra maiúscula.")
        if not re.search(r"[a-z]", senha):
            raise ValidacaoError("Senha deve conter ao menos uma letra minúscula.")
        if not re.search(r"\d", senha):
            raise ValidacaoError("Senha deve conter ao menos um dígito.")
        return senha

    @staticmethod
    def _hash_senha(senha: str) -> str:
        return hashlib.sha256(senha.encode()).hexdigest()

    def verificar_senha(self, senha: str) -> bool:
        return self._hash_senha(senha) == self._senha_hash

    def alterar_senha(self, senha_atual: str, nova_senha: str) -> None:
        if not self.verificar_senha(senha_atual):
            raise ValidacaoError("Senha atual incorreta.")
        self._senha_hash = self._hash_senha(self._validar_senha(nova_senha))

    # ── Representação ────────────────────────────────────────────

    def __str__(self) -> str:
        status = "ativo" if self._ativo else "inativo"
        return f"{self._nome} ({self._idade} anos) - {self._email} [{status}]"

    def __repr__(self) -> str:
        return (
            f"Usuario(nome={self._nome!r}, idade={self._idade}, "
            f"email={self._email!r}, ativo={self._ativo})"
        )

    # ── Serialização ─────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "nome": self._nome,
            "idade": self._idade,
            "email": self._email,
            "senha_hash": self._senha_hash,
            "ativo": self._ativo,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Usuario":
        """Reconstrói um Usuario a partir de dicionário (sem revalidar senha)."""
        obj = object.__new__(cls)
        obj._nome = dados["nome"]
        obj._idade = dados["idade"]
        obj._email = dados["email"]
        obj._senha_hash = dados["senha_hash"]
        obj._ativo = dados["ativo"]
        return obj


# ── Repository (persistência) ────────────────────────────────────────

class UsuarioRepository:
    """Persiste usuários em arquivo JSON (padrão Repository)."""

    def __init__(self, caminho: str = "usuarios.json") -> None:
        self._caminho = Path(caminho)
        self._usuarios: list[Usuario] = []
        self._carregar()

    # ── Persistência ─────────────────────────────────────────────

    def _carregar(self) -> None:
        if self._caminho.exists():
            try:
                dados = json.loads(self._caminho.read_text(encoding="utf-8"))
                self._usuarios = [Usuario.from_dict(d) for d in dados]
                logger.info("Carregados %d usuários de %s", len(self._usuarios), self._caminho)
            except (json.JSONDecodeError, KeyError) as exc:
                logger.error("Erro ao carregar dados: %s", exc)
                self._usuarios = []

    def _salvar(self) -> None:
        self._caminho.write_text(
            json.dumps([u.to_dict() for u in self._usuarios], indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        logger.debug("Dados salvos em %s", self._caminho)

    # ── Busca reutilizável ───────────────────────────────────────

    def _buscar_por(
        self,
        campo: str,
        valor: str,
        *,
        apenas_ativos: bool = False,
    ) -> Optional[Usuario]:
        """Busca genérica por qualquer atributo público do Usuario."""
        for usuario in self._usuarios:
            if apenas_ativos and not usuario.ativo:
                continue
            if getattr(usuario, campo, None) == valor:
                return usuario
        return None

    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        return self._buscar_por("email", email.lower())

    def buscar_por_nome(self, nome: str) -> Optional[Usuario]:
        return self._buscar_por("nome", nome)

    # ── CRUD ─────────────────────────────────────────────────────

    def adicionar(self, usuario: Usuario) -> None:
        if self.buscar_por_email(usuario.email):
            raise EmailDuplicadoError(f"E-mail já cadastrado: {usuario.email}")
        self._usuarios.append(usuario)
        self._salvar()
        logger.info("Usuário adicionado: %s", usuario)

    def listar(self, *, apenas_ativos: bool = True) -> list[Usuario]:
        if apenas_ativos:
            return [u for u in self._usuarios if u.ativo]
        return list(self._usuarios)

    def atualizar(self, email: str, **campos: object) -> Usuario:
        usuario = self.buscar_por_email(email)
        if not usuario:
            raise UsuarioNaoEncontradoError(f"Usuário não encontrado: {email}")
        for campo, valor in campos.items():
            if hasattr(usuario, campo):
                setattr(usuario, campo, valor)
            else:
                raise ValidacaoError(f"Campo inválido: {campo}")
        self._salvar()
        logger.info("Usuário atualizado: %s", usuario)
        return usuario

    def desativar(self, email: str) -> None:
        usuario = self.buscar_por_email(email)
        if not usuario:
            raise UsuarioNaoEncontradoError(f"Usuário não encontrado: {email}")
        usuario._ativo = False
        self._salvar()
        logger.info("Usuário desativado: %s", email)

    def remover(self, email: str) -> None:
        usuario = self.buscar_por_email(email)
        if not usuario:
            raise UsuarioNaoEncontradoError(f"Usuário não encontrado: {email}")
        self._usuarios.remove(usuario)
        self._salvar()
        logger.info("Usuário removido: %s", email)


# ── Gerenciador (fachada de alto nível) ──────────────────────────────

class GerenciadorUsuarios:
    """Fachada que orquestra operações sobre o repositório de usuários."""

    def __init__(self, repositorio: Optional[UsuarioRepository] = None) -> None:
        self._repo = repositorio or UsuarioRepository()

    def cadastrar(self, nome: str, idade: int, email: str, senha: str) -> Usuario:
        try:
            usuario = Usuario(nome, idade, email, senha)
            self._repo.adicionar(usuario)
            return usuario
        except UsuarioError:
            raise
        except Exception as exc:
            logger.exception("Erro inesperado ao cadastrar usuário")
            raise UsuarioError(f"Falha ao cadastrar: {exc}") from exc

    def buscar(self, email: str) -> Usuario:
        usuario = self._repo.buscar_por_email(email)
        if not usuario:
            raise UsuarioNaoEncontradoError(f"Usuário não encontrado: {email}")
        return usuario

    def listar(self, *, apenas_ativos: bool = True) -> list[Usuario]:
        return self._repo.listar(apenas_ativos=apenas_ativos)

    def atualizar(self, email: str, **campos: object) -> Usuario:
        return self._repo.atualizar(email, **campos)

    def desativar(self, email: str) -> None:
        self._repo.desativar(email)

    def remover(self, email: str) -> None:
        self._repo.remover(email)


# ── Demo ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    gerenciador = GerenciadorUsuarios(UsuarioRepository("usuarios_demo.json"))

    # Cadastro com validação
    try:
        gerenciador.cadastrar("João Silva", 25, "joao@email.com", "Senha123forte")
        gerenciador.cadastrar("Maria Souza", 30, "maria@email.com", "Outra1senha")
    except UsuarioError as e:
        logger.warning("Cadastro falhou: %s", e)

    # Tentativa com dados inválidos (será rejeitada)
    try:
        gerenciador.cadastrar("Pedro", -5, "emailinvalido", "p")
    except ValidacaoError as e:
        logger.warning("Validação correta — dados rejeitados: %s", e)

    # Listagem
    logger.info("=== Usuários ativos ===")
    for i, usuario in enumerate(gerenciador.listar(), start=1):
        logger.info("%d. %s", i, usuario)

    # Busca
    try:
        encontrado = gerenciador.buscar("joao@email.com")
        logger.info("Encontrado: %r", encontrado)
    except UsuarioNaoEncontradoError as e:
        logger.warning("%s", e)

    # Atualização com validação
    try:
        gerenciador.atualizar("maria@email.com", idade=31)
    except UsuarioError as e:
        logger.warning("Atualização falhou: %s", e)

    # Desativação
    try:
        gerenciador.desativar("joao@email.com")
        logger.info("=== Após desativação ===")
        for i, usuario in enumerate(gerenciador.listar(), start=1):
            logger.info("%d. %s", i, usuario)
    except UsuarioError as e:
        logger.warning("%s", e)
