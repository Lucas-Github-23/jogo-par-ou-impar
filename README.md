# 🎲 Jogo de Par ou Ímpar em Python com Estatísticas Persistentes & Painel Web

Um joguinho clássico e direto de **Par ou Ímpar** feito em Python que calcula e exibe as **chances exatas de vitória** para ambos os jogadores e armazena automaticamente o **histórico e estatísticas acumuladas** em um arquivo `estatisticas.json`.

O projeto conta também com um painel visual limpo em `index.html` para acompanhar o desempenho das partidas pelo navegador!

---

## 🎯 Funcionalidades

1. **Cálculo de Probabilidades**:
   - Calcula o espaço amostral exato para qualquer intervalo escolhido (0 a 5, 1 a 5, 0 a 10 ou personalizado).
   - Mostra a porcentagem exata de chance de vitória de cada jogador antes e durante as partidas.
   - Demonstra a curiosidade matemática: jogando de **1 a 5 (sem zero)**, quem escolhe **PAR tem 52% de chance (13 combinações)** contra **48% de ÍMPAR (12 combinações)**!

2. **Armazenamento Automático em JSON**:
   - Cada partida finalizada é registrada automaticamente em [`estatisticas.json`](estatisticas.json).
   - Salva data/hora, intervalo usado, total de rodadas, placar, vencedor e as jogadas individuais.

3. **Painel Visual Web (`index.html`)**:
   - Interface limpa e moderna para visualizar as estatísticas com cards de KPIs, barras comparativas de aproveitamento e lista de partidas.

---

## 📦 Pré-requisitos & Instalação de Bibliotecas

### Preciso instalar alguma biblioteca via `pip`?
**Não!** O projeto foi desenvolvido de forma inteligente utilizando **100% da Biblioteca Padrão do Python (Standard Library)**. 

Isso significa que:
- **Zero instalações com `pip`:** Não é necessário rodar `pip install` para nenhuma dependência.
- Todas as bibliotecas utilizadas (`random`, `json`, `http.server`, `socketserver`, `webbrowser`, `datetime`, `os`, `sys`) já vêm embutidas por padrão no Python 3.

### Como garantir que o Python está instalado:
O único requisito é ter o **Python 3.8 ou superior** instalado na máquina.

1. **Verifique se você já possui o Python:**
   Abra o seu terminal (Prompt de Comando ou PowerShell) e digite:
   ```bash
   python --version
   ```
   *(Se exibir `Python 3.x.x`, você já está pronto para rodar!)*

2. **Caso precise instalar o Python:**
   - **Windows:** Baixe pelo site oficial [python.org](https://www.python.org/downloads/) (marque a caixa *"Add python.exe to PATH"* durante a instalação) ou instale via PowerShell:
     ```bash
     winget install Python.Python.3.11
     ```
   - **Linux (Ubuntu/Debian):**
     ```bash
     sudo apt update && sudo apt install python3
     ```
   - **macOS:**
     ```bash
     brew install python
     ```

Basta executar no terminal:

```bash
python main.py
```

### Menu Principal do Jogo:
```text
=======================================================
          JOGO DE PAR OU ÍMPAR COM ESTATÍSTICAS
=======================================================
1 - Jogar Partida
2 - Ver Histórico no Terminal
3 - Abrir Painel Visual no Navegador (index.html)
4 - Zerar Estatísticas
5 - Sair
=======================================================
```

---

## 🌐 Como Rodar o Painel Web com `server.py`

### Por que usar o `server.py`?
Quando você abre um arquivo HTML dando duplo clique direto no Windows (`file:///...`), por motivos de segurança (política de **CORS**), os navegadores modernos bloqueiam o comando `fetch()` de ler arquivos locais como o `estatisticas.json`.

Ao rodar o servidor local com o `server.py`, a página ganha permissão para ler o `estatisticas.json` em tempo real via protocolo `http://`!

### Passo a passo para rodar:

1. **Inicie o servidor local no terminal:**
   ```bash
   python server.py
   ```

2. **Acesso automático:**
   - O script iniciará o servidor na porta `8000` e **abrirá automaticamente o seu navegador** no endereço:
     👉 **http://localhost:8000**
   - O `index.html` carregará na hora todos os dados de vitórias, rodadas e histórico de partidas!

3. **Atualizando os dados:**
   - Enquanto o servidor estiver rodando, continue jogando suas partidas no terminal (`python main.py`).
   - Para ver os novos resultados no navegador, basta clicar no botão **"Atualizar Dados"** no topo da página.

4. **Para encerrar o servidor:**
   - No terminal onde o `server.py` estiver rodando, pressione `Ctrl + C`.

---

> 💡 **Dica (Comando nativo alternativo):**  
> Você também pode subir o servidor nativo de uma linha do Python sem precisar de scripts extras:
> ```bash
> python -m http.server 8000
> ```
> E em seguida acessar `http://localhost:8000` no seu navegador.

---

## 📁 Estrutura de Arquivos

- `main.py`: Jogo principal no terminal com menus, cálculo de probabilidade e registro de dados.
- `server.py`: Servidor HTTP leve para servir o painel web e liberar a leitura do JSON sem restrições de CORS.
- `index.html`: Dashboard visual moderno para acompanhar o histórico de partidas.
- `estatisticas.json`: Base de dados acumulada de todas as partidas jogadas.
- `core/`: Módulos de regras e cálculo combinatório analítico.
