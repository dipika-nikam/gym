from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from . models import Profile, Product, Order, OrderItem, ClassSchedule, AddUsers, StaffMember, Lead
from django.contrib.auth.models import User
from core.forms import ContactForm, ProfileForm, CustomUserForm, UserUpdateForm, LeadForm, StaffMemberForm, UpdateLeadForm
from django.contrib import messages
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from .forms import ProductForm, StaffMemberForm, StaffUpdateForm


def index(request):
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, ordered=False)
        if order:
            total = len(order[0].items.all())
            return render(request, "index.html", {"cart":total})

    return render(request, "index.html")

# def classes(request):
#     return render(request, "class.html")

def classes(request):
    class_schedules = ClassSchedule.objects.all()
    return render(request, 'class.html', {'class_schedules': class_schedules})

def contact(request):
    if request.method =="POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Thanks for your message.")
    return render(request, "contact.html")

def profile(request):
    user = get_object_or_404(Profile, user=request.user)
    return render(request, "profile.html", {"profile":user})

def editprofile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile')
        else:
            print(form.errors)
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form,
    }
    return render(request, 'editprofile.html', context)


def subscribe(request):
    return render(request, "subscribe.html")

@login_required(login_url='/authentication/login/')
def payment(request, choice):
    if choice == "all":
        name = "All round fitness"
        price = 30
    elif choice == "body_building":
        name = "Body Building"
        price = 25
    elif choice == "muscle_building":
        name = "Muscle Building"
        price = 20

    data = {
        "name":name,
        "price":price,
        "choice":choice
        }
    return render(request, "payment.html", {"data":data})


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request, choice):
    user = get_object_or_404(Profile, user=request.user)
    user.subscribed_type = choice
    user.save()
    if choice == "all":
        price = 3000
    elif choice == "body_building":
        price = 2500
    elif choice == "muscle_building":
        price = 2000
    if request.method == 'GET':
        domain_url = settings.DOMAIN_URL
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success/{CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        "quantity":1,
                        "price_data":{
                            "unit_amount":price,
                            "product_data":{
                                "name":"muscle"
                            },
                            "currency":"usd"
                        }
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

def success(request, session_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id)
    if session.payment_status == "paid":
        user = get_object_or_404(Profile, user=request.user)
        user.is_subscribed = True
        user.subscribed_type
        user.checkout_session = session_id
        user.payment_id = session.payment_intent
        user.save()
    messages.success(
                request, "Thanks for your payment.")
    return redirect("subscribe")

def ordersuccess(request, id, session_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id)
    if session.payment_status == "paid":
        order = get_object_or_404(Order, pk=id)
        order.ordered = True
        order.order_status = "ACCEPTED"
        order.checkout_session = session_id
        order.payment_id = session.payment_intent
        order.save()

    messages.success(
                request, "Thanks for your payment. Order placed successfully.")
    return redirect("products")

def canceled(request):
    return HttpResponse("sorry something went wrong")


def products(request):
    items = Product.objects.all()
    return render(request, "products.html", {"items":items})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm()

    context = {
        'form': form,
    }
    return render(request, 'add_product.html', context)


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('products')

def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
    }
    return render(request, 'update_product.html', context)

@login_required(login_url='/authentication/login/')
def cart(request):
    order = Order.objects.filter(user=request.user, ordered= False)

    if order:
        return render(request, "cart.html", {"order":order[0]})
    else:
        return render(request, "cart.html")

@login_required(login_url='/authentication/login/')
def add_to_cart(request, choice):
    item = get_object_or_404(Product, pk=choice)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user = request.user,
        ordered = False
    )

    order_qs = Order.objects.filter(user=request.user, ordered= False)
    if order_qs.exists() :
        order = order_qs[0]

        if order.items.filter(item__pk = item.pk).exists() :
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Added quantity Item")
            return redirect("cart")
        else:
            order.items.add(order_item)
            messages.info(request, "Item added to your cart")
            return redirect("cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date = ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added to your cart")
        return redirect("cart")

@csrf_exempt
def order_checkout(request, id):
    order = get_object_or_404(Order, pk=id)

    if request.method == 'GET':
        domain_url = settings.DOMAIN_URL
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'ordersuccess/'+str(order.id)+'/{CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        "quantity":1,
                        "price_data":{
                            "unit_amount":int(order.get_total_price())*100,
                            "product_data":{
                                "name":"muscle"
                            },
                            "currency":"usd"
                        }
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

@login_required(login_url='/authentication/login/')
def users(request):
    items = AddUsers.objects.all()
    return render(request, "allusers.html", {"items":items})

@login_required(login_url='/authentication/login/')
def add_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'User has been added successfully.')
            return redirect('all-users')
    else:
        form = CustomUserForm()

    context = {'form': form}
    return render(request, 'add_user.html', context)

def delete_user(request, user_id):
    user = get_object_or_404(AddUsers, id=user_id)
    user.delete()
    return redirect('all-users')

def update_user(request, user_id):
    user = get_object_or_404(AddUsers, id = user_id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
            return redirect('all-users')
    else:
        form = UserUpdateForm(instance = user)

    context = {
        'form' : form,
    }
    return render(request, 'update_user.html', context)

def update_quantity(request, item_id, new_quantity):
    item = get_object_or_404(OrderItem, id=item_id)
    item.quantity = new_quantity
    item.save()
    return JsonResponse({'message': 'Quantity updated successfully'})

def remove_product(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)
    item.delete()
    return JsonResponse({'message': 'Product removed from cart'})

def all_leads(request):
    items = Lead.objects.all()
    return render(request, "all_leads.html", {"items":items})

def add_lead(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lead has been added successfully.')
            return redirect('all_leads')
    else:
        form = LeadForm()

    context = {'form': form}
    return render(request, 'add_lead.html', context)

def update_lead(request, lead_id):
    user = get_object_or_404(Lead, id = lead_id)
    if request.method == 'POST':
        form = UpdateLeadForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
            return redirect('all_leads')
    else:
        form = UpdateLeadForm(instance = user)

    context = {
        'form' : form,
    }
    return render(request, 'update_lead.html', context)

def delete_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    lead.delete()
    return redirect('all_leads')

@login_required(login_url='/authentication/login/')
def staff_member(request):
    if request.method == 'POST':
        form = StaffMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'User has been added successfully.')
            return redirect('allstaff-member')
    else:
        form = StaffMemberForm()

    context = {'form': form}
    return render(request, 'staff_member.html', context)


def all_staff(request):
    items = StaffMember.objects.all()
    return render(request, "allstaff.html", {"items":items})

def delete_staff(request, user_id):
    user = get_object_or_404(StaffMember, id=user_id)
    user.delete()
    return redirect('allstaff-member')

def update_staff(request, user_id):
    user = get_object_or_404(StaffMember, id = user_id)
    if request.method == 'POST':
        form = StaffUpdateForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
            return redirect('allstaff-member')
    else:
        form = StaffUpdateForm(instance = user)

    context = {
        'form' : form,
    }
    return render(request, 'update_user.html', context)

def migation_assistant(request):
    return render(request, "migration_assistant.html")

def import_members(request):
    return render(request, 'import_members.html')
