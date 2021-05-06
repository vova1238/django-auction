from website.models import Category

def main_processor(request):
    categories = Category.objects.all()[:5]
    return {"first_five_categories": categories}