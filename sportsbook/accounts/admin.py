from django.contrib import admin,messages
from .models import Account
from .models import Matchess
from .models import bets as Bet
from .models import Deposite
from .models import Withdraw,WebsiteUser
from django.utils import timezone
from django.contrib.auth import get_user_model
User=get_user_model()

@admin.register(WebsiteUser)
class WebsiteUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'username', 'balance', 'exp')
    search_fields = ('username',)

@admin.register(Matchess)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('match_id', 'match_name', 'Team1', 'Team2', 'date', 'time')
    search_fields = ('match_name', 'Team1', 'Team2')
    list_filter = ('match_status', 'date')
    ordering = ('-date',)
    actions = ['settle_selected_matches']

@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    list_display = ('bet_id', 'username', 'match_id', 'bet_amount', 'win_amount', 'bet_status')
    search_fields = ('username',)
    list_filter = ('bet_status', 'bet_time')

@admin.register(Deposite)
class DepositeAdmin(admin.ModelAdmin):
    list_display = ('deposite_id', 'username', 'amount', 'UTR', 'created_at', 'status')
    search_fields = ('username', 'UTR')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)
    actions = ['approve_deposits', 'reject_deposits']

    def approve_deposits(self, request, queryset):
        count = 0
        for deposit in queryset.filter(status='pending'):
            deposit.status = 'approved'
            deposit.approved_at = timezone.now()
            deposit.save()

            try:
                user = WebsiteUser.objects.get(username=deposit.username)
            except WebsiteUser.DoesNotExist:
                self.message_user(request, f"User '{deposit.username}' not found.", level=messages.ERROR)
                continue

            account, _ = Account.objects.get_or_create(user=user, defaults={'username': user.username, 'balance': 0, 'exp': 0})
            account.balance += deposit.amount
            account.save()
            count += 1

        self.message_user(request, f"{count} deposits approved and balance updated.")
    approve_deposits.short_description = "Approve selected deposits"

    def reject_deposits(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, f"{updated} deposits rejected.")
    reject_deposits.short_description = "Reject selected deposits"

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status in ['approved', 'rejected']:
            return [f.name for f in self.model._meta.fields]
        return super().get_readonly_fields(request, obj)

@admin.register(Withdraw)
class WithdrawAdmin(admin.ModelAdmin):
    list_display = ('withdraw_id', 'username', 'amount', 'created_at', 'status')
    search_fields = ('username',)
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)
    actions = ['approve_withdrawals', 'reject_withdrawals']

    def approve_withdrawals(self, request, queryset):
        approved_count = queryset.filter(status='pending').update(status='approved')
        self.message_user(request, f"{approved_count} withdrawals approved.")
    approve_withdrawals.short_description = "Approve selected withdrawals"

    def reject_withdrawals(self, request, queryset):
        rejected_count = 0
        for withdraw in queryset.filter(status='pending'):
            try:
                account = Account.objects.get(username=withdraw.username)
                account.balance += withdraw.amount  # refund
                account.save()
                withdraw.status = 'rejected'
                withdraw.save()
                rejected_count += 1
            except Account.DoesNotExist:
                self.message_user(
                    request,
                    f"Account for {withdraw.username} not found.",
                    level=messages.ERROR
                )
        self.message_user(request, f"{rejected_count} withdrawals rejected and refunded.")
    reject_withdrawals.short_description = "Reject selected withdrawals"

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status in ['approved', 'rejected']:
            return [f.name for f in self.model._meta.fields]
        return super().get_readonly_fields(request, obj)