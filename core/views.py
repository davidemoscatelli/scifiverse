from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Article, Category

def home(request):
    # Raccogliamo i parametri dall'URL
    category_slug = request.GET.get('category')
    media_type = request.GET.get('media_type')
    search_query = request.GET.get('q')
    
    # Partiamo da tutti gli articoli
    articles = Article.objects.all()
    featured_article = None
    
    # L'articolo "In Primo Piano" si mostra SOLO se non stiamo filtrando o cercando
    if not category_slug and not media_type and not search_query:
        featured_article = articles.filter(is_featured=True).first()
        if featured_article:
            articles = articles.exclude(id=featured_article.id)
    
    # Applichiamo i filtri se presenti
    if category_slug:
        articles = articles.filter(categories__slug=category_slug)
        
    if media_type:
        articles = articles.filter(media_type=media_type)
        
    if search_query:
        # Cerca nel titolo, nella sinossi O nel contenuto
        articles = articles.filter(
            Q(title__icontains=search_query) | 
            Q(short_description__icontains=search_query) |
            Q(content__icontains=search_query)
        ).distinct()
    
    categories = Category.objects.all()
    
    context = {
        'featured_article': featured_article,
        'recent_articles': articles[:15], # Limitiamo a 15 risultati per ora
        'categories': categories,
        'active_category': category_slug,
        'active_media_type': media_type,
        'search_query': search_query,
    }
    return render(request, 'core/home.html', context)

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'core/article_detail.html', {'article': article})