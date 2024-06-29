from django.shortcuts import render, redirect
from products.models import Product
from django.contrib import messages
from .forms import ContactForm

# Create your views here.


def index(request):
    """ A view to return the index page """

    # Fetch top-rated products
    top_rated_products = Product.objects.filter(rating__isnull=False).order_by(
        '-rating')[:12]
    product_chunks = [top_rated_products[i:i + 4] for i in range(
        0, len(top_rated_products), 4)]

    context = {
        'product_chunks': product_chunks,
    }

    return render(request, 'home/index.html', context)


def contact_page(request):
    ''' Renders contact page and handles contact form submissions '''

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact') 
    else:
        form = ContactForm()

    context = {
        'form': form,
    }

    return render(request, 'home/contactus.html', context)


def faq_page(request):
    ''' Renders FAQ page  '''

    return render(request, 'home/faq.html')


def privacy_page(request):
    ''' Renders privacy page  '''

    return render(request, 'home/privacy.html')
