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
from django.views.decorators.http import require_GET

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
    count = User.objects.all().count()
    if not count: count = 0
    return render(request, 'frontend/index.html', {"count": count, "days": delta.days})


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
    count = User.objects.all().count()
    if not count: count = 0
    return render(request, 'frontend/stats.html', {"count": count})


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
    for i in range(profile_count):
        p = Profile.objects.get(code=i+1)
        if p.ads in [None, '']: continue
        a = []
        adss = save_asList(p, p.ads)
        for ad in adss:
            if int(ad[3]) > 1:
                a.append(ad)
        ads.append(a)
    return render(request, 'frontend/viewads.html', {"profile": profile, "ads": ads})


@login_required(login_url='login_page')
def viewads_add(request, *args, **kwargs):
    user_obj = User.objects.get(username=str(request.user.username))
    profile = Profile.objects.get(user=user_obj)
    plans_count = AdsPlan.objects.all().count()
    plans = [ad for ad in AdsPlan.objects.all()]
    details = []
    if profile.no_plan in ['no_plan', None]: profile.no_plan = 0
    if profile.ads in ['ads', None]: profile.ads = ''
    if profile.url in ['url', None]: profile.ads = ''
    if profile.title in ['title', None]: profile.ads = ''
    profile.purchase_balance = 1200000
    profile.save()

    ch = [ad.name[4:] for ad in AdsPlan.objects.all()]
    for i in range(plans_count):
        if f'{i+1}' in request.POST:
            no_plan = AdsPlan.objects.get(id=i+1).name
        else:
            numbers = tuple(ch)
            no_plan = numbers[profile.no_plan-1]
    if plans_count == 0: no_plan = 0

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
                    profile.no_plan = 0
                    save_ads(profile, b)
                    return HttpResponse(json.dumps({"success": True, "ads": b}), content_type="application/json")
                else:
                    return HttpResponse(json.dumps({"success": False, }), content_type="application/json")

            if editsite_form.is_valid():
                no_ad = int(list(request.POST)[-1])-1
                if no_ad == "no_plan": no_ad = 0
                if request.is_ajax():
                    profile.url = editsite_form.cleaned_data.get('url')
                    profile.title = editsite_form.cleaned_data.get('title')
                    profile.no_plan = int(editsite_form.cleaned_data.get('no_plan'))
                    ch = tuple([ad.name[4:] for ad in AdsPlan.objects.all()])
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
    print("-"*20)
    print(profile)
    if profile.per_hour in ['per_hour', None]: profile.per_hour = 0
    print(profile.per_hour)

    a = pytz.utc.localize(datetime.utcnow())
    b = a-profile.plan_created
    second = b.seconds
    hour = second/3600

    if PlansPlan.objects.all().count():
        try:
            plan = PlansPlan.objects.get(id=1)
            if hour > 24:
                profile.profit = 24*(profile.per_hour/plan.per_hour)
            else:
                profile.profit = hour*(profile.per_hour/plan.per_hour)
        except:
            plan = None
            profile.profit = 0

        if plan:
            if f"inv" in request.POST and request.is_ajax:
                coin = int(request.POST["coin"])
                if profile.purchase_balance >= coin:
                    profile.purchase_balance -= coin
                    profile.investment_plans = a
                    profile.per_hour += coin*plan.per_hour
                    if profile.profit > (profile.per_hour/plan.per_hour)*24:
                        profile.profit = (profile.per_hour/plan.per_hour)*24
                    profile.profit = profile.per_hour*hour
                    profile.save()
                    return HttpResponse(json.dumps({"success": True, "pb": profile.purchase_balance, "ph": profile.per_hour, "profit": profile.profit}), content_type="application/json")
                else:
                    return HttpResponse(json.dumps({"success": False}), content_type="application/json")

    else: plan = None


    print("-"*20)
    print(profile.profit)
    print(profile.per_hour)
    if profile.profit > (profile.per_hour/plan.per_hour)*24:
        profile.profit = (profile.per_hour/plan.per_hour)*24
        max_profit = 100
    elif profile.profit == 0:
        max_profit = 0
    else:
        max_profit = int((profile.profit/((profile.per_hour/plan.per_hour)*24)*100))
    profile.profit = profile.per_hour*hour
    profile.save()

    if "collect" in request.POST:
        if request.is_ajax:
            profile.balance += profile.profit/2
            profile.purchase_balance += profile.profit/2
            profile.profit = 0
            profile.plan_created = pytz.utc.localize(datetime.utcnow())
            profile.save()
            return HttpResponse(json.dumps({"success": True, "profit": profile.profit, "max_profit": 0, "pb": profile.purchase_balance}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"success": False}), content_type="application/json")

    return render(request, 'frontend/plans.html', {"profile": profile,
                                                   "plan": plan,
                                                   "per_hour": profile.per_hour,
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
    profile_count = Profile.objects.all().count()
    ads = []
    count = 0
    for i in range(profile_count):
        p = Profile.objects.get(code=i+1)
        if p.ads in [None, '']: continue
        ads.append(save_asList(p, p.ads))
    for ad in ads:
        count += len(ad)
    return render(request, 'frontend/account.html', {"profile": profile, "direct_referrals": direct_referrals, "count": count})


def error_404(request, *args, **argv):
    return render(request, 'frontend/404.html', {}, status=404)

@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /admin/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
