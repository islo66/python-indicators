from django.shortcuts import render
from IE.models import Regions, WeightIndicators, Indicators
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def index(request):
    regions = Regions.objects.all()
    weight_indicators = WeightIndicators.get_distinct_years(WeightIndicators)
    parent_indicators = Indicators.objects.filter(parent=None).all()

    if (request.method == 'POST'):
        year = request.POST.get('year')
        region = request.POST.get('region')
        min = {}
        max = {}
        for parent_indicator in parent_indicators:
            min[parent_indicator.id] = request.POST.get('min[' + str(parent_indicator.id) + ']')
            max[parent_indicator.id] = request.POST.get('max[' + str(parent_indicator.id) + ']')
        Indicators.calculate_indicators_weight(Indicators, year, region, max, min)
    return render(request, 'index.html',
                  {'regions': regions, 'weight_indicators': weight_indicators, 'parent_indicators': parent_indicators})
