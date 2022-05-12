from django.contrib.auth.models import User, Group 

from rest_framework import serializers

from drf_tutorial.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

# Гиперсвязывание - хороший REST-дизайн 
class QSUserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]

class QSGroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Group
        fields = ["url", "name"]

"""
    Сериализаторы позволяют преобразовывать данные из Json-а в экземпляры модели 
    и позволяет преобразовывать экземпляры модели в Json 

    Объявление сериализаторов работает приблизительно также, как и объявление форм
"""
class SnippetSerializer(serializers.Serializer):
    
    """
        Сериализатор очень напоминает форму, и включает аналогичные флаги валидации для разных полей, такие как 
        required, max_length и default
    """

    # Здесь определяются поля - который будут сериализованы / десериализованы 
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    # Как понял - это стиль формы - эквивалентно widgets=widgets.TextArea у Form 
    code = serializers.CharField(style={"base_template": "textarea.html"})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default="python")
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default="friendly")

    # create() и update() определяют, каким образом полноценные экземпляры модели будут сохранены при вызове serializer.save()

    def create(self, validated_data):
        """
            Create and return a new Snippet instance, given the validated data
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
            Update and return an existing Snippet instance, given the validated data 
        """
        instance.title = validated_data.get("title", instance.title)
        instance.code = validated_data.get("code", instance.code)
        instance.linenos = validated_data.get("linenos", instance.linenos)
        instance.language = validated_data.get("language", instance.language)
        instance.style = validated_data.get("style", instance.style)
        instance.save()

        return instance 

# также как есть Form и ModelForm - так и есть Serializer и ModelSerializer 
# следует понимать, что это всего лишь шорткат для создания сериализатора, который 
# автоматически определяет набор полей, содержит простые имплементации методов create() и update()
class SnippetModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ["id", "title", "code", "linenos", "language", "style"]
