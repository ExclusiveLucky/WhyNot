import httpx
import asyncio

task_count = 5

async def fetch():
    async with httpx.AsyncClient(timeout=4*task_count) as client:  # Увеличьте время ожидания до 10 секунд
        response = await client.get('http://127.0.0.1:8000/test')
        print(response.json())

async def main():
    tasks = [fetch() for _ in range(task_count)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())