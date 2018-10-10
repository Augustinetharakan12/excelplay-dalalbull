import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

import redis

redis_conn = redis.Redis("localhost", 6378)

for userid in redis_conn.hkeys("online-users"):
	print(userid)

print("consumers")

from .models import * 

class PortfolioConsumer(AsyncConsumer):
	async def websocket_connect(self, event):
		print("connected",event)

		
		await self.send({
			"type":"websocket.accept"
			})

		#await asyncio.sleep(10)
		await self.send({
			"type":"websocket.send",
			"text":"Hello World"
			})

	#When a message is received from the websocket
	async def websocket_receive(self, event):
		print("receive",event)

	async def websocket_disconnect(self, event):
		print("disconnected",event)