from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.reverse import reverse 

from slugify import slugify 


class MultipleLookupsHyperLinkedIdentityField(HyperlinkedIdentityField):
    """
        Необходим для генерации корректного URL в сериализаторе во вложенном REST API
        с возможностью подстановки нескольких значений в URL

        Оригинальное поле - дает только одну подстановку
    """

    def __init__(self, *args, **kwargs):
        """
            Конструктор, вдобавок к наследуемой модели, ожидает именованный аргумент 
            lookup_fields - кортеж кортежей размерность 2, где
            1-й элемент: поле из модели 
            2-й элемент: параметр URL 
        """
        self.lookup_fields = kwargs.pop("lookup_fields", (("pk", "pk"),))
        super().__init__(*args, **kwargs)

    def get_url(self, obj, view_name, request, format):
        """
            Возвращает URL к объекту по самому объекту
        """
        
        """
            Необходимо сгенерировать kwargs, для передачи в reverse 
            Суть в том, что по пути модели через кучу точек (связи между моделями)
            Получить финальное значение, которое будет подставлено в итоговый URL 
            (вызов функции reverse)

            obj - экземпляр объекта модели - насколько понял
        """
        kwargs = {}

        for model_field, url_parameter in self.lookup_fields:
            attribute = obj 
            for field in model_field.split("."):
                attribute = getattr(attribute, field)
            kwargs[url_parameter] = attribute

        return reverse(viewname=view_name, kwargs=kwargs, request=request, format=format)

def slugify_function(text: str) -> str:
    """
        Функция для генерации slug-поля из строки
        Slug-поле используется для красивых url 
        Строка вида текст1-текст2-...-текстn
        То, что переваривает браузер
    """
    return slugify(text=text, lowercase=True)
    