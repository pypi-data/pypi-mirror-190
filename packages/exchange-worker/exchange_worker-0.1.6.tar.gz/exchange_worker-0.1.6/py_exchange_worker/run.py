import asyncio
from asyncio import Queue, sleep

q = Queue()

loop = asyncio.get_event_loop()


async def h(tick):
    await q.put(tick)


def handler(tick):
    l = asyncio.get_event_loop()
    l.run_until_complete(h(tick))
    print(tick)


async def sub():
    from exchange_worker.exchange_worker import ExchangeListener
    await ExchangeListener().subscribe(
        ["ethusdt", "btcusdt"],
        handler
    )


async def main():
    # await ExchangeListener().subscribe(["ethusdt", "btcusdt"], lambda x: print(">>> " + str(x)))
    asyncio.create_task(sub())

    while True:
        # print(1)
        try:
            # attempt retrieve an item
            item = await q.get()
            print(item)
        except asyncio.QueueEmpty:
            pass
        # item = await q.get()
        # await sleep(1)


loop.run_until_complete(main())
