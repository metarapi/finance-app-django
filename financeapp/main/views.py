from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.core import serializers
from django.template.context_processors import csrf
from django.template.loader import render_to_string
from .models import Portfolio, Stock, PortfolioStock, HistoricalData, CalculatedStockData, CalculatedPortfolioData
from .forms import PortfolioForm
import yfinance as yf
import pandas as pd
from django.db import IntegrityError

# Create your views here.

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
    portfolio_stocks = PortfolioStock.objects.filter(portfolio=portfolio)
    #print(portfolio_stocks.query)
    stocks = [ps.stock for ps in portfolio_stocks]
    context = {'portfolio': portfolio, 'stocks': stocks}
    return render(request, 'portfolio_detail.html', context)

@login_required
def search_stock(request):
    search_text = request.POST.get('search')
    portfolio_id = request.POST.get('portfolio_id')
        
    if not search_text:
        return HttpResponse('')  # Return early if search text is empty

    results = Stock.objects.filter(ticker__icontains=search_text)
    # Get the portfolio
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)

    # Select only the first five results
    results = results[:5]

    # Pass on the results and the portfolio ID to the template
    context = {
        'results': results,
        'portfolio': portfolio,
    }
    
    return render(request, 'search_results.html', context)

@login_required
def add_to_portfolio(request):
    # Get the portfolio ID and stock ID from the request
    stock_id = request.POST.get('stock_id')
    portfolio_id = request.POST.get('portfolio_id')

    # Find the corresponding portfolio and stock
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    stock = get_object_or_404(Stock, id=stock_id)

    # Create a new PortfolioStock object instance (junction table entry)
    #portfolio_stock = PortfolioStock(portfolio=portfolio, stock=stock)
    #portfolio_stock.save()

    # Get or create a new PortfolioStock object instance (junction table entry)
    portfolio_stock, created = PortfolioStock.objects.get_or_create(portfolio=portfolio, stock=stock)

    # Retrieve the stocks in the portfolio
    portfolio_stocks = PortfolioStock.objects.filter(portfolio=portfolio)
    stocks = [ps.stock for ps in portfolio_stocks]

    context = {
        'stocks': stocks,
        'portfolio': portfolio,
    }

    return render(request, 'portfolio.html', context)

@login_required
def remove_from_portfolio(request):

    # Get the portfolio ID and stock ID from the request
    stock_id = request.POST.get('stock_id')
    portfolio_id = request.POST.get('portfolio_id')

    print(f'Stock ID: {stock_id}')
    print(f'Portfolio ID: {portfolio_id}')

    if not stock_id or not portfolio_id:
        return HttpResponseBadRequest('Stock ID and Portfolio ID are required')
    
    # Find the corresponding portfolio and stock
    portfolio_stock = get_object_or_404(PortfolioStock, portfolio=portfolio_id, stock=stock_id)

    # Delete the stock from the portfolio
    portfolio_stock.delete()

    # Retrieve the portfolio to pass on to the template
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)

    # Retrieve the stocks in the portfolio
    portfolio_stocks = PortfolioStock.objects.filter(portfolio=portfolio)
    stocks = [ps.stock for ps in portfolio_stocks]

    context = {
        'stocks': stocks,
        'portfolio': portfolio,      
    }

    return render(request, 'portfolio.html', context)



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



'''
# These functions are used to add stocks to the database and remove incomplete stocks
# They are not used in the application itself
# This is for testing purposes only

stockDB = pd.read_csv('D:/Coding/financeApp/financeapp/static/stocks.csv')

def add_stocks():
    
    for ticker in stockDB['ticker']:
        # Retrieve the stock data
        stock_info = yf.Ticker(ticker)

        if stock_info.info.get('shortName', '') == '':
            continue

        # Check if all required data is available
        if not all([
            stock_info.info.get('shortName'),
            stock_info.info.get('longName'),
            stock_info.info.get('sector'),
            stock_info.info.get('industry'),
            stock_info.info.get('exchange'),
            stock_info.info.get('country'),
        ]):
            print(f"Skipping {ticker} due to missing data")
            continue

        print(ticker,
            stock_info.info.get('shortName', ''),
            stock_info.info.get('longName', ''),
            stock_info.info.get('sector', ''),
            stock_info.info.get('industry', ''),
            stock_info.info.get('exchange', ''),
            stock_info.info.get('country', '')        
        )

        # Update or create a new Stock object
        Stock.objects.update_or_create(
            ticker=ticker,
            defaults={
                'short_name': stock_info.info.get('shortName', ''),
                'long_name': stock_info.info.get('longName', ''),
                'sector': stock_info.info.get('sector', ''),
                'industry': stock_info.info.get('industry', ''),
                'exchange': stock_info.info.get('exchange', ''),
                'country': stock_info.info.get('country', ''),
                'dataRetrieved': False,
            }
        )
    return print('Stocks added to database')


def remove_incomplete_stocks():
    # Iterate over all Stock objects
    for stock in Stock.objects.all():
        # Check if any required field is missing
        if not all([
            stock.short_name,
            stock.long_name,
            stock.sector,
            stock.industry,
            stock.exchange,
            stock.country,
        ]):
            print(f"Deleting {stock.ticker} due to missing data")
            stock.delete()

    return print('Incomplete stocks removed from database')

remove_incomplete_stocks()
add_stocks()

'''