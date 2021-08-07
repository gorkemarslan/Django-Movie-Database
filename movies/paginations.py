from django.core.paginator import InvalidPage
from django.http import Http404
from django.utils.translation import gettext as _


def custom_paginate_queryset(obj, queryset, page_size):
    """
    The method is used to override paginate_queryset() method with the following customizations:
        * float page numbers are converted to int.
        * If a page number is less or equal to 0, then returns the first page.
        * If a page is greater than the last page, then returns the last page.
    """
    paginator = obj.get_paginator(
        queryset, page_size, orphans=obj.get_paginate_orphans(),
        allow_empty_first_page=obj.get_allow_empty())
    page_kwarg = obj.page_kwarg
    page = obj.kwargs.get(page_kwarg) or obj.request.GET.get(page_kwarg) or 1
    # Now page queries can be float. If it is, make it float() first, then apply int()
    # Remember that page is an instance of str class
    try:
        page_number = int(float(page))
    except ValueError:
        if page == 'last':
            page_number = paginator.num_pages
        else:
            raise Http404(_('Page is not “last”, nor can it be converted to an int.'))

    try:
        if page_number > paginator.num_pages:
            page_number = paginator.num_pages
        elif page_number <= 0:
            page_number = 1
        page = paginator.page(page_number)
        return paginator, page, page.object_list, page.has_other_pages()
    except InvalidPage as e:
        raise Http404(_('Invalid page (%(page_number)s): %(message)s') % {
            'page_number': page_number,
            'message': str(e)
        })
