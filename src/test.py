import asyncio

from client.root import RootClient
from store.root import RootStore

# access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MjIxZDBkYS0yMWMxLTQ3NGQtYmYyYi1mMzRlYWE5MjdiOWEiLCJzaWQiOiJjMTVkNDJkZi1jODdjLTQwNzEtYmJmOS0zZjUwYWQzM2YzMDEiLCJleHAiOjE3NjQ2ODYzMDEsImp0aSI6IjEyZDMyMTNlLWIxMGMtNGNlZC1iMjQwLTUxZWQ3MTYzNzdmNyIsInR5cGUiOiJhY2Nlc3MifQ.E6WtVtCvt5pH0qgqMGf0G_-Vz3mWfcnd_QO2d2i_I_E"
# refresh_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MjIxZDBkYS0yMWMxLTQ3NGQtYmYyYi1mMzRlYWE5MjdiOWEiLCJzaWQiOiJjMTVkNDJkZi1jODdjLTQwNzEtYmJmOS0zZjUwYWQzM2YzMDEiLCJleHAiOjE3NjUyOTAyMDEsImp0aSI6IjY3YzE2MWY1LTYzOWYtNDc0NC05NTYwLWJkN2ZkNmNiNWMxYiIsInR5cGUiOiJyZWZyZXNoIn0.J--8_BU-EdJ_S9y6sgzM3ALaRJVkYhQM_hVjwbIM6lA"

root_store = RootStore()


async def main():
    root_client = RootClient(root_store)
    try:
        await root_client.auth.login("neiroslav", "123")

        #

        chats = await root_client.chat.list_by_user(0)
        print(chats)

        #

        await root_client.auth.logout()
    finally:
        await root_client.close()


asyncio.run(main())
