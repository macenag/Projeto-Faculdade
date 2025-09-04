import socket
import time
import random
from itertools import cycle

HOST = '127.0.0.1'
PORT = 65432

print("🤖 Iniciando Simulador de Sensores (ESP32) com Lógica Específica...")

# --- Variáveis de controle da simulação ---
# Ciclo de umidade para a demonstração (40% -> 32% -> 56% -> repete)
humidity_cycle = cycle([40, 32, 56]) 
current_humidity = next(humidity_cycle)

# Controle de temperatura
current_temperature = random.uniform(30.0, 38.0)
last_temp_update_time = time.time()

# O loop principal agora roda a cada 15 segundos para o ciclo de umidade
LOOP_INTERVAL = 15 

while True:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print(f"✔️ Conectado ao servidor principal. Enviando dados a cada {LOOP_INTERVAL} segundos.")
            
            # Zera o ciclo de umidade a cada nova conexão
            humidity_cycle = cycle([40, 32, 56])

            while True:
                # --- Lógica de Umidade ---
                # Pega o próximo valor do ciclo de 15 em 15 segundos
                current_humidity = next(humidity_cycle)

                # --- Lógica de Temperatura ---
                # Verifica se já se passaram 30 segundos para atualizar a temperatura
                if time.time() - last_temp_update_time >= 30:
                    current_temperature = random.uniform(30.0, 38.0)
                    last_temp_update_time = time.time()
                    print("   -> (Temperatura atualizada)")

                # --- Envio dos Dados ---
                payload = f"SENSOR_DATA:{current_temperature:.1f},{current_humidity:.1f}"
                s.sendall(payload.encode('utf-8'))
                print(f"-> Dados enviados: Temp={current_temperature:.1f}°C, Umidade={current_humidity:.1f}%")
                
                # Opcional: continua simulando movimento
                if random.random() < 0.1:
                    mov_payload = "MOV:INTERNO"
                    s.sendall(mov_payload.encode('utf-8'))

                time.sleep(LOOP_INTERVAL)
                
    except ConnectionRefusedError:
        print(f"❌ Servidor principal não encontrado. Tentando novamente em {LOOP_INTERVAL} segundos...")
        time.sleep(LOOP_INTERVAL)
    except Exception as e:
        print(f"⚠️ Erro: {e}. Reconectando...")
        time.sleep(LOOP_INTERVAL)