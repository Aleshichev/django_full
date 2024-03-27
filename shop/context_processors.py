from .models import Category


def categories(request):
    """
    Retrieves a dictionary containing a list of top-level categories from the database.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        dict: A dictionary containing a single key-value pair. The key is "categories" and the value is a queryset of Category objects with no parent.
    """
    return {
        "categories": Category.objects.filter(parent=None),
    }