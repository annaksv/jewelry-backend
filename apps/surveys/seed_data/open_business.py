SECTION = "ВАШ БИЗНЕС"
ONE = "Выберите один вариант"
MANY = "Можно выбрать несколько вариантов"


def opt(code, label, *tags, exclusive=False):
    return {"code": code, "label": label, "tags": list(tags), "is_exclusive": exclusive}


def question(code, step, text, kind, options, hint, show_if=None):
    return {
        "code": code,
        "step_label": step,
        "section_label": SECTION,
        "text": text,
        "help_text": hint,
        "kind": kind,
        "is_required": True,
        "show_if": show_if or {},
        "options": options,
    }


SCENARIO = {
    "slug": "open-business",
    "title": "Открыть ювелирный бизнес",
    "description": (
        "Ответьте на несколько вопросов и получите пошаговый маршрут: "
        "от регистрации бизнеса до первой законной продажи изделия"
    ),
    "card_title": "Выход на рынок",
    "card_subtitle": "Хочу открыть ювелирный бизнес",
    "order": 2,
    "is_published": True,
    "questions": [
        question("q1", "1", "У вас уже есть ИП или юридическое лицо?", "single", [
            opt("ip", "Да, есть ИП", "org:ip"),
            opt("llc", "Да, есть юридическое лицо", "org:llc"),
            opt("none", "Нет", "org:none"),
        ], ONE),

        question("q2", "2", "Чем вы планируете заниматься?", "single", [
            opt("produce", "Производить ювелирные изделия", "activity:produce"),
            opt("sell", "Продавать готовые ювелирные изделия", "activity:sell"),
            opt("produce_sell", "Производить и продавать", "activity:produce", "activity:sell"),
            opt("services", "Оказывать ювелирные услуги", "activity:services"),
        ], ONE),

        question("q3", "3", "Кто будет заниматься изготовлением изделий?", "single", [
            opt("self", "Я / мое ЮЛ", "mfr:self"),
            opt("contractor_ru", "Сторонний производитель в России", "mfr:contractor_ru"),
            opt("foreign", "Производитель за рубежом", "mfr:foreign"),
            opt("mixed", "И сами, и через подрядчиков", "mfr:mixed"),
        ], ONE, show_if={"any": [{"option": "q2.produce"}, {"option": "q2.produce_sell"}]}),

        question("q4", "4", "С какими изделиями вы будете работать?", "multi", [
            opt("metal", "Из драгоценных металлов", "material:metal"),
            opt("stone", "С драгоценными камнями", "material:stone"),
            opt("metal_stone", "И с драгоценными металлами, и с драгоценными камнями", "material:metal", "material:stone", exclusive=True),
            opt("bijou", "Только бижутерия и недрагоценные материалы", "material:bijou", exclusive=True),
        ], MANY, show_if={"not": {"option": "q2.services"}}),

        question("q5", "5", "Откуда будут поступать изделия или материалы?", "single", [
            opt("ru", "Из России", "source:ru"),
            opt("abroad", "Из-за границы", "source:abroad"),
            opt("both", "И из России, и из-за границы", "source:both"),
            opt("undecided", "Пока не решил", "source:undecided"),
        ], ONE, show_if={"not": {"option": "q2.services"}}),

        question("q6", "6", "Как вы будете продавать изделия?", "multi", [
            opt("store", "В магазине или шоуруме", "sale:store"),
            opt("online", "Через сайт или социальные сети", "sale:online"),
            opt("marketplace", "Через маркетплейсы", "sale:marketplace"),
            opt("wholesale", "Оптом другим компаниям", "sale:wholesale"),
        ], MANY, show_if={"any": [{"option": "q2.sell"}, {"option": "q2.produce_sell"},
                                  {"option": "q2.services"}]}),

        question("q7", "7", "Будете ли вы работать с изделиями клиентов или бывшими в употреблении изделиями?",
                 "single", [
            opt("new_only", "Нет, только с новыми изделиями", "items:new_only"),
            opt("client", "Да, с изделиями клиентов", "items:client"),
            opt("used", "Да, с бывшими в употреблении изделиями", "items:used"),
            opt("client_used", "И с теми, и с другими", "items:client", "items:used"),
        ], ONE),

        question("q7_1", "7.1", "Что вы будете делать с изделиями клиента?", "single", [
            opt("repair", "Ремонтировать", "client_work:repair"),
            opt("rework", "Переделывать", "client_work:rework"),
            opt("new_from_client_material", "Изготавливать новое изделие из материала клиента",
                "client_work:new_from_material"),
            opt("several", "Несколько вариантов", "client_work:several"),
        ], ONE, show_if={"all": [{"answered": "q7"}, {"not": {"option": "q7.new_only"}}]}),

        question("q8", "8", "Будете ли вы создавать собственный бренд или собственный дизайн?", "single", [
            opt("own", "Да", "brand:own"),
            opt("others", "Нет, буду работать с готовыми изделиями других брендов", "brand:others"),
            opt("both", "И то, и другое", "brand:own", "brand:others"),
        ], ONE),

        question("q9", "9", "Будут ли у вас сотрудники?", "single", [
            opt("yes", "Да", "staff:yes"),
            opt("no", "Нет", "staff:no"),
            opt("unknown", "Пока не знаю", "staff:unknown"),
        ], ONE),

        question("q10", "10", "Есть ли у вас помещение для работы?", "single", [
            opt("yes", "Да", "premises:yes"),
            opt("no", "Нет, но планируется", "premises:no"),
            opt("none", "Отдельное помещение не планируется", "premises:none"),
        ], ONE),
    ],
}
