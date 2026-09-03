/**
 * Par ou Ímpar - Frontend Controller & Mathematical Dashboard
 */

// Web Audio API Sound Synthesizer (Zero dependências externas)
const SoundFX = {
    ctx: null,
    init() {
        if (!this.ctx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (AudioContext) {
                this.ctx = new AudioContext();
            }
        }
    },
    playTone(freq, type = 'sine', duration = 0.1, gainVal = 0.15) {
        try {
            this.init();
            if (!this.ctx) return;
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = type;
            osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
            gain.gain.setValueAtTime(gainVal, this.ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + duration);
            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start();
            osc.stop(this.ctx.currentTime + duration);
        } catch (e) {
            console.warn('Audio FX error:', e);
        }
    },
    click() { this.playTone(400, 'sine', 0.05, 0.1); },
    chipSelect() { this.playTone(550, 'triangle', 0.08, 0.12); },
    win() {
        this.playTone(523.25, 'triangle', 0.15, 0.2); // C5
        setTimeout(() => this.playTone(659.25, 'triangle', 0.15, 0.2), 120); // E5
        setTimeout(() => this.playTone(783.99, 'triangle', 0.25, 0.25), 240); // G5
    },
    lose() {
        this.playTone(330, 'sawtooth', 0.15, 0.15);
        setTimeout(() => this.playTone(293.66, 'sawtooth', 0.25, 0.15), 150);
    }
};

// Estado Global da Aplicação
const AppState = {
    modo: 'ai', // 'ai' ou 'pvp'
    dificuldadeIA: 'medio',
    p1Nome: 'Você',
    p2Nome: 'Computador',
    p1Escolha: 'PAR',
    p1Valor: 2,
    min1: 0,
    max1: 5,
    min2: 0,
    max2: 5,
    placarP1: 0,
    placarP2: 0,
    historicoRodadas: []
};

// ==========================================
// MÁQUINA MATEMÁTICA CLIENT-SIDE (FALLBACK & LIVE)
// ==========================================
function calcularMatematica(min1, max1, min2, max2) {
    if (min1 > max1) [min1, max1] = [max1, min1];
    if (min2 > max2) [min2, max2] = [max2, min2];

    const vals1 = [];
    for (let i = min1; i <= max1; i++) vals1.push(i);

    const vals2 = [];
    for (let i = min2; i <= max2; i++) vals2.push(i);

    const pares1 = vals1.filter(x => x % 2 === 0).length;
    const impares1 = vals1.length - pares1;

    const pares2 = vals2.filter(x => x % 2 === 0).length;
    const impares2 = vals2.length - pares2;

    const totalCombos = vals1.length * vals2.length;
    const combosPar = (pares1 * pares2) + (impares1 * impares2);
    const combosImpar = (pares1 * impares2) + (impares1 * pares2);

    const pctPar = (combosPar / totalCombos) * 100;
    const pctImpar = (combosImpar / totalCombos) * 100;

    let vantagem = 'EQUILIBRADO';
    if (combosPar > combosImpar) vantagem = 'PAR';
    else if (combosImpar > combosPar) vantagem = 'ÍMPAR';

    const diferencaPct = Math.abs(pctPar - pctImpar);

    // Distribuição de somas
    const distSomas = {};
    const matriz = [];

    for (let i = 0; i < vals1.length; i++) {
        const row = [];
        const x1 = vals1[i];
        for (let j = 0; j < vals2.length; j++) {
            const x2 = vals2[j];
            const soma = x1 + x2;
            const ehPar = (soma % 2 === 0);
            distSomas[soma] = (distSomas[soma] || 0) + 1;
            row.push({ x1, x2, soma, ehPar });
        }
        matriz.push(row);
    }

    return {
        min1, max1, min2, max2,
        vals1, vals2,
        pares1, impares1, pares2, impares2,
        totalCombos, combosPar, combosImpar,
        pctPar, pctImpar, vantagem, diferencaPct,
        distSomas, matriz
    };
}

// ==========================================
// INICIALIZAÇÃO & TABS
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initGameControls();
    initLab();
    initMonteCarlo();
    updateGameOdds();
    renderNumberChips();
    renderMatrix();
});

function initTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const panes = document.querySelectorAll('.tab-pane');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            SoundFX.click();
            tabBtns.forEach(b => b.classList.remove('active'));
            panes.forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            const targetId = btn.getAttribute('data-tab');
            const targetPane = document.getElementById(targetId);
            if (targetPane) targetPane.classList.add('active');

            if (targetId === 'matrix-tab') {
                renderMatrix();
            } else if (targetId === 'lab-tab') {
                updateLab();
            }
        });
    });
}

// ==========================================
// SEÇÃO DO JOGO
// ==========================================
function initGameControls() {
    // Escolha de Paridade
    const btnPar = document.getElementById('btn-choose-par');
    const btnImpar = document.getElementById('btn-choose-impar');

    btnPar.addEventListener('click', () => {
        SoundFX.click();
        btnPar.classList.add('active-parity');
        btnImpar.classList.remove('active-parity');
        AppState.p1Escolha = 'PAR';
    });

    btnImpar.addEventListener('click', () => {
        SoundFX.click();
        btnImpar.classList.add('active-parity');
        btnPar.classList.remove('active-parity');
        AppState.p1Escolha = 'ÍMPAR';
    });

    // Modos de Jogo (AI vs PvP)
    const modeRadios = document.querySelectorAll('input[name="game-mode"]');
    const aiDiffGroup = document.getElementById('ai-difficulty-group');
    const pvpBox = document.getElementById('pvp-box');
    const labelP2 = document.getElementById('label-p2');

    modeRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            SoundFX.click();
            AppState.modo = e.target.value;
            if (AppState.modo === 'pvp') {
                aiDiffGroup.classList.add('hidden');
                pvpBox.classList.remove('hidden');
                labelP2.textContent = 'Jogador 2';
                AppState.p2Nome = 'Jogador 2';
            } else {
                aiDiffGroup.classList.remove('hidden');
                pvpBox.classList.add('hidden');
                labelP2.textContent = 'Computador';
                AppState.p2Nome = 'Computador';
            }
        });
    });

    // Revelar senha temporariamente no PvP
    const btnReveal = document.getElementById('btn-reveal-temp');
    const pvpSecretInput = document.getElementById('pvp-input-p2');
    if (btnReveal && pvpSecretInput) {
        btnReveal.addEventListener('mousedown', () => pvpSecretInput.type = 'text');
        btnReveal.addEventListener('mouseup', () => pvpSecretInput.type = 'password');
        btnReveal.addEventListener('mouseleave', () => pvpSecretInput.type = 'password');
    }

    // Presets
    const presets = document.querySelectorAll('.btn-preset');
    presets.forEach(p => {
        p.addEventListener('click', () => {
            SoundFX.click();
            presets.forEach(b => b.classList.remove('active'));
            p.classList.add('active');

            const min1 = parseInt(p.getAttribute('data-min1'));
            const max1 = parseInt(p.getAttribute('data-max1'));
            const min2 = parseInt(p.getAttribute('data-min2'));
            const max2 = parseInt(p.getAttribute('data-max2'));

            document.getElementById('game-min1').value = min1;
            document.getElementById('game-max1').value = max1;
            document.getElementById('game-min2').value = min2;
            document.getElementById('game-max2').value = max2;

            AppState.min1 = min1;
            AppState.max1 = max1;
            AppState.min2 = min2;
            AppState.max2 = max2;

            updateGameOdds();
            renderNumberChips();
        });
    });

    // Custom range inputs
    ['game-min1', 'game-max1', 'game-min2', 'game-max2'].forEach(id => {
        document.getElementById(id).addEventListener('input', () => {
            AppState.min1 = parseInt(document.getElementById('game-min1').value) || 0;
            AppState.max1 = parseInt(document.getElementById('game-max1').value) || 5;
            AppState.min2 = parseInt(document.getElementById('game-min2').value) || 0;
            AppState.max2 = parseInt(document.getElementById('game-max2').value) || 5;
            updateGameOdds();
            renderNumberChips();
        });
    });

    // Botão de Jogar Rodada
    const btnPlay = document.getElementById('btn-play-round');
    btnPlay.addEventListener('click', jogarRodada);
}

function renderNumberChips() {
    const container = document.getElementById('number-chips-container');
    container.innerHTML = '';

    const min = Math.min(AppState.min1, AppState.max1);
    const max = Math.max(AppState.min1, AppState.max1);

    if (AppState.p1Valor < min || AppState.p1Valor > max) {
        AppState.p1Valor = min;
    }

    for (let i = min; i <= max; i++) {
        const btn = document.createElement('button');
        btn.className = `chip-btn ${i === AppState.p1Valor ? 'selected' : ''}`;
        btn.textContent = i;
        btn.addEventListener('click', () => {
            SoundFX.chipSelect();
            document.querySelectorAll('.chip-btn').forEach(c => c.classList.remove('selected'));
            btn.classList.add('selected');
            AppState.p1Valor = i;
        });
        container.appendChild(btn);
    }
}

function updateGameOdds() {
    const math = calcularMatematica(AppState.min1, AppState.max1, AppState.min2, AppState.max2);

    const barPar = document.getElementById('game-bar-par');
    const barImpar = document.getElementById('game-bar-impar');
    const txtPctPar = document.getElementById('game-pct-par');
    const txtPctImpar = document.getElementById('game-pct-impar');
    const verdict = document.getElementById('game-odds-verdict');
    const tip = document.getElementById('game-odds-tip');

    barPar.style.width = `${math.pctPar}%`;
    barImpar.style.width = `${math.pctImpar}%`;
    txtPctPar.textContent = `${math.pctPar.toFixed(1)}% PAR`;
    txtPctImpar.textContent = `${math.pctImpar.toFixed(1)}% ÍMPAR`;

    document.getElementById('p1-par-sub').textContent = `${math.pctPar.toFixed(1)}%`;
    document.getElementById('p1-impar-sub').textContent = `${math.pctImpar.toFixed(1)}%`;

    if (math.vantagem === 'EQUILIBRADO') {
        verdict.textContent = '50.0% vs 50.0% (Equilibrado)';
        verdict.style.color = 'var(--accent-green)';
        tip.textContent = `Intervalo justo! Ambas as escolhas têm exatamente ${math.combosPar} de ${math.totalCombos} chances de vitória.`;
    } else if (math.vantagem === 'PAR') {
        verdict.textContent = `Vantagem de PAR (+${math.diferencaPct.toFixed(1)}%)`;
        verdict.style.color = 'var(--primary-cyan-bright)';
        tip.textContent = `Atenção: Quem joga PAR tem ${math.combosPar} chances contra ${math.combosImpar} de ÍMPAR neste intervalo!`;
    } else {
        verdict.textContent = `Vantagem de ÍMPAR (+${math.diferencaPct.toFixed(1)}%)`;
        verdict.style.color = 'var(--primary-magenta-bright)';
        tip.textContent = `Atenção: Quem joga ÍMPAR tem ${math.combosImpar} chances contra ${math.combosPar} de PAR neste intervalo!`;
    }
}

async function jogarRodada() {
    SoundFX.click();
    const btnPlay = document.getElementById('btn-play-round');
    btnPlay.disabled = true;

    let valP2 = 0;

    if (AppState.modo === 'pvp') {
        const inputP2 = document.getElementById('pvp-input-p2');
        valP2 = parseInt(inputP2.value);
        if (isNaN(valP2) || valP2 < AppState.min2 || valP2 > AppState.max2) {
            alert(`Jogador 2 precisa digitar um número válido entre ${AppState.min2} e ${AppState.max2}!`);
            btnPlay.disabled = false;
            return;
        }
        inputP2.value = '';
    } else {
        // Modo IA
        valP2 = calcularJogadaIA();
    }

    // Animação dramática de contagem
    const btnText = btnPlay.querySelector('.btn-text');
    const countdown = ['UM...', 'DOIS...', 'TRÊS...', 'E JÁ! ✋🤚'];

    for (let i = 0; i < countdown.length; i++) {
        btnText.textContent = countdown[i];
        SoundFX.playTone(350 + (i * 80), 'triangle', 0.1, 0.15);
        await new Promise(r => setTimeout(r, 320));
    }

    btnText.textContent = '1, 2, 3 E JÁ! ✋';
    btnPlay.disabled = false;

    // Resolução da Rodada
    const valP1 = AppState.p1Valor;
    const soma = valP1 + valP2;
    const resultadoParidade = (soma % 2 === 0) ? 'PAR' : 'ÍMPAR';

    const p1Ganhou = (AppState.p1Escolha === resultadoParidade);

    if (p1Ganhou) {
        AppState.placarP1++;
        SoundFX.win();
    } else {
        AppState.placarP2++;
        SoundFX.lose();
    }

    document.getElementById('score-p1').textContent = AppState.placarP1;
    document.getElementById('score-p2').textContent = AppState.placarP2;

    // Exibir Caixa de Resultado
    const resultBox = document.getElementById('round-result-box');
    const resultBadge = document.getElementById('result-badge');
    const revP1Name = document.getElementById('rev-p1-name');
    const revP1Val = document.getElementById('rev-p1-val');
    const revP2Name = document.getElementById('rev-p2-name');
    const revP2Val = document.getElementById('rev-p2-val');
    const revSumVal = document.getElementById('rev-sum-val');
    const revParityVal = document.getElementById('rev-parity-val');
    const resultMsg = document.getElementById('result-message-text');

    resultBox.classList.remove('hidden');

    revP1Name.textContent = AppState.p1Nome;
    revP1Val.textContent = valP1;
    revP2Name.textContent = AppState.p2Nome;
    revP2Val.textContent = valP2;
    revSumVal.textContent = soma;
    revParityVal.textContent = resultadoParidade;

    if (resultadoParidade === 'PAR') {
        revParityVal.style.color = 'var(--primary-cyan-bright)';
    } else {
        revParityVal.style.color = 'var(--primary-magenta-bright)';
    }

    if (p1Ganhou) {
        resultBadge.textContent = '🎉 VITÓRIA DE ' + AppState.p1Nome.toUpperCase() + '!';
        resultBadge.className = 'result-status status-win';
        resultMsg.textContent = `A soma de ${valP1} + ${valP2} deu ${soma} (${resultadoParidade}). Você escolheu ${AppState.p1Escolha} e faturou a rodada!`;
    } else {
        resultBadge.textContent = '💥 VITÓRIA DE ' + AppState.p2Nome.toUpperCase() + '!';
        resultBadge.className = 'result-status status-loss';
        resultMsg.textContent = `A soma de ${valP1} + ${valP2} deu ${soma} (${resultadoParidade}). ${AppState.p2Nome} venceu esta rodada!`;
    }

    // Registra no histórico
    AppState.historicoRodadas.push({ valP1, valP2, soma, resultadoParidade, p1Ganhou });
}

function calcularJogadaIA() {
    const diff = document.querySelector('input[name="ai-diff"]:checked')?.value || 'medio';
    const min = Math.min(AppState.min2, AppState.max2);
    const max = Math.max(AppState.min2, AppState.max2);
    const opcoes = [];
    for (let i = min; i <= max; i++) opcoes.push(i);

    if (diff === 'facil' || AppState.historicoRodadas.length < 2) {
        return opcoes[Math.floor(Math.random() * opcoes.length)];
    }

    // Adaptativo: analisa jogadas recentes do jogador
    const ultimas = AppState.historicoRodadas.slice(-5);
    const paresJogador = ultimas.filter(r => r.valP1 % 2 === 0).length;
    const probP1Par = paresJogador / ultimas.length;

    const escolhaIA = (AppState.p1Escolha === 'PAR') ? 'ÍMPAR' : 'PAR';
    const querPar = (escolhaIA === 'PAR' && probP1Par >= 0.5) || (escolhaIA === 'ÍMPAR' && probP1Par < 0.5);

    const candidatos = opcoes.filter(x => querPar ? (x % 2 === 0) : (x % 2 !== 0));
    if (candidatos.length > 0 && Math.random() > 0.2) {
        return candidatos[Math.floor(Math.random() * candidatos.length)];
    }

    return opcoes[Math.floor(Math.random() * opcoes.length)];
}

// ==========================================
// SEÇÃO DO LABORATÓRIO MATEMÁTICO
// ==========================================
function initLab() {
    ['lab-min1', 'lab-max1', 'lab-min2', 'lab-max2'].forEach(id => {
        document.getElementById(id).addEventListener('input', updateLab);
    });
    updateLab();
}

window.definirLab = function(min1, max1, min2, max2) {
    SoundFX.click();
    document.getElementById('lab-min1').value = min1;
    document.getElementById('lab-max1').value = max1;
    document.getElementById('lab-min2').value = min2;
    document.getElementById('lab-max2').value = max2;
    updateLab();
};

function updateLab() {
    const min1 = parseInt(document.getElementById('lab-min1').value) || 0;
    const max1 = parseInt(document.getElementById('lab-max1').value) || 5;
    const min2 = parseInt(document.getElementById('lab-min2').value) || 0;
    const max2 = parseInt(document.getElementById('lab-max2').value) || 5;

    const math = calcularMatematica(min1, max1, min2, max2);

    document.getElementById('lab-total-combos').textContent = math.totalCombos;
    document.getElementById('lab-par-combos').textContent = math.combosPar;
    document.getElementById('lab-par-pct').textContent = `${math.pctPar.toFixed(2)}% de probabilidade`;
    document.getElementById('lab-impar-combos').textContent = math.combosImpar;
    document.getElementById('lab-impar-pct').textContent = `${math.pctImpar.toFixed(2)}% de probabilidade`;

    const verdictEl = document.getElementById('lab-verdict');
    const marginEl = document.getElementById('lab-margin');

    if (math.vantagem === 'EQUILIBRADO') {
        verdictEl.textContent = 'JOGO JUSTO';
        verdictEl.style.color = 'var(--accent-green)';
        marginEl.textContent = 'Probabilidade idêntica (50/50)';
    } else if (math.vantagem === 'PAR') {
        verdictEl.textContent = 'PAR VENCE';
        verdictEl.style.color = 'var(--primary-cyan-bright)';
        marginEl.textContent = `+${math.diferencaPct.toFixed(2)}% de margem a favor de PAR`;
    } else {
        verdictEl.textContent = 'ÍMPAR VENCE';
        verdictEl.style.color = 'var(--primary-magenta-bright)';
        marginEl.textContent = `+${math.diferencaPct.toFixed(2)}% de margem a favor de ÍMPAR`;
    }

    // Explicação Didática Dinâmica
    const titleEl = document.getElementById('lab-dive-title');
    const textEl = document.getElementById('lab-dive-text');
    const eqPar = document.getElementById('lab-equations').children[0].querySelector('code');
    const eqImpar = document.getElementById('lab-equations').children[1].querySelector('code');

    titleEl.textContent = `Demonstração Analítica para os Intervalos [${min1}..${max1}] vs [${min2}..${max2}]:`;
    textEl.textContent = `O Jogador 1 dispõe de ${math.pares1} números pares e ${math.impares1} ímpares. O Jogador 2 dispõe de ${math.pares2} números pares e ${math.impares2} ímpares. Multiplicando cada possibilidade mútua de paridade chegamos à decomposição analítica exata:`;

    eqPar.textContent = `(Pares₁ × Pares₂) + (Ímpares₁ × Ímpares₂) = (${math.pares1}×${math.pares2}) + (${math.impares1}×${math.impares2}) = ${math.pares1 * math.pares2} + ${math.impares1 * math.impares2} = ${math.combosPar} combinações`;
    eqImpar.textContent = `(Pares₁ × Ímpares₂) + (Ímpares₁ × Pares₂) = (${math.pares1}×${math.impares2}) + (${math.impares1}×${math.pares2}) = ${math.pares1 * math.impares2} + ${math.impares1 * math.pares2} = ${math.combosImpar} combinações`;
}

// ==========================================
// SEÇÃO DO SIMULADOR MONTE CARLO
// ==========================================
function initMonteCarlo() {
    const btnSim = document.getElementById('btn-run-sim');
    btnSim.addEventListener('click', runMonteCarlo);
}

window.setSimRounds = function(rounds) {
    SoundFX.click();
    document.getElementById('sim-rounds-val').value = rounds;
    document.querySelectorAll('.rounds-chips .btn-chip').forEach(btn => {
        if (btn.textContent.replace('.', '') == rounds) {
            btn.classList.add('active-chip');
        } else {
            btn.classList.remove('active-chip');
        }
    });
};

function runMonteCarlo() {
    SoundFX.click();
    const rounds = parseInt(document.getElementById('sim-rounds-val').value) || 50000;
    const min1 = AppState.min1;
    const max1 = AppState.max1;
    const min2 = AppState.min2;
    const max2 = AppState.max2;

    const math = calcularMatematica(min1, max1, min2, max2);

    let vitoriasPar = 0;
    let vitoriasImpar = 0;
    const freqSomas = {};

    for (let r = 0; r < rounds; r++) {
        const x1 = Math.floor(Math.random() * (max1 - min1 + 1)) + min1;
        const x2 = Math.floor(Math.random() * (max2 - min2 + 1)) + min2;
        const soma = x1 + x2;

        freqSomas[soma] = (freqSomas[soma] || 0) + 1;
        if (soma % 2 === 0) vitoriasPar++;
        else vitoriasImpar++;
    }

    const pctEmpPar = (vitoriasPar / rounds) * 100;
    const pctEmpImpar = (vitoriasImpar / rounds) * 100;

    const erroPar = Math.abs(pctEmpPar - math.pctPar);
    const erroImpar = Math.abs(pctEmpImpar - math.pctImpar);

    document.getElementById('sim-emp-par').textContent = `${pctEmpPar.toFixed(2)}%`;
    document.getElementById('sim-emp-par-count').textContent = `${vitoriasPar.toLocaleString('pt-BR')} vitórias`;
    document.getElementById('sim-theo-par-diff').textContent = `Teórico: ${math.pctPar.toFixed(2)}% (Erro: ${erroPar.toFixed(2)}%)`;

    document.getElementById('sim-emp-impar').textContent = `${pctEmpImpar.toFixed(2)}%`;
    document.getElementById('sim-emp-impar-count').textContent = `${vitoriasImpar.toLocaleString('pt-BR')} vitórias`;
    document.getElementById('sim-theo-impar-diff').textContent = `Teórico: ${math.pctImpar.toFixed(2)}% (Erro: ${erroImpar.toFixed(2)}%)`;

    // Gráfico de Frequência das Somas
    const chartArea = document.getElementById('sim-chart-bars');
    chartArea.innerHTML = '';

    const maxFreq = Math.max(...Object.values(freqSomas));
    const sortedKeys = Object.keys(freqSomas).map(Number).sort((a, b) => a - b);

    sortedKeys.forEach(soma => {
        const count = freqSomas[soma];
        const heightPct = (count / maxFreq) * 100;
        const ehPar = (soma % 2 === 0);

        const col = document.createElement('div');
        col.className = 'bar-col';
        col.title = `Soma ${soma}: ${count.toLocaleString('pt-BR')} ocorrências (${((count/rounds)*100).toFixed(1)}%)`;

        const pillar = document.createElement('div');
        pillar.className = `bar-pillar ${ehPar ? 'par' : 'impar'}`;
        pillar.style.height = `${heightPct}%`;

        const label = document.createElement('span');
        label.className = 'bar-label';
        label.textContent = soma;

        col.appendChild(pillar);
        col.appendChild(label);
        chartArea.appendChild(col);
    });

    SoundFX.win();
}

// ==========================================
// SEÇÃO DA MATRIZ DE COMBINAÇÕES
// ==========================================
function renderMatrix() {
    const table = document.getElementById('matrix-table-el');
    table.innerHTML = '';

    const math = calcularMatematica(AppState.min1, AppState.max1, AppState.min2, AppState.max2);

    // Header (Colunas = Jogador 2)
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');

    const cornerTh = document.createElement('th');
    cornerTh.textContent = 'P1 \\ P2';
    headerRow.appendChild(cornerTh);

    math.vals2.forEach(x2 => {
        const th = document.createElement('th');
        th.textContent = x2;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Body (Linhas = Jogador 1)
    const tbody = document.createElement('tbody');
    math.matriz.forEach(row => {
        const tr = document.createElement('tr');
        const rowTh = document.createElement('th');
        rowTh.textContent = row[0].x1;
        tr.appendChild(rowTh);

        row.forEach(item => {
            const td = document.createElement('td');
            td.className = `matrix-cell ${item.ehPar ? 'cell-par' : 'cell-impar'}`;
            td.textContent = item.soma;
            td.title = `${item.x1} + ${item.x2} = ${item.soma} (${item.ehPar ? 'PAR' : 'ÍMPAR'})`;
            td.addEventListener('mouseenter', () => SoundFX.playTone(300 + (item.soma * 30), 'sine', 0.04, 0.05));
            tr.appendChild(td);
        });

        tbody.appendChild(tr);
    });
    table.appendChild(tbody);
}
