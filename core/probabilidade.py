"""
Módulo de Cálculo Probabilístico e Combinatório para o Jogo de Par ou Ímpar.
Realiza cálculos analíticos exatos do espaço amostral e simulações de Monte Carlo.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
import random


@dataclass
class ResultadoProbabilidade:
    """Contém a análise probabilística completa de um cenário de jogo."""
    min1: int
    max1: int
    min2: int
    max2: int
    total_combinacoes: int
    pares_p1: int
    impares_p1: int
    pares_p2: int
    impares_p2: int
    combinacoes_par: int
    combinacoes_impar: int
    prob_par: float
    prob_impar: float
    pct_par: float
    pct_impar: float
    vantagem: str  # 'PAR', 'ÍMPAR' ou 'EQUILIBRADO'
    diferenca_pct: float
    explicacao_didatica: str
    distribuicao_somas: Dict[int, int]
    matriz: List[List[Dict[str, any]]]

    def resumo_formatado(self) -> str:
        """Retorna uma string sumarizada e elegante dos resultados."""
        return (
            f"Espaço Amostral: {self.total_combinacoes} combinações\n"
            f"Vitória de PAR:   {self.combinacoes_par:>{len(str(self.total_combinacoes))}} "
            f"({self.pct_par:.2f}%)\n"
            f"Vitória de ÍMPAR: {self.combinacoes_impar:>{len(str(self.total_combinacoes))}} "
            f"({self.pct_impar:.2f}%)\n"
            f"Veredito: {self.vantagem}"
            + (f" (+{self.diferenca_pct:.2f}% de margem)" if self.diferenca_pct > 0 else " (Probabilidades estritamente idênticas)")
        )


def calcular_probabilidade_exata(min1: int, max1: int, min2: int, max2: int) -> ResultadoProbabilidade:
    """
    Calcula a probabilidade combinatória analítica exata de vitória para Par e Ímpar.
    
    A soma de dois inteiros X1 e X2 é:
      - PAR   se (X1 é par E X2 é par) OU (X1 é ímpar E X2 é ímpar)
              N_par = (Pares_1 * Pares_2) + (Ímpares_1 * Ímpares_2)
      - ÍMPAR se (X1 é par E X2 é ímpar) OU (X1 é ímpar E X2 é par)
              N_impar = (Pares_1 * Ímpares_2) + (Ímpares_1 * Pares_2)
    """
    if min1 > max1:
        min1, max1 = max1, min1
    if min2 > max2:
        min2, max2 = max2, min2

    valores_p1 = list(range(min1, max1 + 1))
    valores_p2 = list(range(min2, max2 + 1))

    pares_p1 = sum(1 for x in valores_p1 if x % 2 == 0)
    impares_p1 = len(valores_p1) - pares_p1

    pares_p2 = sum(1 for x in valores_p2 if x % 2 == 0)
    impares_p2 = len(valores_p2) - pares_p2

    total_combinacoes = len(valores_p1) * len(valores_p2)

    if total_combinacoes == 0:
        raise ValueError("Intervalos de jogadores não podem ser vazios.")

    combinacoes_par = (pares_p1 * pares_p2) + (impares_p1 * impares_p2)
    combinacoes_impar = (pares_p1 * impares_p2) + (impares_p1 * pares_p2)

    prob_par = combinacoes_par / total_combinacoes
    prob_impar = combinacoes_impar / total_combinacoes
    pct_par = prob_par * 100
    pct_impar = prob_impar * 100

    diferenca = abs(pct_par - pct_impar)

    if combinacoes_par > combinacoes_impar:
        vantagem = "PAR"
    elif combinacoes_impar > combinacoes_par:
        vantagem = "ÍMPAR"
    else:
        vantagem = "EQUILIBRADO"

    # Construção da matriz completa e distribuição das somas
    distribuicao_somas: Dict[int, int] = {}
    matriz: List[List[Dict[str, any]]] = []

    for x1 in valores_p1:
        linha = []
        for x2 in valores_p2:
            soma = x1 + x2
            eh_par = (soma % 2 == 0)
            vencedor = "PAR" if eh_par else "ÍMPAR"
            distribuicao_somas[soma] = distribuicao_somas.get(soma, 0) + 1
            linha.append({
                "x1": x1,
                "x2": x2,
                "soma": soma,
                "eh_par": eh_par,
                "vencedor": vencedor
            })
        matriz.append(linha)

    # Elaboração da explicação didática
    if vantagem == "EQUILIBRADO":
        explicacao = (
            f"O jogo é perfeitamente justo! Com {total_combinacoes} combinações possíveis, "
            f"ambos os lados possuem exatamente {combinacoes_par} cenários de vitória ({pct_par:.1f}%)."
        )
    elif min1 == 1 and max1 == 5 and min2 == 1 and max2 == 5:
        explicacao = (
            "CURIOSIDADE MATEMÁTICA: No clássico de 1 a 5 dedos sem o zero, há 3 números ímpares "
            "{1, 3, 5} e apenas 2 pares {2, 4} para cada jogador. Como Ímpar + Ímpar resulta em Par "
            "(3x3 = 9 combinações) e Par + Par resulta em Par (2x2 = 4), temos 13 somas pares contra "
            "12 ímpares. Quem escolhe PAR tem 52% de chance de vencer!"
        )
    elif vantagem == "PAR":
        explicacao = (
            f"Quem escolhe PAR tem vantagem de {diferenca:.2f}%! Há {combinacoes_par} combinações "
            f"de soma par contra {combinacoes_impar} de soma ímpar no espaço de {total_combinacoes} pares ordenados."
        )
    else:
        explicacao = (
            f"Quem escolhe ÍMPAR tem vantagem de {diferenca:.2f}%! Há {combinacoes_impar} combinações "
            f"de soma ímpar contra {combinacoes_par} de soma par no espaço de {total_combinacoes} pares ordenados."
        )

    return ResultadoProbabilidade(
        min1=min1,
        max1=max1,
        min2=min2,
        max2=max2,
        total_combinacoes=total_combinacoes,
        pares_p1=pares_p1,
        impares_p1=impares_p1,
        pares_p2=pares_p2,
        impares_p2=impares_p2,
        combinacoes_par=combinacoes_par,
        combinacoes_impar=combinacoes_impar,
        prob_par=prob_par,
        prob_impar=prob_impar,
        pct_par=pct_par,
        pct_impar=pct_impar,
        vantagem=vantagem,
        diferenca_pct=diferenca,
        explicacao_didatica=explicacao,
        distribuicao_somas=dict(sorted(distribuicao_somas.items())),
        matriz=matriz
    )


def simular_monte_carlo(
    min1: int,
    max1: int,
    min2: int,
    max2: int,
    num_rodadas: int = 50000,
    seed: int = None
) -> Dict[str, any]:
    """
    Executa uma simulação estocástica de Monte Carlo de N rodadas.
    Permite validar empiricalmente o Teorema Central do Limite e a Lei dos Grandes Números.
    """
    if seed is not None:
        random.seed(seed)

    vitorias_par = 0
    vitorias_impar = 0
    frequencia_somas: Dict[int, int] = {}
    frequencia_jogadas_p1: Dict[int, int] = {}
    frequencia_jogadas_p2: Dict[int, int] = {}

    for _ in range(num_rodadas):
        x1 = random.randint(min1, max1)
        x2 = random.randint(min2, max2)
        soma = x1 + x2

        frequencia_jogadas_p1[x1] = frequencia_jogadas_p1.get(x1, 0) + 1
        frequencia_jogadas_p2[x2] = frequencia_jogadas_p2.get(x2, 0) + 1
        frequencia_somas[soma] = frequencia_somas.get(soma, 0) + 1

        if soma % 2 == 0:
            vitorias_par += 1
        else:
            vitorias_impar += 1

    pct_empirica_par = (vitorias_par / num_rodadas) * 100
    pct_empirica_impar = (vitorias_impar / num_rodadas) * 100

    teorico = calcular_probabilidade_exata(min1, max1, min2, max2)

    erro_par = abs(pct_empirica_par - teorico.pct_par)
    erro_impar = abs(pct_empirica_impar - teorico.pct_impar)

    return {
        "num_rodadas": num_rodadas,
        "vitorias_par": vitorias_par,
        "vitorias_impar": vitorias_impar,
        "pct_empirica_par": pct_empirica_par,
        "pct_empirica_impar": pct_empirica_impar,
        "pct_teorica_par": teorico.pct_par,
        "pct_teorica_impar": teorico.pct_impar,
        "erro_absoluto_pct": (erro_par + erro_impar) / 2,
        "frequencia_somas": dict(sorted(frequencia_somas.items())),
        "frequencia_jogadas_p1": dict(sorted(frequencia_jogadas_p1.items())),
        "frequencia_jogadas_p2": dict(sorted(frequencia_jogadas_p2.items())),
        "convergencia_ok": ((erro_par + erro_impar) / 2) < 1.0  # Erro < 1% esperado para 50k
    }


def calcular_probabilidade_ponderada(
    pesos_p1: Dict[int, float],
    pesos_p2: Dict[int, float]
) -> Dict[str, any]:
    """
    Calcula a probabilidade de vitória quando jogadores jogam com distribuição de probabilidade não-uniforme
    (por exemplo, quando um jogador tem vícios ou a IA adapta seus lances com base em frequência histórica).
    """
    soma_pesos1 = sum(pesos_p1.values())
    soma_pesos2 = sum(pesos_p2.values())

    # Normalizar distribuições
    prob_p1 = {k: v / soma_pesos1 for k, v in pesos_p1.items()}
    prob_p2 = {k: v / soma_pesos2 for k, v in pesos_p2.items()}

    prob_total_par = 0.0
    prob_total_impar = 0.0

    for x1, p1 in prob_p1.items():
        for x2, p2 in prob_p2.items():
            prob_conjunta = p1 * p2
            if (x1 + x2) % 2 == 0:
                prob_total_par += prob_conjunta
            else:
                prob_total_impar += prob_conjunta

    pct_par = prob_total_par * 100
    pct_impar = prob_total_impar * 100

    return {
        "prob_par": prob_total_par,
        "prob_impar": prob_total_impar,
        "pct_par": pct_par,
        "pct_impar": pct_impar,
        "vantagem": "PAR" if pct_par > pct_impar else ("ÍMPAR" if pct_impar > pct_par else "EQUILIBRADO")
    }
