from .models import Category

def categories_processors(request):
    return {
         'categorys':Category.objects.filter(parent=None)
    }

