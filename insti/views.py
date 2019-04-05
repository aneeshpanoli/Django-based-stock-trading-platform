from django.conf.urls.static import static
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views import View
from .forms import SearchCompanyForm, FindCusipForm
from static.py import process13Fdata
# Create your views here.
class instiView(TemplateView):

    def get(self, request, *args, **kwargs):
        the_form = SearchCompanyForm()
        context = {
            "title": "pyzyme.com",
            "form": the_form,
        }
        return render(request, "insti/query.html", context)
    # template_name = "stockAnalysis/query.html"
    def post(self, request, *args, **kwargs):
        form = SearchCompanyForm(request.POST)
        form1 = FindCusipForm(request.POST)
        if request.method == 'POST' and 'instiSearch' in request.POST.keys():
            if request.POST['tickerSymbol'] == "summary13F":
                tickrjs = "positiveChange"
            else:
                start13Fprocess = process13Fdata.process13FHR(request.POST['tickerSymbol'])
                print(request.POST['tickerSymbol'])
                tickrjs = start13Fprocess.com_data()
            context = {
                "tickr": tickrjs,
                "form": form,
                "form1":form1,
            }
            return render(request, "insti/results.html", context)
        elif request.method == 'POST' and 'cusipSearch' in request.POST.keys():
            tickr = request.POST['cusip']
            start13Fprocess = process13Fdata.process13FHR(tickr)
            cusipDict = start13Fprocess.com_of_interest()
            context = {
                "tickr": tickr,
                "form": form,
                "form1":form1,
                "data" : cusipDict,
            }
            return render(request, "insti/results.html", context)
        else:
            tickr = request.POST['cusipSearch']
            context = {
                "tickr": tickr,
                "form": form,
                "form1":form1,
                "data" : cusipDict,
            }
            return render(request, "homepage/inv_keyword.html", context)
