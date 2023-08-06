import asyncio
from enkanetwork import EnkaNetworkAPI

client = EnkaNetworkAPI(lang="th", user_agent="EnkaNetwork.py/1.4.0 (Dev mode)")

async def main():
    async with client:
        # data = await client.fetch_user_by_username(
        #     profile_id="Algoinde"
        # )
        data = await client.fetch_user(618285856, info=True)
        print(data.owner.username)

asyncio.run(main())