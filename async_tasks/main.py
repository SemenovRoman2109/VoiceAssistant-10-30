import asyncio

async def say_hello():
    print("Hello")
    await asyncio.sleep(2)
    print("2 seconds later")

asyncio.run(say_hello())