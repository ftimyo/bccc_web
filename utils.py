import re
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage
import datetime

#search Utilities
def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

#paging Utilities
def pager(entries, page, default_page_size=7):
    paginator = Paginator(entries, default_page_size)
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        result = paginator.page(paginator.num_pages)
    return result

#Data Filter

def date_range_filter(entries, sdate, edate):
    fmt = "%m/%d/%Y"
    try:
        sdate = datetime.datetime.strptime(sdate, fmt)
    except:
        sdate = ''

    if sdate:
        entries = entries.filter(pub_time__gte=sdate)
        sdate = sdate.strftime(fmt)

    try:
        edate = datetime.datetime.strptime(edate, fmt)
        edate = edate + datetime.timedelta(days=1)
    except:
        edate = ''

    if edate:
        entries = entries.filter(pub_time__lte=edate)
        edate = edate.strftime(fmt)

    return entries

def control_filter(request, domain, entries):
    sort_field={'newest': '-pub_time', 'oldest': 'pub_time'}
    sort=request.GET.get('sort')
    search=request.GET.get('search')
    page=request.GET.get('page')
    sdate=request.GET.get('sdate')
    edate=request.GET.get('edate')

    if entries and (sdate or edate):
        entries = date_range_filter(entries, sdate, edate)

    if entries and search:
        search_fields = ['title', 'text']
        if domain == 'sermon':
            search_fields += ['keywords']
        entries = entries.filter(get_query(search, search_fields))

    if entries:
        entries = entries.order_by(sort_field.get(sort, '-pub_time'))
        sort = {'newest': 'newest', 'oldest': 'oldest'}.get(sort, 'newest')

    if entries:
        entries = pager(entries, page, 25)

    if not search:
        search=''
    if not edate:
        edate=''
    if not sdate:
        sdate=''

    return {'entries': entries, 'sort': sort, 'search': search, 'sdate': sdate, 'edate': edate}

class MediaFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name):
        return name

    def _save(self, name, content):
        if self.exists(name):
            # if the file exists, do not call the superclasses _save method
            return name
        # if the file is new, DO call it
        return super(MediaFileSystemStorage, self)._save(name, content)

