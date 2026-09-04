import sys
import os
import random
import json
from datetime import datetime

if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stdin, 'reconfigure'):
            sys.stdin.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

ARQUIVO_ESTATISTICAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "estatisticas.json")


def carregar_estatisticas():
    """Carrega as estatísticas do arquivo JSON ou inicializa uma estrutura vazia."""
    if not os.path.exists(ARQUIVO_ESTATISTICAS):
        return {
            "total_partidas": 0,
            "total_rodadas": 0,
            "vitorias_jogador": 0,
            "vitorias_computador": 0,
            "empates": 0,
            "total_somas_pares": 0,
            "total_somas_impares": 0,
            "historico_partidas": []
        }

    try:
        with open(ARQUIVO_ESTATISTICAS, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "total_partidas": 0,
            "total_rodadas": 0,
            "vitorias_jogador": 0,
            "vitorias_computador": 0,
            "empates": 0,
            "total_somas_pares": 0,
            "total_somas_impares": 0,
            "historico_partidas": []
        }


def salvar_estatisticas(dados):
    """Salva os dados consolidados no arquivo JSON."""
    try:
        with open(ARQUIVO_ESTATISTICAS, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"  [!] Aviso: Nao foi possivel salvar as estatisticas: {e}")


def registrar_partida(historico_rodadas, vitorias_jogador, vitorias_computador, intervalo_str):
    """Atualiza as estatísticas acumuladas com os resultados da partida recém-jogada."""
    stats = carregar_estatisticas()

    total_rodadas_partida = len(historico_rodadas)
    if total_rodadas_partida == 0:
        return

    stats["total_partidas"] += 1
    stats["total_rodadas"] += total_rodadas_partida
    stats["vitorias_jogador"] += vitorias_jogador
    stats["vitorias_computador"] += vitorias_computador

    if vitorias_jogador > vitorias_computador:
        vencedor = "Você"
    elif vitorias_computador > vitorias_jogador:
        vencedor = "Computador"
    else:
        vencedor = "Empate"
        stats["empates"] += 1

    for r in historico_rodadas:
        if r["resultado"] == "PAR":
            stats["total_somas_pares"] += 1
        else:
            stats["total_somas_impares"] += 1

    registro = {
        "partida_numero": stats["total_partidas"],
        "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "intervalo": intervalo_str,
        "placar": f"Você {vitorias_jogador} x {vitorias_computador} Computador",
        "vencedor": vencedor,
        "total_rodadas": total_rodadas_partida,
        "detalhes": historico_rodadas
    }

    stats["historico_partidas"].append(registro)
    salvar_estatisticas(stats)
    print(f"\n[✓] Partida registrada com sucesso no arquivo: '{os.path.basename(ARQUIVO_ESTATISTICAS)}'!")


def exibir_estatisticas():
    """Exibe um relatório detalhado e formatado de todas as partidas jogadas."""
    stats = carregar_estatisticas()
    total_partidas = stats.get("total_partidas", 0)
    total_rodadas = stats.get("total_rodadas", 0)

    print("\n" + "=" * 55)
    print("           HISTÓRICO & ESTATÍSTICAS ACUMULADAS")
    print("=" * 55)

    if total_partidas == 0:
        print("  Ainda não há partidas registradas.")
        print("  Jogue uma partida primeiro para gerar estatísticas!")
        print("=" * 55 + "\n")
        return

    v_jog = stats.get("vitorias_jogador", 0)
    v_pc = stats.get("vitorias_computador", 0)
    pares = stats.get("total_somas_pares", 0)
    impares = stats.get("total_somas_impares", 0)

    taxa_jog = (v_jog / total_rodadas * 100) if total_rodadas > 0 else 0
    taxa_pc = (v_pc / total_rodadas * 100) if total_rodadas > 0 else 0

    print(f"• Total de Partidas Realizadas: {total_partidas}")
    print(f"• Total de Rodadas Jogadas:     {total_rodadas}")
    print("-" * 55)
    print(f"• Vitórias de Você:            {v_jog:>3} rodadas ({taxa_jog:.1f}%)")
    print(f"• Vitórias do Computador:      {v_pc:>3} rodadas ({taxa_pc:.1f}%)")
    print("-" * 55)
    print(f"• Total de somas que deram PAR:   {pares:>3} ({((pares/total_rodadas)*100 if total_rodadas else 0):.1f}%)")
    print(f"• Total de somas que deram ÍMPAR: {impares:>3} ({((impares/total_rodadas)*100 if total_rodadas else 0):.1f}%)")
    print("-" * 55)

    print("\nÚLTIMAS PARTIDAS:")
    historico = stats.get("historico_partidas", [])
    ultimas = historico[-5:]  # Mostra até as últimas 5 partidas

    for p in ultimas:
        print(f"  Partida #{p['partida_numero']} [{p['data_hora']}]")
        print(f"    Intervalo: {p['intervalo']} | {p['placar']} | Vencedor: {p['vencedor']}")

    print(f"\n[i] Arquivo de dados completo: {ARQUIVO_ESTATISTICAS}")
    print("=" * 55 + "\n")


def zerar_estatisticas():
    """Permite ao usuário limpar o histórico de estatísticas."""
    confirmacao = input("\nTem certeza que deseja zerar todas as estatísticas? (s/N): ").strip().lower()
    if confirmacao in ['s', 'sim', 'y', 'yes']:
        dados_vazios = {
            "total_partidas": 0,
            "total_rodadas": 0,
            "vitorias_jogador": 0,
            "vitorias_computador": 0,
            "empates": 0,
            "total_somas_pares": 0,
            "total_somas_impares": 0,
            "historico_partidas": []
        }
        salvar_estatisticas(dados_vazios)
        print("[✓] Todas as estatísticas foram zeradas com sucesso!\n")
    else:
        print("Operação cancelada.\n")


def calcular_probabilidades(min_p1=0, max_p1=5, min_p2=0, max_p2=5):
    """Calcula as combinações possíveis e as probabilidades exatas de vitória para Par e Ímpar."""
    if min_p1 > max_p1:
        min_p1, max_p1 = max_p1, min_p1
    if min_p2 > max_p2:
        min_p2, max_p2 = max_p2, min_p2

    valores_p1 = list(range(min_p1, max_p1 + 1))
    valores_p2 = list(range(min_p2, max_p2 + 1))

    pares_p1 = sum(1 for x in valores_p1 if x % 2 == 0)
    impares_p1 = len(valores_p1) - pares_p1

    pares_p2 = sum(1 for x in valores_p2 if x % 2 == 0)
    impares_p2 = len(valores_p2) - pares_p2

    total_combinacoes = len(valores_p1) * len(valores_p2)

    combos_par = (pares_p1 * pares_p2) + (impares_p1 * impares_p2)
    combos_impar = (pares_p1 * impares_p2) + (impares_p1 * pares_p2)

    pct_par = (combos_par / total_combinacoes) * 100
    pct_impar = (combos_impar / total_combinacoes) * 100

    return {
        "min_p1": min_p1,
        "max_p1": max_p1,
        "min_p2": min_p2,
        "max_p2": max_p2,
        "valores_p1": valores_p1,
        "valores_p2": valores_p2,
        "pares_p1": pares_p1,
        "impares_p1": impares_p1,
        "pares_p2": pares_p2,
        "impares_p2": impares_p2,
        "total_combinacoes": total_combinacoes,
        "combos_par": combos_par,
        "combos_impar": combos_impar,
        "pct_par": pct_par,
        "pct_impar": pct_impar
    }


def exibir_tabela_combinacoes(dados):
    """Exibe uma tabela simples de todas as somas possíveis."""
    v1 = dados["valores_p1"]
    v2 = dados["valores_p2"]

    print("\nTABELA DE COMBINAÇÕES (Somas):")
    print("Linhas: Você | Colunas: Computador\n")

    header = " Você \\ PC |" + "".join(f"{x:^5}|" for x in v2)
    print(header)
    print("-" * len(header))

    for x1 in v1:
        linha = f"   {x1:^6} |"
        for x2 in v2:
            soma = x1 + x2
            paridade = "P" if soma % 2 == 0 else "I"
            linha += f" {soma:>2}({paridade})|"
        print(linha)
    print("Legenda: (P) = Soma Par, (I) = Soma Ímpar\n")


def exibir_painel_probabilidades(dados):
    """Apresenta as probabilidades calculadas de forma clara."""
    print("=" * 55)
    print("           ANÁLISE DE PROBABILIDADES")
    print("=" * 55)
    print(f"• Intervalo do Jogador:    {dados['min_p1']} a {dados['max_p1']} ({dados['pares_p1']} pares, {dados['impares_p1']} ímpares)")
    print(f"• Intervalo do Computador: {dados['min_p2']} a {dados['max_p2']} ({dados['pares_p2']} pares, {dados['impares_p2']} ímpares)")
    print(f"• Espaço Amostral:         {dados['total_combinacoes']} combinações possíveis")
    print("-" * 55)
    print(f"• Chance de dar PAR:   {dados['combos_par']:>2}/{dados['total_combinacoes']}  ({dados['pct_par']:.1f}%)")
    print(f"• Chance de dar ÍMPAR: {dados['combos_impar']:>2}/{dados['total_combinacoes']}  ({dados['pct_impar']:.1f}%)")

    if dados['pct_par'] == dados['pct_impar']:
        print("  [i] O jogo é 100% equilibrado (50% vs 50%).")
    elif dados['pct_par'] > dados['pct_impar']:
        diff = dados['pct_par'] - dados['pct_impar']
        print(f"  [*] Vantagem matemática: PAR tem +{diff:.1f}% de chance!")
        if dados['min_p1'] == 1 and dados['max_p1'] == 5 and dados['min_p2'] == 1 and dados['max_p2'] == 5:
            print("  [!] Curiosidade: Jogando de 1 a 5 sem o zero, PAR tem 13 chances contra 12 de Ímpar.")
    else:
        diff = dados['pct_impar'] - dados['pct_par']
        print(f"  [*] Vantagem matemática: ÍMPAR tem +{diff:.1f}% de chance!")
    print("=" * 55)


def jogar():
    print("\n" + "=" * 55)
    print("            NOVA PARTIDA DE PAR OU ÍMPAR")
    print("=" * 55)

    print("\nEscolha o intervalo de números (dedos):")
    print("1 - Clássico: 0 a 5 dedos (com zero)")
    print("2 - Sem Zero: 1 a 5 dedos (vantagem Par)")
    print("3 - Duas Mãos: 0 a 10 dedos")
    print("4 - Personalizado")
    opcao_intervalo = input("Opção [1]: ").strip()

    if opcao_intervalo == "2":
        dados = calcular_probabilidades(1, 5, 1, 5)
        intervalo_str = "1 a 5 dedos"
    elif opcao_intervalo == "3":
        dados = calcular_probabilidades(0, 10, 0, 10)
        intervalo_str = "0 a 10 dedos"
    elif opcao_intervalo == "4":
        try:
            min_val = int(input("Digite o menor número permitido (ex: 0): ") or 0)
            max_val = int(input("Digite o maior número permitido (ex: 5): ") or 5)
            dados = calcular_probabilidades(min_val, max_val, min_val, max_val)
            intervalo_str = f"{min_val} a {max_val}"
        except ValueError:
            print("Valor inválido. Usando padrão 0 a 5.")
            dados = calcular_probabilidades(0, 5, 0, 5)
            intervalo_str = "0 a 5 dedos"
    else:
        dados = calcular_probabilidades(0, 5, 0, 5)
        intervalo_str = "0 a 5 dedos"

    exibir_painel_probabilidades(dados)

    ver_tabela = input("\nDeseja ver a tabela com todas as combinações? (s/N): ").strip().lower()
    if ver_tabela in ['s', 'sim', 'y', 'yes']:
        exibir_tabela_combinacoes(dados)

    vitorias_jogador = 0
    vitorias_computador = 0
    rodada = 1
    historico_rodadas = []

    while True:
        print(f"\n--- RODADA {rodada} ---")
        print(f"Placar atual: Você {vitorias_jogador} x {vitorias_computador} Computador")

        while True:
            escolha = input("\nVocê escolhe [P]ar ou [I]mpar? ").strip().upper()
            if escolha in ['P', 'PAR']:
                escolha_jogador = "PAR"
                escolha_computador = "ÍMPAR"
                prob_jogador = dados['pct_par']
                prob_pc = dados['pct_impar']
                break
            elif escolha in ['I', 'Í', 'IMPAR', 'ÍMPAR']:
                escolha_jogador = "ÍMPAR"
                escolha_computador = "PAR"
                prob_jogador = dados['pct_impar']
                prob_pc = dados['pct_par']
                break
            print("Opção inválida! Digite P para Par ou I para Ímpar.")

        print(f"-> Você escolheu: {escolha_jogador} ({prob_jogador:.1f}% de chance de vitória)")
        print(f"-> Computador ficou com: {escolha_computador} ({prob_pc:.1f}% de chance de vitória)")

        while True:
            try:
                num_jogador = int(input(f"\nDigite o seu número ({dados['min_p1']} a {dados['max_p1']}): "))
                if dados['min_p1'] <= num_jogador <= dados['max_p1']:
                    break
                print(f"O número deve estar entre {dados['min_p1']} e {dados['max_p1']}.")
            except ValueError:
                print("Por favor, digite um número inteiro válido.")

        num_computador = random.randint(dados['min_p2'], dados['max_p2'])

        soma = num_jogador + num_computador
        resultado_paridade = "PAR" if soma % 2 == 0 else "ÍMPAR"

        print("\n" + "-" * 30)
        print(f"Você jogou:       {num_jogador}")
        print(f"Computador jogou: {num_computador}")
        print(f"Soma: {num_jogador} + {num_computador} = {soma} -> {resultado_paridade}!")
        print("-" * 30)

        if escolha_jogador == resultado_paridade:
            print(f">> PARABÉNS! Você venceu a rodada {rodada}!")
            vencedor_rodada = "Você"
            vitorias_jogador += 1
        else:
            print(f">> O Computador venceu a rodada {rodada}!")
            vencedor_rodada = "Computador"
            vitorias_computador += 1

        historico_rodadas.append({
            "rodada": rodada,
            "num_jogador": num_jogador,
            "num_computador": num_computador,
            "soma": soma,
            "resultado": resultado_paridade,
            "escolha_jogador": escolha_jogador,
            "vencedor_rodada": vencedor_rodada
        })

        rodada += 1
        jogar_novamente = input("\nDeseja jogar outra rodada nesta partida? (S/n): ").strip().lower()
        if jogar_novamente in ['n', 'nao', 'não', 'exit', 'q']:
            break

    print("\n" + "=" * 55)
    print("                FIM DA PARTIDA!")
    print("=" * 55)
    print(f"Total de rodadas: {rodada - 1}")
    print(f"Placar: Você {vitorias_jogador} x {vitorias_computador} Computador")
    if vitorias_jogador > vitorias_computador:
        print("[*] VOCÊ VENCEU ESTA PARTIDA!")
    elif vitorias_computador > vitorias_jogador:
        print("[*] O COMPUTADOR VENCEU ESTA PARTIDA!")
    else:
        print("[*] A PARTIDA TERMINOU EMPATADA!")
    print("=" * 55)

    # Armazenar estatísticas automaticamente no arquivo JSON
    registrar_partida(historico_rodadas, vitorias_jogador, vitorias_computador, intervalo_str)


import webbrowser

def abrir_painel_html():
    """Abre o arquivo index.html no navegador padrão."""
    caminho_html = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    if os.path.exists(caminho_html):
        print(f"\n[✓] Abrindo painel visual no seu navegador: {caminho_html}")
        webbrowser.open(f"file:///{caminho_html.replace(os.sep, '/')}")
    else:
        print("\n[!] Arquivo index.html não encontrado.")


def menu_principal():
    """Menu principal que permite jogar, ver histórico e gerenciar estatísticas."""
    while True:
        print("\n" + "=" * 55)
        print("          JOGO DE PAR OU ÍMPAR COM ESTATÍSTICAS")
        print("=" * 55)
        print("1 - Jogar Partida")
        print("2 - Ver Histórico no Terminal")
        print("3 - Abrir Painel Visual no Navegador (index.html)")
        print("4 - Zerar Estatísticas")
        print("5 - Sair")
        print("=" * 55)

        opcao = input("Escolha uma opção (1-5) [1]: ").strip()

        if opcao in ["1", ""]:
            jogar()
        elif opcao == "2":
            exibir_estatisticas()
        elif opcao == "3":
            abrir_painel_html()
        elif opcao == "4":
            zerar_estatisticas()
        elif opcao in ["5", "sair", "exit", "q"]:
            print("\nObrigado por jogar! Até a próxima!\n")
            break
        else:
            print("Opção inválida! Escolha entre 1 e 5.")


if __name__ == "__main__":
    menu_principal()
