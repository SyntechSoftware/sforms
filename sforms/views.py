
from django.views.generic import FormView

from .utils import build_form

class BaseSFormView(FormView):
    def get_form_class(self):
        return build_form(self.kwargs.get('sform_id'), self.request)
