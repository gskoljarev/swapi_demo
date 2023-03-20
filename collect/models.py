from django.db import models
from django.utils.translation import gettext_lazy as _


class DatasetMetadata(models.Model):
    filename = models.CharField(_('Filename'), max_length=256, null=False, blank=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Dataset Metadata')
        verbose_name_plural = _('Dataset Metadata')

    def __str__(self):
        return "%s - %s" % (self.filename, self.created_at)