from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nome Categoria")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorie"

    def __str__(self):
        return self.name

class Article(models.Model):
    MEDIA_CHOICES = [
        ('film', 'Film'),
        ('serie', 'Serie TV'),
        ('storie', 'Storie'),
        ('racconti', 'Racconti'),
        ('audiolibri', 'Audiolibri'),
    ]

    # Dati dell'opera trattata
    title = models.CharField(max_length=200, verbose_name="Titolo Opera (es. Dune: Parte Due)")
    release_year = models.IntegerField(verbose_name="Anno di uscita")
    media_type = models.CharField(max_length=20, choices=MEDIA_CHOICES, verbose_name="Tipo di Media")
    cover_image = models.ImageField(upload_to='covers/', verbose_name="Immagine di Copertina", blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='articles', blank=True)
    
    # Dati editoriali (La vostra recensione/contenuto)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autore (Team)")
    team_rating = models.DecimalField(
        max_digits=3, decimal_places=1, 
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        verbose_name="Voto Redazione", blank=True, null=True
    )
    short_description = models.TextField(max_length=300, verbose_name="Estratto/Sinossi breve")
    content = models.TextField(verbose_name="Testo Completo dell'Articolo")
    
    # Supporto multimediale per l'archivio (ascoltare e guardare)
    audio_track = models.FileField(upload_to='audio_fragments/', blank=True, null=True, verbose_name="Traccia Audio (Opzionale)")
    video_url = models.URLField(blank=True, null=True, verbose_name="Link Video (Opzionale)")

    is_featured = models.BooleanField(default=False, verbose_name="In Evidenza")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Articolo"
        verbose_name_plural = "Articoli"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - recensito da {self.author.username}"
    

class AudioChapter(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='audio_chapters')
    title = models.CharField(max_length=200, verbose_name="Titolo Traccia/Capitolo")
    audio_file = models.FileField(upload_to='audiobooks/')
    order = models.PositiveIntegerField(default=0, verbose_name="Ordine (1, 2, 3...)")

    class Meta:
        ordering = ['order']
        verbose_name = "Traccia Audio"
        verbose_name_plural = "Tracce Audio"

    def __str__(self):
        return f"{self.order}. {self.title}"

class StoryPart(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='story_parts')
    title = models.CharField(max_length=200, verbose_name="Titolo Capitolo", blank=True, help_text="Lascia vuoto se è un racconto unico")
    content = models.TextField(verbose_name="Testo del Capitolo")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordine (1, 2, 3...)")

    class Meta:
        ordering = ['order']
        verbose_name = "Capitolo Racconto"
        verbose_name_plural = "Capitoli Racconto"

    def __str__(self):
        return f"Capitolo {self.order}: {self.title}"