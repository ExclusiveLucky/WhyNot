import asyncio
from fastapi import FastAPI, APIRouter, Depends
from pydantic import BaseModel
from time import monotonic

app = FastAPI()
router = APIRouter()

class WorkService:
    """
    Сервис для выполнения полезной работы с поддержкой блокировки для контроля параллелизма.
    """
    def __init__(self):
        self.lock = asyncio.Lock()  # Блокировка теперь на уровне всего сервиса (единственный экземпляр)

    async def perform_work(self, duration: float) -> None:
        """
        Выполняет полезную работу (ожидание в течение времени, заданного параметром duration).
        
        :param duration: Количество секунд для ожидания.
        """
        await asyncio.sleep(duration)

    async def run_with_lock(self, duration: float) -> None:
        """
        Выполняет полезную работу, гарантируя, что она не выполняется параллельно с другими вызовами.
        
        :param duration: Количество секунд для ожидания.
        """
        async with self.lock:
            await self.perform_work(duration)


class TestResponse(BaseModel):
    """
    Модель ответа для метода /test, содержащая фактически затраченное время.
    """
    elapsed: float


# Экземпляр WorkService, который будет использоваться глобально
work_service = WorkService()

@router.get("/test", response_model=TestResponse)
async def handler() -> TestResponse:
    """
    Обработчик запроса на /test. Выполняет полезную работу с использованием блокировки и возвращает
    фактически затраченное время.
    
    :return: TestResponse с полем elapsed, показывающим затраченное время.
    """
    start_time = monotonic()
    
    # Выполняем работу через сервис, обеспечивая, что вызовы блокируются
    await work_service.run_with_lock(3)
    
    elapsed_time = monotonic() - start_time
    return TestResponse(elapsed=elapsed_time)


app.include_router(router)