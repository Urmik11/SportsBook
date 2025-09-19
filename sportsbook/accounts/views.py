from django.shortcuts import render,redirect
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from .models import Matchess,Deposite,Withdraw,bets
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .scraper import get_live_score
from django.http import JsonResponse
from .models import Account,WebsiteUser
from .forms import RegistrationForm
from functools import wraps

def main(request):
    if request.session.get('website_user_id'):
        return redirect('home')
    return render(request, 'accounts/main.html')

def website_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.session.get('website_user_id'):
            return view_func(request, *args, **kwargs)
        return redirect('login')
    return wrapper

def register(request):
    if request.session.get('website_user_id'):
        return redirect('home')
    
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = WebsiteUser(username=username, email=email)
            user.set_password(password)
            user.save()
            Account.objects.create(user=user, username=username, balance=0, exp=0)
            messages.success(request, "Registration Successful!")
            return redirect("login")
        else:
            pass
    else:
        form = RegistrationForm()
    return render(request, "accounts/register.html", {"form": form})

def user_login(request):
    if request.session.get('website_user_id'):
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = WebsiteUser.objects.get(username=username)
            if user.check_password(password):
                request.session['website_user_id'] = user.id  
                messages.success(request, f"Welcome, {user.username}!")
                return redirect("home")
            else:
                messages.error(request, "Invalid credentials")
        except WebsiteUser.DoesNotExist:
            messages.error(request, "Invalid credentials")

    return render(request, "accounts/login.html")

def user_logout(request):
    if 'website_user_id' in request.session:
        del request.session['website_user_id']
    return redirect("main")

@website_login_required
def home(request):
    searchTerm=request.GET.get('searchMatch')
    live_matches=Matchess.objects.filter
    if searchTerm:
        live_matches = Matchess.objects.filter(match_status="Active", match_name__icontains=searchTerm)
        upcoming_matches = Matchess.objects.filter(match_status="UpComing", match_name__icontains=searchTerm)
        completed_matches = Matchess.objects.filter(match_status="Completed", match_name__icontains=searchTerm)
    else:
        live_matches = Matchess.objects.filter(match_status="Active").order_by('-date', '-time')
        upcoming_matches = Matchess.objects.filter(match_status="UpComing").order_by('date', 'time')
        completed_matches = Matchess.objects.filter(match_status="Completed").order_by('-date', '-time')
    return render(request, 'accounts/home.html', {'searchTerm':searchTerm,'name':'UD','live_matches':live_matches,'upcoming_matches':upcoming_matches,'completed_matches':completed_matches})

def deposit(request):
    return render(request, 'accounts/deposit.html')


def deposit_submit(request):
    """Handle full deposit form submission (Step 2)"""
    if request.method == "POST":
        try:
            amount = int(request.POST.get("amount"))
        except (TypeError, ValueError):
            messages.error(request, "Invalid amount")
            return redirect('deposit')

        if amount < 300 or amount > 100000:
            messages.error(request, "Deposit amount must be between 300 and 100000")
            return redirect('deposit')

        username = request.POST.get("username", "Guest")
        UTR = request.POST.get("UTR")
        payment_SS = request.FILES.get("payment_SS")

        Deposite.objects.create(
            username=username,
            amount=amount,
            UTR=UTR,
            payment_SS=payment_SS
        )

        messages.success(request, f"Deposit of {amount} has been created successfully!")
        return redirect('deposit')

    return redirect('deposit')

def withdraw(request):
    return render(request, 'accounts/withdraw.html')

def withdraw_submit(request):
    if request.method == "POST":
        amount = int(request.POST.get("amount"))
        username = request.POST.get("username", "Guest")

        Withdraw.objects.create(
            username=username,
            amount=amount,
        )
        return redirect('withdraw')

    return redirect('withdraw')

def bet_submit(request):
    if request.method == "POST":
        try:
            username = request.POST.get("username", "Guest")
            match_id = int(request.POST.get("match_id"))
            bet_amount = int(request.POST.get("bet_amount"))
            win_amount = int(request.POST.get("win_amount"))
            bet_team = request.POST.get("bet_team")

            if bet_amount < 100:
                return JsonResponse({"success": False, "message": "Bet amount must be at least 100"})

            bets.objects.create(
                username=username,
                match_id=match_id,
                bet_amount=bet_amount,
                win_amount=win_amount,
                bet_team=bet_team
            )

            return JsonResponse({"success": True, "message": "Bet placed Successfully"})

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Invalid request"})


def matchs(request,id):
    match=get_object_or_404(Matchess,match_id=id)
    bet=bets.objects.filter(match_id=id).order_by('-bet_id')
    team1_bal=0
    team2_bal=0
    for b in bet:
        profit=int(b.win_amount)-int(b.bet_amount)
        if b.bet_team == "Team1":
            team1_bal=team1_bal+profit
            team2_bal=team2_bal-int(b.bet_amount)
        elif b.bet_team == "Team2":
            team2_bal=team2_bal+profit
            team1_bal=team1_bal-int(b.bet_amount)
    live_score = get_live_score(match.url,match.Team1,match.Team2)
    return render(request, "accounts/match.html", {"match": match, "live_score": live_score,"bets": bet,"team1_bal":team1_bal,"team2_bal":team2_bal})

def live_score_api(request, id):
    match = get_object_or_404(Matchess, match_id=id)
    live_score = get_live_score(match.url)
    return JsonResponse(live_score)

def activeBets(request):
    return render(request, 'accounts/activeBets.html')

def settledBets(request):
    return render(request, 'accounts/settledBets.html')