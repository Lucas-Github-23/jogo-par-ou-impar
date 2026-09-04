# 🎲 Jogo de Par ou Ímpar em Python com Cálculo de Probabilidade

Um joguinho clássico e direto de **Par ou Ímpar** feito em Python que calcula e exibe as **chances exatas de vitória** para ambos os jogadores antes e durante as partidas.

---

## 🎯 Como Funciona

1. **Cálculo de Probabilidades**:
   - O jogo analisa o intervalo de números permitidos (por exemplo, de 0 a 5 dedos).
   - Calcula o número total de combinações possíveis (espaço amostral).
   - Conta quantas somas resultam em **PAR** e quantas em **ÍMPAR**.
   - Mostra a porcentagem exata de chance de vitória de cada jogador.

2. **Curiosidade Matemática**:
   - No clássico **0 a 5 dedos (com zero)**: São 36 combinações (18 pares e 18 ímpares) $\implies$ **50% vs 50%**.
   - No clássico **1 a 5 dedos (sem zero)**: Há 3 números ímpares (1, 3, 5) e 2 pares (2, 4) para cada um. O resultado é 13 somas pares e 12 ímpares $\implies$ **52% para PAR contra 48% para ÍMPAR**!

3. **Partidas**:
   - Escolha Par ou Ímpar.
   - Digite o seu número.
   - O computador escolhe o dele.
   - O jogo calcula a soma, confere a paridade e atualiza o placar.

---

## 🚀 Como Executar

Não precisa instalar nenhuma biblioteca adicional, basta ter o Python instalado:

```bash
python main.py
```

---

## 📋 Exemplo de Execução no Terminal

```text
=======================================================
           ANÁLISE DE PROBABILIDADES
=======================================================
• Intervalo do Jogador:    0 a 5 (3 pares, 3 ímpares)
• Intervalo do Computador: 0 a 5 (3 pares, 3 ímpares)
• Espaço Amostral:         36 combinações possíveis
-------------------------------------------------------
• Chance de dar PAR:   18/36  (50.0%)
• Chance de dar ÍMPAR: 18/36  (50.0%)
⚖️  O jogo é 100% equilibrado (50% vs 50%).
=======================================================
```
