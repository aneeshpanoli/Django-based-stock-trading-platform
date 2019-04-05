"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from ib.views import CommandCenterView, forexWatchlistRefresh\
                    , stockWatchlistRefresh, MarketStatusView\
                    , LiveTradeListRefresh
from insti.views import instiView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^cc/', CommandCenterView.as_view(), name='CommandCenterView'),
    url(r'^insti/', instiView.as_view(), name='instiView'),
    url(r'^dummy2forAjax1/', forexWatchlistRefresh.as_view(), name='forexWatchlistRefresh'),
    url(r'^dummy2forAjax2/', stockWatchlistRefresh.as_view(), name='stockWatchlistRefresh'),
    url(r'^dummy2forAjax3/', MarketStatusView.as_view(), name='MarketStatusView'),
    url(r'^dummy2forAjax4/', LiveTradeListRefresh.as_view(), name='LiveTradeListRefresh'),
]
