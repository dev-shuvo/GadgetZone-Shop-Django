from .models import WebsiteDetails


def website(request):
    try:
        website = WebsiteDetails.get_solo()
    except WebsiteDetails.DoesNotExist:
        website = None

    data = {
        "website": website,
    }

    return data
