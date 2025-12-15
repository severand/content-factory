# 🚀 QUICK START - Мўга-Проект Контент Фабрика

## ✅ Всь код ПОЛНОСТИ РАБОЧИЙ И ГОТОВ К ЗАПУСКУ!

---

## 30 секунд до работы 🚀

### Шаг 1: Клонируй и запусти
```bash
git clone https://github.com/severand/content-factory
cd content-factory
docker-compose up -d
```

### Шаг 2: Проверь
```bash
curl http://localhost:8000/health
```

### Шаг 3: Попробуй!
```bash
# Нсписок парсеров
curl http://localhost:8000/api/v1/modules/parsers

# Парсить RSS новости РИА
curl -X POST http://localhost:8000/api/v1/parsers/rss_parser/test \
  -H "Content-Type: application/json" \
  -d '{"source": "https://ria.ru/export/rss2/all/"}'
```

👏 **ВОТ!👏 Всё работает!

---

## 📃 Что уже загружено в GitHub

### Ядро системы (core/)
- ✅ **Интерфейсы** - базовые классы для всех компонентов
- ✅ **Регистры** - автоматическое обнаружение модулей

### Модули (modules/)
- ✅ **RSS Parser** - работающий парсер RSS лент
- ✅ **Web Parser** - работающий HTML парсер

### Backend (backend/)
- ✅ **FastAPI приложение** - полностью рабочее
- ✅ **API endpoints** - для управления модулями
- ✅ **Module manager** - открыт API 

### DevOps
- ✅ **docker-compose.yml** - для одного клика
- ✅ **Dockerfile** - production-ready
- ✅ **.env.example** - полные конфиги

---

## 💯 API экзамены

### Пример 1: Получить все модули
```bash
curl http://localhost:8000/api/v1/modules | jq
```

**Ответ:**
```json
{
  "status": "success",
  "modules": {
    "parsers": [
      {
        "name": "rss_parser",
        "type": "rss",
        "version": "1.0.0",
        "description": "Universal RSS parser for news feeds"
      },
      {
        "name": "web_parser",
        "type": "web",
        "version": "1.0.0",
        "description": "HTML web page parser using BeautifulSoup"
      }
    ],
    "llm_providers": [],
    "agents": [],
    "social_networks": []
  },
  "stats": {
    "parsers": 2,
    "llm_providers": 0,
    "agents": 0,
    "social_networks": 0
  }
}
```

### Пример 2: Парсить РИА Новости
```bash
curl -X POST http://localhost:8000/api/v1/parsers/rss_parser/test \
  -H "Content-Type: application/json" \
  -d '{"source": "https://ria.ru/export/rss2/all/"}' | jq
```

**Ответ:**
```json
{
  "status": "success",
  "items_count": 20,
  "message": "🌟 Парсинг успешен! Найдено 20 элементов",
  "items": [
    {
      "id": "uuid-123",
      "title": "Президент рассказал...",
      "content": "Полный текст новости...",
      "url": "https://ria.ru/20251215/...",
      "author": "Мария Попова",
      "source_name": "Новости РИА",
      "type": "rss_item",
      "parsed_at": "2025-12-15T19:24:00"
    },
    // ...ещё 19 элементов
  ]
}
```

### Пример 3: Парсить веб-сайт
```bash
curl -X POST http://localhost:8000/api/v1/parsers/web_parser/test \
  -H "Content-Type: application/json" \
  -d '{
    "source": "https://www.bbc.com",
    "css_selectors": {
      "articles": "article",
      "title": "h2, h3",
      "content": "p"
    }
  }' | jq
```

---

## 😔 Понять архитектуру

### Файлы, которые найдения
```
github
├── core/                    # ✅ Основные интерфейсы
│   ├── interfaces/
│   │   ├── parser_interface.py
│   │   ├── llm_interface.py
│   │   ├── social_interface.py
│   │   └── agent_interface.py
│   └── registry/
│       ├── parser_registry.py
│       ├── llm_registry.py
│       ├── agent_registry.py
│       ├── social_registry.py
│       └── registries_manager.py
│
├── modules/
│   ├── parsers/
│   │   ├── rss_parser/         # ✅ Полностью рабочий
│   │   │   ├── __init__.py
│   │   │   └── parser.py
│   │   └── web_parser/         # ✅ Полностью рабочий
│   │       └── parser.py
│   │
│   ├── agents/
│   ├── llm_providers/
│   └── social_networks/
│
├── backend/
│   ├── main.py             # ✅ Полностью рабочое FastAPI
│   └── requirements.txt
│
├── docker-compose.yml      # ✅ Одна команда
├── Dockerfile.backend
├── .env.example
└── README.md
```

---

## ✨ Следующие шагы

### Локальная разработка
```bash
# Остановить Docker
docker-compose down

# Перейти в backend
cd backend

# Установить зависимости
pip install -r requirements.txt

# Запустить с reload
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Создание нового парсера
```bash
# 1. Создай папку
mkdir -p modules/parsers/my_parser

# 2. Напиши код
# modules/parsers/my_parser/parser.py
from core.interfaces.parser_interface import ParserInterface, ParserType, ParsedItem

class MyParser(ParserInterface):
    @property
    def parser_type(self) -> ParserType:
        return ParserType.CUSTOM
    
    @property
    def parser_name(self) -> str:
        return "my_parser"
    
    @property
    def parser_version(self) -> str:
        return "1.0.0"
    
    @property
    def parser_description(self) -> str:
        return "Мой супер-парсер"
    
    async def initialize(self, config):
        pass
    
    async def parse(self, source):
        return [
            ParsedItem({
                "title": "Пример",
                "content": "Описание",
                "url": source
            })
        ]
    
    async def validate_source(self, source):
        return True
    
    async def test_connection(self):
        return True

# 3. Перестартни backend
# Парсер автоматически регистрируется!
```

---

## 💥 Обыкновенные проблемы

### Port 8000 уже занят
```bash
# Найти процесс
lsof -i :8000

# Убить
kill -9 <PID>

# или в Docker пересобрать
docker-compose down && docker-compose up -d
```

### ImportError в одном из модулей
```bash
# Проверить реквизиты
pip install -r backend/requirements.txt

# Проверить PYTHONPATH
export PYTHONPATH=/path/to/content-factory
```

---

## 📛 Дополнительные команды

```bash
# Логи в нреальном времени
docker-compose logs -f backend

# Остановить backend
docker-compose stop backend

# Перестарт backend
docker-compose restart backend

# Очистить всё
docker-compose down -v
```

---

🎈 **Всё готово! Наслаждайся работою!**
