# 🎲 Jogo de Par ou Ímpar com Motor Probabilístico & Combinatório

Um jogo completo, educativo e estatisticamente rigoroso de **Par ou Ímpar** desenvolvido em **Python 3**, projetado tanto para partidas casuais quanto para a exploração profunda do **Espaço Amostral**, **Combinatória** e a **Lei dos Grandes Números**.

Possui duas experiências completas em uma:
1. **Interface de Terminal (CLI)**: Rica em cores ANSI, caixas Unicode formatadas, artes ASCII, animações de contagem dramáticas e modo com entrada protegida/mascarada.
2. **Interface Web Moderna**: Design responsivo *Dark Mode*, *Glassmorphism*, sintetizador de áudio nativo via Web Audio API, matriz interativa de calor e simulador Monte Carlo com gráficos em tempo real (100% nativo, sem necessidade de instalar nenhuma biblioteca externa!).

---

## 🧮 A Matemática por trás do Jogo

Muitas pessoas acreditam que qualquer jogo de Par ou Ímpar é sempre 50% vs 50%. **Matematicamente, isso nem sempre é verdade!** Tudo depende do conjunto de números permitidos para cada jogador.

### 1. Espaço Amostral ($N$)
Para um Jogador 1 com opções no intervalo $[min_1, max_1]$ e Jogador 2 em $[min_2, max_2]$:
$$N = (max_1 - min_1 + 1) \times (max_2 - min_2 + 1)$$

Onde:
- $E_1, E_2$ são as contagens de números **pares** de cada jogador.
- $O_1, O_2$ são as contagens de números **ímpares** de cada jogador.

### 2. Condições de Paridade da Soma
- A soma $X_1 + X_2$ é **PAR** se:
  $$\text{(Par + Par)} \quad \text{OU} \quad \text{(Ímpar + Ímpar)}$$
  $$N_{par} = (E_1 \times E_2) + (O_1 \times O_2)$$

- A soma $X_1 + X_2$ é **ÍMPAR** se:
  $$\text{(Par + Ímpar)} \quad \text{OU} \quad \text{(Ímpar + Par)}$$
  $$N_{impar} = (E_1 \times O_2) + (O_1 \times E_2)$$

---

### 💡 Casos Clássicos e Curiosidades

| Cenário | Intervalos | Combinações Par | Combinações Ímpar | Probabilidade Par | Probabilidade Ímpar | Veredito |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **0 a 5 (Com Zero)** | $[0..5]$ vs $[0..5]$ | 18 | 18 | **50.00%** | **50.00%** | ⚖️ Perfeitamente Justo |
| **1 a 5 (Sem Zero)** | $[1..5]$ vs $[1..5]$ | **13** | 12 | **52.00%** | **48.00%** | ⚡ **Vantagem de PAR (+4%)** |
| **0 a 10 (Duas Mãos)**| $[0..10]$ vs $[0..10]$ | **61** | 60 | **50.41%** | **49.59%** | ⚡ **Vantagem de PAR (+0.82%)** |
| **1 a 6 (Dados RPG)** | $[1..6]$ vs $[1..6]$ | 18 | 18 | **50.00%** | **50.00%** | ⚖️ Perfeitamente Justo |

> **Por que 1 a 5 favorece o PAR?**
> No intervalo $\{1, 2, 3, 4, 5\}$, há 3 números ímpares $\{1, 3, 5\}$ e apenas 2 pares $\{2, 4\}$.
> Como Ímpar + Ímpar = Par ($3 \times 3 = 9$ combinações) e Par + Par = Par ($2 \times 2 = 4$ combinações), temos $9 + 4 = 13$ formas de a soma resultar em Par, contra $6 + 6 = 12$ formas de resultar em Ímpar!

---

## 🚀 Como Executar

O projeto utiliza **apenas a biblioteca padrão do Python** (`random`, `dataclasses`, `http.server`, `unittest`, etc.). Nenhuma dependência externa via `pip` é obrigatória!

### 1. Modo Terminal Interativo (CLI)
Para jogar diretamente no seu terminal ou PowerShell:
```bash
python main.py
```

### 2. Modo Web (Navegador)
Para iniciar a interface web visual moderna:
```bash
python main.py --web
```
Ou execute diretamente:
```bash
python server.py
```
O jogo abrirá automaticamente no seu navegador em `http://localhost:8000`.

### 3. Executando os Testes Automatizados
Para comprovar a precisão matemática analítica e estocástica:
```bash
python -m unittest tests.test_probabilidade
```

---

## 🎮 Modos e Funcionalidades

1. **👤 vs 🤖 Jogador contra IA**:
   - **Fácil**: Escolhas aleatórias e descontraídas.
   - **Médio**: IA baseada em viés estatístico do intervalo selecionado.
   - **Difícil (Adaptativa)**: Algoritmo que rastreia os vícios e padrões das jogadas recentes do usuário para antecipar a melhor resposta matemática.
2. **👥 vs 👤 Modo 2 Jogadores (Local PvP)**:
   - Dois jogadores no mesmo teclado com suporte a digitação mascarada/oculta para ninguém espiar os dedos do outro!
3. **📊 Laboratório de Probabilidades**:
   - Permite personalizar livremente os intervalos de ambos os jogadores e inspecionar a fórmula combinatória resolvida passo a passo.
4. **🎲 Simulador de Monte Carlo**:
   - Simule de 1.000 até 500.000 rodadas em milissegundos para observar a convergência empírica rumo à probabilidade teórica (Teorema Central do Limite).
5. **📐 Matriz de Combinações**:
   - Grade bidimensional colorida mapeando todas as somas possíveis $(x_1, x_2)$ e seus respectivos vencedores.
