"""
Módulo de Histórico e Análise Estatística de Partidas.
Registra partidas, calcula frequências empíricas e gera relatórios de desempenho.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Dict, Optional


@dataclass
class RegistroRodada:
    """Representa o log de uma rodada individual."""
    numero_rodada: int
    data_hora: str
    jogador1_nome: str
    jogador2_nome: str
    escolha_p1: str          # 'PAR' ou 'ÍMPAR'
    escolha_p2: str          # 'PAR' ou 'ÍMPAR'
    valor_p1: int
    valor_p2: int
    soma: int
    resultado_paridade: str   # 'PAR' ou 'ÍMPAR'
    vencedor: str             # Nome do vencedor
    prob_esperada_vencedor: float


class HistoricoSessao:
    """Gerencia o histórico da sessão e métricas estatísticas acumuladas."""

    def __init__(self):
        self.rodadas: List[RegistroRodada] = []
        self.vitorias_p1: int = 0
        self.vitorias_p2: int = 0
        self.empates: int = 0
        self.contagem_jogadas_p1: Dict[int, int] = {}
        self.contagem_jogadas_p2: Dict[int, int] = {}
        self.total_pares: int = 0
        self.total_impares: int = 0
        self.sequencia_atual_vitorias: int = 0
        self.lider_sequencia_atual: Optional[str] = None
        self.maior_sequencia_vitorias: int = 0
        self.dono_maior_sequencia: Optional[str] = None

    def registrar_rodada(
        self,
        jogador1_nome: str,
        jogador2_nome: str,
        escolha_p1: str,
        escolha_p2: str,
        valor_p1: int,
        valor_p2: int,
        prob_esperada_vencedor: float
    ) -> RegistroRodada:
        soma = valor_p1 + valor_p2
        resultado = "PAR" if soma % 2 == 0 else "ÍMPAR"

        if escolha_p1 == resultado:
            vencedor = jogador1_nome
            self.vitorias_p1 += 1
        else:
            vencedor = jogador2_nome
            self.vitorias_p2 += 1

        if resultado == "PAR":
            self.total_pares += 1
        else:
            self.total_impares += 1

        self.contagem_jogadas_p1[valor_p1] = self.contagem_jogadas_p1.get(valor_p1, 0) + 1
        self.contagem_jogadas_p2[valor_p2] = self.contagem_jogadas_p2.get(valor_p2, 0) + 1

        # Controle de streaks
        if vencedor == self.lider_sequencia_atual:
            self.sequencia_atual_vitorias += 1
        else:
            self.lider_sequencia_atual = vencedor
            self.sequencia_atual_vitorias = 1

        if self.sequencia_atual_vitorias > self.maior_sequencia_vitorias:
            self.maior_sequencia_vitorias = self.sequencia_atual_vitorias
            self.dono_maior_sequencia = vencedor

        registro = RegistroRodada(
            numero_rodada=len(self.rodadas) + 1,
            data_hora=datetime.now().strftime("%H:%M:%S"),
            jogador1_nome=jogador1_nome,
            jogador2_nome=jogador2_nome,
            escolha_p1=escolha_p1,
            escolha_p2=escolha_p2,
            valor_p1=valor_p1,
            valor_p2=valor_p2,
            soma=soma,
            resultado_paridade=resultado,
            vencedor=vencedor,
            prob_esperada_vencedor=prob_esperada_vencedor
        )
        self.rodadas.append(registro)
        return registro

    def obter_estatisticas(self) -> Dict[str, any]:
        total = len(self.rodadas)
        if total == 0:
            return {
                "total_rodadas": 0,
                "vitorias_p1": 0,
                "vitorias_p2": 0,
                "taxa_vitoria_p1": 0.0,
                "taxa_vitoria_p2": 0.0,
                "total_pares": 0,
                "total_impares": 0,
                "pct_pares": 0.0,
                "pct_impares": 0.0,
                "maior_sequencia": 0,
                "dono_maior_sequencia": None,
                "contagem_jogadas_p1": {},
                "contagem_jogadas_p2": {}
            }

        return {
            "total_rodadas": total,
            "vitorias_p1": self.vitorias_p1,
            "vitorias_p2": self.vitorias_p2,
            "taxa_vitoria_p1": (self.vitorias_p1 / total) * 100,
            "taxa_vitoria_p2": (self.vitorias_p2 / total) * 100,
            "total_pares": self.total_pares,
            "total_impares": self.total_impares,
            "pct_pares": (self.total_pares / total) * 100,
            "pct_impares": (self.total_impares / total) * 100,
            "maior_sequencia": self.maior_sequencia_vitorias,
            "dono_maior_sequencia": self.dono_maior_sequencia,
            "contagem_jogadas_p1": dict(sorted(self.contagem_jogadas_p1.items())),
            "contagem_jogadas_p2": dict(sorted(self.contagem_jogadas_p2.items()))
        }

    def limpar(self):
        """Reinicia os registros da sessão."""
        self.__init__()
