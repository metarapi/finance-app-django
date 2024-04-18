from django.contrib.auth.models import User
from django.db import models

class Portfolio(models.Model):
    # Each user can have multiple portfolios.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Stock(models.Model):
    # Each portfolio can have multiple stocks, represented as a PortfolioStock.
    # Each stock has only one CalculatedStockData but can have multiple HistoricalData records.
    ticker = models.CharField(max_length=10, unique=True)
    short_name = models.CharField(max_length=100)
    long_name = models.CharField(max_length=200)
    sector = models.CharField(max_length=50)
    industry = models.CharField(max_length=50)
    exchange = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    dataRetrieved = models.BooleanField(default=False) # True if historical data has been retrieved

class PortfolioStock(models.Model):
    # Represents a stock in a portfolio.
    # Junction table between Portfolio and Stock.
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

class HistoricalData(models.Model):
    # Each stock can have multiple historical data records.
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    open = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.IntegerField()
    dividends = models.DecimalField(max_digits=10, decimal_places=2)

class CalculatedStockData(models.Model):
    # Each stock can have multiple calculated data records for different future dates.
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField() # Future dates
    price = models.DecimalField(max_digits=10, decimal_places=2) # Predicted prices at future dates
    deviation = models.DecimalField(max_digits=10, decimal_places=2) # Predicted price spread
    dividends = models.DecimalField(max_digits=10, decimal_places=2) # Predicted dividends at future dates

class CalculatedPortfolioData(models.Model):
    # Each portfolio can have multiple calculated data records for different future dates.
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    date = models.DateField() # Future dates
    total_value = models.DecimalField(max_digits=10, decimal_places=2) # Sum of predicted prices of all stocks in the portfolio
    total_deviation = models.DecimalField(max_digits=10, decimal_places=2) # Sum of predicted price spreads of all stocks in the portfolio
    total_dividends = models.DecimalField(max_digits=10, decimal_places=2) # Sum of predicted dividends of all stocks in the portfolio



'''
Old models

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Stock(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.PROTECT)
    ticker = models.CharField(max_length=10)
    short_name = models.CharField(max_length=100)
    long_name = models.CharField(max_length=200)
    sector = models.CharField(max_length=50)
    industry = models.CharField(max_length=50)
    exchange = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    dataRetrieved = models.BooleanField(default=False)

class HistoricalData(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    open = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.IntegerField()
    dividends = models.DecimalField(max_digits=10, decimal_places=2)

class CalculatedData(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField() # Future dates
    price = models.DecimalField(max_digits=10, decimal_places=2) # Predicted prices at future dates
    deviation = models.DecimalField(max_digits=10, decimal_places=2) # Predicted price spread
    dividends = models.DecimalField(max_digits=10, decimal_places=2) # Predicted dividends at future dates

'''
# Create your models here.

