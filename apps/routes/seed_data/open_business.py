"""Блоки маршрута «Открыть ювелирный бизнес».

Файл сгенерирован из BACKEND_RESULTS.json (22.10.2026, правки юристов). Тексты, заголовки и ссылки
соответствуют макету frontend. Ссылка: label (текст), kind (article / tool / catalog / scenario),
target (готовый путь на сайте), condition (необязательно: показывать ссылку только при таких ответах).
"""

BLOCKS = [
    {
        "code": "biz.q1.ip",
        "step": "q1",
        "title": "Проверьте виды деятельности ИП",
        "body": "Необходимо проверить, позволяют ли зарегистрированные виды деятельности заниматься выбранной вами моделью ювелирного бизнеса. При необходимости добавьте подходящие ОКВЭД и проверьте, требуется ли изменить другие регистрационные сведения.",
        "condition": {
            "option": "q1.ip"
        },
        "links": [
            {
                "label": "Проверить виды деятельности",
                "kind": "tool",
                "target": "/activities"
            },
            {
                "label": "Как открыть ювелирный бизнес после регистрации ИП или ООО",
                "kind": "article",
                "target": "/knowledge/after-registration?from=business"
            }
        ]
    },
    {
        "code": "biz.q1.llc",
        "step": "q1",
        "title": "Проверьте виды деятельности компании",
        "body": "Необходимо проверить, соответствуют ли виды деятельности компании тому, чем вы планируете заниматься в ювелирной сфере. Если необходимых ОКВЭД нет, их следует добавить до начала соответствующей деятельности.",
        "condition": {
            "option": "q1.llc"
        },
        "links": [
            {
                "label": "Проверить виды деятельности",
                "kind": "tool",
                "target": "/activities"
            },
            {
                "label": "Как открыть ювелирный бизнес после регистрации ИП или ООО",
                "kind": "article",
                "target": "/knowledge/after-registration?from=business"
            }
        ]
    },
    {
        "code": "biz.q1.none",
        "step": "q1",
        "title": "Зарегистрируйте бизнес",
        "body": "Сначала необходимо зарегистрировать бизнес. Выберите подходящую форму - ИП или юридическое лицо, определите виды деятельности и налоговый режим, после чего пройдите государственную регистрацию.",
        "condition": {
            "option": "q1.none"
        },
        "links": [
            {
                "label": "Как зарегистрировать ИП или ООО для ювелирного бизнеса",
                "kind": "article",
                "target": "/knowledge/business-registration?from=business"
            }
        ]
    },
    {
        "code": "biz.q2.produce",
        "step": "q2",
        "title": "Организуйте ювелирное производство",
        "body": "Вам необходимо организовать производство: определить место работы, порядок приобретения и учета материалов, оформить необходимые регистрации и обеспечить соблюдение требований к изготовлению и подготовке изделий к дальнейшему обороту.",
        "condition": {
            "option": "q2.produce"
        },
        "links": [
            {
                "label": "Как подготовить бизнес к производству и продаже украшения?",
                "kind": "article",
                "target": "/knowledge/production-business?from=business"
            }
        ]
    },
    {
        "code": "biz.q2.sell",
        "step": "q2",
        "title": "Организуйте продажу ювелирных изделий",
        "body": "Вам необходимо организовать законное приобретение и дальнейшую продажу изделий: найти поставщиков, получать необходимые документы на товар и соблюдать требования к учету, маркировке и информированию покупателей.",
        "condition": {
            "option": "q2.sell"
        },
        "links": [
            {
                "label": "Как открыть ювелирный бизнес после регистрации ИП или ООО",
                "kind": "article",
                "target": "/knowledge/after-registration?from=business"
            }
        ]
    },
    {
        "code": "biz.q2.produce_sell",
        "step": "q2",
        "title": "Организуйте производство и продажи",
        "body": "Вам потребуется одновременно организовать производство и продажи: обеспечить законное получение материалов, изготовление и учет изделий, а затем подготовить их к розничной или оптовой реализации.",
        "condition": {
            "option": "q2.produce_sell"
        },
        "links": [
            {
                "label": "Как подготовить бизнес к производству и продаже украшения?",
                "kind": "article",
                "target": "/knowledge/production-business?from=business"
            },
            {
                "label": "Как открыть ювелирный бизнес после регистрации ИП или ООО",
                "kind": "article",
                "target": "/knowledge/after-registration?from=business"
            }
        ]
    },
    {
        "code": "biz.q2.services",
        "step": "q2",
        "title": "Организуйте оказание ювелирных услуг",
        "body": "Необходимо определить перечень услуг и порядок приема изделий клиентов. Необходимо правильно оформлять передачу изделий и материалов, учитывать их движение и устанавливать ответственность за сохранность имущества клиента.",
        "condition": {
            "option": "q2.services"
        },
        "links": [
            {
                "label": "Как открыть ювелирную мастерскую",
                "kind": "article",
                "target": "/knowledge/jewelry-workshop?from=business"
            },
            {
                "label": "Как открыть ювелирный бизнес после регистрации ИП или ООО",
                "kind": "article",
                "target": "/knowledge/after-registration?from=business"
            }
        ]
    },
    {
        "code": "biz.q3.self",
        "step": "q3",
        "title": "Оформите собственное производство",
        "body": "Вам нужно оформить себя именно как изготовителя: определить, где будет вестись изготовление, кто отвечает за учет материалов и готовых изделий, а также какие действия должен выполнять сам изготовитель до передачи изделия в продажу.",
        "condition": {
            "option": "q3.self"
        },
        "links": [
            {
                "label": "Что нужно оформить производителю ювелирных изделий",
                "kind": "article",
                "target": "/knowledge/manufacturer-obligations?from=business"
            }
        ]
    },
    {
        "code": "biz.q3.contractor_ru",
        "step": "q3",
        "title": "Проверьте российского производителя",
        "body": "До начала работы проверьте изготовителя и письменно распределите обязанности: кто покупает и передает материалы, кто отвечает за их учет, кто оформляет готовое изделие, кто устраняет брак и кому принадлежат права на созданный дизайн.",
        "condition": {
            "option": "q3.contractor_ru"
        },
        "links": [
            {
                "label": "Что проверить перед работой с ювелирным производителем",
                "kind": "article",
                "target": "/knowledge/manufacturer-check?from=business"
            }
        ]
    },
    {
        "code": "biz.q3.foreign",
        "step": "q3",
        "title": "Оформите работу с иностранным производителем",
        "body": "Сначала определите, кто будет выступать российским импортером и отвечать за ввоз готовых изделий. В договоре с иностранным производителем зафиксируйте характеристики товара и комплект документов, необходимых для последующего ввоза и продажи в России.",
        "condition": {
            "option": "q3.foreign"
        },
        "links": [
            {
                "label": "Что учесть при заказе украшений у иностранного производителя",
                "kind": "article",
                "target": "/knowledge/foreign-manufacturer?from=business"
            },
            {
                "label": "Как импортировать ювелирные товары",
                "kind": "article",
                "target": "/knowledge/jewelry-import?from=business"
            }
        ]
    },
    {
        "code": "biz.q3.mixed",
        "step": "q3",
        "title": "Разделите собственное и контрактное производство",
        "body": "Разделите изделия на собственное и контрактное производство и заранее определите, кто отвечает за каждый этап по каждой группе товаров: материалы, изготовление, учет, документы, брак и подготовку изделия к продаже.",
        "condition": {
            "option": "q3.mixed"
        },
        "links": [
            {
                "label": "Как организовать смешанную модель производства",
                "kind": "article",
                "target": "/knowledge/mixed-production?from=business"
            },
            {
                "label": "Что проверить перед работой с ювелирным производителем",
                "kind": "article",
                "target": "/knowledge/manufacturer-check?from=business"
            }
        ]
    },
    {
        "code": "biz.q4.metal",
        "step": "q4",
        "title": "Проверьте требования к драгоценным металлам",
        "body": "Для работы с изделиями из драгоценных металлов необходимо проверить требования специального учета, работы в ГИИС ДМДК, учета изделий, а также правил клеймения и маркировки.",
        "condition": {
            "all": [
                {
                    "tag": "material:metal"
                },
                {
                    "not": {
                        "tag": "material:stone"
                    }
                }
            ]
        },
        "links": [
            {
                "label": "Требования для работы с драгоценными металлами",
                "kind": "article",
                "target": "/knowledge/precious-metals?from=business"
            },
            {
                "label": "Что такое специальный учет и ГИИС ДМДК",
                "kind": "article",
                "target": "/knowledge/special-account?from=business"
            },
            {
                "label": "Открыть каталог поставщиков",
                "kind": "catalog",
                "target": "/suppliers?from=business&category=metals",
                "condition": {
                    "all": [
                        {
                            "tag": "material:metal"
                        },
                        {
                            "not": {
                                "tag": "material:stone"
                            }
                        }
                    ]
                }
            }
        ]
    },
    {
        "code": "biz.q4.stone",
        "step": "q4",
        "title": "Проверьте требования к драгоценным камням",
        "body": "Проверьте требования к обороту драгоценных камней: специальному учету, работе в ГИИС ДМДК, документам о происхождении и характеристиках камней и отражению операций с ними.",
        "condition": {
            "all": [
                {
                    "tag": "material:stone"
                },
                {
                    "not": {
                        "tag": "material:metal"
                    }
                }
            ]
        },
        "links": [
            {
                "label": "Работа с драгоценными камнями",
                "kind": "article",
                "target": "/knowledge/precious-stones?from=business"
            },
            {
                "label": "Что такое специальный учет и ГИИС ДМДК",
                "kind": "article",
                "target": "/knowledge/special-account?from=business"
            },
            {
                "label": "Открыть каталог поставщиков",
                "kind": "catalog",
                "target": "/suppliers?from=business&category=stones",
                "condition": {
                    "all": [
                        {
                            "tag": "material:stone"
                        },
                        {
                            "not": {
                                "tag": "material:metal"
                            }
                        }
                    ]
                }
            }
        ]
    },
    {
        "code": "biz.q4.metal_stone",
        "step": "q4",
        "title": "Проверьте специальные требования к ДМДК",
        "body": "Вам потребуется соблюдать требования, относящиеся и к драгоценным металлам, и к драгоценным камням: специальный учет, ГИИС ДМДК, документы на материалы, учет изделий, клеймение и маркировку.",
        "condition": {
            "all": [
                {
                    "tag": "material:metal"
                },
                {
                    "tag": "material:stone"
                }
            ]
        },
        "links": [
            {
                "label": "Требования для работы с драгоценными металлами",
                "kind": "article",
                "target": "/knowledge/precious-metals?from=business"
            },
            {
                "label": "Работа с драгоценными камнями",
                "kind": "article",
                "target": "/knowledge/precious-stones?from=business"
            },
            {
                "label": "Что такое специальный учет и ГИИС ДМДК",
                "kind": "article",
                "target": "/knowledge/special-account?from=business"
            },
            {
                "label": "Открыть каталог поставщиков",
                "kind": "catalog",
                "target": "/suppliers?from=business",
                "condition": {
                    "all": [
                        {
                            "tag": "material:metal"
                        },
                        {
                            "tag": "material:stone"
                        }
                    ]
                }
            }
        ]
    },
    {
        "code": "biz.q4.bijou",
        "step": "q4",
        "title": "Проверьте общие требования к продукции",
        "body": "Специальные требования, установленные для оборота драгоценных металлов и драгоценных камней, к такой продукции не применяются. Вам следует ориентироваться на общие требования к производству и продаже товаров: иметь документы на приобретаемую продукцию и материалы, правильно доводить информацию о товаре до покупателя и соблюдать требования выбранного способа продажи.",
        "condition": {
            "option": "q4.bijou"
        },
        "links": []
    },
    {
        "code": "biz.q5.ru",
        "step": "q5",
        "title": "Подготовьте закупки в России",
        "body": "Выберите надежного поставщика до заключения договора. При каждом приобретении получайте и сохраняйте документы, подтверждающие происхождение, характеристики и передачу материалов или изделий.",
        "condition": {
            "option": "q5.ru"
        },
        "links": [
            {
                "label": "Документы для договора поставки",
                "kind": "article",
                "target": "/knowledge/supply-documents?from=business"
            },
            {
                "label": "Купля-продажа ювелирных товаров",
                "kind": "article",
                "target": "/knowledge/jewelry-purchase?from=business"
            },
            {
                "label": "Открыть каталог поставщиков",
                "kind": "catalog",
                "target": "/suppliers?from=business&category=metals",
                "condition": {
                    "all": [
                        {
                            "tag": "material:metal"
                        },
                        {
                            "not": {
                                "tag": "material:stone"
                            }
                        }
                    ]
                }
            },
            {
                "label": "Открыть каталог поставщиков",
                "kind": "catalog",
                "target": "/suppliers?from=business&category=stones",
                "condition": {
                    "all": [
                        {
                            "tag": "material:stone"
                        },
                        {
                            "not": {
                                "tag": "material:metal"
                            }
                        }
                    ]
                }
            },
            {
                "label": "Открыть каталог поставщиков",
                "kind": "catalog",
                "target": "/suppliers?from=business",
                "condition": {
                    "all": [
                        {
                            "tag": "material:metal"
                        },
                        {
                            "tag": "material:stone"
                        }
                    ]
                }
            },
            {
                "label": "Открыть каталог поставщиков",
                "kind": "catalog",
                "target": "/suppliers?from=business",
                "condition": {
                    "option": "q4.bijou"
                }
            }
        ]
    },
    {
        "code": "biz.q5.abroad",
        "step": "q5",
        "title": "Организуйте импорт",
        "body": "До первого приобретения определите порядок импорта: выберите поставщика, заключите внешнеторговый договор, подготовьте документы для ввоза и учтите таможенные и специальные требования к соответствующим товарам.",
        "condition": {
            "option": "q5.abroad"
        },
        "links": [
            {
                "label": "Как импортировать ювелирные товары",
                "kind": "article",
                "target": "/knowledge/jewelry-import?from=business"
            },
            {
                "label": "Документы для договора поставки",
                "kind": "article",
                "target": "/knowledge/supply-documents?from=business"
            },
            {
                "label": "Открыть каталог поставщиков",
                "kind": "catalog",
                "target": "/suppliers?from=business&category=metals",
                "condition": {
                    "all": [
                        {
                            "tag": "material:metal"
                        },
                        {
                            "not": {
                                "tag": "material:stone"
                            }
                        }
                    ]
                }
            },
            {
                "label": "Открыть каталог поставщиков",
                "kind": "catalog",
                "target": "/suppliers?from=business&category=stones",
                "condition": {
                    "all": [
                        {
                            "tag": "material:stone"
                        },
                        {
                            "not": {
                                "tag": "material:metal"
                            }
                        }
                    ]
                }
            },
            {
                "label": "Открыть каталог поставщиков",
                "kind": "catalog",
                "target": "/suppliers?from=business",
                "condition": {
                    "all": [
                        {
                            "tag": "material:metal"
                        },
                        {
                            "tag": "material:stone"
                        }
                    ]
                }
            },
            {
                "label": "Открыть каталог поставщиков",
                "kind": "catalog",
                "target": "/suppliers?from=business",
                "condition": {
                    "option": "q4.bijou"
                }
            }
        ]
    },
    {
        "code": "biz.q5.both",
        "step": "q5",
        "title": "Организуйте российские и импортные закупки",
        "body": "Разделите договоры купли-продажи на российские и импортные. Для российских поставщиков организуйте проверку и получение документов, а для иностранных дополнительно предусмотрите внешнеторговый договор, таможенное оформление и требования к ввозу.",
        "condition": {
            "option": "q5.both"
        },
        "links": [
            {
                "label": "Купля-продажа ювелирных товаров",
                "kind": "article",
                "target": "/knowledge/jewelry-purchase?from=business"
            },
            {
                "label": "Как импортировать ювелирные товары",
                "kind": "article",
                "target": "/knowledge/jewelry-import?from=business"
            },
            {
                "label": "Документы для договора поставки",
                "kind": "article",
                "target": "/knowledge/supply-documents?from=business"
            },
            {
                "label": "Открыть каталог поставщиков",
                "kind": "catalog",
                "target": "/suppliers?from=business&category=metals",
                "condition": {
                    "all": [
                        {
                            "tag": "material:metal"
                        },
                        {
                            "not": {
                                "tag": "material:stone"
                            }
                        }
                    ]
                }
            },
            {
                "label": "Открыть каталог поставщиков",
                "kind": "catalog",
                "target": "/suppliers?from=business&category=stones",
                "condition": {
                    "all": [
                        {
                            "tag": "material:stone"
                        },
                        {
                            "not": {
                                "tag": "material:metal"
                            }
                        }
                    ]
                }
            },
            {
                "label": "Открыть каталог поставщиков",
                "kind": "catalog",
                "target": "/suppliers?from=business",
                "condition": {
                    "all": [
                        {
                            "tag": "material:metal"
                        },
                        {
                            "tag": "material:stone"
                        }
                    ]
                }
            },
            {
                "label": "Открыть каталог поставщиков",
                "kind": "catalog",
                "target": "/suppliers?from=business",
                "condition": {
                    "option": "q4.bijou"
                }
            }
        ]
    },
    {
        "code": "biz.q5.undecided",
        "step": "q5",
        "title": "Определите схему закупок",
        "body": "Сначала определите, где вы будете приобретать изделия или материалы. При приобретении в России основными задачами будут проверка поставщика и получение документов на товар. При приобретении за рубежом дополнительно потребуются внешнеторговый договор, таможенное оформление и соблюдение требований к ввозу. Если хотите сначала изучить возможных российских поставщиков, воспользуйтесь Каталогом поставщиков.",
        "condition": {
            "option": "q5.undecided"
        },
        "links": [
            {
                "label": "Открыть каталог поставщиков",
                "kind": "catalog",
                "target": "/suppliers?from=business&category=metals",
                "condition": {
                    "all": [
                        {
                            "tag": "material:metal"
                        },
                        {
                            "not": {
                                "tag": "material:stone"
                            }
                        }
                    ]
                }
            },
            {
                "label": "Открыть каталог поставщиков",
                "kind": "catalog",
                "target": "/suppliers?from=business&category=stones",
                "condition": {
                    "all": [
                        {
                            "tag": "material:stone"
                        },
                        {
                            "not": {
                                "tag": "material:metal"
                            }
                        }
                    ]
                }
            },
            {
                "label": "Открыть каталог поставщиков",
                "kind": "catalog",
                "target": "/suppliers?from=business",
                "condition": {
                    "all": [
                        {
                            "tag": "material:metal"
                        },
                        {
                            "tag": "material:stone"
                        }
                    ]
                }
            },
            {
                "label": "Открыть каталог поставщиков",
                "kind": "catalog",
                "target": "/suppliers?from=business",
                "condition": {
                    "option": "q4.bijou"
                }
            }
        ]
    },
    {
        "code": "biz.q6.store",
        "step": "q6",
        "title": "Подготовьте розничную точку",
        "body": "Подготовьте место розничной торговли: проверьте требования к помещению, оформлению точки продаж, кассе, информации для покупателей и документам на реализуемые изделия.",
        "condition": {
            "option": "q6.store"
        },
        "links": [
            {
                "label": "Как открыть ювелирный магазин",
                "kind": "article",
                "target": "/knowledge/jewelry-store?from=business"
            }
        ]
    },
    {
        "code": "biz.q6.online",
        "step": "q6",
        "title": "Организуйте дистанционные продажи",
        "body": "Подготовьте дистанционную продажу: разместите обязательную информацию о продавце и товарах, определите правила оплаты, доставки и возврата, а также оформите необходимые документы сайта и обработку персональных данных.",
        "condition": {
            "option": "q6.online"
        },
        "links": [
            {
                "label": "Как продавать украшения через интернет",
                "kind": "article",
                "target": "/knowledge/online-sales?from=business"
            }
        ]
    },
    {
        "code": "biz.q6.marketplace",
        "step": "q6",
        "title": "Подготовьте продажи на маркетплейсах",
        "body": "Проверьте требования выбранной площадки к ювелирным товарам, подготовьте документы и карточки изделий и определите, какие обязанности выполняет продавец, а какие - маркетплейс.",
        "condition": {
            "option": "q6.marketplace"
        },
        "links": [
            {
                "label": "Продажа украшений на маркетплейсах",
                "kind": "article",
                "target": "/knowledge/marketplace-sales?from=business"
            }
        ]
    },
    {
        "code": "biz.q6.wholesale",
        "step": "q6",
        "title": "Организуйте оптовые продажи",
        "body": "Организуйте оптовую продажу через договоры с покупателями и правильный документооборот. Отдельно определите порядок передачи изделий, оплаты, приемки и документов, которые должны сопровождать товар.",
        "condition": {
            "option": "q6.wholesale"
        },
        "links": [
            {
                "label": "Оптовая торговля ювелирными изделиями",
                "kind": "article",
                "target": "/knowledge/wholesale-jewelry?from=business"
            }
        ]
    },
    {
        "code": "biz.q7.new_only",
        "step": "q7",
        "title": "Организуйте работу с новыми изделиями",
        "body": "Дополнительных действий, связанных с приемом имущества клиентов или оборотом бывших в употреблении изделий, вам не потребуется. При приобретении новых изделий сохраняйте документы от поставщика, подтверждающие их происхождение, характеристики и поступление в ваш бизнес.",
        "condition": {
            "option": "q7.new_only"
        },
        "links": [
            {
                "label": "Документы для договора поставки",
                "kind": "article",
                "target": "/knowledge/supply-documents?from=business"
            }
        ]
    },
    {
        "code": "biz.q7.client",
        "step": "q7",
        "title": "Организуйте прием изделий клиентов",
        "body": "Необходимо организовать прием имущества клиента: фиксировать характеристики изделия, его состояние, массу и переданные материалы, выдавать подтверждающий документ и определять ответственность за сохранность изделия.",
        "condition": {
            "option": "q7.client"
        },
        "links": [
            {
                "label": "Как принимать изделия клиентов",
                "kind": "article",
                "target": "/knowledge/client-jewelry?from=business"
            }
        ]
    },
    {
        "code": "biz.q7.used",
        "step": "q7",
        "title": "Организуйте оборот бывших в употреблении изделий",
        "body": "Проверьте специальные правила приобретения и дальнейшего оборота бывших в употреблении ювелирных изделий. Необходимо правильно оформлять их прием, происхождение, учет и последующую продажу.",
        "condition": {
            "option": "q7.used"
        },
        "links": [
            {
                "label": "Работа с ювелирными изделиями, бывшими в употреблении",
                "kind": "article",
                "target": "/knowledge/used-jewelry?from=business"
            }
        ]
    },
    {
        "code": "biz.q7.client_used",
        "step": "q7",
        "title": "Разделите порядок работы с изделиями",
        "body": "Организуйте отдельно работу с изделиями клиентов и с изделиями, которые вы приобретаете для последующей продажи. Для каждой схемы должны быть свои документы приема, учета и дальнейшего движения изделий.",
        "condition": {
            "option": "q7.client_used"
        },
        "links": [
            {
                "label": "Как принимать изделия клиентов",
                "kind": "article",
                "target": "/knowledge/client-jewelry?from=business"
            },
            {
                "label": "Работа с ювелирными изделиями, бывшими в употреблении",
                "kind": "article",
                "target": "/knowledge/used-jewelry?from=business"
            }
        ]
    },
    {
        "code": "biz.q7_1.repair",
        "step": "q7_1",
        "title": "Оформите прием изделий на ремонт",
        "body": "Оформляйте прием изделия на ремонт с подробным описанием его состояния, характеристик и согласованной работы. Укажите сроки, стоимость и ответственность за повреждение или утрату изделия.",
        "condition": {
            "option": "q7_1.repair"
        },
        "links": [
            {
                "label": "Как оформить ремонт украшения",
                "kind": "article",
                "target": "/knowledge/jewelry-repair?from=business"
            }
        ]
    },
    {
        "code": "biz.q7_1.rework",
        "step": "q7_1",
        "title": "Оформите прием изделий на переделку",
        "body": "До начала работы зафиксируйте, какое изделие и в каком состоянии передал клиент, какие изменения необходимо выполнить и что происходит с исходными материалами после переделки.",
        "condition": {
            "option": "q7_1.rework"
        },
        "links": [
            {
                "label": "Как оформить переделку украшения",
                "kind": "article",
                "target": "/knowledge/jewelry-remaking?from=business"
            }
        ]
    },
    {
        "code": "biz.q7_1.new_from_client_material",
        "step": "q7_1",
        "title": "Оформите работу с материалом клиента",
        "body": "Оформите передачу материала клиента, его характеристики и количество, согласуйте требования к новому изделию и предусмотрите порядок учета использованного материала, отходов и остатков.",
        "condition": {
            "option": "q7_1.new_from_client_material"
        },
        "links": [
            {
                "label": "Изготовление украшения из материала клиента",
                "kind": "article",
                "target": "/knowledge/client-materials?from=business"
            }
        ]
    },
    {
        "code": "biz.q7_1.several",
        "step": "q7_1",
        "title": "Разделите порядок оказания ювелирных услуг",
        "body": "Используйте отдельный порядок оформления для ремонта, переделки и изготовления нового изделия из материала клиента. Для каждой операции должны фиксироваться переданные материалы, результат работы и ответственность сторон.",
        "condition": {
            "option": "q7_1.several"
        },
        "links": [
            {
                "label": "Как оформить ремонт украшения",
                "kind": "article",
                "target": "/knowledge/jewelry-repair?from=business"
            },
            {
                "label": "Как оформить переделку украшения",
                "kind": "article",
                "target": "/knowledge/jewelry-remaking?from=business"
            },
            {
                "label": "Изготовление украшения из материала клиента",
                "kind": "article",
                "target": "/knowledge/client-materials?from=business"
            }
        ]
    },
    {
        "code": "biz.q8.own",
        "step": "q8",
        "title": "Защитите бренд и дизайн",
        "body": "Проверьте, кому принадлежат права на название и дизайн украшений, и оформите передачу прав от тех, кто участвовал в их создании. Если вы придумали дизайн сами или получили его от дизайнера, пройдите опрос «Оформить права на дизайн», чтобы определить, как оформить права до начала продаж. Если похожие изделия уже продает другой производитель, пройдите также опрос «Другой производитель предлагает похожие товары».",
        "condition": {
            "option": "q8.own"
        },
        "links": [
            {
                "label": "Как закрепить права на изделие за собой?",
                "kind": "article",
                "target": "/knowledge/design-rights?from=business"
            },
            {
                "label": "Что защищается товарным знаком в ювелирном бизнесе?",
                "kind": "article",
                "target": "/knowledge/trademark-protection?from=business"
            },
            {
                "label": "Оформить права на дизайн",
                "kind": "scenario",
                "target": "/design/survey?first=1&from=business"
            },
            {
                "label": "Другой производитель предлагает похожие изделия",
                "kind": "scenario",
                "target": "/similar-products/survey?first=1&from=business"
            }
        ]
    },
    {
        "code": "biz.q8.others",
        "step": "q8",
        "title": "Проверьте права на чужие бренды",
        "body": "Проверьте происхождение изделий и получите от поставщика документы, подтверждающие их характеристики и передачу вам. Какие документы нужны и что предусмотреть в договоре с российским или иностранным поставщиком, читайте в статьях «Документы для договора поставки» и «Купля-продажа ювелирных товаров». Названия брендов указывайте достоверно, а чужие фотографии и рекламные материалы используйте только при наличии права на них.",
        "condition": {
            "option": "q8.others"
        },
        "links": [
            {
                "label": "Документы для договора поставки",
                "kind": "article",
                "target": "/knowledge/supply-documents?from=business"
            },
            {
                "label": "Купля-продажа ювелирных товаров",
                "kind": "article",
                "target": "/knowledge/jewelry-purchase?from=business"
            }
        ]
    },
    {
        "code": "biz.q8.both",
        "step": "q8",
        "title": "Оформите права на собственные и чужие бренды",
        "body": "Для собственного бренда проверьте права на название и дизайн украшений, а также оформите передачу прав от тех, кто участвовал в их создании. Чтобы разобраться с оформлением своего дизайна до начала продаж, пройдите опрос «Оформить права на дизайн».\n\nЕсли похожие изделия уже продает другой производитель, пройдите также опрос «Другой производитель предлагает похожие товары». Для готовых изделий других брендов проверьте происхождение и получите документы, подтверждающие их характеристики и передачу вам. Перечень документов и условия договора с поставщиком разбираются в статьях «Документы для договора поставки» и «Купля-продажа ювелирных товаров». Названия брендов указывайте достоверно, а чужие фотографии и рекламные материалы используйте только при наличии права на них.",
        "condition": {
            "option": "q8.both"
        },
        "links": [
            {
                "label": "Как закрепить права на изделие за собой?",
                "kind": "article",
                "target": "/knowledge/design-rights?from=business"
            },
            {
                "label": "Что защищается товарным знаком в ювелирном бизнесе?",
                "kind": "article",
                "target": "/knowledge/trademark-protection?from=business"
            },
            {
                "label": "Документы для договора поставки",
                "kind": "article",
                "target": "/knowledge/supply-documents?from=business"
            },
            {
                "label": "Купля-продажа ювелирных товаров",
                "kind": "article",
                "target": "/knowledge/jewelry-purchase?from=business"
            },
            {
                "label": "Оформить права на дизайн",
                "kind": "scenario",
                "target": "/design/survey?first=1&from=business"
            },
            {
                "label": "Другой производитель предлагает похожие изделия",
                "kind": "scenario",
                "target": "/similar-products/survey?first=1&from=business"
            }
        ]
    },
    {
        "code": "biz.q9.yes",
        "step": "q9",
        "title": "Оформите сотрудников",
        "body": "До допуска сотрудников к работе оформите трудовые отношения и определите их ответственность за изделия, материалы и иное имущество. Для дизайнеров и других творческих работников отдельно урегулируйте права на создаваемые ими результаты.",
        "condition": {
            "option": "q9.yes"
        },
        "links": [
            {
                "label": "Как оформить сотрудников ювелирного бизнеса",
                "kind": "article",
                "target": "/knowledge/employees?from=business"
            }
        ]
    },
    {
        "code": "biz.q9.no",
        "step": "q9",
        "title": "Организуйте работу без сотрудников",
        "body": "Если вы будете вести бизнес самостоятельно, отдельные действия по оформлению работников сейчас не требуются. Если позднее решите нанять сотрудника, до его фактического допуска к работе потребуется оформить трудовые отношения; при доступе сотрудника к изделиям и материалам также заранее определите вопросы материальной ответственности.",
        "condition": {
            "option": "q9.no"
        },
        "links": []
    },
    {
        "code": "biz.q9.unknown",
        "step": "q9",
        "title": "Определите необходимость найма сотрудников",
        "body": "Решите, сможете ли вы выполнять основные процессы самостоятельно или потребуется нанимать работников. Если сотрудники понадобятся, перед началом их работы нужно будет оформить трудовые отношения, определить ответственность за переданные им изделия и материалы, а для работников, создающих дизайн, – отдельно урегулировать права на результаты их работы.",
        "condition": {
            "option": "q9.unknown"
        },
        "links": []
    },
    {
        "code": "biz.q10.yes",
        "step": "q10",
        "title": "Проверьте помещение",
        "body": "Проверьте, подходит ли помещение для выбранного вида деятельности и может ли оно использоваться как место производства, торговли или оказания услуг. При необходимости оформите сведения о месте деятельности в соответствующих государственных системах.",
        "condition": {
            "option": "q10.yes"
        },
        "links": [
            {
                "label": "Проверить помещение",
                "kind": "article",
                "target": "/knowledge/check-premises?from=business"
            }
        ]
    },
    {
        "code": "biz.q10.no",
        "step": "q10",
        "title": "Подберите помещение",
        "body": "Определите, требуется ли отдельное помещение для выбранной модели бизнеса. Если вы планируете производство, мастерскую или офлайн-магазин, необходимо подобрать подходящее помещение и оформить право его использования.",
        "condition": {
            "option": "q10.no"
        },
        "links": [
            {
                "label": "Как выбрать помещение",
                "kind": "article",
                "target": "/knowledge/choose-premises?from=business"
            }
        ]
    },
    {
        "code": "biz.q10.none",
        "step": "q10",
        "title": "Проверьте, требуется ли вам помещение",
        "body": "Сопоставьте это решение с выбранной моделью бизнеса. Если вы только продаете товары дистанционно, отдельная торговая точка может не потребоваться. Если же вы планируете собственное производство, мастерскую, хранение изделий или офлайн-продажи, необходимо заранее определить место ведения такой деятельности и проверить требования к его оформлению.",
        "condition": {
            "option": "q10.none"
        },
        "links": []
    }
]
