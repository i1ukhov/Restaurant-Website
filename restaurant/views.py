from django.views.generic import TemplateView


class Homepage(TemplateView):
    template_name = "restaurant/index.html"


class AboutPage(TemplateView):
    template_name = "restaurant/about.html"


