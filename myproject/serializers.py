from django.core.serializers.json import Serializer

# http://d.hatena.ne.jp/tatz_tsuchiya/20130625/1372157983
# http://stackoverflow.com/questions/9403120/getting-django-to-serialize-objects-without-the-fields-field
class Serializer(Serializer):
    # https://github.com/django/django/blob/7f51876f99851fdc3fef63aecdfbcffa199c26b9/django/core/serializers/python.py#L39
    def get_dump_object(self, obj):
        return self._current

    def start_serialization(self):
        super(Serializer, self).start_serialization()
        # 日本語対応
        self.json_kwargs["ensure_ascii"] = False
        # タブインデントは2にしておく
        self.json_kwargs['indent'] = 2
        # JSONエンコーダーのクラスはデフォルトで「DjangoJSONEncoder」が指定されている
        # https://github.com/django/django/blob/1d1e246db6ae8a8c7b9a54f3485809a36c5ee373/django/core/serializers/json.py#L41