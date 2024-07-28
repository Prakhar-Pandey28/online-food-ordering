from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Pizza, Burger, Order, Item
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import NewUserForm
from django.contrib import messages
from django.conf import settings
import random
import json
import stripe

# Set your Stripe secret key
stripe.api_key = settings.STRIPE_SECRET_KEY

def randomOrderNumber(length):
    sample = 'ABCDEFGHJKLMNPQRSTUVWXYZ123456789'
    return ''.join(random.choice(sample) for _ in range(length))

def get_total_count():
    pizzas_count = Pizza.objects.count()
    burgers_count = Burger.objects.count()
    return pizzas_count + burgers_count

def index(request):
    request.session.set_expiry(0)
    total_count = get_total_count()
    ctx = {'active_link': 'index', 'total_count': total_count}
    return render(request, 'food/index.html', ctx)

def pizza_view(request):
    request.session.set_expiry(0)
    pizzas = Pizza.objects.all()
    total_count = get_total_count()
    ctx = {
        'pizzas': pizzas,
        'active_link': 'pizza',
        'total_count': total_count
    }
    return render(request, 'food/pizza.html', ctx)

def burger_view(request):
    request.session.set_expiry(0)
    burgers = Burger.objects.all()
    total_count = get_total_count()
    ctx = {
        'burgers': burgers,
        'active_link': 'burger',
        'total_count': total_count
    }
    return render(request, 'food/burgers.html', ctx)

@csrf_exempt
def order_view(request):
    if request.method == 'POST' and request.is_ajax():
        data = json.loads(request.body)
        note = data.get('note')
        orders = data.get('orders')
        bill = data.get('bill')

        request.session['note'] = note
        request.session['order'] = orders
        request.session['bill'] = bill

        randomNum = randomOrderNumber(6)
        while Order.objects.filter(number=randomNum).exists():
            randomNum = randomOrderNumber(6)

        order = Order(
            customer=request.user if request.user.is_authenticated else None,
            number=randomNum,
            bill=float(bill),
            note=note
        )
        order.save()
        request.session['orderNum'] = order.number

        for article in orders:
            item = Item(
                order=order,
                name=article[0],
                price=float(article[2]),
                size=article[1],
            )
            item.save()

        return JsonResponse({'status': 'success', 'orderNum': order.number})
    else:
        total_count = get_total_count()
        ctx = {'active_link': 'order', 'total_count': total_count}
        return render(request, 'food/order.html', ctx)


@csrf_exempt
def create_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            note = data.get('note')
            orders = data.get('orders')
            bill = data.get('bill')

            print(f"Received payment request with note: {note}, orders: {orders}, bill: {bill}")

            payment_intent = stripe.PaymentIntent.create(
                amount=int(bill * 100),  # Amount in cents
                currency='usd',
                payment_method_types=['card'],
                metadata={'note': note, 'orders': json.dumps(orders)}  # Convert orders to JSON string
            )
            print(f"Payment intent created successfully: {payment_intent}")

            return JsonResponse({
                'status': 'success',
                'payment_url': payment_intent.client_secret
            })
        except stripe.error.StripeError as e:
            print(f"Stripe error: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)})
        except Exception as e:
            print(f"General error: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def payment_callback(request, client_secret):
    # Handle payment success or failure here
    orderNum = request.session.get('orderNum', '')
    if orderNum:
        # Verify the payment intent status using client_secret
        try:
            payment_intent = stripe.PaymentIntent.retrieve(client_secret)
            if payment_intent.status == 'succeeded':
                # Finalize the order
                # Save the order status or send confirmation email
                return redirect('food:success')
            else:
                return redirect('food:order')
        except stripe.error.StripeError as e:
            print(f"Stripe error: {e}")
            return redirect('food:order')

    return redirect('food:index')

def success(request):
    orderNum = request.session.get('orderNum', '')
    bill = request.session.get('bill', '')
    items = Item.objects.filter(order__number=orderNum) if orderNum else []

    ctx = {'orderNum': orderNum, 'bill': bill, 'items': items}
    return render(request, 'food/success.html', ctx)

def signup(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('food:login')
        else:
            return render(request, 'food/signup.html', {'form': form})
    else:
        form = NewUserForm()
        return render(request, 'food/signup.html', {'form': form})

def logIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('food:index')
        else:
            messages.error(request, 'Username and/or password are incorrect')

    total_count = get_total_count()
    return render(request, 'food/login.html', {'active_link': 'login', 'total_count': total_count})

def logOut(request):
    auth_logout(request)
    return redirect('food:index')
