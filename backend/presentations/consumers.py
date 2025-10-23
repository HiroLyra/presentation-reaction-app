import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ReactionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        WebSocket接続時の処理
        """
        self.presentation_id = self.scope["url_route"]["kwargs"]["presentation_id"]

        self.room_group_name = f"presentation_{self.presentation_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        """
        WebSocket切断時の処理
        """
        # グループから離脱
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """
        クライアントからメッセージを受信した時の処理
        """
        data = json.loads(text_data)
        reaction_type = data.get("reaction_type")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "reaction_message",
                "reaction_type": reaction_type,
            },
        )

    async def reaction_message(self, event):
        """
        グループから受け取ったメッセージをクライアントに送信
        """
        reaction_type = event["reaction_type"]

        await self.send(
            text_data=json.dumps(
                {
                    "reaction_type": reaction_type,
                }
            )
        )
