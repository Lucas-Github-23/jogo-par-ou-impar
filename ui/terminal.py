"""
Interface de Linha de Comando (CLI) Estilizada para Par ou Ímpar.
Utiliza códigos ANSI e caracteres Unicode para proporcionar uma experiência visual rica.
"""

import os
import sys
import time
import getpass

if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stdin, 'reconfigure'):
            sys.stdin.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
from typing import List, Optional
from core.probabilidade import ResultadoProbabilidade
from core.historico import HistoricoSessao, RegistroRodada


# Cores ANSI para terminais modernos
class Cores:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    # Cores de texto
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Cores Brilhantes
    B_RED = "\033[91m"
    B_GREEN = "\033[92m"
    B_YELLOW = "\033[93m"
    B_BLUE = "\033[94m"
    B_MAGENTA = "\033[95m"
    B_CYAN = "\033[96m"
    B_WHITE = "\033[97m"

    # Fundos
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_DARK = "\033[100m"


def habilitar_ansi_windows():
    """Garante suporte a ANSI e codificação UTF-8 no prompt do Windows."""
    if sys.platform == "win32":
        try:
            if hasattr(sys.stdout, 'reconfigure'):
                sys.stdout.reconfigure(encoding='utf-8')
            if hasattr(sys.stdin, 'reconfigure'):
                sys.stdin.reconfigure(encoding='utf-8')
        except Exception:
            pass
        try:
            os.system('')
        except Exception:
            pass


def limpar_tela():
    """Limpa a tela do terminal de forma segura."""
    if sys.stdout.isatty():
        os.system('cls' if os.name == 'nt' else 'clear')


def imprimir_banner():
    """Exibe o cabeçalho estilizado do jogo com arte ASCII."""
    banner = f"""
{Cores.B_CYAN}  ██████╗  █████╗ ██████╗      ██████╗ ██╗   ██╗    ██╗███╗   ███╗██████╗  █████╗ ██████╗ 
  ██╔══██╗██╔══██╗██╔══██╗    ██╔═══██╗██║   ██║    ██║████╗ ████║██╔══██╗██╔══██╗██╔══██╗
  ██████╔╝███████║██████╔╝    ██║   ██║██║   ██║    ██║██╔████╔██║██████╔╝███████║██████╔╝
  ██╔═══╝ ██╔══██║██╔══██╗    ██║   ██║██║   ██║    ██║██║╚██╔╝██║██╔═══╝ ██╔══██║██╔══██╗
  ██║     ██║  ██║██║  ██║    ╚██████╔╝╚██████╔╝    ██║██║ ╚═╝ ██║██║     ██║  ██║██║  ██║
  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝     ╚═════╝  ╚═════╝     ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝{Cores.RESET}
{Cores.B_YELLOW}             [ PROBABILITY & COMBINATORICS ENGINE - EDITION 2026 ]{Cores.RESET}
"""
    print(banner)


def barra_progresso_visual(pct_par: float, pct_impar: float, largura: int = 32) -> str:
    """Gera uma barra visual colorida representando as probabilidades relativas."""
    blocos_par = int(round((pct_par / 100.0) * largura))
    blocos_impar = largura - blocos_par

    barra_par = f"{Cores.B_CYAN}{'█' * blocos_par}"
    barra_impar = f"{Cores.B_MAGENTA}{'█' * blocos_impar}{Cores.RESET}"
    return f"[{barra_par}{barra_impar}]"


def imprimir_painel_probabilidade(
    res: ResultadoProbabilidade,
    nome_p1: str = "Jogador 1",
    nome_p2: str = "Jogador 2"
):
    """Renderiza um painel estético com a análise probabilística detalhada."""
    largura = 70
    linha_div = "─" * largura

    print(f"\n{Cores.B_WHITE}╭{linha_div}╮{Cores.RESET}")
    titulo = " 📊 ANÁLISE PROBABILÍSTICA EXATA DO ESPAÇO AMOSTRAL "
    print(f"{Cores.B_WHITE}│{Cores.BOLD}{Cores.B_YELLOW}{titulo.center(largura)}{Cores.RESET}{Cores.B_WHITE}│{Cores.RESET}")
    print(f"{Cores.B_WHITE}├{linha_div}┤{Cores.RESET}")

    # Configuração de intervalos
    info_intervalos = (
        f"  • {Cores.BOLD}{nome_p1}:{Cores.RESET} [{res.min1} a {res.max1}] ({res.pares_p1} pares, {res.impares_p1} ímpares)\n"
        f"  • {Cores.BOLD}{nome_p2}:{Cores.RESET} [{res.min2} a {res.max2}] ({res.pares_p2} pares, {res.impares_p2} ímpares)\n"
        f"  • {Cores.BOLD}Total de Combinações Possíveis:{Cores.RESET} {res.total_combinacoes} pares ordenados"
    )
    for linha in info_intervalos.split('\n'):
        print(f"{Cores.B_WHITE}│{Cores.RESET} {linha:<{largura+10}}{Cores.B_WHITE}│{Cores.RESET}")

    print(f"{Cores.B_WHITE}├{linha_div}┤{Cores.RESET}")

    # Barra visual e porcentagens
    barra = barra_progresso_visual(res.pct_par, res.pct_impar, largura=30)
    print(f"{Cores.B_WHITE}│{Cores.RESET}  Distribuição Teórica: {barra}                      {Cores.B_WHITE}│{Cores.RESET}")
    
    txt_par = f"{Cores.B_CYAN}{Cores.BOLD}PAR:{Cores.RESET}   {res.combinacoes_par:>3}/{res.total_combinacoes} ({res.pct_par:.2f}%)"
    txt_impar = f"{Cores.B_MAGENTA}{Cores.BOLD}ÍMPAR:{Cores.RESET} {res.combinacoes_impar:>3}/{res.total_combinacoes} ({res.pct_impar:.2f}%)"
    print(f"{Cores.B_WHITE}│{Cores.RESET}  {txt_par}     │     {txt_impar}          {Cores.B_WHITE}│{Cores.RESET}")

    # Veredito
    if res.vantagem == "EQUILIBRADO":
        veredito = f"{Cores.B_GREEN}{Cores.BOLD}⚖️  JOGO 100% JUSTO (50.00% vs 50.00%){Cores.RESET}"
    elif res.vantagem == "PAR":
        veredito = f"{Cores.B_CYAN}{Cores.BOLD}⚡ VANTAGEM MATEMÁTICA: PAR (+{res.diferenca_pct:.2f}% de margem){Cores.RESET}"
    else:
        veredito = f"{Cores.B_MAGENTA}{Cores.BOLD}⚡ VANTAGEM MATEMÁTICA: ÍMPAR (+{res.diferenca_pct:.2f}% de margem){Cores.RESET}"

    print(f"{Cores.B_WHITE}├{linha_div}┤{Cores.RESET}")
    print(f"{Cores.B_WHITE}│{Cores.RESET}  {veredito:<{largura+15}}{Cores.B_WHITE}│{Cores.RESET}")

    # Curiosidade / Explicação Didática (quebra em linhas se necessário)
    print(f"{Cores.B_WHITE}│{Cores.RESET}  {Cores.DIM}{Cores.ITALIC}💡 {res.explicacao_didatica[:65]}{Cores.RESET} {Cores.B_WHITE}│{Cores.RESET}")
    if len(res.explicacao_didatica) > 65:
        print(f"{Cores.B_WHITE}│{Cores.RESET}     {Cores.DIM}{Cores.ITALIC}{res.explicacao_didatica[65:130]}{Cores.RESET} {Cores.B_WHITE}│{Cores.RESET}")
    if len(res.explicacao_didatica) > 130:
        print(f"{Cores.B_WHITE}│{Cores.RESET}     {Cores.DIM}{Cores.ITALIC}{res.explicacao_didatica[130:195]}{Cores.RESET} {Cores.B_WHITE}│{Cores.RESET}")

    print(f"{Cores.B_WHITE}╰{linha_div}╯{Cores.RESET}\n")


def imprimir_matriz_combinacoes(res: ResultadoProbabilidade, nome_p1: str = "P1", nome_p2: str = "P2"):
    """Exibe a matriz de somas bidimensional colorida."""
    valores_p1 = list(range(res.min1, res.max1 + 1))
    valores_p2 = list(range(res.min2, res.max2 + 1))

    if len(valores_p1) > 12 or len(valores_p2) > 12:
        print(f"{Cores.YELLOW}A matriz é muito grande ({len(valores_p1)}x{len(valores_p2)}) para renderização no terminal.{Cores.RESET}")
        return

    print(f"\n{Cores.BOLD}{Cores.B_YELLOW}🎲 MATRIZ DE COMBINAÇÕES ({nome_p1} ↓ linhas vs {nome_p2} → colunas):{Cores.RESET}")
    print(f"{Cores.DIM}Legenda: {Cores.B_CYAN}[P] Soma Par{Cores.RESET} {Cores.DIM}| {Cores.B_MAGENTA}[I] Soma Ímpar{Cores.RESET}\n")

    # Cabeçalho das colunas (P2)
    header = f"   {nome_p1[:4]:<4}│"
    for x2 in valores_p2:
        header += f" {x2:^5} "
    print(header)
    print("   " + "─" * 5 + "┼" + ("───────" * len(valores_p2)))

    # Linhas (P1)
    for i, x1 in enumerate(valores_p1):
        linha_str = f"   {x1:^4}│"
        for j, x2 in enumerate(valores_p2):
            item = res.matriz[i][j]
            soma = item["soma"]
            if item["eh_par"]:
                celula = f"{Cores.B_CYAN}{soma:>2}(P){Cores.RESET}"
            else:
                celula = f"{Cores.B_MAGENTA}{soma:>2}(I){Cores.RESET}"
            linha_str += f"  {celula} "
        print(linha_str)
    print()


def animacao_contagem():
    """Animação dramática de contagem para o jogo."""
    frases = [
        f"{Cores.B_YELLOW}UM...{Cores.RESET}",
        f"{Cores.B_CYAN}DOIS...{Cores.RESET}",
        f"{Cores.B_GREEN}TRÊS...{Cores.RESET}",
        f"{Cores.B_RED}{Cores.BOLD}E JÁ! ✋🤚{Cores.RESET}\n"
    ]
    sys.stdout.write("\n")
    for f in frases:
        sys.stdout.write(f"  {f}  ")
        sys.stdout.flush()
        time.sleep(0.4)
    print()


def ler_jogada_mascarada(prompt: str, min_val: int, max_val: int) -> int:
    """Lê um número inteiro de forma oculta para modo 2 jogadores no mesmo teclado."""
    while True:
        try:
            entrada = getpass.getpass(f"{prompt} (oculto para oponente): ")
            val = int(entrada.strip())
            if min_val <= val <= max_val:
                print(f"  {Cores.GREEN}✓ Número registrado com segurança!{Cores.RESET}")
                return val
            else:
                print(f"  {Cores.RED}Número fora do intervalo permitido ({min_val} a {max_val}). Tente novamente.{Cores.RESET}")
        except ValueError:
            print(f"  {Cores.RED}Por favor, digite um número inteiro válido.{Cores.RESET}")


def ler_inteiro(prompt: str, min_val: int, max_val: int, oculto: bool = False) -> int:
    """Lê um número garantindo validação e suporte a modo oculto."""
    if oculto:
        return ler_jogada_mascarada(prompt, min_val, max_val)

    while True:
        try:
            val = int(input(prompt).strip())
            if min_val <= val <= max_val:
                return val
            print(f"  {Cores.RED}Por favor, digite um valor entre {min_val} e {max_val}.{Cores.RESET}")
        except ValueError:
            print(f"  {Cores.RED}Entrada inválida! Digite um número inteiro.{Cores.RESET}")


def imprimir_resultado_rodada(registro: RegistroRodada, nome_usuario: str):
    """Exibe o resultado da rodada de forma cinematográfica."""
    soma = registro.soma
    cor_res = Cores.B_CYAN if registro.resultado_paridade == "PAR" else Cores.B_MAGENTA

    print(f"\n{Cores.BOLD}╭───────────────────────────────────────────────────╮{Cores.RESET}")
    print(f"{Cores.BOLD}│                💥 RESULTADO DO CONFRONTO          │{Cores.RESET}")
    print(f"{Cores.BOLD}├───────────────────────────────────────────────────┤{Cores.RESET}")
    print(f"│  {registro.jogador1_nome} jogou: {Cores.BOLD}{registro.valor_p1}{Cores.RESET}  (Escolha: {registro.escolha_p1})")
    print(f"│  {registro.jogador2_nome} jogou: {Cores.BOLD}{registro.valor_p2}{Cores.RESET}  (Escolha: {registro.escolha_p2})")
    print(f"{Cores.BOLD}├───────────────────────────────────────────────────┤{Cores.RESET}")
    print(f"│  SOMA: {registro.valor_p1} + {registro.valor_p2} = {Cores.BOLD}{soma}{Cores.RESET} ➔ {cor_res}{Cores.BOLD}DEU {registro.resultado_paridade}!{Cores.RESET}")
    
    if registro.vencedor == nome_usuario:
        print(f"│  🏆 {Cores.B_GREEN}{Cores.BOLD}PARABÉNS! {registro.vencedor} VENCEU ESTA RODADA!{Cores.RESET}")
    else:
        print(f"│  👑 {Cores.B_YELLOW}{Cores.BOLD}VITÓRIA DE: {registro.vencedor}!{Cores.RESET}")

    print(f"{Cores.BOLD}╰───────────────────────────────────────────────────╯{Cores.RESET}\n")


def imprimir_relatorio_sessao(historico: HistoricoSessao):
    """Apresenta o balanço estatístico final da sessão."""
    stats = historico.obter_estatisticas()
    if stats["total_rodadas"] == 0:
        print(f"{Cores.YELLOW}Nenhuma rodada foi jogada ainda.{Cores.RESET}")
        return

    print(f"\n{Cores.B_WHITE}╔════════════════════════════════════════════════════════╗{Cores.RESET}")
    print(f"{Cores.B_WHITE}║           📈 RELATÓRIO ESTATÍSTICO DA SESSÃO           ║{Cores.RESET}")
    print(f"{Cores.B_WHITE}╠════════════════════════════════════════════════════════╣{Cores.RESET}")
    print(f"║  Total de Rodadas Realizadas: {stats['total_rodadas']:<24} ║")
    print(f"║  Vitórias Jogador 1: {stats['vitorias_p1']} ({stats['taxa_vitoria_p1']:.1f}%)                         ║")
    print(f"║  Vitórias Jogador 2: {stats['vitorias_p2']} ({stats['taxa_vitoria_p2']:.1f}%)                         ║")
    print(f"║  Ocorrências de PAR:   {stats['total_pares']} ({stats['pct_pares']:.1f}%)                         ║")
    print(f"║  Ocorrências de ÍMPAR: {stats['total_impares']} ({stats['pct_impares']:.1f}%)                         ║")
    if stats["dono_maior_sequencia"]:
        print(f"║  Maior Sequência: {stats['maior_sequencia']} vitórias seguidas ({stats['dono_maior_sequencia'][:12]})   ║")
    print(f"{Cores.B_WHITE}╚════════════════════════════════════════════════════════╝{Cores.RESET}\n")
