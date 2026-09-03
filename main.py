import sys
import os

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

import argparse
from core.probabilidade import (
    calcular_probabilidade_exata,
    simular_monte_carlo
)
from core.jogo import JogoParOuImpar, DificuldadeIA
from core.historico import HistoricoSessao
from ui.terminal import (
    habilitar_ansi_windows,
    limpar_tela,
    imprimir_banner,
    imprimir_painel_probabilidade,
    imprimir_matriz_combinacoes,
    animacao_contagem,
    ler_inteiro,
    imprimir_resultado_rodada,
    imprimir_relatorio_sessao,
    Cores
)
import server


def configurar_intervalos_interativo(jogo: JogoParOuImpar):
    """Permite ao usuário escolher um preset ou customizar intervalos de dedos/números."""
    print(f"\n{Cores.BOLD}{Cores.B_YELLOW}⚙️  CONFIGURAÇÃO DE INTERVALOS (DEDOS/NÚMEROS):{Cores.RESET}")
    print("  [1] Clássico com Zero: 0 a 5 dedos (Justo: 50% vs 50%)")
    print("  [2] Clássico sem Zero: 1 a 5 dedos (⚡ Vantagem Par: 52% vs 48%)")
    print("  [3] Duas Mãos: 0 a 10 dedos (61 combinações Par vs 60 Ímpar)")
    print("  [4] Intervalos Personalizados (Definir min e max para cada um)")

    opcao = ler_inteiro(f"  {Cores.CYAN}Escolha uma opção (1-4) [Padrão 1]: {Cores.RESET}", 1, 4)

    if opcao == 1:
        jogo.atualizar_intervalos(0, 5, 0, 5)
    elif opcao == 2:
        jogo.atualizar_intervalos(1, 5, 1, 5)
    elif opcao == 3:
        jogo.atualizar_intervalos(0, 10, 0, 10)
    elif opcao == 4:
        print(f"\n{Cores.DIM}Intervalo do Jogador 1:{Cores.RESET}")
        min1 = ler_inteiro("  Mínimo P1: ", 0, 50)
        max1 = ler_inteiro(f"  Máximo P1 (>= {min1}): ", min1, 50)
        print(f"\n{Cores.DIM}Intervalo do Jogador 2 / Computador:{Cores.RESET}")
        min2 = ler_inteiro("  Mínimo P2: ", 0, 50)
        max2 = ler_inteiro(f"  Máximo P2 (>= {min2}): ", min2, 50)
        jogo.atualizar_intervalos(min1, max1, min2, max2)

    print(f"\n  {Cores.GREEN}✓ Intervalos configurados com sucesso!{Cores.RESET}")


def jogar_contra_ia(jogo: JogoParOuImpar):
    """Fluxo de jogo contra a inteligência artificial."""
    limpar_tela()
    imprimir_banner()
    print(f"{Cores.BOLD}{Cores.B_CYAN}🤖 MODO: JOGADOR VS COMPUTADOR{Cores.RESET}")

    configurar_intervalos_interativo(jogo)

    print(f"\n{Cores.BOLD}Escolha o nível da IA:{Cores.RESET}")
    print("  [1] Fácil: Jogadas e escolhas puramente aleatórias")
    print("  [2] Médio: Aproveita o viés estatístico do intervalo")
    print("  [3] Difícil: Adaptativa (prevê padrões das suas jogadas anteriores)")
    op_ia = ler_inteiro(f"  {Cores.CYAN}Nível da IA (1-3) [Padrão 2]: {Cores.RESET}", 1, 3)

    dificuldade = {
        1: DificuldadeIA.FACIL,
        2: DificuldadeIA.MEDIO,
        3: DificuldadeIA.DIFICIL
    }[op_ia]

    nome_jogador = input(f"\n{Cores.CYAN}Qual o seu nome? [Jogador 1]: {Cores.RESET}").strip() or "Jogador 1"
    nome_ia = f"IA ({dificuldade.capitalize()})"

    while True:
        limpar_tela()
        imprimir_banner()
        print(f"{Cores.BOLD}PLACAR ATUAL: {Cores.B_CYAN}{nome_jogador}: {jogo.placar_p1}{Cores.RESET}  x  {Cores.B_MAGENTA}{nome_ia}: {jogo.placar_p2}{Cores.RESET}")

        # Exibir painel de probabilidade do cenário atual
        imprimir_painel_probabilidade(jogo.obter_analise_probabilidade(), nome_jogador, nome_ia)

        # Escolha de Paridade
        print(f"{Cores.BOLD}Sua vez de escolher:{Cores.RESET}")
        print("  [1] PAR")
        print("  [2] ÍMPAR")
        escolha_num = ler_inteiro(f"  {Cores.CYAN}Digite 1 para PAR ou 2 para ÍMPAR: {Cores.RESET}", 1, 2)
        escolha_p1 = "PAR" if escolha_num == 1 else "ÍMPAR"
        escolha_ia = "ÍMPAR" if escolha_p1 == "PAR" else "PAR"

        print(f"\n  Você escolheu: {Cores.BOLD}{escolha_p1}{Cores.RESET}")
        print(f"  {nome_ia} ficou com: {Cores.BOLD}{escolha_ia}{Cores.RESET}")

        # Jogada de dedos/número
        val_p1 = ler_inteiro(
            f"\n  {nome_jogador}, digite seu número [{jogo.min_p1} a {jogo.max_p1}]: ",
            jogo.min_p1,
            jogo.max_p1
        )

        val_ia = jogo.decidir_jogada_ia(dificuldade, escolha_ia, nome_jogador)

        animacao_contagem()

        registro, _ = jogo.executar_rodada(
            nome_p1=nome_jogador,
            nome_p2=nome_ia,
            escolha_p1=escolha_p1,
            valor_p1=val_p1,
            valor_p2=val_ia
        )

        imprimir_resultado_rodada(registro, nome_jogador)

        continuar = input(f"{Cores.YELLOW}Deseja jogar outra rodada? (S/n): {Cores.RESET}").strip().lower()
        if continuar in ['n', 'nao', 'não', 'exit', 'q']:
            break


def jogar_dois_jogadores(jogo: JogoParOuImpar):
    """Fluxo de jogo local para 2 pessoas no mesmo teclado."""
    limpar_tela()
    imprimir_banner()
    print(f"{Cores.BOLD}{Cores.B_GREEN}👥 MODO: 2 JOGADORES (LOCAL PvP){Cores.RESET}")

    configurar_intervalos_interativo(jogo)

    nome_p1 = input(f"\n{Cores.CYAN}Nome do Jogador 1 [P1]: {Cores.RESET}").strip() or "Jogador 1"
    nome_p2 = input(f"{Cores.MAGENTA}Nome do Jogador 2 [P2]: {Cores.RESET}").strip() or "Jogador 2"

    while True:
        limpar_tela()
        imprimir_banner()
        print(f"{Cores.BOLD}PLACAR: {Cores.B_CYAN}{nome_p1}: {jogo.placar_p1}{Cores.RESET}  x  {Cores.B_MAGENTA}{nome_p2}: {jogo.placar_p2}{Cores.RESET}")

        imprimir_painel_probabilidade(jogo.obter_analise_probabilidade(), nome_p1, nome_p2)

        # Escolha de Paridade pelo P1
        print(f"{Cores.BOLD}{nome_p1}, escolha sua paridade:{Cores.RESET}")
        print("  [1] PAR")
        print("  [2] ÍMPAR")
        escolha_num = ler_inteiro(f"  {Cores.CYAN}Opção (1-2): {Cores.RESET}", 1, 2)
        escolha_p1 = "PAR" if escolha_num == 1 else "ÍMPAR"
        escolha_p2 = "ÍMPAR" if escolha_p1 == "PAR" else "PAR"

        print(f"\n  • {nome_p1}: {Cores.BOLD}{escolha_p1}{Cores.RESET}")
        print(f"  • {nome_p2}: {Cores.BOLD}{escolha_p2}{Cores.RESET}")

        print(f"\n{Cores.DIM}Os valores serão digitados de forma oculta para não haver espiadinha!{Cores.RESET}")

        val_p1 = ler_inteiro(
            f"  {nome_p1}, digite seu número [{jogo.min_p1} a {jogo.max_p1}]",
            jogo.min_p1,
            jogo.max_p1,
            oculto=True
        )

        val_p2 = ler_inteiro(
            f"  {nome_p2}, digite seu número [{jogo.min_p2} a {jogo.max_p2}]",
            jogo.min_p2,
            jogo.max_p2,
            oculto=True
        )

        animacao_contagem()

        registro, _ = jogo.executar_rodada(
            nome_p1=nome_p1,
            nome_p2=nome_p2,
            escolha_p1=escolha_p1,
            valor_p1=val_p1,
            valor_p2=val_p2
        )

        imprimir_resultado_rodada(registro, nome_p1)

        continuar = input(f"{Cores.YELLOW}Deseja jogar outra rodada? (S/n): {Cores.RESET}").strip().lower()
        if continuar in ['n', 'nao', 'não', 'exit', 'q']:
            break


def laboratório_probabilidade():
    """Modo investigativo: explora qualquer intervalo e gera matriz e métricas."""
    limpar_tela()
    imprimir_banner()
    print(f"{Cores.BOLD}{Cores.B_YELLOW}📊 LABORATÓRIO MATEMÁTICO & COMBINATÓRIO{Cores.RESET}")
    print("Analise detalhadamente qualquer configuração de dedos ou valores.\n")

    min1 = ler_inteiro("  Mínimo Jogador 1: ", 0, 50)
    max1 = ler_inteiro(f"  Máximo Jogador 1 (>= {min1}): ", min1, 50)
    min2 = ler_inteiro("  Mínimo Jogador 2: ", 0, 50)
    max2 = ler_inteiro(f"  Máximo Jogador 2 (>= {min2}): ", min2, 50)

    res = calcular_probabilidade_exata(min1, max1, min2, max2)

    limpar_tela()
    imprimir_banner()
    imprimir_painel_probabilidade(res, "P1", "P2")
    imprimir_matriz_combinacoes(res, "P1", "P2")

    input(f"{Cores.YELLOW}Pressione Enter para voltar ao menu principal...{Cores.RESET}")


def simulador_monte_carlo():
    """Executa simulação de Monte Carlo com até 1.000.000 de rodadas no terminal."""
    limpar_tela()
    imprimir_banner()
    print(f"{Cores.BOLD}{Cores.B_MAGENTA}🎲 SIMULADOR ESTOCÁSTICO DE MONTE CARLO{Cores.RESET}")
    print("Comprova a Lei dos Grandes Números através de simulações em larga escala.\n")

    min1 = ler_inteiro("  Mínimo Jogador 1: ", 0, 20)
    max1 = ler_inteiro(f"  Máximo Jogador 1 (>= {min1}): ", min1, 20)
    min2 = ler_inteiro("  Mínimo Jogador 2: ", 0, 20)
    max2 = ler_inteiro(f"  Máximo Jogador 2 (>= {min2}): ", min2, 20)

    print("\n  Quantas rodadas deseja simular?")
    print("  [1] 10.000 rodadas")
    print("  [2] 50.000 rodadas")
    print("  [3] 100.000 rodadas")
    print("  [4] 500.000 rodadas")
    op = ler_inteiro("  Escolha (1-4) [Padrão 2]: ", 1, 4)
    rounds_map = {1: 10000, 2: 50000, 3: 100000, 4: 500000}
    num_rodadas = rounds_map[op]

    print(f"\n{Cores.CYAN}⏳ Executando {num_rodadas:,} rodadas... Por favor aguarde...{Cores.RESET}")
    sim = simular_monte_carlo(min1, max1, min2, max2, num_rodadas=num_rodadas)

    print(f"\n{Cores.B_GREEN}✓ Simulação concluída com sucesso!{Cores.RESET}\n")
    print(f"  • Total de Rodadas: {sim['num_rodadas']:,}")
    print(f"  • Vitórias de PAR:   {sim['vitorias_par']:,} ({sim['pct_empirica_par']:.2f}%)  [Teórico: {sim['pct_teorica_par']:.2f}%]")
    print(f"  • Vitórias de ÍMPAR: {sim['vitorias_impar']:,} ({sim['pct_empirica_impar']:.2f}%)  [Teórico: {sim['pct_teorica_impar']:.2f}%]")
    print(f"  • Erro Absoluto Médio: {sim['erro_absoluto_pct']:.3f}%")
    print(f"  • Validação Teórica: {Cores.GREEN if sim['convergencia_ok'] else Cores.RED}{'CONVERGÊNCIA CONFIRMADA' if sim['convergencia_ok'] else 'DESVIO'}{Cores.RESET}")

    input(f"\n{Cores.YELLOW}Pressione Enter para retornar ao menu...{Cores.RESET}")


def menu_principal():
    """Loop do menu principal no terminal."""
    habilitar_ansi_windows()
    jogo = JogoParOuImpar()

    while True:
        limpar_tela()
        imprimir_banner()

        print(f"{Cores.BOLD}ESCOLHA UMA OPÇÃO:{Cores.RESET}\n")
        print(f"  {Cores.B_CYAN}[1]{Cores.RESET} 👤 vs 🤖 Jogar contra o Computador (IA)")
        print(f"  {Cores.B_GREEN}[2]{Cores.RESET} 👤 vs 👤 Modo 2 Jogadores (Local no mesmo teclado)")
        print(f"  {Cores.B_YELLOW}[3]{Cores.RESET} 📊 Laboratório de Probabilidades & Matriz de Combinações")
        print(f"  {Cores.B_MAGENTA}[4]{Cores.RESET} 🎲 Simulador Monte Carlo (Lei dos Grandes Números)")
        print(f"  {Cores.B_BLUE}[5]{Cores.RESET} 🌐 Iniciar Interface Web Moderna no Navegador")
        print(f"  {Cores.WHITE}[6]{Cores.RESET} 📈 Ver Estatísticas e Histórico da Sessão")
        print(f"  {Cores.RED}[7]{Cores.RESET} ❌ Sair")

        opcao = ler_inteiro(f"\n{Cores.BOLD}Digite sua opção (1-7): {Cores.RESET}", 1, 7)

        if opcao == 1:
            jogar_contra_ia(jogo)
        elif opcao == 2:
            jogar_dois_jogadores(jogo)
        elif opcao == 3:
            laboratório_probabilidade()
        elif opcao == 4:
            simulador_monte_carlo()
        elif opcao == 5:
            server.iniciar_servidor(abrir_navegador=True)
            input(f"\n{Cores.YELLOW}Pressione Enter para retornar ao menu principal...{Cores.RESET}")
        elif opcao == 6:
            limpar_tela()
            imprimir_banner()
            imprimir_relatorio_sessao(jogo.historico)
            input(f"{Cores.YELLOW}Pressione Enter para voltar ao menu...{Cores.RESET}")
        elif opcao == 7:
            limpar_tela()
            print(f"\n{Cores.B_CYAN}Obrigado por jogar Par ou Ímpar & Explorar a Matemática! Até logo! 👋{Cores.RESET}\n")
            break


def main():
    parser = argparse.ArgumentParser(description="Jogo de Par ou Ímpar com Motor Probabilístico")
    parser.add_argument("--web", action="store_true", help="Inicia diretamente o servidor e a interface Web no navegador")
    parser.add_argument("--port", type=int, default=8000, help="Porta para o servidor web (padrão 8000)")
    parser.add_argument("--no-browser", action="store_true", help="Não abre o navegador automaticamente no modo web")
    args = parser.parse_args()

    if args.web:
        server.iniciar_servidor(porta=args.port, abrir_navegador=not args.no_browser)
    else:
        menu_principal()


if __name__ == "__main__":
    main()
