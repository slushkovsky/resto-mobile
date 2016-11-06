# FIXME: separate into python files in module views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from rest_framework import generics
from smsaero import utils as SMS
import redis
import json
import re
import uuid

from .models import Venue, PhoneAuthUser, User
from .serializers import VenueSerializer, UserSerializer, SessionSerializer
from .filters import VenueFilter
from .utils import generate_sms_code


r = redis.Redis()


def register_step_phone(request):
    phone = json.loads(request.body)['phone']
    regexp = re.compile(r"^\+\d{11}$")

    if regexp.match(phone) is None:
        response = {"status": "error",
                    "error_code": "BAD_PHONE",
                    "message": "Некорректный формат телефона"}
        return JsonResponse(status=400, data=response)

    if PhoneAuthUser.objects.filter(phone=phone).exists():
        response = {"status": "error",
                    "error_code": "PHONE_CONFLICT",
                    "message": "Пользователь с данным номером уже зарегистрирован"}
        return JsonResponse(status=409, data=response)

    try:
        sms_code = generate_sms_code()
        sms = SMS.send_sms(phone, sms_code)
        if sms is None:  # FIXME: доработать код smsaero
            raise Exception('Требуется сигнатура')

        token = uuid.uuid4().hex  # FIXME: need something more secure
        r.set('%s_sms' % token, sms_code)  # TODO: add redis timeliving
        r.set('%s_phone' % token, phone)

        response = {"status": "OK", "signup_token": token}
        return JsonResponse(response)
    except Exception:
        response = {"status": "error",
                    "error_code": "SMS_UNAVAILABLE",
                    "message": "Сервис отправки SMS недоступен"}
        return JsonResponse(status=503, data=response)


def register_step_code(request):
    data = json.loads(request.body)
    code = data['code']
    token = data['signup_token']
    if code != r.get('%s_sms' % token):
        return JsonResponse(status=400,  # FIXME: Errors codes and messages
                            data={"status": "Error", "error_code": "", "message": ""})
    return JsonResponse({"status": "OK"})


def register_step_password(request):
    data = json.loads(request.body)
    token = data["signup_token"]
    password = data["password"]  # hash!
    phone = r.get('%s_phone' % token)

    if phone is None:
        return JsonResponse(status=400,  # FIXME: Errors codes and messages
                            data={"status": "Error", "error_code": "", "message": ""})

    PhoneAuthUser.objects.create(phone=phone, password=password, user=User.objects.create())
    return JsonResponse({"status": "OK"})


def authorize(request):
    json.loads(request.body)


class SessionView(generics.CreateAPIView):  # TODO: write serializer
    serializer_class = SessionSerializer


class VenuesView(generics.ListAPIView):
    serializer_class = VenueSerializer

    def get(self, request, *args, **kwargs):
        qs = VenueFilter(request.GET, queryset=Venue.objects.all())
        response = map(model_to_dict, qs)
        return JsonResponse(response, safe=False)


class UsersView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return request.user


@login_required
def get_orders(request):
    session = request.GET.get('session')
    if not session:
        return HttpResponse(status=400)
