from .models import Balance

def user_balance(request):
    if request.user.is_authenticated:
        try:
            balance = Balance.objects.get(user=request.user)
            return {'user_balance': balance.amount}
        except Balance.DoesNotExist:
            balance = Balance.objects.create(user=request.user)
            return {'user_balance': balance.amount}
    return {'user_balance': 0.00}