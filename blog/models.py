from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib.auth.models import User

class BlogPost(models.Model):
    title = models.CharField(max_length=128)
    pub_date = models.DateTimeField(editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    text = models.TextField()

    class Meta:
        verbose_name = _('Blog Entry')
        verbose_name_plural = _('Blog Entries')

    def save(self, *args, **kwargs):
        if not self.id:
            self.pub_date = timezone.now()
        super(BlogPost, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('blog.views.index')
