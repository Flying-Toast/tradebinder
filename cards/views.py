from django.shortcuts import render, get_object_or_404
from .models import Card


def card_detail(request, setcode, collectornum):
    card = get_object_or_404(Card, set__code=setcode, collector_number=collectornum)
    return render(request, "cards/card_detail.html", {"card": card})
