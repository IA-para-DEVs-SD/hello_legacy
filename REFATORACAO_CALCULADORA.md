# Refatoração: calculadora_ruim.py

## Problemas no código original

- Função única `calc()` fazendo tudo: input, lógica e output misturados
- Recursão sem limite para continuar o loop
- Sem validação de inputs (quebrava com letras ou divisão por zero)
- Encadeamento de `if/elif` para selecionar a operação
- Sem type hints
- Strings de mensagem espalhadas no código
- Sem testes

---

## O que foi refatorado

### 1. Classe `Calculadora`
A lógica de cálculo foi encapsulada em uma classe com métodos dedicados por operação.
Isso isola a lógica de negócio de qualquer interação com o usuário.

```python
# antes
if z == "+":
    r = a + b
    print("resultado:", r)
elif z == "/":
    if b == 0:
        print("erro!")

# depois
class Calculadora:
    def somar(self, a: float, b: float) -> float:
        return a + b

    def dividir(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError(MSG_DIVISAO_ZERO)
        return a / b
```

### 2. Dicionário no lugar de if/elif
O método `calcular` usa um dicionário para mapear o símbolo da operação ao método correspondente.

```python
operacoes = {
    "+": self.somar,
    "-": self.subtrair,
    "*": self.multiplicar,
    "/": self.dividir,
}
```

### 3. Separação de input/output da lógica
Funções dedicadas para leitura e validação de cada tipo de entrada.

```python
def ler_numero(prompt: str) -> Optional[float]: ...
def ler_operacao() -> Optional[str]: ...
def ler_continuar() -> bool: ...
```

### 4. Loop while no lugar de recursão
A repetição do programa era feita com recursão (`calc()` chamando a si mesma), o que pode causar `RecursionError` com uso prolongado.

```python
# antes
if c == "s":
    calc()  # recursão sem limite

# depois
while True:
    ...
    if not ler_continuar():
        break
```

### 5. Validação com try/except
Inputs inválidos são capturados e o usuário é informado sem o programa quebrar.

```python
try:
    return float(input(prompt))
except ValueError:
    print(MSG_NUMERO_INVALIDO)
    return None
```

### 6. Type hints
Todos os métodos e funções possuem anotações de tipo.

```python
def calcular(self, a: float, b: float, operacao: str) -> float: ...
```

### 7. Constantes para mensagens
Todas as strings exibidas ao usuário foram extraídas para constantes no topo do arquivo.

```python
MSG_DIVISAO_ZERO = "Erro: divisão por zero não é permitida."
MSG_OPERACAO_INVALIDA = "Erro: operação inválida. Use +, -, * ou /."
```

### 8. Testes unitários
A classe `TestCalculadora` cobre todas as operações, casos de erro e operação inválida.

```python
class TestCalculadora(unittest.TestCase):
    def test_dividir_por_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calc.dividir(5, 0)
```

---

## Como executar

```bash
# Rodar a calculadora
python calculadora_ruim_refatorada.py

# Rodar os testes
python calculadora_ruim_refatorada.py --test
```
