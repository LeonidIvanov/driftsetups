from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.views.generic import ListView

from setup.models import Setup


class SearchListView(ListView):
    """
    Display a Setup List page filtered by the search query.
    """
    model = Setup
    paginate_by = 16
    template_name = 'search_list.html'
    context_object_name = 'setups'

    def get_context_data(self, **kwargs):
        context = super(SearchListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        qs = Setup.objects.all()

        keywords = self.request.GET.get('q')
        if keywords:
            query = SearchQuery(keywords)
            title_vector = SearchVector('name', weight='A')
            car_sub_model_vector = SearchVector(
                'sub_model_setup__car_model__brand__name',
                'sub_model_setup__car_model__name',
                'sub_model_setup__name',
                weight='B')
            content_vector = SearchVector('description', weight='D')
            vectors = title_vector + car_sub_model_vector + content_vector
            qs = qs.annotate(search=vectors).filter(search=query)
            qs = qs.annotate(rank=SearchRank(vectors, query)).order_by('-rank')

        return qs