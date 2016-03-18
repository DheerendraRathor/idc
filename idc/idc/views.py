from django.core.urlresolvers import reverse
from django.views.generic import RedirectView


class IndexView(RedirectView):

    pattern_name = 'blog:posts'