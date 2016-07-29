import telepot
import json
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .parse import parse_rss

telegramBot = telepot.Bot('')


def showPosts():
    return render_to_string('feed.md', {'items': parse_rss()[1]})


def showHelp():
    return render_to_string('help.md')


class BotView(View):
    def post(self, request, botToken):
        if botToken != '':
            return HttpResponseForbidden('Invalid token')

        commands = {
            '/start': showHelp(),
            '/help': showHelp(),
            '/feed': showPosts(),
        }

        raw = request.body.decode('utf-8')

        try:
            payload = json.loads(raw)
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')
        else:
            chat_id = payload['message']['chat']['id']
            cmd = payload['message'].get('text')
            func = commands.get(cmd.split()[0].lower())
            if func:
                if cmd == '/start':
                    (code, response) = parse_rss()
                    if code == 200:
                        telegramBot.sendMessage(chat_id, func, parse_mode='Markdown')
                    else:
                        telegramBot.sendMessage(chat_id, 'Some problems occurs!', parse_mode='Markdown')
                else:
                    telegramBot.sendMessage(chat_id, func, parse_mode='Markdown')
            else:
                telegramBot.sendMessage(chat_id, 'Not valid command!')

        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(BotView, self).dispatch(request, *args, **kwargs)
