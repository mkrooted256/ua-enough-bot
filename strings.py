
from typing import List


class Question:
    def __init__(self, text: str, answers: List[str] = [], ans_tokens: List[int] = []):
        self.text = text
        self.answers = answers
        self.tokens = ans_tokens

ANS_NONE, ANS_TOO_BUSY, ANS_TOO_LARGE_DONATION, ANS_ABROAD, ANS_SAD, ANS_MUST_NOT_HAPPY = range(6)


welcome_text = \
"""Вітаю! Я бот, що може порекомендувати, як допомагати країні найпростішими діями. Навіть якщо немає часу, сил та/або настрою.
Але спочатку, будь ласка, пройдіть коротке опитування.
Почнімо?"""

questions: List[Question] = [
    Question(
        "Наскільки багато часу ви приділяєте волонтерству чи роботі, що безпосередньо наближають перемогу?",
        [
            "Небагато, як виходить",
            "До чотирьох годин на день",
            "Займаюсь волонтерством 8 годин на день без вихідних",
            "Цілодобово. Вдень плету маскувальні сітки, вночі розвожу бронежилети по гарячим точкам.",
        ], [0, ANS_TOO_BUSY, ANS_TOO_BUSY, ANS_TOO_BUSY]),

    Question(
        "Скільки ви в середьому переказуєте на рахунки Армії та благодійних організацій щотижнево?",
        [
            "Скільки комфортно. Так, щоб залишались гроші на життя",
            "Значну частину зарплати",
            "Всю зарплату + самостійно організовую благодійні збори",
            "Зазвичай вистачає на дрон, партію аптечок та три старлінки",
        ], [0, ANS_TOO_LARGE_DONATION, ANS_TOO_LARGE_DONATION, ANS_TOO_LARGE_DONATION]),

    Question(
        "Який варіант краще за все описує, як ви підтримуєте українську економіку?",
        [
            "Тривожуся за неї з-за кордону",
            "Купую продукти, відвідую кафе, користуюсь громадським транспортом. Сплачую зв'язок, інтернет, комунальні послуги та\або податки",
            "Займаюся суспільно корисними справами: вхожу до складу наглядових рад, маю свою громадську організацію, ходжу на суботники тощо",
            "На початку військового наступу став місцевим чиновником та зараз створюю економічний рай в своєму місті",
            "Відкриваю новий бізнес кожні 2 тижні, а прибуток звітую десятикратно - щоб Україна отримувала більше податків",
        ], [ANS_ABROAD, 0, 0, 0, 0]),
        
    Question(
        "Як ви себе почуваєте? Чи буває у вас таке, що ви радієте, хоча й в країні війна?",
        [
            "Іноді буваю в гарному настрої",
            "Так, я щасливий! Президент хіба не наказав жити далі?",
            "З 24 лютого почуваю себе не дуже добре",
            "Ви що, яка радість. Не можна радіти поки таке відбувається.",
        ], [0, 0, ANS_SAD, ANS_MUST_NOT_HAPPY]),
]

default_ans = [
    "Ви молодець! \nВи знаходитесь саме там і робите саме те, що необхідно для нашої спільної Перемоги! Бережіть себе. Ви нам потрібні."
]

special_ans = dict()
special_ans[ANS_TOO_BUSY]= \
"""Дуже круто, що ви допомагаєте наближувати Перемогу! Тільки турбуйтеся, будь ласка, і про себе. Вам же ще її (Перемогу) святкувати!
Вас, може, нічого не переконає взяти собі вихідний, але пам'ятайте, що 
будь-яка ваша допомога ще знадобиться пізніше, для відновлення країни та підтримки близьких. 
Отож зробіть щось зараз для вашої особистої радості, щоб потім не довелося рятувати вас :)"""

# TODO: рекомендація коли людина багато витрачає на благодійність
special_ans[ANS_TOO_LARGE_DONATION]= \
"""Розмір ваших пожертв вражає! Сподіваємося, що ви іноді купуєте щось для себе. Час пригадати, коли в останній раз ви придбали щось для душі та оптимізму✨"""

# TODO: рекомендація коли людина за кордоном
special_ans[ANS_ABROAD]= \
"""Ви молодець, що змогли виїхати! А в гарячих точках ще й чим менше цивільних тим легше працювати нашим військовим."""

# TODO: рекомендація коли людина відповіла, що сумує з початку війни
special_ans[ANS_SAD]= \
"""Зараз такі складні часи, але ви так круто тримаєтесь (серйозно). Пам’ятаєте, що коли складно, не обов’язково бути з цим на самоті? Можна звернутись за консультацією чи просто до розмови із психологом. Тим більше, що зараз багато волонтерів, що допомагають безкоштовно. 
Можна почати, наприклад, <a href="https://novy.tv/ua/news/2022/04/15/bezkoshtovna-psyhologichna-dopomoga-dlya-ukrayincziv-spysok-resursiv-ta-nomery-telefoniv">з цього списку</a>.

Вороги намагаються вкрасти у нас не просто суверенність та відчуття безпеки, а й жагу до життя, до кращого майбутнього, до задоволення. Під час війни важливо не просто вижити, а зберегтися. І наші військові дуже просять всіх, хто в тилу - живіть, радійте, ходіть до перукарень і кафе - Живіть. Бо саме за це йде боротьба."""

# TODO: рекомендація коли людина відповіла, що не дозволяє собі радіти
special_ans[ANS_MUST_NOT_HAPPY]= \
"""Вороги намагаються вкрасти у нас не просто суверенність та відчуття безпеки, а й жагу до життя, до кращого майбутнього, до задоволення. Під час війни важливо не просто вижити, а зберегтися. І наші військові дуже просять всіх, хто в тилу - живіть, радійте, ходіть до перукарень і кафе - Живіть. Бо саме за це йде боротьба.

Зараз такі складні часи, але ви так круто тримаєтесь (серйозно). Пам’ятаєте, що коли складно, не обов’язково бути з цим на самоті? Можна звернутись за консультацією чи просто до розмови із психологом. Тим більше, що зараз багато волонтерів, що допомагають безкоштовно. 
Можна почати, наприклад, <a href="https://novy.tv/ua/news/2022/04/15/bezkoshtovna-psyhologichna-dopomoga-dlya-ukrayincziv-spysok-resursiv-ta-nomery-telefoniv">з цього списку</a>"""