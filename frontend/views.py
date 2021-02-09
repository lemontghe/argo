import json
import pytz
from datetime import date, datetime
from time import time
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate
from django.contrib.auth import login as Login
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, PasswordChangingForm, PasswordResetingForm, PaymentForm, AddSurfForm, EditSiteForm, SiteBalanceForm
from .models import Profile, Ad, AdsPlan, PlansPlan
from django.db import transaction
from django.http import HttpResponse


class PasswordResetingView(PasswordResetView):
    form_class = PasswordResetingForm
    success_url = reverse_lazy("login_page")


@user_passes_test(lambda user: not user.username, login_url='/', redirect_field_name=None)
def login(request, *args, **kwargs):
    uservalue = ''
    passwordvalue = ''
    form = LoginForm(request.POST or None)
    if form.is_valid():
        uservalue = form.cleaned_data.get("username")
        passwordvalue = form.cleaned_data.get("password")
        user = authenticate(username=uservalue, password=passwordvalue)
        if user is not None:
            Login(request, user)
            context= {'form': form,
                      'error': 'The login has been successful'}
            return redirect("/account/")
        else:
            context= {'form': form,
                      'error': 'The username and password combination is incorrect'}
            return render(request, 'frontend/login.html', context )
    else: context= {'form': form}
    return render(request, 'frontend/login.html', context)


@user_passes_test(lambda user: not user.username, login_url='/', redirect_field_name=None)
def signup(request, *args, **kwargs):
    profile_id = request.session.get('ref_profile')
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        if profile_id is not None:
            recommended_by_profile = Profile.objects.get(id=profile_id)
            instance = form.save()
            registered_user = User.objects.get(id=instance.id)
            registered_profile = Profile.objects.get(user=registered_user)
            registered_profile.recommended_by = recommended_by_profile.user
            registered_profile.save()
        else:
            form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')

    return render(request, 'frontend/signup.html', {"form": form})


def index(request, *args, **kwargs):
    d0 = date(2020, 12, 27)
    d1 = date.today()
    delta = d1 - d0

    code = str(kwargs.get('ref_code'))
    try:
        profile = Profile.objects.get(code=code)
        request.session['ref_profile'] = profile.id
    except:
        pass

    return render(request, 'frontend/index.html', {"count": User.objects.all().count(), "days": delta.days})


def about(request, *args, **kwargs):
    return render(request, 'frontend/about.html')


def contacts(request, *args, **kwargs):
    return render(request, 'frontend/contacts.html')


def recovery(request, *args, **kwargs):
    return render(request, 'frontend/recovery.html')


@login_required(login_url='login_page')
def referrals(request):
    user_obj = User.objects.get(username=str(request.user.username))
    code = Profile.objects.get(user=user_obj).code
    profile = Profile.objects.get(user=user_obj)
    return render(request, 'frontend/referrals.html', {"code": code, "profile": profile})


def stats(request, *args, **kwargs):
    user_obj = User.objects.get(username=str(request.user.username))
    profile = Profile.objects.get(user=user_obj)
    return render(request, 'frontend/stats.html', {"count": User.objects.all().count()})


@login_required(login_url='login_page')
def terms(request, *args, **kwargs):
    user_obj = User.objects.get(username=str(request.user.username))
    profile = Profile.objects.get(user=user_obj)
    return render(request, 'frontend/terms.html', {"profile": profile})


@login_required(login_url='login_page')
def insert(request, *args, **kwargs):
    user_obj = User.objects.get(username=str(request.user.username))
    profile = Profile.objects.get(user=user_obj)
    return render(request, 'frontend/insert.html', {"profile": profile})


def save_ads(profile, b):
    if len(profile.ads):
        a = ""
        for i in b:
            for j in range(len(i)):
                if j == len(i)-1:
                    a += i[j]
                else:
                    a += i[j]+"ው"
            a += ""
        profile.ads = a
    profile.save()


def save_asList(profile, obj):
    if len(obj):
        a = obj
        if a.count('') > 1:
            a = a.split('')
        else:
            a = a.replace('', '').split("ው")
        if '' in a: a.remove('')
        if obj == profile.investment_plans: return a
        b = []
        if a[-1] == "Started" or a[-1] == "Stopped":
            b = [a]
        else:
            for x in a:
                x = x.split("ው")
                b.append(x)
        return b
    return []


@login_required(login_url='login_page')
def viewads(request, *args, **kwargs):
    user_obj = User.objects.get(username=str(request.user.username))
    profile = Profile.objects.get(user=user_obj)
    profile_count = Profile.objects.count()
    ads = []
    plans = []
    for i in range(profile_count):
        p = Profile.objects.get(code=i+10000)
        if p.ads in [None, '']: continue
        ads.append(save_asList(p, profile.ads))
        #  for ad in ads[i]:
            #  if int(ad[0]) == 1:
                #  ad.insert(0, 1)
                #  ad.insert(1, 1)
    return render(request, 'frontend/viewads.html', {"profile": profile, "ads": ads})


@login_required(login_url='login_page')
def viewads_add(request, *args, **kwargs):
    user_obj = User.objects.get(username=str(request.user.username))
    profile = Profile.objects.get(user=user_obj)
    plans_count = AdsPlan.objects.count()
    plans = []
    details = []
    for i in range(plans_count):
        plans.append(AdsPlan.objects.get(id=i+1))
    if profile.no_plan in ['no_plan', None]: profile.no_plan = 0
    if profile.ads in ['ads', None]: profile.ads = ''
    if profile.url in ['url', None]: profile.ads = ''
    if profile.title in ['title', None]: profile.ads = ''
    #  profile.purchase_balance = 600
    #  profile.ads = ""
    #  Ad.objects.all().delete()
    #  Ad.id = 0
    #  profile.save()

    if '1' in request.POST:
        no_plan = "Micro"
    elif '2' in request.POST:
        no_plan = "Macro"
    elif '3' in request.POST:
        no_plan = "Extended"
    elif '4' in request.POST:
        no_plan = "Economy"
    elif '5' in request.POST:
        no_plan = "Normal"
    elif '6' in request.POST:
        no_plan = "Premium"
    else:
        numbers = ("Micro",
            "Macro",
            "Extended",
            "Economy",
            "Normal",
            "Premium")
        no_plan = numbers[profile.no_plan-1]

    if request.method == 'POST':
        addsurf_form = AddSurfForm(request.POST, instance=request.user.profile)
        editsite_form = EditSiteForm(request.POST, instance=request.user.profile)
        site_balance_form = SiteBalanceForm(request.POST, instance=request.user.profile)
        b = save_asList(profile, profile.ads)
        if site_balance_form.is_valid():
            if request.is_ajax():
                no_ad = int(list(request.POST)[-1])-1
                coin = site_balance_form.cleaned_data.get('coin')
                if '+' in coin: coin.replace('+', '')
                if int(coin) <= profile.purchase_balance:
                    b[no_ad][3] = str(int(b[no_ad][3])+int(coin))
                    save_ads(profile, b)
                    profile.purchase_balance -= int(coin)
                    profile.save()
                    return HttpResponse(json.dumps({"success": True, "sb": b[no_ad][3], "pb": profile.purchase_balance}), content_type="application/json")
                else:
                    return HttpResponse(json.dumps({"success": False}), content_type="application/json")
            else:
                return HttpResponse(json.dumps({"success": False}), content_type="application/json")
        if "no_plan" not in request.POST:
            if addsurf_form.is_valid():
                if request.is_ajax():
                    ad = Ad.objects.create(left_views=0, site_balance=0, viewed=0)
                    profile.url = addsurf_form.cleaned_data.get('url')
                    profile.title = addsurf_form.cleaned_data.get('title')
                    profile.ads += f"{no_plan}ው{profile.url}ው{profile.title}ው{ad.site_balance}ው{ad.id}ው{ad.viewed}ውStarted"
                    addsurf_form.save()
                    profile.save()
                    b = save_asList(profile, profile.ads)
                    return HttpResponse(json.dumps({"success": True, "ads": b}), content_type="application/json")
                else:
                    return HttpResponse(json.dumps({"success": False}), content_type="application/json")
        else:
            if "stop" in request.POST:
                if request.is_ajax():
                    no_ad = int(list(request.POST)[-1])-1
                    b[no_ad][-1] = "Stopped"
                    save_ads(profile, b)
                    return HttpResponse(json.dumps({"success": True, "ads": b}), content_type="application/json")
                else:
                    return HttpResponse(json.dumps({"success": False, }), content_type="application/json")
            if "resume" in request.POST:
                if request.is_ajax():
                    no_ad = int(list(request.POST)[-1])-1
                    b[no_ad][-1] = "Started"
                    save_ads(profile, b)
                    return HttpResponse(json.dumps({"success": True, "ads": b}), content_type="application/json")
                else:
                    return HttpResponse(json.dumps({"success": False, }), content_type="application/json")
            if "delete" in request.POST:
                if request.is_ajax():
                    no_ad = int(list(request.POST)[-1])-1
                    profile.purchase_balance += int(b[no_ad][3])
                    Ad.objects.filter(id=b[no_ad][4]).delete()
                    b.pop(no_ad)
                    save_ads(profile, b)
                    return HttpResponse(json.dumps({"success": True, "ads": b}), content_type="application/json")
                else:
                    return HttpResponse(json.dumps({"success": False, }), content_type="application/json")

            if editsite_form.is_valid():
                no_ad = int(list(request.POST)[-1])-1
                if request.is_ajax():
                    profile.url = editsite_form.cleaned_data.get('url')
                    profile.title = editsite_form.cleaned_data.get('title')
                    profile.no_plan = int(editsite_form.cleaned_data.get('no_plan'))
                    numbers = ("Micro",
                        "Macro",
                        "Extended",
                        "Economy",
                        "Normal",
                        "Premium")
                    no_plan = numbers[profile.no_plan-1]
                    b[no_ad][0] = no_plan
                    b[no_ad][1] = profile.url
                    b[no_ad][2] = profile.title
                    profile.save()
                    save_ads(profile, b)
                    return HttpResponse(json.dumps({"success": True, "ads": b}), content_type="application/json")
                else:
                    return HttpResponse(json.dumps({"success": False}), content_type="application/json")

        save_ads(profile, b)
        return redirect('/viewads/add/')
    else:
        addsurf_form = AddSurfForm(instance=request.user.profile)
        editsite_form = EditSiteForm(instance=request.user.profile)
        site_balance_form = SiteBalanceForm(instance=request.user.profile)

    b = save_asList(profile, profile.ads)
    profile.save()
    return render(request, 'frontend/viewads_add.html', {"profile": profile,
                                                         "addsurf_form": addsurf_form,
                                                         "editsite_form": editsite_form,
                                                         "plans": plans,
                                                         "site_balance_form": site_balance_form,
                                                         "is_ads": len(profile.ads),
                                                         "ads": b
                                                         })


@login_required(login_url='login_page')
def payment(request, *args, **kwargs):
    user_obj = User.objects.get(username=str(request.user.username))
    profile = Profile.objects.get(user=user_obj)
    return render(request, 'frontend/payment.html', {"profile": profile})


@login_required(login_url='login_page')
def plans(request, *args, **kwargs):
    user_obj = User.objects.get(username=str(request.user.username))
    profile = Profile.objects.get(user=user_obj)
    if profile.plans in ['plans', None]: profile.ads = ''
    if profile.investment_plans in ['plans', None]: profile.investment_plans = ''
    #  if '0' in profile.investment_plans and len(profile.investment_plans) > 1: profile.investment_plans = profile.investment_plans.replace('0', '')

    a = pytz.utc.localize(datetime.utcnow())
    b = a-profile.plan_created
    second = b.seconds
    hour = second/3600

    profile.per_hour = 0
    b = save_asList(profile, profile.investment_plans)
    l = PlansPlan.objects.count()
    prof = [0]*l
    max_prof = [0]*l

    for plan in PlansPlan.objects.all():
        profile.per_hour += plan.per_hour*int(b[plan.id-1])
        if len(save_asList(profile, profile.investment_plans)) != PlansPlan.objects.count():
            profile.investment_plans += f"0"
        if f"{plan.id}" in request.POST:
            if profile.purchase_balance >= plan.price:
                profile.purchase_balance -= plan.price
                b[plan.id-1] = str(int(b[plan.id-1])+1)
                a = ""
                for i in b:
                    a += str(i)
                    a += ""
                profile.investment_plans = a
        plan.save()

    for i in range(l):
        plan = PlansPlan.objects.get(id=i+1)
        max_prof[i] = 24*plan.per_hour*int(b[i])
        if hour > 24:
            profile.profit = 24*profile.per_hour
            prof[i] = 24*plan.per_hour*int(b[i])
        else:
            profile.profit = hour*profile.per_hour
            prof[i] = hour*plan.per_hour*int(b[i])

    if "collect" in request.POST:
        profile.balance += profile.profit/2
        profile.purchase_balance += profile.profit/2
        profile.profit = 0
        profile.plan_created = pytz.utc.localize(datetime.utcnow())
    if profile.profit > profile.per_hour*24:
        profile.profit = profile.per_hour*24
        max_profit = 100
    elif profile.profit == 0:
        max_profit = 0
    else:
        max_profit = int((profile.profit/(profile.per_hour*24)*100))
        #  max_profit = int(sum(max_prof))

    profile.save()

    return render(request, 'frontend/plans.html', {"profile": profile,
                                                   "plans": zip(PlansPlan.objects.all(), prof, max_prof, save_asList(profile, profile.investment_plans)),
                                                   "profit": profile.profit,
                                                   "max_profit": max_profit,
                                                   })


@login_required(login_url='login_page')
def exchange(request, *args, **kwargs):
    user_obj = User.objects.get(username=str(request.user.username))
    profile = Profile.objects.get(user=user_obj)
    return render(request, 'frontend/exchange.html', {"profile": profile})


@login_required(login_url='login_page')
def settings(request, *args, **kwargs):
    user_obj = User.objects.get(username=str(request.user.username))
    profile = Profile.objects.get(user=user_obj)

    if request.method == 'POST':
        form = PasswordChangingForm(request.user, request.POST)
        payment_form = PaymentForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/account/')
        else:
            messages.error(request, 'Please correct the error below.')
        if payment_form.is_valid():
            payment_form.save()
            messages.success(request, 'Your wallet was successfully linked!')
            return redirect('/account/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        payment_form = PaymentForm(instance=request.user.profile)
        form = PasswordChangingForm(request.user)

    return render(request, 'frontend/settings.html', {"profile": profile, "form": form, "payment_form": payment_form })


@login_required(login_url='login_page')
def account(request, *args, **kwargs):
    user_obj = User.objects.get(username=str(request.user.username))
    profile = Profile.objects.get(user=user_obj)
    direct_referrals = profile.recs_number()
    if profile.investment_plans == None: profile.investment_plans = ''
    profile_count = Profile.objects.count()
    ads = []
    count = 0
    for i in range(profile_count):
        p = Profile.objects.get(code=i+10000)
        print(p.ads)
        if p.ads in [None, '']: continue
        ads.append(save_asList(p, profile.ads))
    #  for ad in ads:
        #  count += len(ad)
        #  print(ad)
    return render(request, 'frontend/account.html', {"profile": profile, "direct_referrals": direct_referrals, "investment_plans": len(profile.investment_plans)})


def error_404(request, *args, **argv):
    return render(request, 'frontend/404.html', {}, status=404)
