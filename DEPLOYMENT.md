# Развертывание

## Локальное развертывание

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd telegram-bot
```

### 2. Создание виртуального окружения

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

```bash
copy .env.example .env
```

Отредактируйте файл `.env` и добавьте ваши токены:

```env
BOT_TOKEN=ваш_токен_бота
AMVERA_LLM_TOKEN=ваш_токен_amvera
CONTEXT7_API_KEY=ваш_ключ_context7
```

### 5. Запуск бота

```bash
python -m src.bot.main
```

## Развертывание на сервере

### Требования

- Python 3.11+
- pip
- git

### 1. Подключение к серверу

```bash
ssh user@server-ip
```

### 2. Клонирование репозитория

```bash
git clone <repository-url>
cd telegram-bot
```

### 3. Создание виртуального окружения

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 5. Настройка переменных окружения

```bash
cp .env.example .env
nano .env
```

Добавьте ваши токены в файл `.env`.

### 6. Запуск бота в фоне

#### Использование screen

```bash
screen -S telegram-bot
python -m src.bot.main
# Нажмите Ctrl+A, затем D для выхода из screen
```

Для возврата в screen:
```bash
screen -r telegram-bot
```

#### Использование nohup

```bash
nohup python -m src.bot.main > logs/bot.log 2>&1 &
```

#### Использование systemd

Создайте файл `/etc/systemd/system/telegram-bot.service`:

```ini
[Unit]
Description=Telegram Bot with Amvera LLM
After=network.target

[Service]
Type=simple
User=<username>
WorkingDirectory=/home/<username>/telegram-bot
Environment="PATH=/home/<username>/telegram-bot/.venv/bin"
ExecStart=/home/<username>/telegram-bot/.venv/bin/python -m src.bot.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Затем запустите сервис:

```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
```

Проверьте статус:

```bash
sudo systemctl status telegram-bot
```

## Docker развертывание

### 1. Создание Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "src.bot.main"]
```

### 2. Создание .dockerignore

```
.git
.venv
__pycache__
*.pyc
.env
logs
```

### 3. Сборка образа

```bash
docker build -t telegram-bot:latest .
```

### 4. Запуск контейнера

```bash
docker run -d \
  --name telegram-bot \
  -e BOT_TOKEN=ваш_токен_бота \
  -e AMVERA_LLM_TOKEN=ваш_токен_amvera \
  -e CONTEXT7_API_KEY=ваш_ключ_context7 \
  -v $(pwd)/logs:/app/logs \
  telegram-bot:latest
```

### 5. Docker Compose

Создайте файл `docker-compose.yml`:

```yaml
version: '3.8'

services:
  telegram-bot:
    build: .
    container_name: telegram-bot
    environment:
      BOT_TOKEN: ${BOT_TOKEN}
      AMVERA_LLM_TOKEN: ${AMVERA_LLM_TOKEN}
      CONTEXT7_API_KEY: ${CONTEXT7_API_KEY}
    volumes:
      - ./logs:/app/logs
    restart: always
```

Запустите:

```bash
docker-compose up -d
```

## Мониторинг

### Проверка логов

```bash
tail -f logs/bot.log
```

### Проверка процесса

```bash
ps aux | grep "python -m src.bot.main"
```

### Проверка использования памяти

```bash
top
```

## Обновление

### 1. Остановка бота

```bash
# Если используется systemd
sudo systemctl stop telegram-bot

# Если используется screen
screen -S telegram-bot -X quit

# Если используется Docker
docker stop telegram-bot
```

### 2. Обновление кода

```bash
git pull origin main
```

### 3. Обновление зависимостей

```bash
pip install -r requirements.txt
```

### 4. Запуск бота

```bash
# Если используется systemd
sudo systemctl start telegram-bot

# Если используется screen
screen -S telegram-bot
python -m src.bot.main

# Если используется Docker
docker start telegram-bot
```

## Резервное копирование

### Резервное копирование логов

```bash
tar -czf logs_backup_$(date +%Y%m%d).tar.gz logs/
```

### Резервное копирование конфигурации

```bash
cp .env .env.backup
```

## Безопасность

### 1. Защита переменных окружения

Убедитесь, что файл `.env` не закоммичен в репозиторий:

```bash
echo ".env" >> .gitignore
```

### 2. Ограничение доступа к файлам

```bash
chmod 600 .env
chmod 700 logs
```

### 3. Использование SSL/TLS

Включите проверку SSL-сертификата в `src/bot/services/amvera_llm.py`:

```python
# Удалите эти строки:
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# И используйте стандартный SSL контекст
```

### 4. Регулярные обновления

```bash
pip install --upgrade -r requirements.txt
```

## Решение проблем

### Ошибка: "Connection refused"

Проверьте, что бот запущен:
```bash
ps aux | grep "python -m src.bot.main"
```

### Ошибка: "Permission denied"

Проверьте права доступа:
```bash
ls -la .env
chmod 600 .env
```

### Ошибка: "Out of memory"

Увеличьте лимит памяти или оптимизируйте код.

### Ошибка: "Timeout"

Проверьте соединение с интернетом и API Amvera.

## Масштабирование

### Использование нескольких экземпляров

Для масштабирования можно использовать:
- Load balancer (nginx, HAProxy)
- Kubernetes
- Docker Swarm

### Использование очереди сообщений

Для обработки большого количества сообщений можно использовать:
- RabbitMQ
- Redis
- Kafka

## Дополнительная информация

- **Python:** https://www.python.org/
- **Docker:** https://www.docker.com/
- **systemd:** https://systemd.io/
- **nginx:** https://nginx.org/
