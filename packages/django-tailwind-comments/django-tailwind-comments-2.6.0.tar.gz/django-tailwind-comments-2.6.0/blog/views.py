from django.shortcuts import render, get_object_or_404
from blog.models import Article


def home(request):
    articles = Article.objects.all()
    return render(request, 'home.html', {'articles': articles})


def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'detail.html', {'article': article})
