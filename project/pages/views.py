from django.views.generic import TemplateView


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'


class LinksDepotView(TemplateView):
    template_name = 'pages/links_depot.html'


class MindMapView(TemplateView):
    template_name = 'pages/mind_map.html'
