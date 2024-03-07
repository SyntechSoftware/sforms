from django import template
from time import time
from ..utils import build_form
from ..models import SForm
from ..signals import form_was_fullfilled
from django.utils.safestring import mark_safe


register = template.Library()


class SFormAssignNode(template.Node):
    def __init__(self, sform_id, url):
        self.sform_id = sform_id
        self.url = url

    def render(self, context):

        request = context.get('request', None)
        if not request:
            return 'sform must be called in HTTP query (request required)'
        sform_id = self.sform_id
        if not sform_id:
            sform_id = context.get('sform_id', context.get('sformid', context.get('formid', None)))

        if not sform_id:
            return f'sform with code "{sform_id}" is not found'
        
        sform = SForm.objects.filter(code=sform_id).first()
        if not sform:
            return f'sform with code "{sform_id}" is not found'

        form_class = build_form(sform.pk, request)

        kwargs = {}
        if request.method in ("POST", "PUT"):
        
            if hasattr(request, 'session'):
                ts = request.session.get(f"_sform_{sform_id}", None)
                if ts and time() - ts < 3600:
                    context['success'] = True
                    return ""

            kwargs.update(
                {
                    "data": request.POST,
                    "files": request.FILES,
                }
            )
            form = form_class(**kwargs)
            if form.is_valid():
                form_was_fullfilled.send_robust(
                    sender=form,
                    form_code=sform_id,
                    form_data=form.changed_data
                )
                success=True
                request.session[f"_sform_{sform_id}"] = time()
            else:
                success=False
        else:
            form = form_class(**kwargs)
            success = None

        context['form'] = form
        context['success'] = success

        if success and self.url:
           
            return mark_safe(f"""
                <script>
                    location.href = "{self.url}";
                </script>
            """)

        return ""

@register.tag
def sform(parser, token):

    args = token.contents.split()

    sform_id = args[1] if len(args) > 1 else None
    if sform_id == "-":
        sform_id = None

    url = args[2] if len(args) > 2 else None

    return SFormAssignNode(sform_id, url)

