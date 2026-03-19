import unittest
from unittest.mock import patch
from io import StringIO
import importlib
import sys


class TestCalculadoraRuim(unittest.TestCase):
    """Testes unitários para a função calc() de calculadora_ruim.py"""

    def _run_calc(self, inputs):
        """
        Helper que importa o módulo calculadora_ruim de forma isolada,
        mockando input e capturando stdout.
        Retorna o texto impresso no stdout.
        """
        # Remove o módulo do cache para forçar re-importação
        if "calculadora_ruim" in sys.modules:
            del sys.modules["calculadora_ruim"]

        with patch("builtins.input", side_effect=inputs):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                importlib.import_module("calculadora_ruim")
                return mock_stdout.getvalue()

    def test_soma(self):
        output = self._run_calc(["5", "3", "+", "n"])
        self.assertIn("8.0", output)

    def test_subtracao(self):
        output = self._run_calc(["10", "4", "-", "n"])
        self.assertIn("6.0", output)

    def test_multiplicacao(self):
        output = self._run_calc(["7", "3", "*", "n"])
        self.assertIn("21.0", output)

    def test_divisao(self):
        output = self._run_calc(["20", "4", "/", "n"])
        self.assertIn("5.0", output)

    def test_divisao_por_zero(self):
        output = self._run_calc(["10", "0", "/", "n"])
        self.assertIn("erro!", output)

    def test_operacao_invalida(self):
        output = self._run_calc(["5", "3", "%", "n"])
        self.assertIn("operacao invalida", output)

    def test_continuar_com_s_minusculo(self):
        output = self._run_calc(["2", "3", "+", "s", "10", "5", "-", "n"])
        self.assertIn("5.0", output)
        self.assertIn("resultado:", output)

    def test_continuar_com_S_maiusculo(self):
        output = self._run_calc(["1", "2", "*", "S", "6", "2", "/", "n"])
        self.assertIn("2.0", output)
        self.assertIn("3.0", output)

    def test_saida_tchau(self):
        output = self._run_calc(["1", "1", "+", "n"])
        self.assertIn("tchau", output)

    def test_input_invalido_levanta_excecao(self):
        if "calculadora_ruim" in sys.modules:
            del sys.modules["calculadora_ruim"]
        with patch("builtins.input", side_effect=["abc", "2", "+", "n"]):
            with self.assertRaises(ValueError):
                importlib.import_module("calculadora_ruim")


if __name__ == "__main__":
    unittest.main()
