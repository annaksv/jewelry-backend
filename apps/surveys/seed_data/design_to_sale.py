"""Сценарий «Реализовать готовый дизайн». Источник: НОВАЯ СТРУКТУРА 12 окт.docx, раздел «ОПРОСНИК».
Формулировки вопросов 2А–2Е и заголовок карточки на главной рабочие, их нужно подтвердить."""

SECTION = "ВАШ ДИЗАЙН"
ONE = "Выберите один вариант"
MANY = "Можно выбрать несколько вариантов"
GRID = "Для каждой строки выберите один статус"


def opt(code, label, *tags, exclusive=False):
    return {"code": code, "label": label, "tags": list(tags), "is_exclusive": exclusive}


def question(code, step, text, kind, options, hint, show_if=None, required=True):
    return {
        "code": code,
        "step_label": step,
        "section_label": SECTION,
        "text": text,
        "help_text": hint,
        "kind": kind,
        "is_required": required,
        "show_if": show_if or {},
        "options": options,
    }


def when(option):
    """Условие показа: на вопрос 1 выбран такой вариант."""
    return {"option": option}


# Строки таблицы 2Е. Порядок важен: основным этапом станет первая строка не со статусом «Готово».
GRID_ROWS = [
    ("s1", "Доказательства авторства и даты создания дизайна сохранены"),
    ("s2", "Решение о патенте и публикации принято"),
    ("s3", "Форма работы и регистрация бизнеса определены"),
    ("s4", "Материалы и обязательные требования определены"),
    ("s5", "Задание изготовителю подготовлено"),
    ("s6", "Изготовитель выбран и проверен"),
    ("s7", "Договор и порядок передачи материалов согласованы"),
    ("s8", "Образец изготовлен и утвержден"),
    ("s9", "Партия изготовлена и принята"),
]

SCENARIO = {
    "slug": "design-to-sale",
    "title": "У меня есть дизайн украшения",
    "description": (
        "Вы самостоятельно создали дизайн украшения. Теперь сохраните доказательства авторства, "
        "определите способ защиты, подготовьте заказ фабрике и пройдите этапы изготовления "
        "и подготовки к продаже."
    ),
    "card_title": "Готовый дизайн",
    "card_subtitle": "Хочу реализовать свой дизайн украшения",
    "order": 1,
    "is_published": True,
    "questions": [
        question("q1", "1", "Что вы хотите сделать сейчас?", "single", [
            opt("protect", "Защитить права на созданный дизайн", "goal:protect"),
            opt("prepare", "Подготовиться к заказу изделия", "goal:prepare"),
            opt("maker", "Найти изготовителя или оформить работу с ним", "goal:maker"),
            opt("produce", "Изготовить образец или заказать партию", "goal:produce"),
            opt("sell", "Подготовить изделие к продаже", "goal:sell"),
            opt("unknown", "Не знаю, с чего начать", "goal:unknown"),
        ], ONE),

        # --- 2. Уточнение задачи: показывается ровно один блок 2А–2Е ---
        question("q2_protect", "2А", "Уточните задачу", "single", [
            opt("evidence", "Нужно зафиксировать авторство и дату создания дизайна", "ask:evidence"),
            opt("patent", "Доказательства авторства уже собраны, нужно решить вопрос с патентом и публикацией",
                "ask:patent"),
            opt("unsure", "Не уверен, какие действия нужны сначала", "ask:unsure"),
        ], ONE, show_if=when("q1.protect")),

        question("q2_prepare", "2Б", "Уточните задачу", "single", [
            opt("business", "Проверить форму работы и готовность бизнеса", "ask:business"),
            opt("materials", "Разобраться с материалами и обязательными требованиями", "ask:materials"),
            opt("brief", "Составить задание для изготовителя", "ask:brief"),
        ], ONE, show_if=when("q1.prepare")),

        question("q2_maker", "2В", "Уточните задачу", "single", [
            opt("find", "Найти фабрику или проверить уже выбранного изготовителя", "ask:find_maker"),
            opt("contract", "Подготовить договор и определить порядок передачи материалов", "ask:contract"),
        ], ONE, show_if=when("q1.maker")),

        question("q2_produce", "2Г", "Уточните задачу", "single", [
            opt("sample", "Изготовить и проверить первый образец", "ask:sample"),
            opt("batch", "Заказать партию и провести приемку", "ask:batch"),
        ], ONE, show_if=when("q1.produce")),

        question("q2_sell", "2Д", "Уточните задачу", "single", [
            opt("docs", "Подготовить документы, маркировку, карточку товара и канал продаж", "ask:sale_docs"),
            opt("check", "Проверить, все ли выполнено перед началом продаж", "ask:sale_check"),
        ], ONE, show_if=when("q1.sell")),

        question("q2_unknown", "2Е", "Отметьте, что из этого уже сделано", "status_grid", [
            opt(code, label, f"stage:{index}") for index, (code, label) in enumerate(GRID_ROWS, start=1)
        ], GRID, show_if=when("q1.unknown")),

        # --- 3–7. Общие вопросы ---
        question("q3", "3", "Какие материалы предусмотрены в дизайне?", "single", [
            opt("metal", "Драгоценный металл без драгоценных камней", "material:metal"),
            opt("stone", "Драгоценные камни без драгоценного металла", "material:stone"),
            opt("metal_stone", "Драгоценный металл и драгоценные камни", "material:metal", "material:stone"),
            opt("bijou", "Недрагоценные материалы и бижутерия", "material:bijou"),
            opt("undefined", "Состав материалов еще не определен", "material:undefined"),
        ], ONE),

        question("q4", "4", "Выбран ли изготовитель?", "single", [
            opt("ru_chosen", "Изготовитель в России уже выбран", "mfr:ru_chosen"),
            opt("foreign", "Изготовитель за рубежом", "mfr:foreign"),
            opt("compare", "Есть несколько вариантов, нужно сравнить и проверить", "mfr:compare"),
            opt("none", "Изготовитель еще не выбран", "mfr:none"),
        ], ONE),

        question("q5", "5", "Что вы собираетесь заказывать?", "single", [
            opt("sample", "Один пробный образец", "order:sample"),
            opt("batch", "Небольшую партию", "order:batch"),
            opt("serial", "Серийное производство", "order:serial"),
        ], ONE),

        question("q6", "6", "От чьего имени вы будете заказывать и продавать?", "single", [
            opt("ip", "От своего имени как индивидуальный предприниматель", "seller:ip"),
            opt("org", "От имени организации", "seller:org"),
            opt("setup", "Нужно выбрать и оформить форму работы", "seller:setup"),
            opt("undecided", "Еще не определился", "seller:undecided"),
        ], ONE),

        question("q7", "7", "Где вы планируете продавать украшение?", "multi", [
            opt("online", "На своем сайте или через социальные сети", "sale:online"),
            opt("marketplace", "На маркетплейсе", "sale:marketplace"),
            opt("store", "В магазине или шоуруме", "sale:store"),
            opt("wholesale", "Оптом другим компаниям", "sale:wholesale"),
            opt("none", "Способ продажи еще не выбран", "sale:none", exclusive=True),
        ], MANY, required=False),
    ],
}
