"""
Testes unitários para validar a exatidão matemática do motor de probabilidade.
"""

import unittest
from core.probabilidade import (
    calcular_probabilidade_exata,
    simular_monte_carlo,
    calcular_probabilidade_ponderada
)


class TestProbabilidadeParOuImpar(unittest.TestCase):

    def test_classico_0_a_5(self):
        """0 a 5 com zero deve ser rigorosamente 50% vs 50%."""
        res = calcular_probabilidade_exata(0, 5, 0, 5)
        self.assertEqual(res.total_combinacoes, 36)
        self.assertEqual(res.pares_p1, 3)
        self.assertEqual(res.impares_p1, 3)
        self.assertEqual(res.combinacoes_par, 18)
        self.assertEqual(res.combinacoes_impar, 18)
        self.assertAlmostEqual(res.pct_par, 50.0, places=4)
        self.assertAlmostEqual(res.pct_impar, 50.0, places=4)
        self.assertEqual(res.vantagem, "EQUILIBRADO")
        self.assertEqual(res.diferenca_pct, 0.0)

    def test_classico_1_a_5_sem_zero(self):
        """1 a 5 sem zero deve favorecer PAR com 52.00% (13/25)."""
        res = calcular_probabilidade_exata(1, 5, 1, 5)
        self.assertEqual(res.total_combinacoes, 25)
        self.assertEqual(res.pares_p1, 2)
        self.assertEqual(res.impares_p1, 3)
        self.assertEqual(res.combinacoes_par, 13)
        self.assertEqual(res.combinacoes_impar, 12)
        self.assertAlmostEqual(res.pct_par, 52.0, places=4)
        self.assertAlmostEqual(res.pct_impar, 48.0, places=4)
        self.assertEqual(res.vantagem, "PAR")
        self.assertAlmostEqual(res.diferenca_pct, 4.0, places=4)

    def test_duas_maos_0_a_10(self):
        """0 a 10 deve ter 121 combinações e favorecer levemente PAR (61/121)."""
        res = calcular_probabilidade_exata(0, 10, 0, 10)
        self.assertEqual(res.total_combinacoes, 121)
        self.assertEqual(res.pares_p1, 6)
        self.assertEqual(res.impares_p1, 5)
        self.assertEqual(res.combinacoes_par, 61)
        self.assertEqual(res.combinacoes_impar, 60)
        self.assertAlmostEqual(res.pct_par, (61 / 121) * 100, places=4)
        self.assertEqual(res.vantagem, "PAR")

    def test_assimetrico_impar_vantagem(self):
        """P1: [1, 1] (apenas ímpar 1), P2: [2, 2] (apenas par 2).
           1+2 = 3 (ímpar). 100% chance de ímpar!"""
        res = calcular_probabilidade_exata(1, 1, 2, 2)
        self.assertEqual(res.pares_p1, 0)
        self.assertEqual(res.impares_p1, 1)
        self.assertEqual(res.pares_p2, 1)
        self.assertEqual(res.impares_p2, 0)
        self.assertEqual(res.combinacoes_par, 0)
        self.assertEqual(res.combinacoes_impar, 1)
        self.assertEqual(res.pct_impar, 100.0)
        self.assertEqual(res.vantagem, "ÍMPAR")

    def test_intervalo_com_vantagem_impar(self):
        """P1: [1, 2] (1 par, 1 ímpar), P2: [1, 1] (0 par, 1 ímpar).
           Combinações: (1,1)->2 (par), (2,1)->3 (ímpar). 50% vs 50%.
           Se P1: [0, 1] (1 par {0}, 1 ímpar {1}), P2: [1, 2] (1 ímpar {1}, 1 par {2}) -> 50%."""
        res = calcular_probabilidade_exata(1, 2, 1, 1)
        self.assertEqual(res.total_combinacoes, 2)
        self.assertEqual(res.combinacoes_par, 1)
        self.assertEqual(res.combinacoes_impar, 1)
        self.assertEqual(res.pct_par, 50.0)
        self.assertEqual(res.pct_impar, 50.0)

    def test_matriz_e_distribuicao_somas(self):
        """Valida que a soma de todas as contagens da matriz é igual ao total."""
        res = calcular_probabilidade_exata(0, 5, 0, 5)
        total_matriz = sum(len(linha) for linha in res.matriz)
        total_dist = sum(res.distribuicao_somas.values())
        self.assertEqual(total_matriz, 36)
        self.assertEqual(total_dist, 36)
        self.assertEqual(res.distribuicao_somas[0], 1)  # 0+0
        self.assertEqual(res.distribuicao_somas[10], 1)  # 5+5
        # 5 pode ser 0+5, 1+4, 2+3, 3+2, 4+1, 5+0 => 6 formas
        self.assertEqual(res.distribuicao_somas[5], 6)

    def test_monte_carlo_convergencia(self):
        """Simulação de 50.000 rodadas para 1 a 5 deve convergir para ~52% com erro < 1.0%."""
        sim = simular_monte_carlo(1, 5, 1, 5, num_rodadas=50000, seed=42)
        self.assertTrue(sim["convergencia_ok"])
        self.assertLess(sim["erro_absoluto_pct"], 1.0)
        self.assertAlmostEqual(sim["pct_teorica_par"], 52.0, places=2)

    def test_probabilidade_ponderada(self):
        """Se P1 só joga 2 (100% par) e P2 joga 50% 1 e 50% 2."""
        pesos_p1 = {2: 1.0}
        pesos_p2 = {1: 1.0, 2: 1.0}
        res = calcular_probabilidade_ponderada(pesos_p1, pesos_p2)
        self.assertAlmostEqual(res["pct_par"], 50.0, places=2)
        self.assertAlmostEqual(res["pct_impar"], 50.0, places=2)


if __name__ == "__main__":
    unittest.main()
