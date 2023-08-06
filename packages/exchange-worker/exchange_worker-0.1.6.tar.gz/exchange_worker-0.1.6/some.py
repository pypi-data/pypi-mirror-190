import asyncio
from exchange_worker.exchange_worker import ExchangeListener


async def main():
    await ExchangeListener().subscribe(["btcusdt", "ethusdt"], lambda x: print(x))


asyncio.run(main())
