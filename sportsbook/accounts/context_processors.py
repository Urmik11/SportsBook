from .models import Account,Deposite,Withdraw,Matchess,WebsiteUser
from .models import bets as Bet

def get_logged_in_user(request):
    user_id = request.session.get('website_user_id')
    if user_id:
        try:
            return WebsiteUser.objects.get(id=user_id)
        except WebsiteUser.DoesNotExist:
            return None
    return None

def Accounts(request):
    user = get_logged_in_user(request)
    if not user:
        return {"account": 0,"my_user": None}
    try:
        account = Account.objects.get(user=user)
        return {"account": account,"my_user": user}
    except Account.DoesNotExist:
        return {"account": 0,"my_user": user}

def Deposits(request):
    user = get_logged_in_user(request)
    if not user:
        return {"deposit": 0}

    deposits = Deposite.objects.filter(username=user.username).order_by('-created_at')
    return {"deposit": deposits}

def Withdraws(request):
    user = get_logged_in_user(request)
    if not user:
        return {"withdraw": 0}

    withdraws = Withdraw.objects.filter(username=user.username).order_by('-created_at')
    return {"withdraw": withdraws}

def Bets(request):
    user = get_logged_in_user(request)
    if not user:
        return {"bet": 0}

    all_bets = Bet.objects.filter(username=user.username).order_by('-bet_time')
    active_bets = Bet.objects.filter(username=user.username, bet_status="Active").order_by('-bet_time')
    settled_bets = Bet.objects.filter(username=user.username, bet_status="Settled").order_by('-bet_time')

    match_map = {m.match_id: m.match_name for m in Matchess.objects.all()}
    match_map1 = {m.match_id: m.Team1 for m in Matchess.objects.all()}
    match_map2 = {m.match_id: m.Team2 for m in Matchess.objects.all()}

    exp = sum(int(b.bet_amount) for b in active_bets)

    for bet in active_bets:
        bet.match_name = match_map.get(bet.match_id, "Unknown")
        bet.match_team1 = match_map1.get(bet.match_id, "Unknown")
        bet.match_team2 = match_map2.get(bet.match_id, "Unknown")

    for bet in settled_bets:
        bet.match_name = match_map.get(bet.match_id, "Unknown")
        bet.match_team1 = match_map1.get(bet.match_id, "Unknown")
        bet.match_team2 = match_map2.get(bet.match_id, "Unknown")

    return {"bet": all_bets, "exp": exp, "activeBets": active_bets, "settledBets": settled_bets}