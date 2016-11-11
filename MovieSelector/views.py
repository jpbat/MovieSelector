from django.views.generic import RedirectView


class RedirectToGitHub(RedirectView):

    url = "https://github.com/jpbat"
