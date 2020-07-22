from django.shortcuts import render,get_object_or_404
from store.models import Category,Product,Cart,CartItem
# Create your views here.
def index(request,category_slug=None):
    products = None 
    category_page = None 

    if category_slug != None :
        category_page = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.all().filter(category=category_page,available=True)
    else :
        products = Product.objects.all().filter(available=True)

    return render(request,'index.html',{'products':products,'category':category_page})

def productPage(request,category_slug,product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug,slug=product_slug)
    except Exception as e:
        raise e
    return render(request,'product.html',{'product':product})

def _cart_id(request):
    cart = request.session.session_key
    if not cart :
        cart = request.session.create()
    return cart

def addCart(request,product_id):
    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist:
        Cart.objects.create(cart_id = _cart_id)
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product,cart=cart)
        if cart_item.quantity < cart_item.product.stock : 
            cart_item.quantity += 1
            cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.create(
            product=product,
            cart=cart,
            quantity=1
        )
        cart_item.save()