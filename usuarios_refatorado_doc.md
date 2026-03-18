# Documentação — usuarios_refatorado.py

## Prompts utilizados

**Prompt 1 — Refatoração:**
> "preciso que vc aja como um programador senior e, seguindo as melhores práticas de clean code e clean architecture, refatore o código usuarios_bagunca.py. Crie outra versão deste script otimizada, com nomes de métodos e variáveis mais intuitivos, eliminando assim a necessidade de comentários. quero também que funcionalidades repetidas sejam desfeitas, e que a performance seja aprimorada."

**Prompt 2 — Documentação:**
> "agora gere um arquivo .md com os prompts usados e a explicação do script gerado"

---

## Explicação do script

### Classe `Usuario`

Representa um único usuário do sistema usando `@dataclass`, o que elimina a necessidade de `__init__` manual e gera `__repr__` automaticamente.

```python
@dataclass
class Usuario:
    nome: str
    idade: int
    email: str
    _senha_hash: str = field(repr=False)  # nunca exposta em repr/print
    ativo: bool = True
```

- `_senha_hash` armazena apenas o hash SHA-256 da senha, nunca o valor original.
- `field(repr=False)` garante que o hash não apareça em logs ou prints acidentais.
- `__str__` formata a exibição do usuário de forma legível.

---

### Exceção `ValidacaoError`

```python
class ValidacaoError(Exception):
    pass
```

Exceção customizada para distinguir erros de negócio (dados inválidos) de erros inesperados do sistema. Permite que o código chamador trate apenas o que é relevante.

---

### Funções auxiliares privadas

| Função | Responsabilidade |
|---|---|
| `_hash_senha(senha)` | Valida tamanho mínimo e retorna SHA-256 da senha |
| `_validar_idade(idade)` | Garante que a idade está entre 0 e 120 |
| `_validar_email(email)` | Valida formato do email via regex |

O prefixo `_` sinaliza que são funções internas do módulo, não parte da API pública.

---

### Classe `GerenciadorUsuarios`

Centraliza todas as operações CRUD. Usa `dict[str, Usuario]` internamente para garantir busca em **O(1)** (contra O(n) do código original com listas paralelas).

#### Métodos

**`cadastrar(nome, idade, email, senha) -> Usuario`**
Valida todos os campos antes de persistir. Bloqueia nomes duplicados. Armazena o hash da senha, nunca o valor em texto puro.

**`buscar(nome) -> Optional[Usuario]`**
Retorna o usuário ou `None`. Busca direta no dicionário, sem loop.

**`_buscar_ou_erro(nome) -> Usuario`**
Método interno reutilizado por `atualizar_idade`, `atualizar_email` e `desativar`. Elimina a lógica de busca duplicada que existia em cada função no código original.

**`atualizar_idade(nome, nova_idade)`**
Valida a nova idade antes de aplicar a mudança.

**`atualizar_email(nome, novo_email)`**
Valida o formato do novo email antes de aplicar a mudança.

**`desativar(nome)`**
Marca o usuário como inativo sem removê-lo do dicionário (soft delete).

**`listar_ativos() -> list[Usuario]`**
Retorna apenas usuários com `ativo=True` usando list comprehension.

---

## Comparativo com o código original

| Problema original | Solução aplicada |
|---|---|
| Listas paralelas globais | `dict[str, Usuario]` encapsulado na classe |
| Busca O(n) com `range(len())` | Busca O(1) via chave do dicionário |
| Senha em texto puro | Hash SHA-256 com validação de força |
| Sem validação de dados | `ValidacaoError` com validadores dedicados |
| Lógica de busca duplicada em cada função | `_buscar_ou_erro` reutilizável |
| Erros sinalizados com `print` | Exceções tipadas |
| Sem type hints | Type hints em todos os métodos e funções |
