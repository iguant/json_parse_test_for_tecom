Для работы необходимо получить Google **key_api** и **CSE_id**
 https://developers.google.com/custom-search/v1/overview
 
и запусть с параметрами --api_key и --cse_id



### Задачка по обработке данных json, yaml, работе с файлами и разбору сайтов


Среда разработки: Python3

Требования: использовать готовые библиотеки python (любые) для работы с json и yaml форматами.

Исходные данные:

Файл настроек в формате yaml (приложен):

```yaml
---

settings:

  search_string: json data example

  pages_count: 10
```

 

Требуемый алгоритм работы программы и результаты:

Читаем файл настроек
Ищем в поисковике google.com строчку, указанную в search_string (в примере это “json data example”)
Просматриваем первые pages_count страниц результатов выдачи google (в примере 10 страниц выдачи google)
Переходим по ссылкам из выдачи и ищем там все объекты в формате json, например, на странице https://json.org/example.html есть такое:
 
```json
{

    "glossary": {

        "title": "example glossary",

               "GlossDiv": {

            "title": "S",

                       "GlossList": {

                "GlossEntry": {

                    "ID": "SGML",

                                      "SortAs": "SGML",

                                      "GlossTerm": "Standard Generalized Markup Language",

                                      "Acronym": "SGML",

                                      "Abbrev": "ISO 8879:1986",

                                      "GlossDef": {

                        "para": "A meta-markup language, used to create markup languages such as DocBook.",

                                              "GlossSeeAlso": ["GML", "XML"]

                    },

                                      "GlossSee": "markup"

                }

            }

        }

    }

}
```

Обрабатываем найденные json. Переносим все ключи, содержащие строки, на первый уровень. Массивы – пропускаем. Если ключи при этом пересекутся и потрется часть данных – не важно. Для объекта выше получим:
 
```json
{

      "title": "S", (или “example glossary”, не важно)

      "ID": "SGML",

      "SortAs": "SGML",

      "GlossTerm": "Standard Generalized Markup Language",

      "Acronym": "SGML",

      "Abbrev": "ISO 8879:1986",

      "para": "A meta-markup language, used to create markup languages such as DocBook.",

      "GlossSee": "markup"

}
```
 

Сохраняем найденные результаты в отдельные файлы в формате yaml.  Имя файла формируем из заголовка ссылки, найденной google, исключив из него недопустимые для имен файлов символы (oc linux). Расширение файла .yml
Например, в выдаче по запросу “json data example” есть страница “JSON Example”. (https://json.org/example.html)  Все результаты по этой странице сохраняем в файл “JSON Example.yml”

Структура файла:

```yaml
---

object_1:

    title: "S"

    ID: "SGML"

    SortAs: "SGML"

    GlossTerm: "Standard Generalized Markup Language"

    Acronym: "SGML"

    Abbrev: "ISO 8879:1986"

    para: "A meta-markup language, used to create markup languages such as DocBook."

    GlossSee: "markup"

object_2:

    тут следующий объект со страницы json.example (если есть)
```
