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
        Indicators.calculate_indicators_weight(Indicators, year, region, min, max)
    return render(request, 'index.html',
                  {'regions': regions, 'weight_indicators': weight_indicators, 'parent_indicators': parent_indicators})


@csrf_exempt
def methodTwo(request):
    regions = Regions.objects.all()
    step = 1
    if (request.method == 'POST'):
        step = request.POST.get('step', 2)
        year = request.POST.get('year')
        region = request.POST.get('region')

        indicators = Indicators.objects.filter(parent__isnull=False).values_list('id', flat=True)
        weight_indicators = WeightIndicators.objects.filter(indicator__in=indicators, region=region, year=year, value=0)

        if (int(step) == 2):
            return render(request, 'method-two.html',
                          {'years': range(1999, 2050), 'regions': regions, 'step': int(step),
                           'region': Regions.objects.get(pk=region), 'year_input': year,
                           'weight_indicators': weight_indicators})
        if (int(step) == 3):
            max = {}
            min = {}
            for ind in weight_indicators:
                max[ind.indicator_id] = request.POST.get('max[' + str(ind.indicator_id) + ']')
                min[ind.indicator_id] = request.POST.get('min[' + str(ind.indicator_id) + ']')
            IC = Indicators.monte_carlo(Indicators, year, region, min, max, weight_indicators)
            return render(request, 'method-two.html',
                          {'years': range(1999, 2050), 'regions': regions, 'step': int(step),
                           'region': Regions.objects.get(pk=region), 'year_input': year, 'IC':IC})
    return render(request, 'method-two.html', {'years': range(1999, 2050), 'regions': regions, 'step': step})
