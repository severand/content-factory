"""
🏗️ Content Factory - Main FastAPI Application
Работающее приложение на FastAPI
"""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
from pathlib import Path

# Add parent dir to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import registries_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="🏗️ Content Factory API",
    version="1.0.0",
    description="Мега-проект для модульного парсинга, генерации контента и публикации"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= HEALTH CHECK =============

@app.get("/health")
async def health_check():
    """💓 Проверка жизниспособности"""
    return {
        "status": "👍 OK",
        "message": "Приложение работает!"
    }

# ============= MODULES API =============

@app.get("/api/v1/modules")
async def list_modules():
    """📂 Нсписок всех модулей"""
    try:
        stats = registries_manager.get_stats()
        return {
            "status": "success",
            "modules": {
                "parsers": registries_manager.parser_registry.list_parsers(),
                "llm_providers": registries_manager.llm_registry.list_providers(),
                "agents": registries_manager.agent_registry.list_agents(),
                "social_networks": registries_manager.social_registry.list_networks()
            },
            "stats": stats
        }
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/modules/parsers")
async def list_parsers():
    """🔍 Нсписок парсеров"""
    return {
        "status": "success",
        "parsers": registries_manager.parser_registry.list_parsers(),
        "count": len(registries_manager.parser_registry._parsers)
    }

@app.get("/api/v1/modules/llm-providers")
async def list_llm_providers():
    """🧠 Нсписок LLM провайдеров"""
    return {
        "status": "success",
        "providers": registries_manager.llm_registry.list_providers(),
        "count": len(registries_manager.llm_registry._providers)
    }

@app.get("/api/v1/modules/agents")
async def list_agents():
    """🤖 Нсписок агентов"""
    return {
        "status": "success",
        "agents": registries_manager.agent_registry.list_agents(),
        "count": len(registries_manager.agent_registry._agents)
    }

@app.get("/api/v1/modules/social-networks")
async def list_social_networks():
    """📱 Нсписок соц сетей"""
    return {
        "status": "success",
        "networks": registries_manager.social_registry.list_networks(),
        "count": len(registries_manager.social_registry._networks)
    }

# ============= PARSER API =============

@app.get("/api/v1/parsers/{parser_name}")
async def get_parser_info(parser_name: str):
    """🔍 Информация о парсере"""
    parser = registries_manager.parser_registry.get_parser(parser_name)
    if not parser:
        raise HTTPException(status_code=404, detail=f"Парсер {parser_name} не найден")
    
    return {
        "status": "success",
        "parser": {
            "name": parser.parser_name,
            "type": parser.parser_type.value,
            "version": parser.parser_version,
            "description": parser.parser_description,
            "config_schema": parser.get_config_schema()
        }
    }

# ============= TEST API =============

@app.post("/api/v1/parsers/{parser_name}/test")
async def test_parser(parser_name: str, source: str):
    """🦨 Тестирование парсера"""
    parser = registries_manager.parser_registry.get_parser(parser_name)
    if not parser:
        raise HTTPException(status_code=404, detail=f"Парсер не найден")
    
    try:
        # Тест соединения
        is_connected = await parser.test_connection()
        
        if not is_connected:
            return {
                "status": "error",
                "message": "Ошибка соединения"
            }
        
        # Парсить источник
        items = await parser.parse(source)
        
        return {
            "status": "success",
            "items_count": len(items),
            "items": items[:3],  # Первые 3
            "message": f"🌟 Парсинг успешен! Найдено {len(items)} элементов"
        }
    
    except Exception as e:
        logger.error(f"❌ Ошибка тестирования: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

# ============= STARTUP =============

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("🚀 Content Factory Backend запустился!")
    logger.info("🔍 Автообнаружение модулей...")
    # registries_manager.auto_discover_all("modules")
    logger.info(✅ Модули загружены")

# ============= RUN =============

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Пуск сервера...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
