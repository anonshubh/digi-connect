from django.shortcuts import render
from django.views.generic import View


# Index Page Of Entire Application
def index_view(request):
    return render(request,'connect/index.html')

# About Page Of Application
def about_view(request):
    return render(request,'about.html')

