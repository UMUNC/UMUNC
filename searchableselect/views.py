from django.db.models.loading import get_model
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models.query_utils import Q


@staff_member_required
def filter_models(request):
    model_name = request.GET.get('model')
    search_fields = request.GET.get('search_field')
    value = request.GET.get('q')

    query = []
    for search_field in search_fields.split():
        if query:
            query = query | Q(**{'{}__icontains'.format(search_field): value})
        else:
            query = Q(**{'{}__icontains'.format(search_field): value})

    model = get_model(model_name)
    print {'{}__icontains'.format(search_field): value}

    values = model.objects.filter(query)#[:10]
    values = [
        dict(pk=value.pk, name=unicode(u"[{}]{}".format(value.profile.Identify, value.profile.Name)))
        for value
        in values
    ]

    return JsonResponse(dict(result=values))
