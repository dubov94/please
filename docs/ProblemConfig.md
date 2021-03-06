# Конфигурируем параметры задачи #
Все изменения происходят в файле default.package, который находится в папке с задачей.
```
~/cubes$ please set main solution solutions/solution.py
cubes(INFO) [15:59:42]: Main solution solutions/solution.py was added successfully
```

Устанавливает основное решение.

_**Примечание:**_ желательно главным решением устанавливать самое медленное из верных, потому что автоконфигурирование TL по команде **`please compute [integer] TL`** происходит именно по главному решению.

```
~/cubes$ please clear tags
~/cubes$ please show tags

~/cubes$ please add tags множества сортировка
~/cubes$ please show tags
множества; сортировка
```
Управление тегами задачи, которые в перспективе помогут в поиске задач на одинаковые темы из базы.
```
~/cubes$ please set problem name Кубики
```
Устанавливает имя задачи. Имя задачи (поле name в default.package), имя папки с задачей и поле shortname в default.package могу различаться. Поле shortname при создании задачи идентично имени папки.

Команды **please set checker PATH\_TO\_CHECKER** и **please set validator PATH\_TO\_VALIDATOR** устанавливают пути до чекера и валидатора соответственно.

Команда **please set standard checker** выведет список встроенных стандартных чекеров. Командой **please set standard checker CHECKER\_NAME** можно установить один из них. [Список стандартных чекеров с описаниями](StandardCheckers.md).

Поля input и output задают соответственно потоки ввода и вывода по умолчанию для решений. Могут быть именем файла или stdin и stdout соответственно.

Поля time\_limit и memory\_limit задают лимит по времени и по памяти соответственно для всех решений.

Поля statement, description и analysis задают пути до условий, описания и разбора соответственно. Заметим, что команда **please generate statement** генерирует pdf из tex-файла, указанного в поле statement.

**Все чекеры, валидаторы и т.п. должны лежать в папке с задаче. В случае нарушения этого ограничения please сообщит об ошибке**

# Поля well\_done\_test и well\_done\_answer #
Задают ключевые слова для проверки соответственно ручных тестов и генерируемых ответов. Доступны следующие опции:
  * endswith\_EOLN - проверяет на наличие символа перевода строки в конце
  * no\_symbols\_less\_32 - проверяет на отсутствие символов с кодами меньшими 32
  * no\_left\_space - проверяет на отсутствие пробелов в началах строк
  * no\_right\_space - проверяет на отсутствие пробелов в концах строк
  * no\_left\_right\_space - проверяет на отсутствие пробелов в началах и концах строк
  * no\_double\_space - проверяет на отсутствие двух подряд идущих пробелов
  * no\_top\_emptyline - проверяет на отсутствие пустых строк в начале
  * no\_bottom\_emptyline - проверяет на отсутствие пустых строк в конце
  * no\_top\_bottom\_emptyline - проверяет на отсутствие пустых строк в начале и конце
  * not\_empty - проверяет на непустоту
  * no\_emptyline - проверяет на отсутствие пустых строк

# Добавить решение #
Чтобы утилита please могла использовать различные (в том числе и неправильные) решения в автоматическом режиме, их необходимо добавить. Для этого выполним команду **`please add solution PATH_TO_SOLUTION [input PATH_OR_STDIN] [output PATH_OR_STDOUT] [possible POSS_VERDICTS_LIST] [expected EXP_VERDICTS_LIST]`**
  * PATH\_OR\_STDIN - имя входного файла для данного решения или stdin
  * PATH\_OR\_STDOUT - имя выходного файла для данного решения или stdout
  * POSS\_VERDICTS\_LIST - список допустимых вердиктов для данного решения, по умолчанию считается пустым
  * EXP\_VERDICTS\_LIST - список обязательных вердиктов для данного решения, по умолчанию считается равным одному ОК

Свойства:
  * Аргументы после PATH можно менять местами
  * Аргументы после PATH могу отсутствовать
  * **POSS\_VERDICTS\_LIST может не содержать EXP\_VERDICTS\_LIST!**
  * По умолчанию input равен глобальному input, аналогично output
  * please умеет самостоятельно определять и приводить пути к относительным с точки зрения папки с задачи
  * **Нельзя** добавлять решения, не лежащие в папке с задачей


Как работает система обязательных и возможных вердиктов:
  * Если на каком-то тесте вердикт отсутствует в списке ожидаемых или возможных, считается, что данное решение на данном тесте **не удовлетворяет** заданным параметрам, на report.html внизу таблицы для данного решения данный вердикт будет указан в met not expected
  * Если после выполнения всех тестов существует вердикт, прописанный в списке обязательных, но при этом данное решение его не получило ни на одном из тестов, считается, что данное решение на данных тестах **не удовлетворяет** заданным параметрам, на report.html внизу таблицы для данного решения данный вердикт будет указан в expected not met

Список возможных вердиктов:
  * OK
  * WA - wrong answer
  * RE - run-time error
  * TL - time limit
  * ML - memory limit
  * PE - presentation error

Примеры:
  * please add solution solutions/solution\_slow.cpp input stdin output test.out expected OK TL

  * please add solution solutions/solution.py

  * please add solution solutions/solution\_wrong.cpp expected OK possible WA

# Изменение параметров решения #
**`please change prop[erties] PATH [ARGS VALUES...]`**

Работает аналогично **please add solution...** с тем отличием, что при отсутствии в конфиге решения с таким путём please сообщит об ошибке

**please change prop sol.py input stdin**

# Удаление параметров решения #
**`please del[ete] prop[erties] PATH [PROPERTIES]`**

Удаляет выбранные свойства.

**Нельзя удалить свойство source, please сообщит об ошибке**

**please del properties solutions/solution.cpp input output**

# Удаление решения #
**`please del[ete] solution PATH`**

Удаляет выбранное решение

**please delete solution sol\_slow.cpp**

# Вид решения в конфиге #
```
solution = {
    source = solutions/sol.cpp #обязательно; путь к решению
    expected = WA #опционально; какие вердикты программа должна получать хотя бы на одном тесте
    possible = OK, WA, RE #опционально; какие вердикты программа может получать на тестах
    input = input.txt #опционально; входной файл, приоритетнее указанного в default.package для всей задачи
    output = stdout #опционально; выходной файл, приоритетнее указанного в default.package для всей задачи
}
```