import asyncio
from exchange_worker import ExchangeListener


async def main():
    await ExchangeListener().subscribe([], lambda x: print(">>> " + str(x)))

asyncio.run(main())
