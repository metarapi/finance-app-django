from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.core import serializers
from django.template.context_processors import csrf
from django.template.loader import render_to_string
from .models import Portfolio, Stock, HistoricalData, CalculatedData
from .forms import PortfolioForm
import yfinance as yf
#from .models import TestModel

auth_url_discord = "https://discord.com/oauth2/authorize?client_id=1220444859987398879&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Faccounts%2Fdiscord%2Flogin%2Fcallback%2F&scope=identify"

def get_updated_portfolio_data():
    # Fetch the updated portfolio data from the database
    portfolios = Portfolio.objects.all()  # replace with your actual query

    # Serialize the data to JSON
    data = serializers.serialize('json', portfolios)

    return data


# Create your views here.
'''
@login_required
@require_GET
def autocomplete(request):
    query = request.GET.get('q', '')
    stocks = Stock.objects.filter(name__icontains=query)[:5]  # Limit to 5 results
    if not stocks and len(query) > 2:  # Fallback to yfinance if no results
        try:
            stock = yf.Ticker(query)
            new_stock = Stock.objects.create(
                name=stock.info['shortName'],
                symbol=query,
                # Add any other fields you need
            )
            stocks = [new_stock]
        except Exception as e:
            print(f"Failed to get data for {query}: {e}")
    results = [{'id': stock.id, 'name': stock.name} for stock in stocks]
    return JsonResponse(results, safe=False)
'''
    
@login_required
def redirect_to_home(request):
    return redirect('home')

@login_required
def home(request):
    portfolios = Portfolio.objects.filter(user=request.user)
    return render(request, 'home.html', {'portfolios': portfolios})

@login_required
def create_portfolio(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST)
        if form.is_valid():
            portfolio = form.save()
            portfolios = Portfolio.objects.filter(user=request.user)
            context = {'portfolios': portfolios, 'form': PortfolioForm(), 'user': request.user}
            data = render_to_string('portfolio_list.html', context, request=request) # The request argument is required for CSRF
            return HttpResponse(data)
        else:
            print(form.errors)
            return HttpResponseBadRequest('Invalid form')

@login_required
def delete_portfolio(request, portfolio_id):
    if request.method == 'POST':
        portfolio = get_object_or_404(Portfolio, id=portfolio_id, user=request.user)
        portfolio.delete()
        # Return the updated list of portfolios as HTML
        portfolios = Portfolio.objects.filter(user=request.user)
        context = {'portfolios': portfolios, 'form': PortfolioForm(), 'user': request.user}
        data = render_to_string('portfolio_list.html', context, request=request) # The request argument is required for CSRF
        return HttpResponse(data)
    else:
        return HttpResponseBadRequest('Invalid method')

@login_required
def portfolio_detail(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    context = {'portfolio': portfolio}
    return render(request, 'portfolio_detail.html', context)

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('/')

# def test_database(request):
#     # Create a new TestModel object and save it to the database
#     new_object = TestModel(name="Test Object")
#     new_object.save()

#     # Retrieve all TestModel objects from the database
#     all_objects = TestModel.objects.all()

#     # Return the objects in the context
#     return render(request, 'test_database.html', {'objects': all_objects})