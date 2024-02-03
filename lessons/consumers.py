import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)

class LessonConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'lesson_updates'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        logger.info("WebSocket connection accepted.")

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        logger.info("WebSocket disconnected.")

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'lesson_message',
                'message': message
            }
        )

    # Receive message from room group
    async def lesson_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
        logger.info(f"Message sent to WebSocket: {message}")

    async def websocket_disconnect(self, message):
        '''
        Called when a WebSocket is disconnected.
        '''
        try:
            await self.disconnect(message)
            logger.info(f"WebSocket connection closed, reason: {message}")
        except Exception as e:
            logger.error("Error during WebSocket disconnection: %s", str(e), exc_info=True)