import asyncio


async def coro(sec):
    print(f'Coroutine {sec} is starting')    
    await asyncio.sleep(sec)
    print(f'Coroutine {sec} is done')
    return sec


async def main():
    futures = {asyncio.ensure_future(coro(i)): f'item({i})' for i in range(1,5)}    

    for future in as_completed_hooked(futures.keys()):
        real_future = await future
        index = futures[real_future]
        print(f'The item is {index}')
        print(f'The result is {real_future.result()}')


def as_completed_hooked(futures):
    wrappers = []

    loop = asyncio.get_event_loop()
    for future in futures:  
        wrapper = loop.create_future()
        future.add_done_callback(wrapper.set_result)
        wrappers.append(wrapper)

    for x in asyncio.as_completed(wrappers):
        yield x


if __name__ == '__main__':
    asyncio.run(main()) 