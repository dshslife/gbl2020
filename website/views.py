from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .utils import MongoDBManager
from pymongo.database import Database
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.decorators import method_decorator
from webpush import send_user_notification

from webpush import send_group_notification
db: Database = MongoDBManager()['startup']

def initNewUser(email):
  try:
    db['users'].insert({'email': email,
    'bingo': [],
    'booth': [],
    'award': False,
    'bingo_line': 0})
  except Exception as e:
    print(e)
    return False
  return True

def index(request):
  if not request.user.is_authenticated:
    return redirect('/login')
  else:
    rep = db['users'].find_one({'email': request.user.email})
    if not rep:
      initNewUser(request.user.email)
      request.session['_id'] = str(db['users'].find_one({'email': request.user.email})['_id'])
      print("INIT NEW USER")
    if not '_id' in request.session:
      request.session['_id'] = str(db['users'].find_one({'email': request.user.email})['_id'])
    plan = db['plan'].find({})
    booth = db['booth'].find({})
    return render(request, "website/information.html", {'plan': plan, 'booth': booth, 'webpush': {'group': 'startup'}})
# Create your views here.

def test(request):
  return render(request, 'website/login.html', {'webpush': {'group': 'startup'}})


def map(request):
  return render(request, 'website/map.html')

@login_required(login_url='/')
def bingo(request):
  bingo = list(db['bingo'].find({}))
  user_bingo = dict(db['users'].find_one({'email': request.user.email}))
  print(user_bingo['bingo'])
  for i in range(len(bingo)):
    if bingo[i]['_id'] in user_bingo['bingo']:
      print(bingo[i])
      bingo[i]['complete'] = True
    else:
      bingo[i]['complete'] = False
  n = 3
  bingo = [bingo[i*n: (i + 1) * n] for i in range((len(bingo) + n - 1) // n)]
  return render(request, "website/bingo.html", {'bingo': bingo, 'award': user_bingo['award']})

@login_required(login_url='/')
def profile(request):
  if not '_id' in request.session:
    request.session['_id'] = str(db['users'].find_one({'email': request.user.email})['_id'])
  booth = db['users'].find_one({'email': request.user.email})['booth']
  print('THIS IS BOOTH')
  return render(request, "website/profile.html", {"visited_booth": booth, 'webpush': {'group': 'startup'}})

def logout(request):
  auth_logout(request)
  return redirect('/')

@login_required(login_url='/')
def information(request):
  plan = db['plan'].find({})
  booth = db['booth'].find({})
  return render(request, "website/information.html", {'plan': plan, 'booth': booth})

class BoothCheck(View):
  @method_decorator(csrf_exempt)
  def dispatch(self, request, *args, **kwargs):
    return super(BoothCheck, self).dispatch(request, *args, **kwargs)

  def post(self, request):
    print(request.body)
    if request.body == None:
      return HttpResponse(status=400)
    else:
      try:
        data = json.loads(request.body)
        print(data)
        if not 'email' in data:
          return JsonResponse(status=400, data={'status': 'NO_EMAIL_ERROR'})
        if 'booth' in data:
          booth = db['booth'].find_one({'club': data['booth']})
          if booth == None:
            return JsonResponse(status=400, data={ 'status': 'NO_BOOTH_ERROR'})
          usertmp = dict(db['users'].find_one({'email': data['email']}))
          if usertmp == None:
            return JsonResponse(status=400, data={ 'status': 'NOT_FOUND_USER_ERROR'})
          else:
            db['users'].update_one({'email': data['email']},{'$push': {'booth': booth['_id']}})
        if 'bingo' in data:
          print(data['bingo'])
          bingo = db['bingo'].find_one({'name': data['bingo']})
          if bingo == None:
            return JsonResponse(status=400, data={ 'status': 'NO_BINGO_ERROR'})
          usertmp = dict(db['users'].find_one({'email': data['email']}))
          if usertmp == None:
            return JsonResponse(status=400, data={ 'status': 'NOT_FOUND_USER_ERROR'})
          else:
            db['users'].update_one({'email': data['email']},{'$push': {'bingo': bingo['_id']}})
        return HttpResponse(status=200)
      except Exception as e:
        return JsonResponse(status=500, data={'error': str(e)})
from webpush.utils import send_to_subscription

class WebPush(View):
  @method_decorator(csrf_exempt)
  def dispatch(self, request, *args, **kwargs):
    return super(WebPush, self).dispatch(request, *args, **kwargs)

  def post(self, request):
    if request.body == None:
      return HttpResponse(status=404)
    else:
      data = json.loads(request.body)
      send_group_notification(group_name="startup",payload={"head": "스타트업 밋업데이 2020", "icon": "https://i.imgur.com/EqNRGOC.png", "url": "https://meetstartup.today", "body": data['message']}, ttl=1000)
      return HttpResponse(status=200)