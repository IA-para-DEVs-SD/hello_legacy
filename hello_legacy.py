#!/usr/bin/env python3
"""
Hello Legacy - Um programa Python clássico
Demonstração de código legado com funções básicas
"""

def greet(name="World"):
    """Função de saudação tradicional"""
    return f"Hello, {name}!"

def farewell(name="World"):
    """Função de despedida"""
    return f"Goodbye, {name}!"

def main():
    """Função principal"""
    print("=" * 40)
    print("  HELLO LEGACY - Sistema Clássico")
    print("=" * 40)
    print()

    # Saudação inicial
    print(greet("LAB 365"))
    print(greet("IA para DEVs"))
    print()

    # Mensagem do sistema
    print("Este é um exemplo de código legado.")
    print("Mantido para referência histórica.")
    print()

    # Despedida
    print(farewell("Legacy Code"))
    print()
    print("=" * 40)

if __name__ == "__main__":
    main()
