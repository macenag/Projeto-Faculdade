import socket
import threading
import time
import math
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

SYSTEM_STATE = {
    "temperatura": 34.0,
    "umidade": 40.0,
    "presenca_interna": "Não Detectada",
    "modo_atual": "Automático",
    "ac_temp": 24,
    "humidifier_status": "Desligado" # Novo estado para o umidificador
}

def _log_to_web(message):
    print(message)
    socketio.emit('server_log', {'message': message})

def _control_ac_ir(temp):
    _log_to_web(f"[CONTROLE AR] Comando IR enviado para definir temperatura em {temp}°C.")

def _trigger_alexa_tts(text):
    _log_to_web(f"[CONTROLE ALEXA] Comando de voz enviado: '{text}'")

def _set_mode_lights(mode):
    # ... (código sem alterações)
    if mode == 'estudar': _log_to_web("[CONTROLE LUZES] Luzes ajustadas para amarelo, 40% de brilho.")
    elif mode == 'jogar': _log_to_web("[CONTROLE LUZES] Luzes ajustadas para azul/roxo, 80% de brilho.")
    elif mode == 'dormir': _log_to_web("[CONTROLE LUZES] Todas as luzes foram desligadas.")
    elif mode == 'automático': _log_to_web("[CONTROLE LUZES] Controle de luzes retornou ao modo padrão.")

# ===================================================================
# --- NOVA FUNÇÃO DE CONTROLE DO UMIDIFICADOR ---
# ===================================================================
def _control_humidifier(target_state):
    """Controla o umidificador, evitando comandos repetidos."""
    current_status_str = SYSTEM_STATE['humidifier_status']
    
    if target_state == 'ON' and current_status_str == 'Desligado':
        SYSTEM_STATE['humidifier_status'] = 'Ligado'
        _log_to_web("[CONTROLE UMIDIFICADOR] Umidade baixa. Enviando comando: 'Alexa, ligar umidificador'")
    elif target_state == 'OFF' and current_status_str == 'Ligado':
        SYSTEM_STATE['humidifier_status'] = 'Desligado'
        _log_to_web("[CONTROLE UMIDIFICADOR] Umidade ideal. Enviando comando: 'Alexa, desligar umidificador'")

def tcp_server_thread():
    HOST = '127.0.0.1'
    PORT = 65432
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT)); s.listen()
        print(f"✔️ Servidor TCP escutando em {HOST}:{PORT}")
        while True:
            conn, _ = s.accept()
            with conn:
                while True:
                    data = conn.recv(1024).decode('utf-8')
                    if not data: break
                    
                    if data.startswith("SENSOR_DATA"):
                        _, values = data.split(':'); temp, hum = values.split(',')
                        SYSTEM_STATE['temperatura'] = float(temp)
                        SYSTEM_STATE['umidade'] = float(hum)

                        # Lógica Automática do Ar-Condicionado
                        if SYSTEM_STATE['modo_atual'] == 'Automático':
                            ambient_temp = SYSTEM_STATE['temperatura']
                            target_ac_temp = max(17, ambient_temp - 10)
                            new_ac_temp = int(math.ceil(target_ac_temp))
                            if new_ac_temp != SYSTEM_STATE['ac_temp']:
                                SYSTEM_STATE['ac_temp'] = new_ac_temp
                                _log_to_web(f"[AUTO CLIMA] Temp. ambiente: {ambient_temp:.1f}°C. Ar ajustado para {new_ac_temp}°C.")

                        # ===================================================================
                        # --- NOVA LÓGICA DE CONTROLE DO UMIDIFICADOR ---
                        # ===================================================================
                        current_humidity = SYSTEM_STATE['umidade']
                        if current_humidity < 40:
                            _control_humidifier('ON')
                        elif current_humidity > 55:
                            _control_humidifier('OFF')

                    elif data.startswith("MOV:INTERNO"):
                        SYSTEM_STATE['presenca_interna'] = f"Detectada às {time.strftime('%H:%M:%S')}"
                    
                    socketio.emit('update_state', SYSTEM_STATE)

def cli_command_thread():
    # ... (código sem alterações)
    print("✔️ Simulador de Comandos Alexa pronto. Digite seus comandos abaixo.")
    while True:
        command = input(); process_cli_command(command)

def process_cli_command(command):
    # ... (código sem alterações)
    processed_command = command.lower().strip()
    if processed_command == "alexa, tenho compromisso hoje?":
        response = "O senhor precisa apresentar o Projeto para o Professor Felipe, tomara que ele não cobre explicação do código."
        _log_to_web(f"[COMANDO DE VOZ] {command}"); _log_to_web(f"[RESPOSTA ALEXA] {response}")
    elif processed_command == "alexa, qual a previsão do dia de hoje":
        response = "Hoje estará um dia quente como sempre nessa cidade, mas graças a Willis Carrier, tem uma máquina que esfria o ar."
        _log_to_web(f"[COMANDO DE VOZ] {command}"); _log_to_web(f"[RESPOSTA ALEXA] {response}")
    elif processed_command: _log_to_web(f"[COMANDO DESCONHECIDO] '{command}'")

@app.route('/')
def index(): return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print("✔️ Cliente Web Conectado!"); socketio.emit('update_state', SYSTEM_STATE)

@socketio.on('set_mode')
def handle_set_mode(data):
    # ... (código sem alterações, apenas o _control_ac_ir foi removido da lógica de modo)
    mode = data['mode']; SYSTEM_STATE['modo_atual'] = mode.capitalize()
    _log_to_web(f"--- MODO {mode.upper()} ATIVADO ---"); _set_mode_lights(mode)
    if mode == 'estudar': SYSTEM_STATE['ac_temp'] = 23
    elif mode == 'jogar': SYSTEM_STATE['ac_temp'] = 20
    elif mode == 'dormir': SYSTEM_STATE['ac_temp'] = 17
    elif mode == 'automático':
        ambient_temp = SYSTEM_STATE['temperatura']; target_ac_temp = max(17, ambient_temp - 10)
        SYSTEM_STATE['ac_temp'] = int(math.ceil(target_ac_temp))
    _control_ac_ir(SYSTEM_STATE['ac_temp'])
    socketio.emit('update_state', SYSTEM_STATE)

@socketio.on('simulate_entry')
def handle_simulate_entry(data):
    # ... (código sem alterações)
    minutes = int(data['minutes_outside'])
    if minutes >= 10: _trigger_alexa_tts("Olá, como foi seu dia? Gostaria de iniciar algum modo?")
    else: _log_to_web("[SISTEMA] Usuário retornou em menos de 10 minutos. Nenhuma saudação necessária.")

if __name__ == '__main__':
    print("🚀 Iniciando Servidor de Automação...")
    tcp_thread = threading.Thread(target=tcp_server_thread); tcp_thread.daemon = True; tcp_thread.start()
    cli_thread = threading.Thread(target=cli_command_thread); cli_thread.daemon = True; cli_thread.start()
    print("✔️ Servidor Web pronto. Acesse http://127.0.0.1:5000 no seu navegador.")
    socketio.run(app, host='127.0.0.1', port=5000)