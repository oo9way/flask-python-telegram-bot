import argparse
import logging
import os

from django.apps import apps
from django.conf import settings
from flask import Flask, request, render_template
from telegram import Update

from tasks.configuration import make_celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
apps.populate(settings.INSTALLED_APPS)

from dispatcher import bot, dispatcher
import sys

from data.models import Script

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
)

celery = make_celery(app)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/webhook/', methods=['POST'])
def webhook() -> str:
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'


@app.route("/", methods=['GET'])
def index():
    context = {
        "items": Script.objects.filter(is_approved=True)
    }
    return render_template("list.html", **context)


@app.route('/details/<id>/', methods=['GET'])
def detail(id):
    try:
        script = Script.objects.get(pk=id)
    except Script.DoesNotExist:
        script = None

    context = {
        "item": script
    }
    return render_template("detail.html", **context)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Telegram Bot with Webhook')
    parser.add_argument('--webhook', type=str, help='Webhook URL')
    parser.add_argument('--port', type=int, default=4500, help='Port number (default: 4500)')
    args = parser.parse_args()

    if args.webhook:
        bot.set_webhook(url=args.webhook)
        sys.stdout.write(f"Webhook set to: {args.webhook}")

    # Run Flask app
    app.run(port=args.port)
