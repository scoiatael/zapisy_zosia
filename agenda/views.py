from django.views.generic.base import TemplateView
from django.utils import timezone

from .models import Agenda

class AgendaView(TemplateView):

    template_name = 'agenda.html'

    def get_context_data(self, **kwargs):
        context = super(AgendaView, self).get_context_data(**kwargs)
        context['agenda'] = Agenda.objects \
            .filter(pub_date__lte=timezone.now()).first()
        return context
