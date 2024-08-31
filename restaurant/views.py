from django.views.generic import TemplateView
from restaurant.models import Dish


class Homepage(TemplateView):
    template_name = "restaurant/index.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        categories = [
            ("appetisers", "Закуски"),
            ("breakfasts", "Завтраки"),
            ("salads", "Салаты"),
            ("cold side dish", "Холодные блюда"),
            ("hot side dish", "Горячие блюда"),
            ("desserts", "Десерты"),
            ("drinks", "Напитки"),
            ("extra", "Дополнительно"),
        ]
        all_dishes = []
        for category in categories:
            dishes = Dish.objects.filter(category=category[0])
            if dishes:
                context_data[category] = dishes
                all_dishes.append({"name": category[1], "dishes": dishes})

        context_data["all"] = all_dishes
        return context_data


class AboutPage(TemplateView):
    template_name = "restaurant/about.html"
