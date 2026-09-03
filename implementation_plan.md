# Jogo de Par ou Ímpar com Motor Probabilístico em Python

Construção de uma aplicação completa, robusta e refinada de **Par ou Ímpar** em Python, que não apenas implementa o jogo tradicional com excelência, mas calcula rigorosamente o espaço amostral, as combinações e as probabilidades de vitória para ambos os jogadores em qualquer configuração de intervalo.

---

## 1. Visão Geral da Arquitetura

O projeto será estruturado de forma modular e limpa:

```
Projeto_Camile/
│
├── core/
│   ├── __init__.py
│   ├── probabilidade.py       # Motor matemático: combinatória exata, matriz de somas, Monte Carlo
│   ├── jogo.py                # Lógica do jogo, gerenciamento de estado, placar e estratégias de IA
│   └── historico.py           # Registro e análise estatística das jogadas da sessão
│
├── ui/
│   ├── __init__.py
│   ├── terminal.py            # Interface CLI rica em ANSI: artes ASCII, barras de probabilidade, matriz colorida
│   └── web/                   # Interface Web moderna embutida (Dark mode, glassmorphism, sem dependências externas)
│       ├── index.html
│       ├── style.css
│       └── app.js
│
├── tests/
│   ├── __init__.py
│   └── test_probabilidade.py  # Testes unitários para validar precisão matemática
│
├── server.py                  # Servidor web leve nativo (Python http.server) com API REST para o motor
├── main.py                    # Ponto de entrada com menu principal interativo e suporte a flag --web
└── README.md                  # Documentação completa com explicações matemáticas e guia de uso
```

---

## 2. O Motor Matemático & Probabilístico (`core/probabilidade.py`)

O jogo calculará de maneira exata e intuitiva:

1. **Espaço Amostral Combinatório ($N$)**:
   - Para intervalos $[min_1, max_1]$ e $[min_2, max_2]$:
     - Quantidade de pares ($E_1, E_2$) e ímpares ($O_1, O_2$) disponíveis para cada jogador.
     - Total de pares ordenados: $N = (max_1 - min_1 + 1) \times (max_2 - min_2 + 1)$.

2. **Cálculo Exato de Vitória**:
   - **Soma Par**: ocorre quando ambos jogam Par ou ambos jogam Ímpar.
     $$N_{par} = (E_1 \times E_2) + (O_1 \times O_2)$$
     $$P(Par) = \frac{N_{par}}{N} \times 100\%$$
   - **Soma Ímpar**: ocorre quando um joga Par e o outro Ímpar.
     $$N_{impar} = (E_1 \times O_2) + (O_1 \times E_2)$$
     $$P(Ímpar) = \frac{N_{impar}}{N} \times 100\%$$

3. **Desmistificação de Vieses Matemáticos (Curiosidade em Destaque)**:
   - **0 a 5 (Clássico com zero)**: 3 pares {0,2,4} e 3 ímpares {1,3,5} $\implies$ **50.00% Par vs 50.00% Ímpar** (Justo).
   - **1 a 5 (Clássico sem zero)**: 2 pares {2,4} e 3 ímpares {1,3,5}:
     $$N_{par} = (2 \times 2) + (3 \times 3) = 4 + 9 = 13 \text{ de } 25 \implies \mathbf{52.00\% \text{ PAR}}$$
     $$N_{impar} = (2 \times 3) + (3 \times 2) = 6 + 6 = 12 \text{ de } 25 \implies \mathbf{48.00\% \text{ ÍMPAR}}$$
     *(A maioria das pessoas não sabe que jogar de 1 a 5 dá 4% de vantagem para quem escolhe Par!)*
   - **0 a 10 (Duas mãos)**: 6 pares {0,2,4,6,8,10} e 5 ímpares {1,3,5,7,9}:
     $$N_{par} = 6 \times 6 + 5 \times 5 = 36 + 25 = 61 \text{ de } 121 \implies \mathbf{50.41\% \text{ PAR}}$$
     $$N_{impar} = 6 \times 5 + 5 \times 6 = 30 + 30 = 60 \text{ de } 121 \implies \mathbf{49.59\% \text{ ÍMPAR}}$$

4. **Matriz de Combinações Visual**:
   - Grade bidimensional mostrando todas as $N$ combinações possíveis de lances, cores indicando vitória de Par ou Ímpar e a distribuição das somas.

5. **Simulador de Monte Carlo**:
   - Simulação de até 1.000.000 de partidas virtuais para demonstrar a convergência empírica para a probabilidade teórica (Lei dos Grandes Números).

---

## 3. Funcionalidades de Jogabilidade (`core/jogo.py`)

- **Modo 1: Jogador vs Máquina (com Níveis de IA)**:
  - *Fácil (Aleatória)*: Escolhe valores e paridade de forma uniforme.
  - *Médio (Estatística Básica)*: Escolhe a paridade com base no viés matemático do intervalo selecionado.
  - *Difícil (Adaptativa / Bayesiana)*: Monitora o padrão de jogadas anteriores do jogador (ex: tendência a jogar mais ímpares ou números baixos) e calcula a melhor resposta para maximizar suas chances de vitória.
- **Modo 2: Dois Jogadores (Local PvP)**:
  - Permite dois amigos jogarem no mesmo teclado.
  - Modo "Mão Oculta" (mascarando a entrada no terminal com `getpass`/eco protegido) para ninguém ver o número do outro antes da revelação!
- **Modo 3: Laboratório de Probabilidade & Monte Carlo**:
  - Análise detalhada sem jogar, permitindo experimentar diferentes intervalos e ver gráficos e matrizes.
- **Estatísticas e Placar da Sessão**:
  - Total de vitórias, taxa real de vitórias vs taxa esperada teoricamente, histórico de rodadas.

---

## 4. Interfaces de Usuário

### A. Terminal CLI Premium (`ui/terminal.py`)
- Cores ANSI vibrantes, suporte a Windows Terminal e PowerShell.
- Barras de porcentagem interativas em ASCII/Unicode:
  `[█████████████░░░░░░░░░░░░] 52.00% PAR (13/25) | 48.00% ÍMPAR (12/25)`
- Animação estilizada de contagem: "1... 2... 3... e JÁ!"
- Matriz completa formatada com caixas Unicode (`┌──┬──┐`).

### B. Interface Web Moderna Opcional (`ui/web/` + `server.py`)
- Executada com comando simples: `python main.py --web` ou acessível pelo menu do terminal.
- 100% nativa em Python (usa `http.server` da biblioteca padrão, **sem necessidade de instalar Flask, FastAPI ou dependências externas**).
- Design profissional: Dark mode, gradientes elegantes, glassmorphism, visualizador dinâmico de matriz interativa, painel de probabilidades em tempo real.

---

## 5. Plano de Verificação

### Testes Automatizados
- Executar suíte de testes unitários `tests/test_probabilidade.py` cobrindo:
  - Intervalos simétricos (0 a 5, 0 a 1) -> exatos 50%/50%.
  - Intervalos assimétricos (1 a 5, 0 a 10, 1 a 6).
  - Soma de combinações ($N_{par} + N_{impar} == N_{total}$).
  - Simulação Monte Carlo convergindo com margem de erro $< 0.5\%$.

### Verificação Manual
- Executar `python main.py` para testar as partidas no terminal, modo 2 jogadores, modo IA e o laboratório.
- Iniciar o servidor web (`python main.py --web`) e verificar no navegador a renderização da interface e a comunicação com a API matemática.
