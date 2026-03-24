import asyncio, time

def deliver_sync(ntime: int, name):
    print(f"Доставляємо товар {name} до вас")
    time.sleep(ntime)
    print(f"Товар {name} доставлено")

time_start = time.time()
deliver_sync(5, "М'яч")
deliver_sync(3, "Телефон")
time_end = time.time()

time_diff = time_end - time_start
print(int(time_diff), "секунд виконувалися функції")

print("")

async def deliver_async(ntime, name):
    print(f"Доставляємо товар {name} до вас")
    await asyncio.sleep(ntime)
    print(f"Товар {name} доставлено")

async def main():
    time_start = time.time()
    await asyncio.gather(deliver_async(3, "М'яч"), deliver_async(3, "Телефон")) 
    time_end = time.time()

    time_diff = time_end - time_start
    print(int(time_diff), "секунд виконувалися функції")

asyncio.run(main())