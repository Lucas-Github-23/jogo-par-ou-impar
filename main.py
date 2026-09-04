import sys
import random

if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stdin, 'reconfigure'):
            sys.stdin.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass


def calcular_probabilidades(min_p1=0, max_p1=5, min_p2=0, max_p2=5):
    """
    Calcula as combinações possíveis e as probabilidades exatas de vitória para Par e Ímpar.
    """
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

    # Soma é PAR se: (Par + Par) OU (Ímpar + Ímpar)
    combos_par = (pares_p1 * pares_p2) + (impares_p1 * impares_p2)

    # Soma é ÍMPAR se: (Par + Ímpar) OU (Ímpar + Par)
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
        print("  [i] O jogo e 100% equilibrado (50% vs 50%).")
    elif dados['pct_par'] > dados['pct_impar']:
        diff = dados['pct_par'] - dados['pct_impar']
        print(f"  [*] Vantagem matematica: PAR tem +{diff:.1f}% de chance!")
        if dados['min_p1'] == 1 and dados['max_p1'] == 5 and dados['min_p2'] == 1 and dados['max_p2'] == 5:
            print("  [!] Curiosidade: Jogando de 1 a 5 sem o zero, PAR tem 13 chances contra 12 de Impar.")
    else:
        diff = dados['pct_impar'] - dados['pct_par']
        print(f"  [*] Vantagem matematica: IMPAR tem +{diff:.1f}% de chance!")
    print("=" * 55)


def jogar():
    print("\n" + "=" * 55)
    print("            JOGUINHO DE PAR OU IMPAR")
    print("=" * 55)

    # Configuracao de intervalo
    print("\nEscolha o intervalo de numeros (dedos):")
    print("1 - Classico: 0 a 5 dedos (com zero)")
    print("2 - Sem Zero: 1 a 5 dedos (vantagem Par)")
    print("3 - Duas Maos: 0 a 10 dedos")
    print("4 - Personalizado")
    opcao_intervalo = input("Opcao [1]: ").strip()

    if opcao_intervalo == "2":
        dados = calcular_probabilidades(1, 5, 1, 5)
    elif opcao_intervalo == "3":
        dados = calcular_probabilidades(0, 10, 0, 10)
    elif opcao_intervalo == "4":
        try:
            min_val = int(input("Digite o menor numero permitido (ex: 0): ") or 0)
            max_val = int(input("Digite o maior numero permitido (ex: 5): ") or 5)
            dados = calcular_probabilidades(min_val, max_val, min_val, max_val)
        except ValueError:
            print("Valor invalido. Usando padrao 0 a 5.")
            dados = calcular_probabilidades(0, 5, 0, 5)
    else:
        dados = calcular_probabilidades(0, 5, 0, 5)

    # Exibe a probabilidade de vitoria antes de comecar
    exibir_painel_probabilidades(dados)

    ver_tabela = input("\nDeseja ver a tabela com todas as combinacoes? (s/N): ").strip().lower()
    if ver_tabela in ['s', 'sim', 'y', 'yes']:
        exibir_tabela_combinacoes(dados)

    # Placar
    vitorias_jogador = 0
    vitorias_computador = 0
    rodada = 1

    while True:
        print(f"\n--- RODADA {rodada} ---")
        print(f"Placar atual: Voce {vitorias_jogador} x {vitorias_computador} Computador")

        # Escolha de Par ou Impar
        while True:
            escolha = input("\nVoce escolhe [P]ar ou [I]mpar? ").strip().upper()
            if escolha in ['P', 'PAR']:
                escolha_jogador = "PAR"
                escolha_computador = "IMPAR"
                prob_jogador = dados['pct_par']
                prob_pc = dados['pct_impar']
                break
            elif escolha in ['I', 'Í', 'IMPAR', 'ÍMPAR']:
                escolha_jogador = "IMPAR"
                escolha_computador = "PAR"
                prob_jogador = dados['pct_impar']
                prob_pc = dados['pct_par']
                break
            print("Opcao invalida! Digite P para Par ou I para Impar.")

        print(f"-> Voce escolheu: {escolha_jogador} ({prob_jogador:.1f}% de chance de vitoria)")
        print(f"-> Computador ficou com: {escolha_computador} ({prob_pc:.1f}% de chance de vitoria)")

        # Escolha do numero
        while True:
            try:
                num_jogador = int(input(f"\nDigite o seu numero ({dados['min_p1']} a {dados['max_p1']}): "))
                if dados['min_p1'] <= num_jogador <= dados['max_p1']:
                    break
                print(f"O numero deve estar entre {dados['min_p1']} e {dados['max_p1']}.")
            except ValueError:
                print("Por favor, digite um numero inteiro valido.")

        # Computador escolhe
        num_computador = random.randint(dados['min_p2'], dados['max_p2'])

        # Resultado
        soma = num_jogador + num_computador
        resultado_paridade = "PAR" if soma % 2 == 0 else "IMPAR"

        print("\n" + "-" * 30)
        print(f"Voce jogou:       {num_jogador}")
        print(f"Computador jogou: {num_computador}")
        print(f"Soma: {num_jogador} + {num_computador} = {soma} -> {resultado_paridade}!")
        print("-" * 30)

        if escolha_jogador == resultado_paridade:
            print(f">> PARABENS! Voce venceu a rodada {rodada}!")
            vitorias_jogador += 1
        else:
            print(f">> O Computador venceu a rodada {rodada}!")
            vitorias_computador += 1

        rodada += 1
        jogar_novamente = input("\nDeseja jogar outra rodada? (S/n): ").strip().lower()
        if jogar_novamente in ['n', 'nao', 'exit', 'q']:
            break

    # Resumo final
    print("\n" + "=" * 55)
    print("                FIM DE JOGO!")
    print("=" * 55)
    print(f"Total de rodadas: {rodada - 1}")
    print(f"Vitorias Voce:       {vitorias_jogador}")
    print(f"Vitorias Computador: {vitorias_computador}")
    if vitorias_jogador > vitorias_computador:
        print("[*] Resultado final: VOCE FOI O GRANDE CAMPEAO!")
    elif vitorias_computador > vitorias_jogador:
        print("[*] Resultado final: O COMPUTADOR VENCEU A DISPUTA!")
    else:
        print("[*] Resultado final: EMPATE!")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    jogar()
