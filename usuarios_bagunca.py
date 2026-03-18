"""
Sistema de Gestão de Usuários — Refatorado
Aplica POO, SOLID, Clean Code, Type Hints, hashing de senhas,
exceções customizadas, logging e busca O(1).
"""

from __future__ import annotations

import hashlib
import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Protocol

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Exceções customizadas
# ---------------------------------------------------------------------------

class UserError(Exception):
    """Base para erros de domínio de usuário."""


class UserNotFoundError(UserError):
    def __init__(self, identifier: str) -> None:
        super().__init__(f"Usuário não encontrado: {identifier}")


class DuplicateEmailError(UserError):
    def __init__(self, email: str) -> None:
        super().__init__(f"E-mail já cadastrado: {email}")


class ValidationError(UserError):
    """Erro genérico de validação de dados."""


# ---------------------------------------------------------------------------
# Validadores (SRP — lógica de validação isolada)
# ---------------------------------------------------------------------------

class Validators:
    """Métodos estáticos de validação reutilizáveis."""

    _EMAIL_RE = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    _MIN_PASSWORD_LEN = 8

    @staticmethod
    def validate_age(age: int) -> int:
        if not isinstance(age, int) or age < 0 or age > 150:
            raise ValidationError(f"Idade inválida: {age}. Deve ser entre 0 e 150.")
        return age

    @staticmethod
    def validate_email(email: str) -> str:
        if not Validators._EMAIL_RE.match(email):
            raise ValidationError(f"E-mail com formato inválido: {email}")
        return email.lower().strip()

    @staticmethod
    def validate_password(plain: str) -> str:
        if len(plain) < Validators._MIN_PASSWORD_LEN:
            raise ValidationError(
                f"Senha deve ter no mínimo {Validators._MIN_PASSWORD_LEN} caracteres."
            )
        if not re.search(r"[A-Z]", plain):
            raise ValidationError("Senha deve conter ao menos uma letra maiúscula.")
        if not re.search(r"[0-9]", plain):
            raise ValidationError("Senha deve conter ao menos um dígito.")
        return plain

    @staticmethod
    def validate_name(name: str) -> str:
        name = name.strip()
        if not name:
            raise ValidationError("Nome não pode ser vazio.")
        return name


# ---------------------------------------------------------------------------
# Hashing de senhas (simula bcrypt via hashlib + salt fixo p/ demo)
# ---------------------------------------------------------------------------

class PasswordHasher:
    """Encapsula hashing e verificação de senhas."""

    _SALT = "kiro_salt_demo_"  # Em produção, usar bcrypt com salt aleatório

    @staticmethod
    def hash(plain: str) -> str:
        salted = f"{PasswordHasher._SALT}{plain}"
        return hashlib.sha256(salted.encode()).hexdigest()

    @staticmethod
    def verify(plain: str, hashed: str) -> bool:
        return PasswordHasher.hash(plain) == hashed


# ---------------------------------------------------------------------------
# Entidade User (encapsulamento via property)
# ---------------------------------------------------------------------------

@dataclass
class User:
    """Entidade de domínio — representa um usuário do sistema."""

    _name: str
    _age: int
    _email: str
    _password_hash: str
    _active: bool = field(default=True)

    # --- Construtores ---------------------------------------------------

    @classmethod
    def create(cls, name: str, age: int, email: str, plain_password: str) -> User:
        """Factory que valida todos os campos antes de criar o User."""
        validated_name = Validators.validate_name(name)
        validated_age = Validators.validate_age(age)
        validated_email = Validators.validate_email(email)
        Validators.validate_password(plain_password)
        pw_hash = PasswordHasher.hash(plain_password)
        return cls(
            _name=validated_name,
            _age=validated_age,
            _email=validated_email,
            _password_hash=pw_hash,
        )

    # --- Properties -----------------------------------------------------

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = Validators.validate_name(value)

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        self._age = Validators.validate_age(value)

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        self._email = Validators.validate_email(value)

    @property
    def active(self) -> bool:
        return self._active

    def deactivate(self) -> None:
        self._active = False
        logger.info("Usuário '%s' desativado.", self._name)

    def activate(self) -> None:
        self._active = True
        logger.info("Usuário '%s' reativado.", self._name)

    def check_password(self, plain: str) -> bool:
        return PasswordHasher.verify(plain, self._password_hash)

    # --- Representação --------------------------------------------------

    def __str__(self) -> str:
        status = "ativo" if self._active else "inativo"
        return f"{self._name} | {self._age} anos | {self._email} | {status}"

    def __repr__(self) -> str:
        return (
            f"User(name={self._name!r}, age={self._age}, "
            f"email={self._email!r}, active={self._active})"
        )


# ---------------------------------------------------------------------------
# Repositório — abstração de persistência (OCP / DIP)
# ---------------------------------------------------------------------------

class UserRepository(ABC):
    """Interface de repositório. Permite trocar in-memory por DB no futuro."""

    @abstractmethod
    def add(self, user: User) -> None: ...

    @abstractmethod
    def find_by_email(self, email: str) -> User: ...

    @abstractmethod
    def find_by_name(self, name: str) -> User: ...

    @abstractmethod
    def list_active(self) -> list[User]: ...

    @abstractmethod
    def list_all(self) -> list[User]: ...

    @abstractmethod
    def remove_by_email(self, email: str) -> None: ...


class InMemoryUserRepository(UserRepository):
    """Implementação em memória com busca O(1) por e-mail."""

    def __init__(self) -> None:
        self._by_email: dict[str, User] = {}

    def add(self, user: User) -> None:
        if user.email in self._by_email:
            raise DuplicateEmailError(user.email)
        self._by_email[user.email] = user

    def find_by_email(self, email: str) -> User:
        email = email.lower().strip()
        try:
            return self._by_email[email]
        except KeyError:
            raise UserNotFoundError(email) from None

    def find_by_name(self, name: str) -> User:
        for user in self._by_email.values():
            if user.name.lower() == name.lower():
                return user
        raise UserNotFoundError(name)

    def list_active(self) -> list[User]:
        return [u for u in self._by_email.values() if u.active]

    def list_all(self) -> list[User]:
        return list(self._by_email.values())

    def remove_by_email(self, email: str) -> None:
        email = email.lower().strip()
        if email not in self._by_email:
            raise UserNotFoundError(email)
        del self._by_email[email]


# ---------------------------------------------------------------------------
# Serviço de Usuários (orquestra validação + repositório)
# ---------------------------------------------------------------------------

class UserService:
    """Camada de serviço — coordena regras de negócio e persistência."""

    def __init__(self, repository: UserRepository) -> None:
        self._repo = repository

    def register(self, name: str, age: int, email: str, password: str) -> User:
        user = User.create(name, age, email, password)
        self._repo.add(user)
        logger.info("Usuário '%s' cadastrado com sucesso.", user.name)
        return user

    def find_by_email(self, email: str) -> User:
        return self._repo.find_by_email(email)

    def find_by_name(self, name: str) -> User:
        return self._repo.find_by_name(name)

    def update_age(self, email: str, new_age: int) -> User:
        user = self._repo.find_by_email(email)
        user.age = new_age
        logger.info("Idade de '%s' atualizada para %d.", user.name, new_age)
        return user

    def update_email(self, current_email: str, new_email: str) -> User:
        user = self._repo.find_by_email(current_email)
        validated = Validators.validate_email(new_email)
        # Verifica duplicidade do novo e-mail
        try:
            self._repo.find_by_email(validated)
            raise DuplicateEmailError(validated)
        except UserNotFoundError:
            pass
        self._repo.remove_by_email(current_email)
        user.email = validated
        self._repo.add(user)
        logger.info("E-mail atualizado para '%s'.", validated)
        return user

    def deactivate(self, email: str) -> None:
        user = self._repo.find_by_email(email)
        user.deactivate()

    def list_active(self) -> list[User]:
        return self._repo.list_active()

    def list_all(self) -> list[User]:
        return self._repo.list_all()


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    repo = InMemoryUserRepository()
    service = UserService(repo)

    # Cadastros válidos
    service.register("João", 25, "joao@email.com", "Senha1234")
    service.register("Maria", 30, "maria@email.com", "Segura99X")

    # Cadastro com dados inválidos — capturado pelas validações
    for bad_args in [
        ("Pedro", -5, "emailinvalido", "p"),
        ("", 20, "a@b.com", "Valida123"),
        ("Ana", 25, "ana@email.com", "curta"),
    ]:
        try:
            service.register(*bad_args)
        except ValidationError as exc:
            logger.warning("Cadastro rejeitado: %s", exc)

    # Listagem
    print("\n=== USUÁRIOS ATIVOS ===")
    for i, user in enumerate(service.list_active(), start=1):
        print(f"  {i}. {user}")

    # Busca
    print("\n=== BUSCAR POR NOME ===")
    try:
        found = service.find_by_name("João")
        print(f"  Encontrado: {found}")
        print(f"  Senha protegida — verificação: {found.check_password('Senha1234')}")
    except UserNotFoundError as exc:
        logger.error(exc)

    # Atualização de idade com validação
    print("\n=== ATUALIZAR IDADE ===")
    try:
        service.update_age("maria@email.com", 31)
    except (UserNotFoundError, ValidationError) as exc:
        logger.error(exc)

    try:
        service.update_age("maria@email.com", 999)
    except ValidationError as exc:
        logger.warning("Idade rejeitada: %s", exc)

    # Desativação
    print("\n=== DESATIVAR USUÁRIO ===")
    service.deactivate("joao@email.com")

    print("\n=== USUÁRIOS ATIVOS APÓS DESATIVAÇÃO ===")
    for i, user in enumerate(service.list_active(), start=1):
        print(f"  {i}. {user}")
