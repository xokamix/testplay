import json
from channels.generic.websocket import AsyncWebsocketConsumer
from lessons.models import Lesson
from django.utils.timezone import make_aware
from dateutil.rrule import rrulestr
import datetime
import logging

logger = logging.getLogger(__name__)

class LessonConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'lesson_updates'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        logger.info("WebSocket connection accepted.")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        logger.info("WebSocket disconnected.")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')

        if action in ['schedule', 'update', 'delete']:
            lesson_id = text_data_json.get('lesson_id', None)
            await self.update_lesson_calendar(lesson_id, action)

    async def update_lesson_calendar(self, lesson_id, action):
        message = {'action': action, 'lesson_id': lesson_id}

        if action != 'delete':
            try:
                lesson = Lesson.objects.get(id=lesson_id)
                schedule = lesson.schedule
                end_recurrence = lesson.end_recurrence
                recurrence_rule = lesson.recurrence_rule

                occurrences = []
                if recurrence_rule:
                    rrule = rrulestr(recurrence_rule, dtstart=schedule)
                    end_date = end_recurrence if end_recurrence else schedule + datetime.timedelta(days=365)
                    for occurrence in rrule.between(make_aware(datetime.datetime.now()), end_date, inc=True):
                        occurrences.append(occurrence.strftime("%Y-%m-%d %H:%M"))
                
                message['occurrences'] = occurrences
            except Lesson.DoesNotExist:
                logger.error(f"Lesson with id '{lesson_id}' does not exist.", exc_info=True)
                return
            except Exception as e:
                logger.error(f"Error updating lesson calendar for lesson_id {lesson_id}: {e}", exc_info=True)
                return

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'lesson_update_message',
                'message': message
            }
        )

    async def lesson_update_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))
        logger.info(f"Message broadcasted to WebSocket: {message}")