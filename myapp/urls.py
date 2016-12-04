from django.conf.urls import url
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from .views import HandsonTableView
from .models import Header

# http://qiita.com/irxground/items/cd83786b10d81eecce77
urlpatterns = [
    # 一覧ページ
    url(r'^records/$',
        ListView.as_view(model=Header),
        name='record-index',
    ),
    # 新規作成ページ
    url(r'^records/new$', 
        TemplateView.as_view(template_name='myapp/detail.html'),
        name='record-new'
    ),
    # 編集ページ
    url(r'^records/(?P<pk>[0-9]+)/edit$', 
        TemplateView.as_view(template_name='myapp/detail.html'),
        name='record-edit'
    ),
    # Ajax用
    url(r'^ajax/records/(?P<pk>[0-9]+)$',
        HandsonTableView.as_view(),
        name='ajax',
    ),
]