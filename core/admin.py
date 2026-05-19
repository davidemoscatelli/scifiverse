from django.contrib import admin
from .models import Category, Article, AudioChapter, StoryPart

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

# Creiamo le interfacce "Inline"
class AudioChapterInline(admin.StackedInline):
    model = AudioChapter
    extra = 0 # Quanti campi vuoti mostrare di default

class StoryPartInline(admin.StackedInline):
    model = StoryPart
    extra = 0

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'is_featured', 'created_at')
    list_filter = ('media_type', 'is_featured', 'categories')
    search_fields = ('title', 'content')
    filter_horizontal = ('categories',)
    
    # Aggiungiamo le sezioni inline alla pagina di inserimento
    inlines = [AudioChapterInline, StoryPartInline]