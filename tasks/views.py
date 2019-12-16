from django.views.generic import TemplateView


class IndexView(TemplateView):
    """トップページ"""

    template_name = 'index.html'

