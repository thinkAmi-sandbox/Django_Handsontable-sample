import json
from django.views import View
from django.views.generic import ListView
from django.http import HttpResponse
from django.core import serializers
from django.utils import timezone
from .models import Header, Detail


NEW_PAGE_ID = 0

# Ajax用のViewだとテンプレートは不要なので、django.views.Viewを使う(Django 1.10からこのパッケージ名で良いらしい)
# https://docs.djangoproject.com/en/1.10/ref/class-based-views/base/#django.views.generic.base.View
class HandsonTableView(View):
    def get(self, request, *args, **kwargs):
        # http://stackoverflow.com/questions/13527843/accessing-primary-key-from-url-in-django-view-class
        details = Detail.objects.filter(header__pk=self.kwargs.get('pk')).select_related().all()

        # serializerがjson.dumpしてるので、JsonResponseを使うと二重でjson.dump()してしまうため、普通のレスポンスを使う
        # http://stackoverflow.com/questions/26373992/use-jsonresponse-to-serialize-a-queryset-in-django-1-7
        # https://github.com/django/django/blob/1d1e246db6ae8a8c7b9a54f3485809a36c5ee373/django/core/serializers/json.py#L63
        # https://github.com/django/django/blob/190d2ff4a7a392adfe0b12552bd71871791d87aa/django/http/response.py#L526
        return HttpResponse(
            serializers.serialize('handsontablejson', details),
            content_type='application/json'
        )


    def post(self, request, *args, **kwargs):
        # http://stackoverflow.com/questions/29780060/trying-to-parse-request-body-from-post-in-django
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        header = self.update_header(self.kwargs.get('pk'))

        # 明細部分は、DELETE&INSERTで作る
        Detail.objects.filter(header=header).delete()

        for b in body:
            Detail(
                header=header,
                purchase_date=b.get('purchase_date'),
                name = b.get('name'),
                price = b.get('price'),
            ).save()

        return HttpResponse('OK')


    def update_header(self, pk):
        if int(pk) == NEW_PAGE_ID:
            new_header = Header(update_at = timezone.now())
            new_header.save()

            # 念のため、保存できたかidをprint
            # http://stackoverflow.com/questions/14832115/get-the-last-inserted-id-in-django
            print(Header.objects.latest('id').id)
            return new_header

        # QuerysetObjectではなくRecordObjectとするため、first()で絞り込む
        # AttributeError: 'QuerySet' object has no attribute 'save'
        # http://stackoverflow.com/questions/6221510/django-calling-save-on-a-queryset-object-queryset-object-has-no-attribute-s
        header = Header.objects.filter(pk=pk).first()
        header.update_at = timezone.now()
        header.save()
        return header

