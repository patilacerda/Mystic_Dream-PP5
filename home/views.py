from django.shortcuts import render

# Create your views here.


def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')


def contact_page(request):
    ''' Renders contact page  '''

    return render(request, 'home/contactus.html')


def faq_page(request):
    ''' Renders FAQ page  '''

    return render(request, 'home/faq.html')


def privacy_page(request):
    ''' Renders privacy page  '''

    return render(request, 'home/privacy.html')
