from django.shortcuts import render
from products.models import Product

# Create your views here.


def index(request):
    """ A view to return the index page """

    # Fetch top-rated products
    top_rated_products = Product.objects.filter(rating__isnull=False).order_by('-rating')[:12]
    product_chunks = [top_rated_products[i:i + 4] for i in range(0, len(top_rated_products), 4)]
    
    context = {
        'product_chunks': product_chunks,
    }

    return render(request, 'home/index.html', context)


def contact_page(request):
    ''' Renders contact page  '''

    return render(request, 'home/contactus.html')


def faq_page(request):
    ''' Renders FAQ page  '''

    return render(request, 'home/faq.html')


def privacy_page(request):
    ''' Renders privacy page  '''

    return render(request, 'home/privacy.html')
