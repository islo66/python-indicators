from django.contrib import admin
from IE.models import Indicators, IndicatorsAdmin, Regions, WeightIndicators, WeightIndicatorsAdmin


admin.site.register(Indicators, IndicatorsAdmin)
admin.site.register(Regions)
admin.site.register(WeightIndicators, WeightIndicatorsAdmin)
