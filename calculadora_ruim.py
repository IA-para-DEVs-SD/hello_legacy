def calc():
    print("=== CALCULADORA ===")
    x = input("numero 1: ")
    y = input("numero 2: ")
    z = input("operacao (+,-,*,/): ")

    a = float(x)
    b = float(y)

    if z == "+":
        r = a + b
        print("resultado:", r)
    elif z == "-":
        r = a - b
        print("resultado:", r)
    elif z == "*":
        r = a * b
        print("resultado:", r)
    elif z == "/":
        if b == 0:
            print("erro!")
        else:
            r = a / b
            print("resultado:", r)
    else:
        print("operacao invalida")

    c = input("continuar? (s/n): ")
    if c == "s" or c == "S" or c == "sim" or c == "SIM":
        calc()
    else:
        print("tchau")

calc()
