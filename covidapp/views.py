from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Message, UserProfile
from .serializers import MessageSerializer, UserSerializer
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage


def home(request):
    return render(request, 'index.html')


def finder(request):
    return render(request, 'finder.html')


def signup(request):
    return render(request, 'signup.html')


def fallback(request):
    return render(request, 'fallback.html')


def takesurvey(request):
    return render(request, 'survey.html')


def trackerna(request):
    return render(request, 'trackerna.html')


def awareness(request):
    return render(request, 'awareness.html')


def diet(request):
    return render(request, 'diet.html')


def chatindex(request):
    if request.user.is_authenticated:
        return redirect('chats')
    if request.method == 'GET':
        return render(request, 'chatindex.html', {'error': ''})
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
        else:
            return render(request, 'chatindex.html', {'error': 'Invalid Username/Password'})
        return redirect('chats')


@csrf_exempt
def user_list(request, pk=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        if pk:
            users = User.objects.filter(id=pk)
        else:
            users = User.objects.all().filter(is_active=True)
        serializer = UserSerializer(
            users, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        if len(data['username'].split(' ')) == 1:
            try:
                email = data['email']
                user = User.objects.create_user(username=data['username'], password=data['password'], email=email)
                user.is_active = False
                user.save()
                UserProfile.objects.create(user=user)
                current_site = get_current_site(request)
                mail_subject = 'Activate your hospital finder account.'
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return JsonResponse({'login': '0', 'created': '1'}, status=201)
            except Exception:
                return JsonResponse({'login': '0', 'created': '0'}, status=400)
        else:
            return JsonResponse({'login': '0', 'created': '0'}, status=400)


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(
            sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(
            messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('chatindex')
    if request.method == "GET":
        return render(request, 'chatchat.html',
                      {'users': User.objects.exclude(username=request.user.username)})


def message_view(request, sender, receiver):
    if not request.user.is_authenticated:
        return redirect('chatindex')
    if request.method == "GET":
        return render(request, "chatmessages.html",
                      {'users': User.objects.exclude(username=request.user.username),
                       'receiver': User.objects.get(id=receiver),
                       'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                       Message.objects.filter(sender_id=receiver, receiver_id=sender)})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')
