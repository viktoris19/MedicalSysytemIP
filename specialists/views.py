from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models.specialists import get_specialist_by_id, sort_specialists
from storage import load_specialists


def specialists(request: HttpRequest) -> HttpResponse:
    specialists_list = load_specialists('data/specialists.json')
    context = {'specialists': sort_specialists(specialists_list)}
    return render(request, 'specialists/specialist_list.html', context)


def specialist_detail(
    request: HttpRequest, specialist_id: int,
) -> HttpResponse:
    specialists_list = load_specialists('data/specialists.json')
    specialist = get_specialist_by_id(specialists_list, specialist_id)

    if specialist is None:
        return render(
            request,
            'specialists/specialist_not_found.html',
            status=404,
        )

    context = {'specialist': specialist}
    return render(
        request, 'specialists/specialist_detail.html', context,
    )