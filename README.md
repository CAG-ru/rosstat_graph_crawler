# Rosstat Graph Crawler

## Что такое граф сайта?

Граф сайта описывает его уровневую структуру. Узлы (вершины) графа представляют собой веб-страницы; соединяющие их ребра — направленные связи, или гиперссылки, ведущие с одной страницы на другую. Как правило, граф организован в виде реляционной базы данных.

## Зачем нужен граф сайта Росстата?

Граф сайта Росстата обеспечивает охват всех веб-страниц, на которые можно попасть, навигируясь по сайту. Он освобождает пользователя от необходимости знать порядок переходов по ссылкам, чтобы попасть на тот или иной узел. Организация графа в виде реляционной базы позволяет использовать средства и методы баз данных для доступа к информации.

## Как организован граф сайта Росстата?

Граф сайта Росстата, [опубликованный](https://data-in.ru/data-catalog/datasets/152/) в рамках проекта ИНИД (Инфраструктура научно-исследовательских данных), организован в виде реляционной базы данных. В ней хранится следующая информация о 104711 собранных узлах:

- `id` — уникальный идентификатор узла (тип данных bigint),
- `rootname` — наименование корневого узла (varchar),
- `level` — уровень графа, т.е. удаленность веб-страницы от корневого узла, выраженная в количестве переходов по гиперссылкам (integer),
- `name` — заголовок веб-страницы (text),
- `path` — абсолютный url-адрес веб-страницы (text),
- `redirect` — url-адрес, с которого произошло перенаправление (text),
- `parent` — url-адрес родительского узла (text),
- `document` — HTML-код веб-страницы в узле (text),
- `file` — содержимое документа в узле в двоичном коде (bytea),
- `type` — формат документа в узле в виде MIME-типа (varchar),
- `done` — отметка о пересборе узла (bool),
- `hash` — хэш-функция содержимого узла (varchar),
- `href` — значение атрибута `<href>` гиперссылки, по которой осуществляется переход на узел (text),
- `timestamp` — время сбора узла графа (timestamp).

Наибольшую ценность представляет поле `file` графа — сохраняя из него двоичный код содержимого документа, фактически происходит "скачивание" файла с сайта Росстата на локальный компьютер без посещения сайта. Сравнивая поля `hash` узлов на идентичность, можно определить одинаковые документы в узлах графа.

## Зачем нужен Rosstat Graph Crawler

**Rosstat Graph Crawler** — это инструмент для ускоренного поиска и парсинга данных в узлах графа сайта Росстата. С его помощью возможно:
1) искать заданные слова в содержимом веб-страниц в узлах графа;
2) определять наименования таблиц в файлах с расширениями `.docx`, `.xlsx`, `.xls`, `.htm`, в том числе вложенных в архивы `.zip` и `.rar`;
3) среди спарсенных наименований таблиц находить те, которые ближе всего заданным ключевым словам по метрике косинусного расстояния.

Примеры работы инструмента приведены в jupyter notebook `how_to_crawl.ipynb`. В этом ноутбуке можно менять текст для поиска, идентификаторы узлов графа для определения названий таблиц и ключевые слова для расчета относительно них косинусного расстояния.

Парсеры **Rosstat Graph Crawler** закрывают 60% файлов, найденных в узлах графа (включая файлы, упакованные в архивы):

<p align="center">
<img src="https://i.imgur.com/BbbxO7G.jpg" width=600/>
</p>

P.S. [Pub crawl](https://ru.wikipedia.org/wiki/Барный_тур) — способ неплохо провести время, до утра посещая пабы и бары. **Rosstat Graph Crawler** посещает узлы графа сайта Росстата, и запуск инструмента на всем объеме графа также может занять целую ночь.

## Лицензия

MIT license

## Контакты разработчиков

[Центр перспективных управленческих решений](https://cpur.ru/)

Тарас Афанасенко, [t.afanasenko@cpur.ru]  
Юлия Хабибуллина, [y.khabibullina@cpur.ru]