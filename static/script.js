document.addEventListener('DOMContentLoaded', () => {
    const socket = io();

    // --- Elementos da Página ---
    const tempEl = document.getElementById('temperatura');
    const umidadeEl = document.getElementById('umidade');
    const umidificadorEl = document.getElementById('umidificador'); // NOVO ELEMENTO
    const presencaEl = document.getElementById('presenca');
    const modoAtualEl = document.getElementById('modo_atual');
    const acTempEl = document.getElementById('ac_temp');
    const acStatusEl = document.getElementById('ac_status');
    // ...outros elementos sem alteração

    // --- RECEBENDO DADOS DO SERVIDOR ---
    socket.on('update_state', (state) => {
        tempEl.textContent = state.temperatura.toFixed(1);
        umidadeEl.textContent = state.umidade.toFixed(1);
        umidificadorEl.textContent = state.humidifier_status; // ATUALIZA O STATUS
        presencaEl.textContent = state.presenca_interna;
        modoAtualEl.textContent = state.modo_atual;
        acTempEl.textContent = state.ac_temp;

        if (state.modo_atual === 'Automático') {
            acStatusEl.textContent = "Controlado Automaticamente";
        } else {
            acStatusEl.textContent = `Fixo (Modo ${state.modo_atual})`;
        }
    });

    // O resto do arquivo não precisa de alterações...
    const modeButtons = document.querySelectorAll('.mode-btn');
    const logOutput = document.getElementById('log-output');
    const radioSim = document.getElementById('foraSim');
    const radioNao = document.getElementById('foraNao');
    const minutosContainer = document.getElementById('minutos-container');
    const minutosInput = document.getElementById('minutosFora');
    const btnSimulateEntry = document.getElementById('btn_simulate_entry');

    socket.on('server_log', (data) => {
        const logEntry = document.createElement('p');
        const timestamp = new Date().toLocaleTimeString();
        logEntry.textContent = `[${timestamp}] ${data.message}`;
        logOutput.appendChild(logEntry);
        logOutput.scrollTop = logOutput.scrollHeight;
    });

    modeButtons.forEach(button => {
        button.addEventListener('click', () => {
            const mode = button.getAttribute('data-mode');
            socket.emit('set_mode', { mode: mode });
        });
    });

    radioSim.addEventListener('change', () => minutosContainer.style.display = 'block');
    radioNao.addEventListener('change', () => minutosContainer.style.display = 'none');
    
    btnSimulateEntry.addEventListener('click', () => {
        if (radioSim.checked) {
            socket.emit('simulate_entry', { minutes_outside: minutosInput.value });
        } else {
            const logEntry = document.createElement('p');
            const timestamp = new Date().toLocaleTimeString();
            logEntry.textContent = `[${timestamp}] [SISTEMA] Simulação de entrada cancelada: usuário já estava no quarto.`;
            logOutput.appendChild(logEntry);
        }
    });
});