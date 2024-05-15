from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages


def register(request):
    # """
    # Handles user registration.

    # Input:
    # - request (HttpRequest): The HTTP request object.

    # Output:
    # - HttpResponse: Renders the registration page or redirects to the login page upon successful registration.
    
    # This function authenticates the user's credentials and logs the user in if the credentials are valid. If the credentials are invalid, it displays an error message.
    # """
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context={'form': form}
    return render(request, 'app/register.html',context)
def loginPage(request):
    # """
    # Handles user login.

    # Input:
    # - request (HttpRequest): The HTTP request object.

    # Output:
    # - HttpResponse: Renders the login page or redirects to the home page upon successful login.
    # """
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'user or password incorrect')
    context={}
    return render(request, 'app/login.html',context)
def logoutPage(request):
    #     Input:
    # - request (HttpRequest): The HTTP request object.

    # Output:
    # - redirect('login'): Redirects the user to the login page after logging out.

    # This function logs the user out and redirects them to the login page.
    # """
    logout(request)
    return redirect('login')
def search(request):
    # Input:
    # - request (HttpRequest): The HTTP request object.

    # Output:
    # - render(request, 'app/search.html', context): Renders the search page with the search results.

    # This function processes the search query, retrieves the matching products, and passes the necessary data to the search page template for rendering.
    # """
    if request.method == 'POST':
        searched = request.POST['searched']
        keys = Product.objects.filter(name__contains=searched)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0,'get_cart_total_items': 0}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    return render(request, 'app/search.html',{'searched':searched,'keys':keys,'products': products,'cartItems': cartItems})
def category(request):
    # """
    # Retrieves the categories and subcategories, and the products for the selected category.

    # Input:
    # - request: The HTTP request object.

    # Output:
    # - A rendered template 'app/category.html' with the following context:
    #     - categories: A queryset of all categories where 'is_sub' is False.
    #     - active_category: The selected category slug from the request.
    #     - products: A queryset of products filtered by the selected category slug.
    #     - seen_values: An empty list.
    #     - subcategories: A queryset of all subcategories.
    # """
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', '')
    
    subcategories = SubCategory.objects.all()
    seen_values = []
    action = request.GET.get('action', '')
    products = Product.objects.filter(category__slug=active_category)
    context = {
        'categories': categories,
        'active_category': active_category,
        'products': products,
        'seen_values': seen_values,
        'subcategories': subcategories
    }
    return render(request, 'app/category.html', context)
def home(request):
    # """
    # Retrieves the products, cart items, and categories, and renders the 'app/home.html' template.

    # Input:
    # - request: The HTTP request object.

    # Output:
    # - A rendered template 'app/home.html' with the following context:
    #     - products: A queryset of all products.
    #     - cartItems: The number of items in the cart.
    #     - user_login: A string indicating whether the user is logged in or not.
    #     - user_not_login: A string indicating whether the user is not logged in or not.
    #     - categories: A queryset of all categories where 'is_sub' is False.
    #     - items: A queryset of all order items for the current user's cart.
    # """
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login="hidden"
        user_login = "show"
    else :
        items = []
        order = {'get_cart_items': 0,'get_cart_total_items': 0}
        cartItems = order['get_cart_items']
        user_not_login="show"
        user_login = "hidden"
    if user_not_login == "show":
        user_login = "hidden"
        
    categories = Category.objects.filter(is_sub=False)
    products = Product.objects.all()
    context={'products': products,'cartItems': cartItems,'user_login': user_login,'user_not_login': user_not_login,'categories': categories,'items':items}
    return render(request,'app/home.html',context)

def cart(request):
    # """
    # Handles the cart functionality for authenticated and non-authenticated users.

    # Input:
    # - request: The HTTP request object.

    # Output:
    # - Renders the 'app/cart.html' template with the following context:
    #     - items: The order items in the cart.
    #     - order: The order object.
    #     - cartItems: The number of items in the cart.
    #     - user_login: A flag indicating whether the user is logged in.
    #     - user_not_login: A flag indicating whether the user is not logged in.
    #     - categories: The categories without sub-categories.
    # """
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items        
        user_not_login="hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0,'get_cart_total_items': 0}
        cartItems = order['get_cart_items']
        user_not_login="show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub=False)
    context={'items':items,'order':order,'cartItems': cartItems,'user_login': user_login,'user_not_login': user_not_login,'categories': categories}
    return render(request,'app/cart.html',context)
def detail(request):
    # """
    # Handles the detail page for a product.

    # Input:
    # - request: The HTTP request object.

    # Output:
    # - Renders the 'app/detail.html' template with the following context:
    #     - categories: The categories without sub-categories.
    #     - products: The product details.
    #     - items: The order items in the cart.
    #     - order: The order object.
    #     - cartItems: The number of items in the cart.
    #     - user_login: A flag indicating whether the user is logged in.
    #     - user_not_login: A flag indicating whether the user is not logged in.
    # """
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items        
        user_not_login="hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0,'get_cart_total_items': 0}
        cartItems = order['get_cart_items']
        user_not_login="show"
        user_login = "hidden"
    id = request.GET.get('id','')    
    
    products = Product.objects.filter(id=id)
    categories = Category.objects.filter(is_sub=False)
    context={'categories':categories,'products':products,'items':items,'order':order,'cartItems': cartItems,'user_login': user_login,'user_not_login': user_not_login,'categories': categories}
    return render(request,'app/detail.html',context)
def checkout(request):
    # """
    # Handles the checkout functionality for authenticated and non-authenticated users.

    # Input:
    # - request: The HTTP request object.

    # Output:
    # - Renders the 'app/checkout.html' template with the following context:
    #     - items: The order items in the cart.
    #     - order: The order object.
    #     - cartItems: The number of items in the cart.
    #     - user_login: A flag indicating whether the user is logged in.
    #     - user_not_login: A flag indicating whether the user is not logged in.
    #     - categories: The categories without sub-categories.
    # """
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login="hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0,'get_cart_total_items': 0}
        cartItems = order['get_cart_items']
        user_not_login="show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub=False)
    context={'items':items,'order':order,'cartItems': cartItems,'user_login': user_login,'user_not_login': user_not_login,'categories': categories}
    return render(request,'app/checkout.html',context)
def updateItem(request):
    # """
    # Updates the quantity of an item in the cart.

    # Input:
    # - request: The HTTP request object, containing the product ID and the action (add or remove).

    # Output:
    # - A JSON response indicating that the item was added.
    # """
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete = False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product = product)
    if action == 'add':
        orderItem.quantity +=1
    elif action == 'remove':
        orderItem.quantity -=1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('added',safe=False)