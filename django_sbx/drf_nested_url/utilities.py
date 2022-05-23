from slugify import slugify 

def slugify_function(text: str) -> str:
    """
        Функция для генерации slug-поля из строки
        Slug-поле используется для красивых url 
        Строка вида текст1-текст2-...-текстn
        То, что переваривает браузер
    """
    return slugify(text=str, lowercase=True)