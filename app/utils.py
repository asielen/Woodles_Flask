from itsdangerous import URLSafeTimedSerializer
from werkzeug.routing import BaseConverter

from .. import app

ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])


class card_question_parser(BaseConverter):
    """
    takes a string like: card:question or card
    and returns
    card, quesion
    or
    card
    """

    def to_python(self, value):
        if value.find(":"):
            return value.split(':')
        return value

    def to_url(self, values):
        if len(values) > 2:  # Strip out everything extra
            values = values[:2]
        return ':'.join(BaseConverter.to_url(value)
                        for value in values)
