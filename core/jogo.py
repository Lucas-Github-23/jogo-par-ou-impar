"""
Lógica principal do Jogo de Par ou Ímpar.
Controla o fluxo de rodadas, configurações de partida e algoritmos de IA.
"""

import random
from typing import Tuple, Dict, Optional, List
from core.probabilidade import calcular_probabilidade_exata, ResultadoProbabilidade
from core.historico import HistoricoSessao, RegistroRodada


class DificuldadeIA:
    FACIL = "facil"         # Jogadas e escolhas puramente aleatórias
    MEDIO = "medio"         # Aproveita o viés matemático do intervalo
    DIFICIL = "dificil"     # IA adaptativa / preditiva baseada no perfil do jogador


class JogoParOuImpar:
    """Gerenciador de partidas de Par ou Ímpar."""

    def __init__(
        self,
        min_p1: int = 0,
        max_p1: int = 5,
        min_p2: int = 0,
        max_p2: int = 5,
        melhor_de: int = 0  # 0 significa rodadas livres contínuas; > 0 significa primeiro a N vitórias
    ):
        self.min_p1 = min_p1
        self.max_p1 = max_p1
        self.min_p2 = min_p2
        self.max_p2 = max_p2
        self.melhor_de = melhor_de

        self.historico = HistoricoSessao()
        self.probabilidade_atual = calcular_probabilidade_exata(min_p1, max_p1, min_p2, max_p2)

        self.placar_p1 = 0
        self.placar_p2 = 0
        self.partida_encerrada = False
        self.campeao: Optional[str] = None

    def atualizar_intervalos(self, min_p1: int, max_p1: int, min_p2: int, max_p2: int):
        """Atualiza a faixa de números e recalcula o espaço amostral."""
        self.min_p1 = min_p1
        self.max_p1 = max_p1
        self.min_p2 = min_p2
        self.max_p2 = max_p2
        self.probabilidade_atual = calcular_probabilidade_exata(min_p1, max_p1, min_p2, max_p2)

    def obter_analise_probabilidade(self) -> ResultadoProbabilidade:
        """Retorna o objeto com todos os cálculos analíticos da configuração atual."""
        return self.probabilidade_atual

    def decidir_paridade_ia(self, dificuldade: str = DificuldadeIA.MEDIO) -> str:
        """
        A IA decide entre PAR ou ÍMPAR.
        - Fácil: 50% de chance aleatória.
        - Médio/Difícil: Escolhe a opção que possui viés matemático favorável.
        """
        if dificuldade == DificuldadeIA.FACIL:
            return random.choice(["PAR", "ÍMPAR"])

        # Para Médio ou Difícil, joga conforme a vantagem do intervalo
        if self.probabilidade_atual.vantagem == "PAR":
            return "PAR"
        elif self.probabilidade_atual.vantagem == "ÍMPAR":
            return "ÍMPAR"
        else:
            return random.choice(["PAR", "ÍMPAR"])

    def decidir_jogada_ia(
        self,
        dificuldade: str,
        escolha_ia: str,
        nome_oponente: str = "Jogador 1"
    ) -> int:
        """
        Gera o número de dedos/valor jogado pela IA.
        - Fácil: Seleção aleatória uniforme no intervalo.
        - Médio: Leve ponderação nos números mais estratégicos.
        - Difícil: Avalia o histórico de jogadas do oponente para antecipar paridade.
        """
        opcoes = list(range(self.min_p2, self.max_p2 + 1))

        if dificuldade == DificuldadeIA.FACIL or len(self.historico.rodadas) < 2:
            return random.choice(opcoes)

        if dificuldade == DificuldadeIA.MEDIO:
            # Mistura aleatória com pesos uniformes
            return random.choice(opcoes)

        # Dificuldade Difícil (Adaptativa / Bayesiana)
        # Analisa a tendência recente do oponente (últimas até 5 rodadas)
        ultimas_rodadas = self.historico.rodadas[-5:]
        valores_oponente = [r.valor_p1 for r in ultimas_rodadas]

        # Frequência de paridade do oponente
        oponente_jogou_pares = sum(1 for v in valores_oponente if v % 2 == 0)
        prob_oponente_par = oponente_jogou_pares / len(valores_oponente)

        # Se a IA é PAR:
        #   Ela ganha se (IA_par E Op_par) OU (IA_impar E Op_impar)
        #   Se Op tem alta chance de jogar PAR (> 0.5), IA deve jogar PAR!
        #   Se Op tem alta chance de jogar ÍMPAR, IA deve jogar ÍMPAR!
        # Se a IA é ÍMPAR:
        #   Ela ganha se (IA_par E Op_impar) OU (IA_impar E Op_par)
        #   Se Op tem alta chance de jogar PAR (> 0.5), IA deve jogar ÍMPAR!
        #   Se Op tem alta chance de jogar ÍMPAR, IA deve jogar PAR!
        quer_par = (escolha_ia == "PAR" and prob_oponente_par >= 0.5) or \
                   (escolha_ia == "ÍMPAR" and prob_oponente_par < 0.5)

        candidatos = [x for x in opcoes if (x % 2 == 0 if quer_par else x % 2 != 0)]

        if not candidatos:
            candidatos = opcoes

        # Adiciona 20% de aleatoriedade para não ser perfeitamente previsível
        if random.random() < 0.20:
            return random.choice(opcoes)

        return random.choice(candidatos)

    def executar_rodada(
        self,
        nome_p1: str,
        nome_p2: str,
        escolha_p1: str,
        valor_p1: int,
        valor_p2: int
    ) -> Tuple[RegistroRodada, bool]:
        """
        Processa uma rodada completa de jogo.
        Retorna o registro da rodada e um booleano indicando se a partida/set encerrou.
        """
        escolha_p1 = escolha_p1.upper().strip()
        escolha_p2 = "ÍMPAR" if escolha_p1 == "PAR" else "PAR"

        # Probabilidade teórica de vitória do vencedor
        prob_esperada = self.probabilidade_atual.pct_par if (valor_p1 + valor_p2) % 2 == 0 else self.probabilidade_atual.pct_impar

        registro = self.historico.registrar_rodada(
            jogador1_nome=nome_p1,
            jogador2_nome=nome_p2,
            escolha_p1=escolha_p1,
            escolha_p2=escolha_p2,
            valor_p1=valor_p1,
            valor_p2=valor_p2,
            prob_esperada_vencedor=prob_esperada
        )

        if registro.vencedor == nome_p1:
            self.placar_p1 += 1
        else:
            self.placar_p2 += 1

        # Verificar término se houver modo melhor de N
        if self.melhor_de > 0:
            alvo_vitorias = (self.melhor_de // 2) + 1
            if self.placar_p1 >= alvo_vitorias:
                self.partida_encerrada = True
                self.campeao = nome_p1
            elif self.placar_p2 >= alvo_vitorias:
                self.partida_encerrada = True
                self.campeao = nome_p2

        return registro, self.partida_encerrada

    def reiniciar_placar(self):
        """Reinicia os placares da partida atual mantendo o histórico se desejado."""
        self.placar_p1 = 0
        self.placar_p2 = 0
        self.partida_encerrada = False
        self.campeao = None
