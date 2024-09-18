import httpx
import asyncio

# Задаем количество задач, которое будет выполнено параллельно
TASK_COUNT = 5

async def fetch() -> None:
    """
    Выполняет HTTP GET запрос к эндпоинту /test на локальном FastAPI сервере.

    Функция использует httpx.AsyncClient для выполнения асинхронного HTTP запроса.
    Время ожидания запроса увеличено пропорционально количеству задач для предотвращения тайм-аутов.
    
    :raises httpx.RequestError: В случае ошибок при выполнении запроса.
    """
    timeout_seconds = 4 * TASK_COUNT  # Рассчитываем тайм-аут на основе количества задач
    async with httpx.AsyncClient(timeout=timeout_seconds) as client:
        try:
            response = await client.get('http://127.0.0.1:8000/test')
            response.raise_for_status()  # Проверка на успешный статус ответа
            print(response.json())
        except httpx.HTTPStatusError as exc:
            print(f"HTTP ошибка: {exc.response.status_code} при запросе {exc.request.url}")
        except httpx.RequestError as exc:
            print(f"Ошибка при запросе {exc.request.url}: {exc}")

async def main() -> None:
    """
    Запускает несколько параллельных HTTP запросов к серверу с помощью asyncio.
    
    Использует asyncio.gather для одновременного выполнения нескольких задач.
    """
    # Создаем список задач для параллельного выполнения
    tasks = [fetch() for _ in range(TASK_COUNT)]
    
    # Ожидаем завершения всех задач
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    """
    Точка входа в программу. Запускает event loop с помощью asyncio.run.
    """
    asyncio.run(main())
