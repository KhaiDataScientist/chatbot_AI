from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'chatbot_ai/index.html')

def chat(request):
    return render(request, 'chatbot_ai/chat.html')
def account(request):
    return render(request, 'chatbot_ai/account.html')
