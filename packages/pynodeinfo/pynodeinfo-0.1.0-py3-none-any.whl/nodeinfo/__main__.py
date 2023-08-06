import nodeinfo
import aiohttp
import asyncio
import sys

async def main():
    """Read a hostname from arguments
    and print it's nodeinfo
    """

    for host in sys.argv[1:]:

        print(await nodeinfo.load(host))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
