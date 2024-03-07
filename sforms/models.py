from django.db import models
from django.core.validators import RegexValidator
from .constants import FieldTypes

alphanumeric = RegexValidator(r'^[0-9a-z\_]*$', 'Only lowercase alphanumeric characters and underscore are allowed.')


class SForm(models.Model):
    code = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=150)
    label = models.CharField(max_length=250)
    description = models.TextField(blank=True, default="")

    class Meta:
        verbose_name = "S-Form"
        verbose_name_plural = "S-Forms"


class SFormRow(models.Model):
    form = models.ForeignKey(SForm, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, validators=[alphanumeric])
    fieldtype = models.CharField(max_length=15, choices=FieldTypes.CHOICES)
    required = models.BooleanField(default=False)
    label = models.CharField(max_length=150, null=True, blank=True)
    placeholder = models.CharField(max_length=150, null=True, blank=True)
    default = models.CharField(max_length=150, null=True, blank=True)
    values = models.TextField(default="", blank=True, help_text="List of Value or Value:Label, each value on a new line ")
    order = models.IntegerField(default=0, db_index=True)

    class Meta:
        ordering = ('order', )
        unique_together = ["form", "name"]
        verbose_name = "S-Form's row"


class SFormResult(models.Model):
    form_code = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    meta = models.JSONField(default=dict)
    values = models.JSONField(default=dict)

    def __str__(self):
        return f'{self.form_code} {self.timestamp}'

    class Meta:
        verbose_name = "S-Form result"
        verbose_name_plural = "S-Form results"


class SFormResultAttach(models.Model):
    result = models.ForeignKey(SFormResult, on_delete=models.CASCADE)
    field = models.CharField(max_length=50)
    value = models.FileField()

    def __str__(self):
        return self.field
    