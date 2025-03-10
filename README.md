# MisProject

**MisProject** — простейший веб  сервис Медицинской Информационной Системой (МИС). Проект выполнен для выполнения тестового задания Компании 
A SWISS GROUP

## Установка и запуск проекта

### **1. Клонирование репозитория**
Склонируйте проект с GitHub:
```bash
git clone https://github.com/curabby/MisProject.git
cd MisProject/
```
---

### **2. Настройка переменных окружения**
Создайте файл в  **`.env`** директории mailganer/mailganerApp/ 
```bash
touch MisProjectBackend/.env
```
и укажите параметры:
```ini
SECRET_KEY='YOUR_SECRET_KEY'
DEBUG=False
```

---

### 3. Запуск проекта:
в Docker
```bash
docker-compose up --build
```
или через виртуальное окружение

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd MisProjectBackend/
python3 manage.py runserver
```

---
## 5 Прочая информация:
После запуска проекта происходит тестирование функционала, а также добавление фейковых записей в БД.
Для удобства проверяющего создан суперпользователь:
почта - admin@mail.com
пароль - admin

## 6 Документация по API проекта:

```bash
http://127.0.0.1:8000/swagger/
http://127.0.0.1:8000/redoc
```

## 7 Стек:

```bash
django, drf, sqlite, pytest
```
