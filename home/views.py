from itertools import chain

from django.views.generic import TemplateView
from django.utils import timezone

from car.models import CarModel, CarSubModel
from setup.models import Setup, SetupImage


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['top_cars'] = sorted(
            list(
                chain(
                    CarSubModel.objects.all(),
                    CarModel.objects.all()
                )
            ), key=lambda instance: instance.views, reverse=True
        )[:4]
        context['top_setups_by_views'] = Setup.objects.order_by('-views')[:5]
        setups_by_votes = sorted(
            Setup.objects.all(),
            key=lambda s: s.get_votes_total(),
            reverse=True
        )[:100]
        context['top_setups_by_votes_percentage'] = sorted(
            setups_by_votes,
            key=lambda s: s.get_votes_percentage(),
            reverse=True
        )[:5]
        context['top_weekly_setups'] = Setup.objects.filter(
            timestamp__gte=timezone.now() - timezone.timedelta(days=7)
        ).order_by('-views')[:5]
        return context
