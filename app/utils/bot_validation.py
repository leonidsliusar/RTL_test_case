import json
from json import JSONDecodeError

from pydantic_core import ValidationError

from app.core.models import InputModel


def validate(bot):
    def validate_inner(func):
        example_request = ('Невалидный запос. Пример запроса:\n'
                           '{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", '
                           '"group_type": "month"}.\n group_type должен быть один из hour, day, week, month')

        async def wrapper(message):
            try:
                aggregate_filter = json.loads(message.text)
                InputModel(**aggregate_filter)
            except (JSONDecodeError, ValidationError):
                return await bot.send_message(chat_id=message.chat.id, text=example_request)
            return await func(message)

        return wrapper
    return validate_inner
