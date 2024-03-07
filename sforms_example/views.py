from django.views.generic import TemplateView
from django.urls import reverse
from sforms.views import BaseSFormView


class SampleFormView(BaseSFormView):
    template_name = 'sforms/sforms_example.html'

    def form_valid(self, form):
        print(form.cleaned_data, flush=True)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('form_example', kwargs={'sform_id': self.kwargs.get('sform_id')})


class SampleTagView(TemplateView):
    template_name = 'sforms/sforms_tag_example.html'
    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
