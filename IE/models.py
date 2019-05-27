from django.db import models
from django.contrib import admin

# from IE.simplex import Tableau
from IE.simplex2 import SimplexSolver
from scipy.optimize import linprog


class Indicators(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.SET_NULL)
    name = models.TextField()

    def __str__(self):
        return self.name

    def calculate_indicators_weight(self, year, region, max, min):
        indicators = self.objects.filter(parent=None).all()
        max_line = []
        max_restriction = []
        max_weight = []
        min_weight = []
        max_calc = []
        min_calc = []
        for item in indicators:
            max_ = []
            min_ = []

            weight_indicator = WeightIndicators.objects.filter(indicator_id=item.id, year=year, region=region).first()
            if not (weight_indicator):
                continue
            max_line.append(float(weight_indicator.value))
            for item2 in indicators:
                if (item2.id == item.id):
                    max_.append(1)
                    min_.append(1)
                else:
                    max_.append(0)
                    min_.append(0)
            max_calc.append(max_)
            min_calc.append(min_)

            if not (max[item.id]):
                max[item.id] = 0
            max_weight.append(float(max[item.id]))
            if not (min[item.id]):
                min[item.id] = 0
            min_weight.append(float(min[item.id]))
            max_restriction.append(1)

        A = [max_restriction] + max_calc + min_calc + max_calc
        b = [1] + max_weight + min_weight + [0, 0, 0]
        tab = SimplexSolver().run_simplex(A=A, b=b, c=max_line, prob='max',
                                          ineq=['=', '<=', '<=', '<=', '>=', '>=', '>=', '>=', '>=', '>='],
                                          enable_msg=False, latex=False)
        return tab


class IndicatorsAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')


class Regions(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class WeightIndicators(models.Model):
    value = models.FloatField()
    weight = models.FloatField()
    region = models.ForeignKey(Regions, blank=False, null=False, related_name='region', on_delete=models.CASCADE)
    indicator = models.ForeignKey(Indicators, blank=False, null=False, related_name='indicator',
                                  on_delete=models.CASCADE)
    year = models.IntegerField()

    def get_distinct_years(self):
        return self.objects.values('year').distinct()


class WeightIndicatorsAdmin(admin.ModelAdmin):
    list_display = ('value', 'weight', 'region', 'indicator')
