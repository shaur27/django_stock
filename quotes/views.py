from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages
# Create your views here.
def home(request):
    import requests
    import json

    if request.method=='POST':
        ticker=request.POST['ticker']

        api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ ticker +"/quote?token=pk_7fdecfad74654dcc97b287d24edbf068")

        try:
            api= json.loads(api_request.content)
        except Exception as e:
            api="Error!"
        return render(request, 'home.html', {'api': api})

    else:
        return render(request, 'home.html')
    #pk_7fdecfad74654dcc97b287d24edbf068

#news api 5ace4197601b4040a907e288f079f9d2

from django.shortcuts import render 
from newsapi.newsapi_client import NewsApiClient
  
# Create your views here.  
def news(request): 
      
    newsapi = NewsApiClient(api_key ='5ace4197601b4040a907e288f079f9d2') 
    #top = newsapi.get_top_headlines(sources ='techcrunch') 
    top = newsapi.get_top_headlines(sources='business-insider')
    l = top['articles'] 
    desc =[] 
    news =[] 
    img =[] 
  
    for i in range(len(l)): 
        f = l[i] 
        news.append(f['title']) 
        desc.append(f['description']) 
        img.append(f['urlToImage']) 
    mylist = zip(news, desc, img) 
  
    return render(request, 'news.html', context ={"mylist":mylist})    

def about(request):
    return render(request, 'about.html', {})

def add_stock(request):

    import requests
    import json

    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock Added"))
            return redirect('add_stock')

    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ str(ticker_item) +"/quote?token=pk_7fdecfad74654dcc97b287d24edbf068")
            try:
                api= json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api="Error!"

        return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})

def delete(request, stock_id):
    item=Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock Deleted"))
    return redirect(delete_stock)

def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker':ticker})