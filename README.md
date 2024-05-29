# Текстовая игра "Вордли"

Перед Вами аналог игры "Wordle" (https://wordle.belousov.one/)
В этой игре игроку предстоит угадать слово из пяти букв за шесть попыток.

## Как играть

Для начала игра предлагает выбрать уровень сложности:

>1. Нормально
>2. Сложно
>3. Кошмар
>4. Ужас


Введите число от 1 до 4 в зависимости от Вашей уверенности в собственной эрудиции.


Когда игра попросит слово, введите Ваш вариант. Может быть повезет и Вы угадаете слово с первого раза. Принимаются существительные из русского литературного языка в единственном числе длиной в 5 букв.


После каждой попытки игра дает подсказку, наводящую игрока к разгадке.

Под каждой буквой введенного слова отображается символ __"?"__, __"!"__ или __"_"__:
- __"?"__ - буква есть в загаданном слове, но не на этой позиции,
- __"!"__ - буква угадана и находится на своем месте,
- __"_"__ - буквы нет в этом слове.
- 
Кроме того дается еще дополнительная подсказка о том, какие буквы можно больше не использовать, так как за время игры проверено что этих букв в загаданном слове нет.

Пример:

![pywordle_ex](https://github.com/PyDevIll/pyWordle/assets/169006885/e477f0a9-0b2b-46a6-9f34-525676ef656f)

Слова загадываются из словаря русских существительных в единственном числе.

Буква Ё заменяется на Е.

Буквы в загаданном слове могут повторяться.



## Особенности:

### Уровни сложности

Не каждое слово в русском языке просто отгадать за разумное количество попыток. Некоторые слова вышли из обихода, или относятся к узкоспециализированной сфере, и до них не просто догадаться, играя в столь незамысловатую игру. А значения некоторых неизвестны самому разработчику.

Поэтому в игре предусмотрены уровни сложности:
 - __Нормально__ - слова из повседневного лексикона среднестатистического человека. Чаще всего состоят только из корня слова _("север", "пирог"...)_
 - __Сложно__ - слова реже используемые или вышедшие из повседневной речи, или образуют редкие формы в сочетании с приставками _("житие", "дожим", "зацеп"...)_
 - __Кошмар__ - могут встретиться слова из научной или профессиональной сферы _("митоз", "ареал", "иваси"...)_
 - __Ужас__ - только для самых эрудированных _("сивуч", "музга", "кнель"...)_

Количество попыток для каждого уровня сложности не меняется.

### Рейтинг слов

В игровом словаре более 50 тысяч слов. Слова нужной длины выбираются автоматически, но не все слова удобны для отгадывания.

Поэтому в игре есть дополнительный словарь, в котором словам присвоен рейтинг сложности от 0 до 5, где 0 - непригодное слово, а 5 - простое для отгадывания.
Этот словарь гораздо менее объемный, так как заполняется вручную.

Чтобы этот рейтинговый словарь пополнить, можно войти в __режим рейтинга__.

Запустить этот режим можно в момент выбора сложности введя число выходящее из диапазона 1..4. Далее выбираем рейтинг от 0 до 5, чтобы перепроверить каждое слово из рейтингового словаря на соответствие определенному рейтингу и исправить его на другой.
Либо ничего не вводить и нажать ENTER, чтобы оценить для рейтингового словаря новые слова из основного.

Начнут предлагаться слова в случайном порядке, в соответствии с Вашим выбором. Оцениваем их вводя число от 0 до 5 на свой субъективный взгляд. Процесс можно остановить не введя никакой оценки просто нажать ENTER, тогда игра вернется в основной режим.

Пример:

![pywordle_ex2](https://github.com/PyDevIll/pyWordle/assets/169006885/b203627b-f383-45ef-a4d0-1334664ffe52)



