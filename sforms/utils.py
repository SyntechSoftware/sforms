from .models import SForm, SFormResult, SFormResultAttach
from .constants import FieldTypes
from django.core.files.base import File
from django.core.files.storage import default_storage
from django import forms
from django.http import Http404


CONTROL_MAPPING = {
    FieldTypes.FIELD_TYPE_TEXT: (forms.CharField, forms.TextInput),
    FieldTypes.FIELD_TYPE_EMAIL: (forms.EmailField, forms.EmailInput),
    FieldTypes.FIELD_TYPE_PASSWORD: (forms.CharField, forms.PasswordInput),
    FieldTypes.FIELD_TYPE_NUMBER: (forms.IntegerField, forms.NumberInput),
    FieldTypes.FIELD_TYPE_TEXTAREA: (forms.CharField, forms.Textarea),
    FieldTypes.FIELD_TYPE_CHECKBOX: (forms.BooleanField, forms.CheckboxInput),
    # FieldTypes.FIELD_TYPE_MULTICHECKBOX: (forms.BooleanField, forms.CheckboxInput),
    FieldTypes.FIELD_TYPE_RADIO: (forms.CharField, forms.RadioSelect),
    FieldTypes.FIELD_TYPE_SELECT: (forms.CharField, forms.Select),
    FieldTypes.FIELD_TYPE_HIDDEN: (forms.CharField, forms.HiddenInput),
    # FieldTypes.FIELD_TYPE_LABEL: (forms.BooleanField, forms.CheckboxInput),
    FieldTypes.FIELD_TYPE_ATTACH: (forms.FileField, forms.FileInput),
}

def _store_call(self):
    if self.is_bound and not self._errors:
        data = {}
        files = {}
        for _k, _v in self.cleaned_data.items():
            if not isinstance(_v, File):
                data[_k] = _v
            else:
                files[_k] = _v

        _meta = {
            _k: f"{_v}"
            for _k, _v in self._request.META.items()
        } if self._request else {}

        res = SFormResult.objects.create(
            form_code=self._form_code,
            meta=_meta,
            values=data,
        )

        for _k, _v in files.items():
            SFormResultAttach.objects.create(
                result=res,
                field = _k,
                value = _v
            )


def build_form(sform_id, request=None):
    form = SForm.objects.filter(code=sform_id).first()
    if not form:
        raise Http404('Not found')

    declared_fields = {}
    for f in form.sformrow_set.order_by('order'):
        field_type, widget_type = CONTROL_MAPPING.get(f.fieldtype, (forms.CharField, forms.TextInput))
        widget_kwargs = {
            'attrs': {
                'placeholder': f.placeholder if f.placeholder else ""
            }
        }
        if f.fieldtype in FieldTypes.HAS_VALUES:

            choices = []
            if f.values:
                for opt in f.values.splitlines():
                    if opt and opt.strip():
                        opt = opt.strip()
                        if ":" in opt:
                            opt_k, opt_v = opt.split(':', 1)
                            choices.append((opt_k, opt_v,))
                        else:
                            choices.append((opt, opt,))
            if not f.required:
                choices.insert(0, (None, "---",)) 
            widget_kwargs['choices'] = choices
        kwargs = {
            'label': f.label if f.label else f.name,
            'initial': f.default if f.default else "",
            'required': f.required,
            'widget': widget_type(**widget_kwargs)
        }

        declared_fields[f.name] = field_type(**kwargs)

    x_SForm = type(f"SForm_{form.code}", (forms.BaseForm, ), { 
        "base_fields": declared_fields, 
        "declared_fields": declared_fields,
        "_request": request,
        "_form_code": form.code,
        "_post_clean": _store_call,
    }) 

    return x_SForm
