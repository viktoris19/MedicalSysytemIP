from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Specialist

def specialists(request: HttpRequest) -> HttpResponse:
    specialists_list = Specialist.objects.all().order_by('last_name')
    return render(
        request,
        'specialists/specialist_list.html',
        {'specialists': specialists_list},
    )

def specialist_detail(request: HttpRequest, specialist_id: int) -> HttpResponse:
    specialist = get_object_or_404(Specialist, id=specialist_id)
    return render(
        request,
        'specialists/specialist_detail.html',
        {'specialist': specialist},
    )