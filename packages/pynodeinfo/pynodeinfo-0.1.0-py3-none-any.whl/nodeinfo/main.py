import aiohttp
import asyncio

async def load(host):

    async with aiohttp.ClientSession() as session:
        nodeinfo_uri = await get_nodeinfo_uri(host, session)

        async with session.get(nodeinfo_uri) as response:

            if not response.ok:
                raise ValueError("NodeInfo Endpoint returns an error: " + response.status)

            if response.content_type != "application/json":
                raise ValueError("NodeInfo endpoint returned content of type: " + response.content_type)

            info = await response.json()
            return info

async def get_nodeinfo_uri(host, session):
    async with session.get("https://" + host + "/.well-known/nodeinfo") as response:

        if not response.ok or response.content_type != "application/json":
            raise ValueError("Host does not provide nodeinfo")

        info = await response.json()

        return get_max_uri(info["links"])

def get_max_uri(links):

    max = links[0]
    max_version = max["rel"].split("/")[-1].split(".")

    for link in links[1:]:
        version = link["rel"].split("/")[-1].split(".")
        if version[0] > max_version[0]:
            max = link
            continue
        if version[1] > max_version[1]:
            max = link
            continue

    return max["href"]

