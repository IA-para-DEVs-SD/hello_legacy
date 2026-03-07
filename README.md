# Hello Legacy

## AVISO IMPORTANTE

**Este repositório contém código PROPOSITALMENTE MAL ESCRITO para fins educacionais.**

O objetivo deste projeto é servir como material de estudo para prática de REFATORAÇÃO DE CÓDIGO. Todos os arquivos Python aqui presentes violam intencionalmente as boas práticas de programação, princípios SOLID, Clean Code e padrões de POO.

**NÃO USE ESTE CÓDIGO EM PRODUÇÃO!**

## 📋 Descrição

Este é um repositório educacional criado para o **LAB 365 - IA para DEVs** com exemplos de código que precisa ser refatorado. Cada arquivo contém comentários detalhados explicando os problemas e sugestões de melhorias.

## 🎯 Objetivo Pedagógico

Este repositório foi criado para:

- Praticar identificação de code smells
- Exercitar refatoração de código legado
- Aplicar princípios SOLID
- Implementar Clean Code
- Praticar Programação Orientada a Objetos
- Melhorar habilidades de design de software

## 📁 Arquivos para Refatoração

### 1. calculadora_ruim.py
**Problemas principais:**
- Função gigante fazendo múltiplas coisas
- Sem tratamento de erros
- Recursão sem limite
- Código duplicado
- Magic numbers
- Variáveis com nomes ruins

**Conceitos a praticar:**
- Criar classes
- Separar responsabilidades
- Tratamento de exceções
- Uso de dicionários
- Type hints

### 2. usuarios_bagunca.py
**Problemas principais:**
- Listas paralelas em vez de objetos
- Variáveis globais
- Senhas em texto puro
- Sem validação de dados
- Lógica de busca O(n)
- Dados sensíveis expostos

**Conceitos a praticar:**
- POO e encapsulamento
- Propriedades privadas
- Validações
- Hash de senhas
- Padrão Repository

### 3. tarefas_gigante.py
**Problemas principais:**
- Função com 100+ linhas
- Código profundamente aninhado
- UI misturada com lógica
- Código massivamente duplicado
- Sem persistência adequada

**Conceitos a praticar:**
- Separação de concerns
- Padrão Command
- Enums
- Métodos pequenos e focados
- Auto-save

### 4. processador_confuso.py
**Problemas principais:**
- Lógica confusa e difícil de entender
- Condicionais aninhados profundamente
- Magic numbers
- Type checking em vez de polimorfismo
- Nomes de variáveis sem significado

**Conceitos a praticar:**
- Strategy Pattern
- Polimorfismo
- Guard clauses
- Nomes descritivos
- Classes especializadas

## 🚀 Como Usar Este Repositório

### Para Estudantes:

1. **Analise o código ruim:**
   ```bash
   python calculadora_ruim.py
   python usuarios_bagunca.py
   python tarefas_gigante.py
   python processador_confuso.py
   ```

2. **Leia os comentários:** Cada arquivo tem comentários detalhados explicando os problemas

3. **Pratique refatoração:**
   - Crie uma nova branch
   - Escolha um arquivo
   - Refatore seguindo as sugestões
   - Compare antes e depois

4. **Desafio:** Refatore todo o código aplicando:
   - Princípios SOLID
   - Clean Code
   - Design Patterns adequados
   - POO corretamente

### Exemplo de Exercício:

```bash
# Crie uma branch para sua refatoração
git checkout -b refactor-calculadora

# Refatore o arquivo
# Crie testes unitários
# Documente suas melhorias

# Commit suas mudanças
git commit -m "Refatorar calculadora aplicando POO e SOLID"
```

## 📦 Requisitos

- Python 3.6 ou superior

## 📚 Estrutura do Projeto

```
hello_legacy/
│
├── calculadora_ruim.py       # Calculadora sem POO, função gigante
├── usuarios_bagunca.py       # Sistema sem classes, listas paralelas
├── tarefas_gigante.py        # Função com 100+ linhas, código duplicado
├── processador_confuso.py    # Lógica confusa, magic numbers
├── hello_legacy.py           # Exemplo simples original
└── README.md                 # Esta documentação
```

## 🎓 Conceitos a Praticar

### Princípios SOLID:
- **S**ingle Responsibility Principle
- **O**pen/Closed Principle
- **L**iskov Substitution Principle
- **I**nterface Segregation Principle
- **D**ependency Inversion Principle

### Clean Code:
- Nomes significativos
- Funções pequenas
- Comentários úteis (não óbvios)
- Formatação consistente
- Tratamento de erros

### Design Patterns:
- Strategy
- Factory
- Repository
- Command
- Observer

## 📖 Recursos Recomendados

- **Clean Code** - Robert C. Martin
- **Refactoring** - Martin Fowler
- **Design Patterns** - Gang of Four
- **Python Clean Code** - Mariano Anaya

## 🎓 Sobre o Projeto

Projeto criado como parte do curso **IA para DEVs** do LAB 365.

**Organização:** [IA-para-DEVs-SD](https://github.com/IA-para-DEVs-SD)

## 📄 Licença

Este projeto é de código aberto e está disponível para fins educacionais.

---

**Nota:** Este código é mantido como "legado" para demonstração de conceitos de manutenção de software antigo.
