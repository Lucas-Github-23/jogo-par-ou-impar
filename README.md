# 🎲 Jogo de Par ou Ímpar em Python com Estatísticas Persistentes

Um joguinho clássico e direto de **Par ou Ímpar** feito em Python que calcula e exibe as **chances exatas de vitória** e armazena automaticamente o **histórico e estatísticas acumuladas** de todas as partidas em um arquivo `estatisticas.json`.

---

## 🎯 Funcionalidades

1. **Cálculo de Probabilidades**:
   - Espaço amostral exato para qualquer intervalo escolhido (0 a 5, 1 a 5, 0 a 10 ou personalizado).
   - Mostra a porcentagem exata de chance de vitória de cada jogador.
   - Demonstra que no intervalo de 1 a 5 (sem zero) quem joga PAR tem 52% de chance (13 combinações) contra 48% de ÍMPAR (12 combinações).

2. **Armazenamento Automático de Estatísticas**:
   - Ao final de cada partida, os dados são salvos automaticamente no arquivo `estatisticas.json`.
   - Registra total de partidas, total de rodadas, vitórias de cada jogador, quantas somas deram PAR vs ÍMPAR e o detalhe de cada jogada.

3. **Visualização do Histórico**:
   - Menu interativo com opção direta para ver estatísticas acumuladas e histórico das últimas partidas.
   - Opção para zerar as estatísticas quando desejar recomeçar.

---

## 🚀 Como Executar

```bash
python main.py
```

### Menu Principal:
```text
=======================================================
          JOGO DE PAR OU ÍMPAR COM ESTATÍSTICAS
=======================================================
1 - Jogar Partida
2 - Ver Histórico & Estatísticas Acumuladas
3 - Zerar Estatísticas
4 - Sair
=======================================================
```

---

## 📁 Onde os dados são salvos?

As estatísticas são salvas no arquivo:
- `estatisticas.json` (no mesmo diretório do jogo).
