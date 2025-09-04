# 🚀 Executando o Projeto IoT

Este projeto implementa um sistema **Cliente/Servidor IoT** utilizando **Flask** e **Flask-SocketIO**, permitindo monitorar sensores (simulados via ESP32) e exibir os dados em tempo real em um painel web.

---

## 📦 Instalação das Dependências

Antes de rodar o projeto, certifique-se de ter o **Python 3.x** instalado.  

No terminal, execute:

```bash
pip install Flask Flask-SocketIO
```

---

## ▶️ Passo a Passo para Rodar

### 1. Iniciar o Servidor Principal
No terminal, execute:

```bash
python app.py
```

- O servidor Flask será iniciado  
- No final, aparecerá algo como:  
  ```
  Acesse http://127.0.0.1:5000 no seu navegador.
  ```

⚠️ **Não feche este terminal**, ele precisa continuar rodando.  

---

### 2. Abrir um Segundo Terminal
No **VS Code**, clique em **Dividir Terminal** (ou abra um novo).  

---

### 3. Iniciar o Simulador de Sensores
No segundo terminal, rode:

```bash
python simulate_esp32.py
```

Se tudo estiver correto, verá mensagens como:  
```
Conectado ao servidor principal
Dados enviados...
```

---

## 🌍 Visualizando no Navegador

Abra seu navegador e acesse:

👉 http://127.0.0.1:5000

### Você verá:
- Dados de **temperatura** e **umidade** em tempo real  
- Botões para simular **presença** e **modos de operação**  
- Um **Log de Eventos** atualizado automaticamente  

---

## 🎮 Interação

- Clique nos botões do painel para simular eventos  
- Veja as atualizações em tempo real no navegador  
- No terminal do **app.py**, digite as **mensagens secretas** para testar respostas do sistema  

---

## 🖼️ Estrutura Visual (VS Code)

Você terá **dois terminais ativos**:
1. `app.py` → Servidor rodando Flask  
2. `simulate_esp32.py` → Simulador de sensores enviando dados 


## 🔑 Mensagens Secretas para testar no terminal:
```
Alexa, Tenho compromisso hoje?
Alexa, qual a previsão do dia de hoje
```
