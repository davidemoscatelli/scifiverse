from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Article, Category

def home(request):
    category_slug = request.GET.get('category')
    media_type = request.GET.get('media_type')
    search_query = request.GET.get('q')
    
    articles = Article.objects.all()
    featured_article = None
    
    # 1. Ricerca testuale: NIENTE primo piano, mostriamo solo i risultati
    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query) | 
            Q(short_description__icontains=search_query) |
            Q(content__icontains=search_query)
        ).distinct()
    
    # 2. Navigazione normale o per sezioni: CERCHIAMO il primo piano
    else:
        # Partiamo da tutti gli articoli che hanno la spunta "In Primo Piano"
        featured_qs = Article.objects.filter(is_featured=True)
        
        # Se l'utente clicca su "Racconti", peschiamo il primo piano tra i racconti
        if media_type:
            featured_qs = featured_qs.filter(media_type=media_type)
        if category_slug:
            featured_qs = featured_qs.filter(categories__slug=category_slug)
            
        # Prendiamo il primo che troviamo con questi filtri
        featured_article = featured_qs.first()
        
        # Escludiamo l'articolo in primo piano dalla lista normale sottostante
        if featured_article:
            articles = articles.exclude(id=featured_article.id)
            
        # Infine, filtriamo anche il resto della lista articoli in base al menu scelto
        if media_type:
            articles = articles.filter(media_type=media_type)
        if category_slug:
            articles = articles.filter(categories__slug=category_slug)
    
    categories = Category.objects.all()
    
    context = {
        'featured_article': featured_article,
        'recent_articles': articles[:15],
        'categories': categories,
        'active_category': category_slug,
        'active_media_type': media_type,
        'search_query': search_query,
    }
    return render(request, 'core/home.html', context)

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'core/article_detail.html', {'article': article})