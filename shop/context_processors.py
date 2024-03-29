from .models import Category


def categories(request):
    """
    Retrieves a dictionary containing a list of top-level categories from the database.

    """
    return {
        "categories": Category.objects.filter(parent=None),
    }