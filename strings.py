
from typing import List


class Question:
    def __init__(self, text: str, answers: List[str] = [], ans_tokens: List[int] = []):
        self.question = text
        self.answers = answers
        self.tokens = ans_tokens

ANS_NONE, ANS_TOO_BUSY, ANS_TOO_LARGE_DONATION, ANS_ABROAD, ANS_SAD, ANS_MUST_NOT_HAPPY = range(6)

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
            "Молюся за неї з-за кордону",
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
    "Ви молодець! Наша головна задача зараз - вижити та готуватися до щасливого життя після війни у відбудованій Україні."
]

special_ans = dict(
    ANS_TOO_BUSY= "Дуже круто, що ви допомагаєте! Тільки, будь ласка, не забувайте про себе та про свої потреби. " + 
        "Вас, може, нічого не переконає взяти собі вихідний, але пам'ятайте, що ви - частина громадян країни, за __щасливе__ майбутнє яких зараз іде боротьба. "+
        "Отож, має сенс до нього дожити.", 
    ANS_TOO_LARGE_DONATION="Розмір ваших пожертв вражає! Сподіваємося, що ви хоч іноді купуєте щось для себе, для душі. ", 
    ANS_ABROAD="", 
    ANS_SAD="", 
    ANS_MUST_NOT_HAPPY=""
)