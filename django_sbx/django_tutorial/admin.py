from django.contrib import admin

from .models import Question, Choice

# Register your models here.
# Регистрация существующих моделей 
# admin.site.register(Question)
admin.site.register(Choice)

class ChoiceInline(admin.StackedInline):
    """
        Чтобы добавить несколько вариантов Choice к созданному Question 
    """
    model = Choice
    extra = 3

class ChoiceInlineTabular(admin.TabularInline):
    """
        Несколько вариантов Choice в табличном виде
    """
    model = Choice
    extra = 3

# Если необходимо переопределить зарегистрированную модель, то необходимо создать класс admin.ModelAdmin, 
# а затем передать его вторым параметром при регистрации 
class QuestionAdmin(admin.ModelAdmin):
    """
        Переопределение порядка отображаемых полей
    """
    # 1
    # fields = ["pub_date", "question_text"]

    # 2 
    # Первый элемент в кортеже - заголовок fieldset
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]
    # 3 
    # inlines = [ChoiceInline]
    # 4
    inlines = [ChoiceInlineTabular] 

    # 5 
    # показывать поля в list-форме, можно передавать методы модели 
    # но не поддерживается сортировка по пользовательским методам 
    list_display = ("question_text", "pub_date", "was_published_recently")

    # Для задания фильтров в панели администрирования 
    list_filter = ["pub_date"]

    # Возможность поиска 
    search_fields = ["question_text"]

admin.site.register(Question, QuestionAdmin)
