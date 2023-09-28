from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

import openai
import os

from dotenv import load_dotenv, find_dotenv
from django.utils import timezone
from django.http import JsonResponse
from chatbot.models import Chat
from chatbot.serializers import ChatSerializer

_ = load_dotenv(find_dotenv())

openai.api_key = os.getenv('OPEN_API_KEY')


def ask_openai(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an helpful assistant focused on learning programming."},
            {"role": "user", "content": message},
        ]
    )

    answer = response.choices[0].message.content.strip()
    return answer


class ChatbotView(APIView):
    def post(self, request, format=None):
        message = request.data.get('message')
        user = request.user if request.user.is_authenticated else None
        response = ask_openai(message)

        # Zakomentowany kod działa dla zalogowanego usera!!!
        # chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        # chat.save()
        #
        # serializer = ChatSerializer(chat)

        return JsonResponse({'message': message, 'response': response})

        # Zamienić return!!!
        # return Response(serializer.data, status=status.HTTP_201_CREATED)
