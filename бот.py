import telebot
from telebot import types
from collections import defaultdict
import datetime

# ---------------- CONFIG ----------------
TOKEN = "8400828602:AAGmF8japcI3YkWRmvd2o9QXoohcYc4I7vQ"
bot = telebot.TeleBot(TOKEN)

# Админ (юзернейм). Бот будет пытаться отправить уведомления на этот ник.
ADMIN_CHAT = 5539798707

# ---------------- STATE -----------------
user_spending = defaultdict(int)      # {user_id: сумма покупок (в т.ч. рефералов)}
referrals = defaultdict(list)         # {referrer_id: [user_id рефералов]}
user_referrer = {}                    # {user_id: referrer_id}
reviews = []                          # список строк вида "@user: текст"

user_language = {}                    # {user_id: "ru" или "ua"}
user_carts = defaultdict(list)        # {user_id: [(product_name, price), ...]}
user_states = {}                      # {user_id: "writing_review" или None}

# Заказы: order_id -> {...}
orders = {}
_next_order_id = 1

# --------------- TEXTS -----------------
texts = {
    # языковой выбор
    "choose_lang": "🌍 Пожалуйста, выберите удобный язык / Будь ласка, оберіть зручну мову:",
    "lang_ru": "🇷🇺 Русский",
    "lang_ua": "🇺🇦 Українська",

    # главное меню
    "welcome_ru": "💨 Добро пожаловать в *VapeAlva*!\nВыберите интересующий раздел:",
    "welcome_ua": "💨 Ласкаво просимо до *VapeAlva*!\nОберіть потрібний розділ:",

    "menu_catalog_ru": "📂 Каталог",
    "menu_catalog_ua": "📂 Каталог",
    "menu_order_ru": "🛒 Заказать",
    "menu_order_ua": "🛒 Замовити",
    "menu_cart_ru": "🛍 Корзина",
    "menu_cart_ua": "🛍 Кошик",
    "menu_about_ru": "ℹ️ О нас",
    "menu_about_ua": "ℹ️ Про нас",
    "menu_partner_ru": "🤝 Партнёрская программа",
    "menu_partner_ua": "🤝 Партнерська програма",
    "menu_orders_ru": "📦 Мои заказы",
    "menu_orders_ua": "📦 Мої замовлення",
    "menu_reviews_ru": "✍ Оставить отзыв",
    "menu_reviews_ua": "✍ Залишити відгук",
    "back_btn_ru": "⬅ Назад",
    "back_btn_ua": "⬅ Назад",

    "please_choose_ru": "Пожалуйста, выберите пункт меню.",
    "please_choose_ua": "Будь ласка, оберіть пункт меню.",

    # отзывы
    "reviews_list_empty_ru": "Пока нет отзывов. Будьте первым!",
    "reviews_list_empty_ua": "Поки немає відгуків. Будьте першими!",
    "thank_review_ru": "✅ Спасибо! Ваш отзыв добавлен.",
    "thank_review_ua": "✅ Дякуємо! Ваш відгук додано.",

    # партнерка / о нас
    "partner_program_ru": (
        "💼 *Партнёрская программа VapeAlva*\n\n"
        "Приглашайте друзей по вашей личной ссылке и получайте ценные бонусы!\n\n"
        "👥 Приглашено пользователей: *{count}*\n"
        "🎁 Когда ваши приглашённые суммарно совершат покупки на *4100 грн*, "
        "вы получите подарок на выбор:\n"
        "• 💨 Любая жидкость из нашего ассортимента\n"
        "• 🔄 Или два картриджа по вашему вкусу\n\n"
        "📌 Всё просто: отправляйте ссылку друзьям, они заказывают — вы копите бонусы.\n\n"
        "🔗 Ваша ссылка: {link}\n"
        "💰 Потрачено по вашей ссылке: {spent} грн"
    ),
    "partner_program_ua": (
        "💼 *Партнерська програма VapeAlva*\n\n"
        "Запрошуйте друзів за вашим унікальним посиланням і отримуйте цінні бонуси!\n\n"
        "👥 Запрошено користувачів: *{count}*\n"
        "🎁 Коли ваші запрошені зроблять покупки на суму *4100 грн*, "
        "ви отримаєте подарунок на вибір:\n"
        "• 💨 Будь-яка рідина з нашого асортименту\n"
        "• 🔄 Або два картриджі на ваш смак\n\n"
        "📌 Просто надсилайте посилання друзям, вони замовляють — ви накопичуєте бонуси.\n\n"
        "🔗 Ваше посилання: {link}\n"
        "💰 Витрачено по вашому посиланню: {spent} грн"
    ),

    "about_ru": "💨 *VapeAlva* — магазин вейп-товаров с проверенными поставщиками.\n🚀 Доставка по всей Украине.\n\n📞 Поддержка: @helperAlva",
    "about_ua": "💨 *VapeAlva* — магазин вейп-товарів з перевіреними постачальниками.\n🚀 Доставка по всій Україні.\n\n📞 Підтримка: @helperAlva",

    # корзина / заказ
    "cart_empty_ru": "🛒 Ваша корзина пуста.",
    "cart_empty_ua": "🛍 Ваш кошик порожній.",
    "cart_title_ru": "🛒 Ваша корзина:\n\n",
    "cart_title_ua": "🛍 Ваш кошик:\n\n",
    "cart_total_ru": "\n*Общая сумма:* {total} ₴",
    "cart_total_ua": "\n*Загальна сума:* {total} ₴",

    "order_button_ru": "Оформить заказ",
    "order_button_ua": "Оформити замовлення",

    "pay_method_ru": "Выберите способ оплаты:",
    "pay_method_ua": "Оберіть спосіб оплати:",
    "pay_on_delivery_ru": "Оплата при получении",
    "pay_on_delivery_ua": "Оплата при отриманні",
    "pay_prepay_ru": "Оплата Картой",
    "pay_prepay_ua": "Оплата Карткою",
    "pay_crypto_ru": "Оплата криптовалютой",
    "pay_crypto_ua": "Оплата криптовалютою",

    "pay_on_delivery_info_ru": "📞 С вами свяжется в ближайшее время наш менеджер для подтверждения заказа.",
    "pay_on_delivery_info_ua": "📞 З вами найближчим часом зв'яжеться наш менеджер для підтвердження замовлення.",

    "prepay_info_ru": (
        "💳 Оплата через бота:\n\n"
        "ФИО карты: Владислав. Г.\n"
        "Номер карты: 4441 1110 3909 5041\n\n"
        "После оплаты нажмите кнопку ниже, чтобы подтвердить оплату."
    ),
    "prepay_info_ua": (
        "💳 Оплата через бота:\n\n"
        "ПІБ карти: Владислав. Г.\n"
        "Номер карти: 4441 1110 3909 5041\n\n"
        "Після оплати натисніть кнопку нижче, щоб підтвердити оплату."
    ),

    "crypto_wallet": "UQDjclQadIIq-DUoTNY53oHfcp9WVi5mRVnUVxVUnQ-vznEc (TON)",

    "pay_done_ru": "Оплачено",
    "pay_done_ua": "Оплачено",

    "clear_cart_ru": "Очистить корзину",
    "clear_cart_ua": "Очистити кошик",

    # реферальные уведомления
    "referral_purchase_ru": "💰 Ваш реферал {user} сделал покупку на сумму {amount} грн.\nОбщая сумма покупок по вашей ссылке: {total} грн.",
    "referral_purchase_ua": "💰 Ваш реферал {user} зробив покупку на суму {amount} грн.\nЗагальна сума покупок по вашому посиланню: {total} грн.",

    "please_choose": "Пожалуйста, выберите пункт меню."
}

def t(key, lang="ru"):
    key_full = f"{key}_{lang}"
    return texts.get(key_full) or texts.get(key) or key

# --------------- PRODUCTS -----------------
# Храним продукты в простом реестре: id -> (category, name, price)
PRODUCTS = {}
PRODUCTS_BY_CATEGORY = defaultdict(list)
_product_id_seq = 1

def add_product(category, name, price):
    global _product_id_seq
    pid = _product_id_seq
    PRODUCTS[pid] = {"category": category, "name": name, "price": int(price)}
    PRODUCTS_BY_CATEGORY[category].append(pid)
    _product_id_seq += 1
    return pid

# Картриджи Vaporesso — цена 135, порядок по сопротивлению/мл (красиво)
cartridge_common_price = 135
add_product("cartridges_vaporesso", "Vaporesso Xros Series 1.0, 3 ml", cartridge_common_price)
add_product("cartridges_vaporesso", "Vaporesso Xros Series 1.0, 2 ml", cartridge_common_price)
add_product("cartridges_vaporesso", "Vaporesso Xros Series 0.8, 3 ml", cartridge_common_price)
add_product("cartridges_vaporesso", "Vaporesso Xros Series 0.8, 2 ml", cartridge_common_price)
add_product("cartridges_vaporesso", "Vaporesso Xros Series 0.6, 3 ml", cartridge_common_price)
add_product("cartridges_vaporesso", "Vaporesso Xros Series 0.6, 2 ml", cartridge_common_price)
add_product("cartridges_vaporesso", "Vaporesso Xros Series 0.4, 3 ml", cartridge_common_price)
add_product("cartridges_vaporesso", "Vaporesso Xros Series 0.4, 2 ml", cartridge_common_price)

# Voopoo cartridges (145)
voopoo_price = 145
add_product("cartridges_voopoo", "Voopoo Argus 3ml 0.7", voopoo_price)
add_product("cartridges_voopoo", "Voopoo Argus 3ml 1.0", voopoo_price)
add_product("cartridges_voopoo", "Voopoo Argus 3ml 0.4", voopoo_price)
add_product("cartridges_voopoo", "Voopoo Vmate 3ml 0.7", voopoo_price)
add_product("cartridges_voopoo", "Voopoo Vmate 2ml 0.7 (для версии TPD)", voopoo_price)
add_product("cartridges_voopoo", "Voopoo Vmate 3ml 0.4", voopoo_price)
add_product("cartridges_voopoo", "Voopoo Vmate 2ml 0.4 (для версии TPD)", voopoo_price)

# Elf Bar ELFX cartridges (135)
add_product("cartridges_elfx", "Elfx 2ml 0.6", 135)
add_product("cartridges_elfx", "Elfx 2ml 0.8", 135)

# Под-системы (pods)
add_product("pods", "Vaporesso xros 5", 1129)
add_product("pods", "Voopoo Argus G2", 1049)
add_product("pods", "Vaporesso xros 5 mini", 850)
add_product("pods", "Elbar Bar ELFX Pro", 849)
add_product("pods", "Vaporesso xros 4 mini", 809)
add_product("pods", "Voopoo Vmate I2 (второе поколение)", 719)
add_product("pods", "Elf Bar EV15000", 299)

# liquids placeholder
add_product("liquids", "(Скоро) Ассортимент жидкостей — в разработке", 0)

# Метки категорий (ru, ua)
CATEGORY_LABELS = {
    "pods": ("💨 Под-системы", "💨 Под-системи"),
    "liquids": ("🧃 Жидкости", "🧃 Рідини"),
    "cartridges": ("🔄 Картриджи", "🔄 Картриджі"),
    "cartridges_vaporesso": ("🔄 Картриджи — Vaporesso", "🔄 Картриджі — Vaporesso"),
    "cartridges_voopoo": ("🔄 Картриджи — Voopoo", "🔄 Картриджі — Voopoo"),
    "cartridges_elfx": ("🔄 Картриджи — Elf Bar ELFX", "🔄 Картриджі — Elf Bar ELFX"),
}

def cat_label(cat, lang="ru"):
    lbls = CATEGORY_LABELS.get(cat, (cat, cat))
    return lbls[0] if lang == "ru" else lbls[1]

# ---------------- HELPERS -----------------
def format_currency(n):
    # n может быть уже отформатированным — защитимся
    try:
        return f"{int(n)} ₴"
    except Exception:
        return f"{n} ₴"

def create_order(user_id, items, total, method, status):
    global _next_order_id
    oid = _next_order_id
    _next_order_id += 1
    orders[oid] = {
        "id": oid,
        "user_id": user_id,
        "items": items.copy(),
        "total": total,
        "method": method,
        "status": status,
        "created": datetime.datetime.utcnow().isoformat()
    }
    return oid

def find_user_pending_order(user_id, statuses=("pending", "cod")):
    user_orders = [o for o in orders.values() if o["user_id"] == user_id and o["status"] in statuses]
    if not user_orders:
        return None
    return max(user_orders, key=lambda x: x["id"])

def notify_admin(text, reply_markup=None):
    try:
        bot.send_message(ADMIN_CHAT, text, parse_mode="Markdown", reply_markup=reply_markup)
    except Exception as e:
        print("Не удалось отправить сообщение админу:", e)

# ---------- START / LANGUAGE HANDLERS ----------
@bot.message_handler(commands=["start"])
def start_handler(message):
    user_id = message.from_user.id
    args = message.text.split()
    if len(args) > 1:
        try:
            referrer_id = int(args[1])
            if referrer_id != user_id and user_id not in referrals[referrer_id]:
                referrals[referrer_id].append(user_id)
                user_referrer[user_id] = referrer_id
                try:
                    bot.send_message(referrer_id,
                                     f"🎉 Новый пользователь @{message.from_user.username or message.from_user.first_name} "
                                     f"зарегистрировался по вашей реферальной ссылке!")
                except Exception:
                    pass
        except Exception:
            pass

    if user_id not in user_language:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(types.KeyboardButton(texts["lang_ru"]), types.KeyboardButton(texts["lang_ua"]))
        bot.send_message(user_id, texts["choose_lang"], reply_markup=markup)
    else:
        send_main_menu(message)

@bot.message_handler(func=lambda m: m.text in [texts["lang_ru"], texts["lang_ua"]])
def set_language(message):
    user_id = message.from_user.id
    if message.text == texts["lang_ru"]:
        user_language[user_id] = "ru"
    else:
        user_language[user_id] = "ua"
    send_main_menu(message)

# ------------- MAIN MENU -------------
def send_main_menu(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, "ru")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    markup.add(
        types.KeyboardButton(t("menu_catalog", lang)),
        types.KeyboardButton(t("menu_order", lang)),
        types.KeyboardButton(t("menu_cart", lang)),
        types.KeyboardButton(t("menu_partner", lang)),
        types.KeyboardButton(t("menu_orders", lang)),
        types.KeyboardButton(t("menu_reviews", lang)),
    )
    bot.send_message(user_id, t("welcome", lang), parse_mode="Markdown", reply_markup=markup)

# ------------- CATALOG / MENU HANDLER -------------
@bot.message_handler(func=lambda m: True)
def menu_handler(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, "ru")
    text = message.text

    # Обработка состояния написания отзыва
    if user_states.get(user_id) == "writing_review":
        # пассивно принимаем отзыв в отдельном хендлере ниже
        return

    if text == t("menu_catalog", lang) or text == t("menu_order", lang):
        show_catalog_main_menu(message)
        return

    if text == t("menu_cart", lang):
        show_cart(message)
        return

    if text == t("menu_about", lang):
        bot.send_message(user_id, texts["about_ru"] if lang == "ru" else texts["about_ua"], parse_mode="Markdown")
        return

    if text == t("menu_partner", lang):
        count = len(referrals.get(user_id, []))
        spent = user_spending.get(user_id, 0)
        try:
            bot_username = bot.get_me().username
        except Exception:
            bot_username = "your_bot_username"
        link = f"https://t.me/{bot_username}?start={user_id}"
        partner_text = texts["partner_program_ru"] if lang == "ru" else texts["partner_program_ua"]
        bot.send_message(user_id, partner_text.format(count=count, spent=spent, link=link), parse_mode="Markdown")
        return

    if text == t("menu_orders", lang):
        show_user_orders(message)
        return

    # Исправленная логика для отзывов:
    if text == t("menu_reviews", lang):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(
            types.KeyboardButton("✍ " + ("Оставить отзыв" if lang == "ru" else "Залишити відгук")),
            types.KeyboardButton("👁 " + ("Просмотреть отзывы" if lang == "ru" else "Переглянути відгуки")),
            types.KeyboardButton(t("back_btn", lang))
        )
        bot.send_message(user_id, t("please_choose", lang), reply_markup=markup)
        return

    if text == "✍ " + ("Оставить отзыв" if lang == "ru" else "Залишити відгук"):
        bot.send_message(user_id, ("Напишите ваш отзыв и отправьте мне." if lang == "ru" else "Напишіть ваш відгук і надішліть мені."))
        user_states[user_id] = "writing_review"
        return

    if text == "👁 " + ("Просмотреть отзывы" if lang == "ru" else "Переглянути відгуки"):
        show_reviews(message)
        return

    if text == t("back_btn", lang):
        send_main_menu(message)
        return

# Обработчик текста при написании отзыва
@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == "writing_review")
def handle_review_text(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, "ru")
    text_msg = message.text.strip()
    if text_msg:
        username = message.from_user.username or message.from_user.first_name
        reviews.append(f"@{username}: {text_msg}")
        bot.send_message(user_id, texts["thank_review_ru"] if lang == "ru" else texts["thank_review_ua"])
        user_states[user_id] = None
    else:
        bot.send_message(user_id, ("Пожалуйста, напишите отзыв." if lang == "ru" else "Будь ласка, напишіть відгук."))

# ---------- КАТАЛОГ ----------
def show_catalog_main_menu(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, "ru")

    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(cat_label("pods", lang), callback_data="cat_pods"),
        types.InlineKeyboardButton(cat_label("liquids", lang), callback_data="cat_liquids"),
        types.InlineKeyboardButton(cat_label("cartridges", lang), callback_data="cat_cartridges"),
        types.InlineKeyboardButton(t("back_btn", lang), callback_data="back_main"),
    )
    bot.send_message(user_id, t("menu_catalog", lang), reply_markup=markup)

def show_catalog_submenu_cartridges(call, lang):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(cat_label("cartridges_vaporesso", lang), callback_data="cat_cartridges_vaporesso"),
        types.InlineKeyboardButton(cat_label("cartridges_voopoo", lang), callback_data="cat_cartridges_voopoo"),
        types.InlineKeyboardButton(cat_label("cartridges_elfx", lang), callback_data="cat_cartridges_elfx"),
        types.InlineKeyboardButton(t("back_btn", lang), callback_data="cat_cartridges_back"),
    )
    try:
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                              text=t("menu_catalog", lang), reply_markup=markup)
    except Exception:
        # fallback if edit failed
        bot.send_message(call.from_user.id, t("menu_catalog", lang), reply_markup=markup)

def show_products_list(call_or_message, category, lang):
    # call_or_message может быть CallbackQuery или Message
    product_ids = PRODUCTS_BY_CATEGORY.get(category, [])
    if not product_ids:
        if isinstance(call_or_message, types.CallbackQuery):
            bot.answer_callback_query(call_or_message.id, "Товары не найдены", show_alert=True)
        else:
            bot.send_message(call_or_message.from_user.id, "Товары не найдены")
        return
    text = f"📦 {cat_label(category, lang)}:\n\n"
    markup = types.InlineKeyboardMarkup(row_width=1)
    for pid in product_ids:
        prod = PRODUCTS[pid]
        text += f"{prod['name']} — {format_currency(prod['price'])}\n"
        markup.add(types.InlineKeyboardButton(f"➕ {prod['name']}", callback_data=f"add_{pid}"))
    markup.add(types.InlineKeyboardButton(t("back_btn", lang), callback_data="back_catalog"))
    if isinstance(call_or_message, types.CallbackQuery):
        try:
            bot.edit_message_text(chat_id=call_or_message.from_user.id, message_id=call_or_message.message.message_id, text=text, reply_markup=markup)
        except Exception:
            bot.send_message(call_or_message.from_user.id, text, reply_markup=markup)
    else:
        bot.send_message(call_or_message.from_user.id, text, reply_markup=markup)

# ---------- CALLBACKS ----------
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    lang = user_language.get(user_id, "ru")
    data = call.data

    try:
        if data == "back_main":
            send_main_menu(call.message)
            bot.answer_callback_query(call.id)
            return

        if data == "cat_pods":
            show_products_list(call, "pods", lang)
            bot.answer_callback_query(call.id)
            return

        if data == "cat_liquids":
            show_products_list(call, "liquids", lang)
            bot.answer_callback_query(call.id)
            return

        if data == "cat_cartridges":
            show_catalog_submenu_cartridges(call, lang)
            bot.answer_callback_query(call.id)
            return

        if data == "cat_cartridges_back":
            show_catalog_main_menu(call.message)
            bot.answer_callback_query(call.id)
            return

        if data == "cat_cartridges_vaporesso":
            show_products_list(call, "cartridges_vaporesso", lang)
            bot.answer_callback_query(call.id)
            return

        if data == "cat_cartridges_voopoo":
            show_products_list(call, "cartridges_voopoo", lang)
            bot.answer_callback_query(call.id)
            return

        if data == "cat_cartridges_elfx":
            show_products_list(call, "cartridges_elfx", lang)
            bot.answer_callback_query(call.id)
            return

        if data.startswith("add_"):
            pid_str = data[4:]
            if not pid_str.isdigit():
                bot.answer_callback_query(call.id, "Ошибка: неверный идентификатор товара", show_alert=True)
                return
            pid = int(pid_str)
            if pid not in PRODUCTS:
                bot.answer_callback_query(call.id, "Ошибка: товар не найден", show_alert=True)
                return
            prod = PRODUCTS[pid]
            user_carts[user_id].append((prod["name"], prod["price"]))
            bot.answer_callback_query(call.id, f"Добавлено: {prod['name']}")
            return

        if data == "back_catalog":
            show_catalog_main_menu(call.message)
            bot.answer_callback_query(call.id)
            return

        if data == "clear_cart":
            user_carts[user_id] = []
            bot.answer_callback_query(call.id, "Корзина очищена" if lang == "ru" else "Кошик очищено")
            try:
                bot.delete_message(call.from_user.id, call.message.message_id)
            except Exception:
                pass
            return

        if data == "order":
            cart = user_carts.get(user_id, [])
            if not cart:
                bot.answer_callback_query(call.id, "Корзина пуста" if lang == "ru" else "Кошик порожній", show_alert=True)
                return
            total = sum(p for _, p in cart)
            order_id = create_order(user_id, cart, total, method="pending", status="pending")

            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton(t("pay_on_delivery", lang), callback_data=f"pay_cod_{order_id}"),
                types.InlineKeyboardButton(t("pay_prepay", lang), callback_data=f"pay_prepay_{order_id}"),
                types.InlineKeyboardButton(t("pay_crypto", lang), callback_data=f"pay_crypto_{order_id}"),
                types.InlineKeyboardButton(t("back_btn", lang), callback_data="back_main")
            )
            try:
                bot.edit_message_text(
                    chat_id=call.from_user.id,
                    message_id=call.message.message_id,
                    text=f"{t('pay_method', lang)}\n\nСумма: {format_currency(total)}",
                    reply_markup=markup
                )
            except Exception:
                bot.send_message(call.from_user.id, f"{t('pay_method', lang)}\n\nСумма: {format_currency(total)}", reply_markup=markup)
            bot.answer_callback_query(call.id)
            return

        # Оплата при получении
        if data.startswith("pay_cod_"):
            parts = data.split('_')
            try:
                order_id = int(parts[-1])
            except ValueError:
                bot.answer_callback_query(call.id, "Ошибка: неверный идентификатор заказа", show_alert=True)
                return
            order = orders.get(order_id)
            if not order or order["user_id"] != user_id:
                bot.answer_callback_query(call.id, "Заказ не найден", show_alert=True)
                return
            order["method"] = "cod"
            order["status"] = "cod"
            user_carts[user_id] = []  # Очистка корзины

            try:
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=t("pay_on_delivery_info", lang)
                )
            except Exception:
                bot.send_message(call.from_user.id, t("pay_on_delivery_info", lang))
            bot.answer_callback_query(call.id)

            notify_admin(
                f"Новый заказ #{order_id} от @{call.from_user.username or call.from_user.first_name}\n"
                f"Метод оплаты: Оплата при получении\n"
                f"Сумма: {format_currency(order['total'])}"
            )
            return

        # Оплата картой
        if data.startswith("pay_prepay_"):
            parts = data.split('_')
            try:
                order_id = int(parts[-1])
            except ValueError:
                bot.answer_callback_query(call.id, "Ошибка: неверный идентификатор заказа", show_alert=True)
                return
            order = orders.get(order_id)
            if not order or order["user_id"] != user_id:
                bot.answer_callback_query(call.id, "Заказ не найден", show_alert=True)
                return
            order["method"] = "prepay"
            order["status"] = "waiting_confirmation"

            try:
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=t("prepay_info", lang)
                )
            except Exception:
                bot.send_message(call.from_user.id, t("prepay_info", lang))

            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton(t("pay_done", lang), callback_data=f"pay_done_{order_id}"))
            bot.send_message(user_id, "💳 Оплатили? Нажмите кнопку ниже для подтверждения.", reply_markup=markup)
            bot.answer_callback_query(call.id)

            notify_admin(
                f"Новый заказ #{order_id} от @{call.from_user.username or call.from_user.first_name}\n"
                f"Метод оплаты: Оплата Картой\n"
                f"Сумма: {format_currency(order['total'])}\n\n"
                f"Для подтверждения оплаты нажмите кнопку ниже.",
                reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton(
                        "Подтвердить оплату",
                        callback_data=f"confirm_payment_{order_id}"
                    )
                )
            )
            return

        # Оплата криптовалютой
        if data.startswith("pay_crypto_"):
            parts = data.split('_')
            try:
                order_id = int(parts[-1])
            except ValueError:
                bot.answer_callback_query(call.id, "Ошибка: неверный идентификатор заказа", show_alert=True)
                return
            order = orders.get(order_id)
            if not order or order["user_id"] != user_id:
                bot.answer_callback_query(call.id, "Заказ не найден", show_alert=True)
                return
            order["method"] = "crypto"
            order["status"] = "waiting_confirmation"

            try:
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text=f"Оплатите криптовалютой на адрес:\n\n{texts.get('crypto_wallet', 'адрес_криптокошелька')}",
                    parse_mode="Markdown"
                )
            except Exception:
                bot.send_message(call.from_user.id, f"Оплатите криптовалютой на адрес:\n\n{texts.get('crypto_wallet', 'адрес_криптокошелька')}")

            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton(t("pay_done", lang), callback_data=f"pay_done_{order_id}"))
            bot.send_message(user_id, "💳 Оплатили? Нажмите кнопку ниже для подтверждения.", reply_markup=markup)
            bot.answer_callback_query(call.id)

            notify_admin(
                f"Новый заказ #{order_id} от @{call.from_user.username or call.from_user.first_name}\n"
                f"Метод оплаты: Криптовалюта\n"
                f"Сумма: {format_currency(order['total'])}\n\n"
                f"Для подтверждения оплаты нажмите кнопку ниже.",
                reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton(
                        "Подтвердить оплату",
                        callback_data=f"confirm_payment_{order_id}"
                    )
                )
            )
            return

        # Клиент нажал "Оплачено" (ожидает подтверждения)
        if data.startswith("pay_done_"):
            try:
                order_id = int(data[9:])
            except ValueError:
                bot.answer_callback_query(call.id, "Ошибка: неверный идентификатор заказа", show_alert=True)
                return
            order = orders.get(order_id)
            if not order or order["user_id"] != user_id:
                bot.answer_callback_query(call.id, "Заказ не найден", show_alert=True)
                return
            if order["status"] == "waiting_confirmation":
                bot.send_message(user_id,
                    "⏳ Ваш платеж ожидает подтверждения. Пожалуйста, дождитесь подтверждения администратора." if lang == "ru"
                    else "⏳ Ваш платіж очікує підтвердження. Будь ласка, зачекайте підтвердження адміністратора.")
                bot.answer_callback_query(call.id)
                return
            else:
                bot.answer_callback_query(call.id, "Ваш заказ уже обработан.", show_alert=True)
                return

        # Админ подтверждает оплату
        if data.startswith("confirm_payment_"):
            if call.from_user.id != ADMIN_CHAT:
                bot.answer_callback_query(call.id, "Доступ запрещён", show_alert=True)
                return
            try:
                order_id = int(data[len("confirm_payment_"):])
            except ValueError:
                bot.answer_callback_query(call.id, "Ошибка: неверный ID заказа", show_alert=True)
                return
            order = orders.get(order_id)
            if not order:
                bot.answer_callback_query(call.id, "Заказ не найден", show_alert=True)
                return
            if order["status"] != "waiting_confirmation":
                bot.answer_callback_query(call.id, "Статус заказа не требует подтверждения", show_alert=True)
                return

            order["status"] = "paid"

            # Уведомляем клиента
            user_id_order = order["user_id"]
            lang_user = user_language.get(user_id_order, "ru")
            bot.send_message(user_id_order,
                "✅ Оплата подтверждена! Ваш заказ обрабатывается." if lang_user == "ru"
                else "✅ Оплата підтверджена! Ваше замовлення обробляється.")

            # Уведомляем админа (подтверждение)
            try:
                uname = bot.get_chat(user_id_order).username
            except Exception:
                uname = None
            notify_admin(
                f"✅ Оплата подтверждена для заказа #{order_id}.\n"
                f"Пользователь: @{uname or user_id_order}\n"
                f"Сумма: {format_currency(order['total'])}"
            )

            bot.answer_callback_query(call.id, "Оплата подтверждена")
            return

        # Просмотр корзины
        if data == "show_cart":
            show_cart(call.message)
            bot.answer_callback_query(call.id)
            return

    except Exception as e:
        print(f"Ошибка в callback_handler: {e}")
        try:
            bot.answer_callback_query(call.id, "Произошла ошибка", show_alert=True)
        except Exception:
            pass

# ---------- ПОКАЗ КОРЗИНЫ ----------
def show_cart(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, "ru")
    cart = user_carts.get(user_id, [])
    if not cart:
        bot.send_message(user_id, texts["cart_empty_ru"] if lang == "ru" else texts["cart_empty_ua"])
        return
    text = t("cart_title", lang)
    total = 0
    for name, price in cart:
        text += f"• {name} — {format_currency(price)}\n"
        total += price
    text += (texts["cart_total_ru"] if lang == "ru" else texts["cart_total_ua"]).format(total=format_currency(total))

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(t("order_button", lang), callback_data="order"),
        types.InlineKeyboardButton(t("clear_cart", lang), callback_data="clear_cart")
    )
    bot.send_message(user_id, text, reply_markup=markup)

# ---------- ОТЗЫВЫ ----------
def show_reviews(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, "ru")
    if not reviews:
        bot.send_message(user_id, texts["reviews_list_empty_ru"] if lang == "ru" else texts["reviews_list_empty_ua"])
        return
    text = "Отзывы:\n\n" if lang == "ru" else "Відгуки:\n\n"
    for r in reviews[-10:]:
        text += r + "\n\n"
    bot.send_message(user_id, text)

# ---------- ЗАКАЗЫ ПОЛЬЗОВАТЕЛЯ ----------
def show_user_orders(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, "ru")
    user_orders = [o for o in orders.values() if o["user_id"] == user_id]
    if not user_orders:
        bot.send_message(user_id,
                         "У вас пока нет заказов." if lang == "ru" else "У вас поки немає замовлень.")
        return
    text = "Ваши заказы:\n\n" if lang == "ru" else "Ваші замовлення:\n\n"
    for o in user_orders:
        status_translations = {
            "pending": {"ru": "Ожидает оплаты", "ua": "Очікує оплати"},
            "cod": {"ru": "Оплата при получении", "ua": "Оплата при отриманні"},
            "waiting_confirmation": {"ru": "Ожидает подтверждения", "ua": "Очікує підтвердження"},
            "paid": {"ru": "Оплачен", "ua": "Оплачено"},
        }
        status_text = status_translations.get(o["status"], {"ru": o["status"], "ua": o["status"]}).get(lang, o["status"])
        text += f"Заказ #{o['id']} — {status_text}\nСумма: {format_currency(o['total'])}\n\n"
    bot.send_message(user_id, text)

# ---------- RUN ----------
if __name__ == "__main__":
    print("Бот запущен")
    bot.infinity_polling()
