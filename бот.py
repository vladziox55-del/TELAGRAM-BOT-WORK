import telebot
from telebot import types

TOKEN = "8400828602:AAGmF8japcI3YkWRmvd2o9QXoohcYc4I7vQ"
bot = telebot.TeleBot(TOKEN)

ADMIN_CHAT_ID = 5539798707 # <--- замени на свой ID

# --- Хранилища данных ---
user_language = {}        # user_id -> "ru" или "ua"
user_carts = {}           # user_id -> list из product_key
orders = {}               # order_id -> dict с заказом
reviews = []              # список dict: {user_id, text, approved, visible}
referrals = {}            # user_id -> list user_id (рефералы)
user_spending = {}        # user_id -> сумма покупок рефералов

order_counter = 1

# --- Товары ---
cartridge_common_price = 145

PRODUCTS = {
    # Voopoo
    "voopoo_argus_3ml_07": {"name_ru": "Voopoo Argus 3ml 0.7", "name_ua": "Voopoo Argus 3ml 0.7", "price": cartridge_common_price, "category": "voopoo"},
    "voopoo_argus_3ml_10": {"name_ru": "Voopoo Argus 3ml 1.0", "name_ua": "Voopoo Argus 3ml 1.0", "price": cartridge_common_price, "category": "voopoo"},
    "voopoo_argus_3ml_04": {"name_ru": "Voopoo Argus 3ml 0.4", "name_ua": "Voopoo Argus 3ml 0.4", "price": cartridge_common_price, "category": "voopoo"},
    "voopoo_vmate_3ml_07": {"name_ru": "Voopoo Vmate 3ml 0.7", "name_ua": "Voopoo Vmate 3ml 0.7", "price": cartridge_common_price, "category": "voopoo"},
    "voopoo_vmate_2ml_07_tpd": {"name_ru": "Voopoo Vmate 2ml 0.7 (TPD)", "name_ua": "Voopoo Vmate 2ml 0.7 (TPD)", "price": cartridge_common_price, "category": "voopoo"},
    "voopoo_vmate_3ml_04": {"name_ru": "Voopoo Vmate 3ml 0.4", "name_ua": "Voopoo Vmate 3ml 0.4", "price": cartridge_common_price, "category": "voopoo"},
    "voopoo_vmate_2ml_04_tpd": {"name_ru": "Voopoo Vmate 2ml 0.4 (TPD)", "name_ua": "Voopoo Vmate 2ml 0.4 (TPD)", "price": cartridge_common_price, "category": "voopoo"},
    # Elf Bar ELFX
    "elfx_2ml_06": {"name_ru": "Elfx 2ml 0.6", "name_ua": "Elfx 2ml 0.6", "price": 135, "category": "elfx"},
    "elfx_2ml_08": {"name_ru": "Elfx 2ml 0.8", "name_ua": "Elfx 2ml 0.8", "price": 135, "category": "elfx"},
    # Vaporesso - постоянный каталог
    "vaporesso_xros_1_0_3ml": {"name_ru": "Vaporesso Xros Series 1.0, 3 ml", "name_ua": "Vaporesso Xros Series 1.0, 3 ml", "price": cartridge_common_price, "category": "vaporesso"},
    "vaporesso_xros_1_0_2ml": {"name_ru": "Vaporesso Xros Series 1.0, 2 ml", "name_ua": "Vaporesso Xros Series 1.0, 2 ml", "price": cartridge_common_price, "category": "vaporesso"},
    "vaporesso_xros_0_8_3ml": {"name_ru": "Vaporesso Xros Series 0.8, 3 ml", "name_ua": "Vaporesso Xros Series 0.8, 3 ml", "price": cartridge_common_price, "category": "vaporesso"},
    "vaporesso_xros_0_8_2ml": {"name_ru": "Vaporesso Xros Series 0.8, 2 ml", "name_ua": "Vaporesso Xros Series 0.8, 2 ml", "price": cartridge_common_price, "category": "vaporesso"},
    "vaporesso_xros_0_6_3ml": {"name_ru": "Vaporesso Xros Series 0.6, 3 ml", "name_ua": "Vaporesso Xros Series 0.6, 3 ml", "price": cartridge_common_price, "category": "vaporesso"},
    "vaporesso_xros_0_6_2ml": {"name_ru": "Vaporesso Xros Series 0.6, 2 ml", "name_ua": "Vaporesso Xros Series 0.6, 2 ml", "price": cartridge_common_price, "category": "vaporesso"},
    "vaporesso_xros_0_4_3ml": {"name_ru": "Vaporesso Xros Series 0.4, 3 ml", "name_ua": "Vaporesso Xros Series 0.4, 3 ml", "price": cartridge_common_price, "category": "vaporesso"},
    "vaporesso_xros_0_4_2ml": {"name_ru": "Vaporesso Xros Series 0.4, 2 ml", "name_ua": "Vaporesso Xros Series 0.4, 2 ml", "price": cartridge_common_price, "category": "vaporesso"},
}

PODS = {
    "vaporesso_xros_5_mini": {"name_ru": "Vaporesso xros 5 mini", "name_ua": "Vaporesso xros 5 mini", "price": 850},
    "vaporesso_xros_4_mini": {"name_ru": "Vaporesso xros 4 mini", "name_ua": "Vaporesso xros 4 mini", "price": 809},
    "vaporesso_xros_5": {"name_ru": "Vaporesso xros 5", "name_ua": "Vaporesso xros 5", "price": 1129},
    "elfx_pro": {"name_ru": "Elbar Bar ELFX Pro", "name_ua": "Elbar Bar ELFX Pro", "price": 849},
    "elf_bar_ev15000": {"name_ru": "Elf Bar EV15000", "name_ua": "Elf Bar EV15000", "price": 299},
    "voopoo_argus_g2": {"name_ru": "Voopoo Argus G2", "name_ua": "Voopoo Argus G2", "price": 1049},
    "voopoo_vmate_i2": {"name_ru": "Voopoo Vmate I2 (второе поколение)", "name_ua": "Voopoo Vmate I2 (друге покоління)", "price": 719},
}

# --- Переводы ---
def t(key, lang):
    texts = {
        "language_select": {"ru": "Выберите язык / Оберіть мову:", "ua": "Оберіть мову / Виберіть язык:"},
        "main_menu": {"ru": "Главное меню", "ua": "Головне меню"},
        "catalog": {"ru": "Каталог", "ua": "Каталог"},
        "cartridges": {"ru": "Картриджи", "ua": "Картриджі"},
        "pods": {"ru": "Под системы", "ua": "Під системи"},
        "liquids": {"ru": "Жидкости (в разработке)", "ua": "Рідини (в розробці)"},
        "back": {"ru": "Назад", "ua": "Назад"},
        "order_created": {"ru": "Заказ #{order_id} создан!", "ua": "Замовлення #{order_id} створено!"},
        "add_cart_success": {"ru": "Товар {name} добавлен в корзину", "ua": "Товар {name} додано в кошик"},
        "cart_empty": {"ru": "Корзина пуста", "ua": "Кошик порожній"},
        "cart_cleared": {"ru": "Корзина очищена", "ua": "Кошик очищено"},
        "pay_cod_info": {"ru": "Вы выбрали оплату при получении.", "ua": "Ви обрали оплату при отриманні."},
        "pay_prepay_info": {"ru": "Оплата картой. Внимание! Переводы принимаются только с карты Monobank. Иначе заказ будет аннулирован.", 
                           "ua": "Оплата картою. Увага! Перекази приймаються тільки з картки Monobank. Інакше замовлення буде анульовано."},
        "pay_crypto_info": {"ru": "Оплатите криптовалютой на адрес ниже.", "ua": "Оплатіть криптовалютою за адресою нижче."},
        "pay_done": {"ru": "Оплачено", "ua": "Оплачено"},
        "pay_done_wait": {"ru": "Ваш платеж ожидает подтверждения администратора.", "ua": "Ваш платіж очікує підтвердження адміністратора."},
        "pay_confirmed": {"ru": "Оплата подтверждена! Скоро с вами свяжутся.", "ua": "Оплата підтверджена! Незабаром з вами зв'яжуться."},
        "referral_notify": {"ru": "Ваши рефералы совершили покупки на сумму {sum} грн. Вы получаете подарок - любую жидкость из ассортимента или любые два картриджа на выбор. Спасибо что остаетесь с нами!", 
                           "ua": "Ваші реферали зробили покупки на суму {sum} грн. Ви отримуєте подарунок - будь-яку рідину з асортименту або будь-які два картриджі на вибір. Дякуємо, що залишаєтесь з нами!"},
        "review_prompt": {"ru": "Напишите ваш отзыв:", "ua": "Напишіть ваш відгук:"},
        "review_added": {"ru": "Спасибо за отзыв! Он будет рассмотрен администратором.", "ua": "Дякуємо за відгук! Він буде розглянутий адміністратором."},
        "order_status_paid": {"ru": "Оплачен ✅", "ua": "Оплачено ✅"},
        "order_status_completed": {"ru": "Завершён ✅", "ua": "Завершено ✅"},
        "confirm_received": {"ru": "Подтвердить получение", "ua": "Підтвердити отримання"},
        "orders_empty": {"ru": "У вас пока нет заказов.", "ua": "У вас поки немає замовлень."},
    }
    return texts.get(key, {}).get(lang, texts.get(key, {}).get("ru", key))

# --- Форматирование суммы ---
def format_currency(amount):
    return f"{amount} грн"

# --- Отправка уведомления админу ---
def notify_admin(text, reply_markup=None):
    bot.send_message(ADMIN_CHAT_ID, text, reply_markup=reply_markup)
 
 # --- Главное меню ---
def main_menu_markup(lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📚 " + t("catalog", lang), "🛒 Заказать")
    markup.row("🧺 Корзина", "👥 Реферальная система")
    markup.row("📦 Мои заказы")
    return markup

# --- Каталог: основное меню ---
def catalog_menu_markup(lang):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(t("cartridges", lang), callback_data="cat_cartridges"),
        types.InlineKeyboardButton(t("pods", lang), callback_data="cat_pods"),
        types.InlineKeyboardButton(t("liquids", lang), callback_data="cat_liquids"),
        types.InlineKeyboardButton(t("back", lang), callback_data="back_main")
    )
    return markup

# --- Меню подкатегорий картриджей ---
def cartridges_menu_markup(lang):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("Voopoo", callback_data="cat_voopoo"),
        types.InlineKeyboardButton("Vaporesso", callback_data="cat_vaporesso"),
        types.InlineKeyboardButton("Elf Bar ELFX", callback_data="cat_elfx"),
        types.InlineKeyboardButton(t("back", lang), callback_data="cat_cartridges_back")
    )
    return markup

# --- Меню товаров категории ---
def products_menu_markup(category, lang):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for key, p in PRODUCTS.items():
        if p["category"] == category:
            name = p["name_ru"] if lang == "ru" else p["name_ua"]
            markup.add(types.InlineKeyboardButton(f"{name} - {p['price']} грн", callback_data=f"add_{key}"))
    markup.add(types.InlineKeyboardButton(t("back", lang), callback_data="cat_cartridges"))
    return markup

# --- Меню подсистем (Pods) ---
def pods_menu_markup(lang):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for key, p in PODS.items():
        name = p["name_ru"] if lang == "ru" else p["name_ua"]
        markup.add(types.InlineKeyboardButton(f"{name} - {p['price']} грн", callback_data=f"add_pod_{key}"))
    markup.add(types.InlineKeyboardButton(t("back", lang), callback_data="cat_pods_back"))
    return markup

# --- Пустое меню для жидкости (в разработке) ---
def liquids_menu_markup(lang):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(t("back", lang), callback_data="cat_liquids_back"))
    return markup

# --- Получить корзину пользователя ---
def get_user_cart(user_id):
    return user_carts.setdefault(user_id, [])

# --- Добавить товар в корзину ---
def add_to_cart(user_id, product_key):
    cart = get_user_cart(user_id)
    cart.append(product_key)

# --- Очистить корзину ---
def clear_cart(user_id):
    user_carts[user_id] = []

# --- Подсчет суммы в корзине ---
def cart_total(user_id):
    cart = get_user_cart(user_id)
    total = 0
    for key in cart:
        # учитываем товары из PRODUCTS и PODS
        if key.startswith("pod_"):
            pod_key = key[4:]
            if pod_key in PODS:
                total += PODS[pod_key]["price"]
        elif key in PRODUCTS:
            total += PRODUCTS[key]["price"]
    return total

# --- Создать заказ ---
def create_order(user_id):
    global order_counter
    cart = get_user_cart(user_id)
    if not cart:
        return None
    total = cart_total(user_id)
    order_id = order_counter
    order_counter += 1
    orders[order_id] = {
        "id": order_id,
        "user_id": user_id,
        "items": cart.copy(),
        "total": total,
        "status": "created",
        "payment_method": None,
        "paid": False,
        "confirmed": False
    }
    clear_cart(user_id)
    return order_id

# --- Форматируем список товаров в заказе для вывода ---
def format_order_items(items, lang):
    lines = []
    for key in items:
        if key.startswith("pod_"):
            pod_key = key[4:]
            if pod_key in PODS:
                name = PODS[pod_key]["name_ru"] if lang == "ru" else PODS[pod_key]["name_ua"]
                price = PODS[pod_key]["price"]
                lines.append(f"{name} - {price} грн")
        elif key in PRODUCTS:
            p = PRODUCTS[key]
            name = p["name_ru"] if lang == "ru" else p["name_ua"]
            price = p["price"]
            lines.append(f"{name} - {price} грн")
    return "\n".join(lines)
    
    
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    if user_id not in user_language:
        # Запрос языка
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.row("Русский 🇷🇺", "Українська 🇺🇦")
        bot.send_message(user_id, "Выберите язык / Оберіть мову:", reply_markup=markup)
    else:
        lang = user_language[user_id]
        bot.send_message(user_id, t("main_menu", lang), reply_markup=main_menu_markup(lang))


@bot.message_handler(func=lambda m: m.text in ["Русский 🇷🇺", "Українська 🇺🇦"])
def set_language(message):
    user_id = message.from_user.id
    if message.text == "Русский 🇷🇺":
        user_language[user_id] = "ru"
    else:
        user_language[user_id] = "ua"
    lang = user_language[user_id]
    bot.send_message(user_id, t("main_menu", lang), reply_markup=main_menu_markup(lang))


@bot.message_handler(func=lambda m: True)
def main_menu_handler(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, "ru")
    text = message.text

    if text == "📚 " + t("catalog", lang):
        bot.send_message(user_id, t("catalog", lang), reply_markup=catalog_menu_markup(lang))
    elif text == "🛒 Заказать":
        bot.send_message(user_id, t("catalog", lang) + " (заказ)", reply_markup=catalog_menu_markup(lang))
    elif text == "🧺 Корзина":
        cart = get_user_cart(user_id)
        if not cart:
            bot.send_message(user_id, t("cart_empty", lang))
        else:
            total = cart_total(user_id)
            text_cart = format_order_items(cart, lang) + f"\n\nИтого: {format_currency(total)}"
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton("Оформить заказ", callback_data="checkout"),
                types.InlineKeyboardButton(t("back", lang), callback_data="back_main"),
                types.InlineKeyboardButton("Очистить корзину", callback_data="clear_cart")
            )
            bot.send_message(user_id, text_cart, reply_markup=markup)
    elif text == "👥 Реферальная система":
        # Покажем сколько человек приглашено и потрачено
        refs = referrals.get(user_id, [])
        spent = user_spending.get(user_id, 0)
        ref_link = f"https://t.me/your_bot_username?start={user_id}"  # замените на ваш username
        bot.send_message(user_id,
                         f"Вы пригласили: {len(refs)} человек(а).\n"
                         f"Потрачено вашими рефералами: {format_currency(spent)}\n"
                         f"Ваша реферальная ссылка:\n{ref_link}")
    elif text == "📦 Мои заказы":
        user_orders = [o for o in orders.values() if o["user_id"] == user_id]
        if not user_orders:
            bot.send_message(user_id, t("orders_empty", lang))
        else:
            for o in user_orders:
                items_text = format_order_items(o["items"], lang)
                status_text = t("order_status_paid", lang) if o["paid"] else o["status"]
                msg = f"Заказ #{o['id']}:\n{items_text}\nСумма: {format_currency(o['total'])}\nСтатус: {status_text}"
                markup = types.InlineKeyboardMarkup()
                if o["paid"] and not o["confirmed"]:
                    markup.add(types.InlineKeyboardButton(t("confirm_received", lang), callback_data=f"confirm_{o['id']}"))
                bot.send_message(user_id, msg, reply_markup=markup)
    elif text == "⭐ Отзывы":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("Оставить отзыв", callback_data="review_add"),
            types.InlineKeyboardButton("Посмотреть отзывы", callback_data="review_show"),
            types.InlineKeyboardButton(t("back", lang), callback_data="back_main")
        )
        bot.send_message(user_id, "Отзывы", reply_markup=markup)
    else:
        bot.send_message(user_id, "Команда не распознана. Пожалуйста, выберите пункт меню.")


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    lang = user_language.get(user_id, "ru")
    data = call.data

    # Навигация назад
    if data == "back_main":
        bot.edit_message_text(t("main_menu", lang), user_id, call.message.message_id, reply_markup=None)
        bot.send_message(user_id, t("main_menu", lang), reply_markup=main_menu_markup(lang))
        bot.answer_callback_query(call.id)
        return

    # Каталог
    if data == "cat_cartridges":
        bot.edit_message_text(t("cartridges", lang), user_id, call.message.message_id,
                              reply_markup=cartridges_menu_markup(lang))
        bot.answer_callback_query(call.id)
        return
    if data == "cat_pods":
        bot.edit_message_text(t("pods", lang), user_id, call.message.message_id,
                              reply_markup=pods_menu_markup(lang))
        bot.answer_callback_query(call.id)
        return
    if data == "cat_liquids":
        bot.edit_message_text(t("liquids", lang), user_id, call.message.message_id,
                              reply_markup=liquids_menu_markup(lang))
        bot.answer_callback_query(call.id)
        return

    # Картриджи — подкатегории
    if data == "cat_voopoo":
        bot.edit_message_text("Voopoo", user_id, call.message.message_id,
                              reply_markup=products_menu_markup("voopoo", lang))
        bot.answer_callback_query(call.id)
        return
    if data == "cat_vaporesso":
        bot.edit_message_text("Vaporesso", user_id, call.message.message_id,
                              reply_markup=products_menu_markup("vaporesso", lang))
        bot.answer_callback_query(call.id)
        return
    if data == "cat_elfx":
        bot.edit_message_text("Elf Bar ELFX", user_id, call.message.message_id,
                              reply_markup=products_menu_markup("elfx", lang))
        bot.answer_callback_query(call.id)
        return

    if data == "cat_cartridges_back":
        bot.edit_message_text(t("catalog", lang), user_id, call.message.message_id,
                              reply_markup=catalog_menu_markup(lang))
        bot.answer_callback_query(call.id)
        return

    # Добавление товара в корзину из каталога
    if data.startswith("add_"):
        product_key = data[4:]
        add_to_cart(user_id, product_key)
        product_name = ""
        if product_key.startswith("pod_"):
            pod_key = product_key[4:]
            product_name = PODS.get(pod_key, {}).get("name_ru", "Товар")
        else:
            product_name = PRODUCTS.get(product_key, {}).get("name_ru", "Товар")
        bot.answer_callback_query(call.id, text=f"Добавлено: {product_name}")
        return

    # Очистить корзину
    if data == "clear_cart":
        clear_cart(user_id)
        bot.edit_message_text(t("cart_cleared", lang), user_id, call.message.message_id)
        bot.answer_callback_query(call.id)
        return

    # Оформление заказа
    if data == "checkout":
        order_id = create_order(user_id)
        if not order_id:
            bot.answer_callback_query(call.id, text="Корзина пуста!")
            return
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("Оплата при получении", callback_data=f"pay_cod_{order_id}"),
            types.InlineKeyboardButton("Оплата картой", callback_data=f"pay_card_{order_id}"),
            types.InlineKeyboardButton("Оплата криптовалютой", callback_data=f"pay_crypto_{order_id}"),
            types.InlineKeyboardButton(t("back", lang), callback_data="back_main")
        )
        bot.edit_message_text(f"Выберите способ оплаты для заказа #{order_id}:", user_id, call.message.message_id,
                              reply_markup=markup)
        bot.answer_callback_query(call.id)
        return

    # Оплата при получении
    if data.startswith("pay_cod_"):
        order_id = int(data.split("_")[-1])
        orders[order_id]["payment_method"] = "cod"
        orders[order_id]["paid"] = False
        # Уведомление админу
        notify_admin(f"Пользователь @{call.from_user.username or call.from_user.id} оформил заказ #{order_id} с оплатой при получении.")
        bot.edit_message_text(t("pay_cod_info", lang), user_id, call.message.message_id)
        bot.answer_callback_query(call.id)
        return

    # Оплата картой
    if data.startswith("pay_card_"):
        order_id = int(data.split("_")[-1])
        orders[order_id]["payment_method"] = "card"
        orders[order_id]["paid"] = False
        payment_info = (
            f"{t('pay_prepay_info', lang)}\n\n"
            "Владислав Г.\n"
            "4441 1110 3909 5051\n\n"
            "После оплаты нажмите кнопку ниже."
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t("pay_done", lang), callback_data=f"paid_confirm_{order_id}"))
        bot.edit_message_text(payment_info, user_id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id)
        return

    # Оплата криптой
    if data.startswith("pay_crypto_"):
        order_id = int(data.split("_")[-1])
        orders[order_id]["payment_method"] = "crypto"
        orders[order_id]["paid"] = False
        payment_info = (
            f"{t('pay_crypto_info', lang)}\n\n"
            "TON Wallet:\n"
            "UQDjclQadIIq-DUoTNY53oHfcp9WVi5mRVnUVxVUnQ-vznEc\n\n"
            "После оплаты нажмите кнопку ниже."
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t("pay_done", lang), callback_data=f"paid_confirm_{order_id}"))
        bot.edit_message_text(payment_info, user_id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id)
        return

    # Подтверждение оплаты пользователем
    if data.startswith("paid_confirm_"):
        order_id = int(data.split("_")[-1])
        bot.edit_message_text(t("pay_done_wait", lang), user_id, call.message.message_id)
        notify_admin(
            f"Пользователь @{call.from_user.username or call.from_user.id} сообщил об оплате заказа #{order_id}.",
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("Подтвердить оплату", callback_data=f"admin_confirm_{order_id}")
            )
        )
        orders[order_id]["paid"] = True
        bot.answer_callback_query(call.id)
        return

    # Админ подтверждает оплату
    if data.startswith("admin_confirm_"):
        if call.from_user.id != ADMIN_CHAT_ID:
            bot.answer_callback_query(call.id, text="Доступ запрещён.")
            return
        order_id = int(data.split("_")[-1])
        orders[order_id]["paid"] = True
        orders[order_id]["status"] = "paid"
        user_id_order = orders[order_id]["user_id"]
        bot.send_message(user_id_order, t("pay_confirmed", user_language.get(user_id_order, "ru")))
        bot.edit_message_text(f"Оплата заказа #{order_id} подтверждена.", call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id)

        # Начисление реферальных сумм
        referrer_id = None
        for ref_id, refs in referrals.items():
            if user_id_order in refs:
                referrer_id = ref_id
                break
        if referrer_id:
            user_spending[referrer_id] = user_spending.get(referrer_id, 0) + orders[order_id]["total"]
            if user_spending[referrer_id] >= 4100:
                # Отправить уведомление о подарке
                bot.send_message(referrer_id, t("referral_notify", user_language.get(referrer_id, "ru")).format(sum=user_spending[referrer_id]))

        return

    # Подтверждение получения заказа пользователем
    if data.startswith("confirm_"):
        order_id = int(data.split("_")[-1])
        order = orders.get(order_id)
        if order and order["user_id"] == user_id:
            order["confirmed"] = True
            order["status"] = "completed"
            bot.edit_message_text(f"Заказ #{order_id} {t('order_status_completed', lang)}", user_id, call.message.message_id)
            bot.answer_callback_query(call.id)
        else:
            bot.answer_callback_query(call.id, text="Ошибка.")

    # Обработка отзывов
    if data == "review_add":
        msg = bot.send_message(user_id, t("review_prompt", lang))
        bot.register_next_step_handler(msg, handle_review_text)
        bot.answer_callback_query(call.id)
        return
    if data == "review_show":
        approved_reviews = [r for r in reviews if r.get("approved")]
        if not approved_reviews:
            bot.send_message(user_id, "Пока нет отзывов.")
        else:
            text = "\n\n".join([r["text"] for r in approved_reviews[-10:]])
            bot.send_message(user_id, text)
        bot.answer_callback_query(call.id)
        return

def handle_review_text(message):
    user_id = message.from_user.id
    text = message.text.strip()
    if len(text) < 3:
        bot.send_message(user_id, "Отзыв слишком короткий, попробуйте еще раз.")
        return
    reviews.append({"user_id": user_id, "text": text, "approved": False})
    bot.send_message(user_id, t("review_added", user_language.get(user_id, "ru")))
    # Отправить администратору
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Одобрить", callback_data=f"review_approve_{len(reviews)-1}"),
        types.InlineKeyboardButton("Удалить", callback_data=f"review_delete_{len(reviews)-1}")
    )
    bot.send_message(ADMIN_CHAT_ID, f"Новый отзыв от @{message.from_user.username or user_id}:\n\n{text}", reply_markup=markup)

# Модерация отзывов админом
@bot.callback_query_handler(func=lambda call: call.data.startswith("review_"))
def review_moderation_handler(call):
    if call.from_user.id != ADMIN_CHAT_ID:
        bot.answer_callback_query(call.id, "Доступ запрещён.")
        return
    data = call.data
    action, idx = data.split("_")[1], int(data.split("_")[2])
    if idx < 0 or idx >= len(reviews):
        bot.answer_callback_query(call.id, "Ошибка.")
        return
    if action == "approve":
        reviews[idx]["approved"] = True
        bot.edit_message_text("Отзыв одобрен.", call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id)
    elif action == "delete":
        reviews.pop(idx)
        bot.edit_message_text("Отзыв удалён.", call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id)
        
@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.from_user.id
    text = message.text
    # Проверяем есть ли параметр реферала
    ref_id = None
    if " " in text:
        parts = text.split()
        if len(parts) > 1 and parts[1].isdigit():
            ref_id = int(parts[1])
    # Если нового пользователя — установим язык и добавим в рефералы
    if user_id not in user_language:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.row("Русский 🇷🇺", "Українська 🇺🇦")
        bot.send_message(user_id, "Выберите язык / Оберіть мову:", reply_markup=markup)
    else:
        lang = user_language[user_id]
        bot.send_message(user_id, t("main_menu", lang), reply_markup=main_menu_markup(lang))

    # Если есть реферал и он не сам себе
    if ref_id and ref_id != user_id:
        # Добавляем в рефералы
        refs = referrals.setdefault(ref_id, [])
        if user_id not in refs:
            refs.append(user_id)

# --- Вспомогательные функции ---

def add_to_cart(user_id, product_key):
    cart = user_carts.setdefault(user_id, [])
    cart.append(product_key)

def clear_cart(user_id):
    user_carts[user_id] = []

def cart_total(user_id):
    cart = get_user_cart(user_id)
    total = 0
    for key in cart:
        if key.startswith("pod_"):
            total += PODS.get(key[4:], {}).get("price", 0)
        else:
            total += PRODUCTS.get(key, {}).get("price", 0)
    return total

def format_order_items(items, lang):
    lines = []
    for key in items:
        if key.startswith("pod_"):
            p = PODS.get(key[4:], None)
            if p:
                name = p["name_ru"] if lang == "ru" else p["name_ua"]
                lines.append(f"• {name} - {format_currency(p['price'])}")
        else:
            p = PRODUCTS.get(key, None)
            if p:
                name = p["name_ru"] if lang == "ru" else p["name_ua"]
                lines.append(f"• {name} - {format_currency(p['price'])}")
    return "\n".join(lines)

def create_order(user_id):
    cart = get_user_cart(user_id)
    if not cart:
        return None
    total = cart_total(user_id)
    global order_counter
    order_id = order_counter
    order_counter += 1
    orders[order_id] = {
        "id": order_id,
        "user_id": user_id,
        "items": cart.copy(),
        "total": total,
        "status": "created",
        "paid": False,
        "confirmed": False,
        "payment_method": None,
    }
    clear_cart(user_id)
    return order_id
    
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    lang = user_language.get(user_id, "ru")
    data = call.data

    # Назад в главное меню
    if data == "back_main":
        bot.edit_message_text(t("main_menu", lang), user_id, call.message.message_id, reply_markup=None)
        bot.send_message(user_id, t("main_menu", lang), reply_markup=main_menu_markup(lang))
        bot.answer_callback_query(call.id)
        return

    # Основное меню -> Каталог
    if data == "catalog":
        bot.edit_message_text(t("catalog", lang), user_id, call.message.message_id, reply_markup=catalog_menu_markup(lang))
        bot.answer_callback_query(call.id)
        return

    # Каталог -> Картриджи
    if data == "cat_cartridges":
        bot.edit_message_text(t("cartridges", lang), user_id, call.message.message_id, reply_markup=cartridges_menu_markup(lang))
        bot.answer_callback_query(call.id)
        return

    # Картриджи -> Voopoo
    if data == "cat_voopoo":
        bot.edit_message_text("Voopoo - выберите товар:", user_id, call.message.message_id,
                              reply_markup=products_menu_markup("voopoo", lang))
        bot.answer_callback_query(call.id)
        return

    # Картриджи -> Vaporesso
    if data == "cat_vaporesso":
        bot.edit_message_text("Vaporesso - выберите товар:", user_id, call.message.message_id,
                              reply_markup=products_menu_markup("vaporesso", lang))
        bot.answer_callback_query(call.id)
        return

    # Картриджи -> Elf Bar ELFX
    if data == "cat_elfx":
        bot.edit_message_text("Elf Bar ELFX - выберите товар:", user_id, call.message.message_id,
                              reply_markup=products_menu_markup("elfx", lang))
        bot.answer_callback_query(call.id)
        return

    # Каталог -> Под системы (pods)
    if data == "cat_pods":
        markup = types.InlineKeyboardMarkup(row_width=1)
        for key, p in PODS.items():
            name = p["name_ru"] if lang == "ru" else p["name_ua"]
            markup.add(types.InlineKeyboardButton(f"{name} - {p['price']} грн", callback_data=f"add_{key}"))
        markup.add(types.InlineKeyboardButton(t("back", lang), callback_data="catalog"))
        bot.edit_message_text(t("pods", lang), user_id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id)
        return

    # Каталог -> Жидкости (в разработке)
    if data == "cat_liquids":
        bot.answer_callback_query(call.id, t("liquids", lang), show_alert=True)
        return

    # Кнопка назад в картриджах
    if data == "cat_cartridges_back":
        bot.edit_message_text(t("catalog", lang), user_id, call.message.message_id, reply_markup=catalog_menu_markup(lang))
        bot.answer_callback_query(call.id)
        return

    # Добавление товара в корзину
    if data.startswith("add_"):
        product_key = data[4:]
        if product_key in PRODUCTS or product_key in PODS:
            add_to_cart(user_id, product_key)
            name = (PRODUCTS.get(product_key) or PODS.get(product_key))["name_ru"] if lang == "ru" else (PRODUCTS.get(product_key) or PODS.get(product_key))["name_ua"]
            bot.answer_callback_query(call.id, t("add_cart_success", lang).format(name=name))
        else:
            bot.answer_callback_query(call.id, "Товар не найден", show_alert=True)
        return

    # Показать корзину
    if data == "show_cart":
        cart = get_user_cart(user_id)
        if not cart:
            bot.answer_callback_query(call.id, t("cart_empty", lang), show_alert=True)
            return
        text = "🧺 Корзина:\n\n" + format_order_items(cart, lang) + f"\n\nИтого: {format_currency(cart_total(user_id))}"
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("Оформить заказ", callback_data="order"),
            types.InlineKeyboardButton(t("cart_cleared", lang), callback_data="clear_cart"),
            types.InlineKeyboardButton(t("back", lang), callback_data="back_main")
        )
        bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id)
        return

    # Очистить корзину
    if data == "clear_cart":
        clear_cart(user_id)
        bot.answer_callback_query(call.id, t("cart_cleared", lang))
        bot.delete_message(user_id, call.message.message_id)
        return

    # Оформить заказ - выбор способа оплаты
    if data == "order":
        cart = get_user_cart(user_id)
        if not cart:
            bot.answer_callback_query(call.id, t("cart_empty", lang), show_alert=True)
            return
        total = cart_total(user_id)
        order_id = create_order(user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("Оплата при получении", callback_data=f"pay_cod_{order_id}"),
            types.InlineKeyboardButton("Оплата картой", callback_data=f"pay_prepay_{order_id}"),
            types.InlineKeyboardButton("Оплата криптовалютой", callback_data=f"pay_crypto_{order_id}"),
            types.InlineKeyboardButton(t("back", lang), callback_data="show_cart")
        )
        bot.send_message(user_id, t("order_created", lang).format(order_id=order_id), reply_markup=markup)
        bot.answer_callback_query(call.id)
        return

    # Оплата при получении
    if data.startswith("pay_cod_"):
        order_id = int(data.split("_")[-1])
        order = orders.get(order_id)
        if not order or order["user_id"] != user_id:
            bot.answer_callback_query(call.id, "Заказ не найден", show_alert=True)
            return
        order["payment_method"] = "cod"
        order["status"] = "paid"
        bot.edit_message_text(t("pay_cod_info", lang), user_id, call.message.message_id)
        bot.answer_callback_query(call.id)
        notify_admin(f"Новый заказ #{order_id} от @{call.from_user.username or call.from_user.first_name}\nМетод оплаты: Оплата при получении\nСумма: {format_currency(order['total'])}")
        return

    # Оплата картой
    if data.startswith("pay_prepay_"):
        order_id = int(data.split("_")[-1])
        order = orders.get(order_id)
        if not order or order["user_id"] != user_id:
            bot.answer_callback_query(call.id, "Заказ не найден", show_alert=True)
            return
        order["payment_method"] = "card"
        order["status"] = "waiting_confirmation"
        text = t("pay_prepay_info", lang) + "\n\n" + "Владислав Г. 4441111039095051"
        bot.edit_message_text(text, user_id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t("pay_done", lang), callback_data=f"pay_done_{order_id}"))
        bot.send_message(user_id, "💳 Оплатили? Нажмите кнопку ниже для подтверждения.", reply_markup=markup)
        bot.answer_callback_query(call.id)
        return

    # Оплата криптовалютой
    if data.startswith("pay_crypto_"):
        order_id = int(data.split("_")[-1])
        order = orders.get(order_id)
        if not order or order["user_id"] != user_id:
            bot.answer_callback_query(call.id, "Заказ не найден", show_alert=True)
            return
        order["payment_method"] = "crypto"
        order["status"] = "waiting_confirmation"
        crypto_text = t("pay_crypto_info", lang) + "\n\n" + "UQDjclQadIIq-DUoTNY53oHfcp9WVi5mRVnUVxVUnQ-vznEc (TON)"
        bot.edit_message_text(crypto_text, user_id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t("pay_done", lang), callback_data=f"pay_done_{order_id}"))
        bot.send_message(user_id, "💳 Оплатили? Нажмите кнопку ниже для подтверждения.", reply_markup=markup)
        bot.answer_callback_query(call.id)
        return

    # Подтверждение оплаты пользователем (кнопка "Оплачено")
    if data.startswith("pay_done_"):
        order_id = int(data.split("_")[-1])
        order = orders.get(order_id)
        if not order or order["user_id"] != user_id:
            bot.answer_callback_query(call.id, "Заказ не найден", show_alert=True)
            return
        if order["status"] != "waiting_confirmation":
            bot.answer_callback_query(call.id, "Ваш заказ уже в обработке.", show_alert=True)
            return
        order["status"] = "waiting_admin_confirmation"
        bot.send_message(user_id, t("pay_done_wait", lang))

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(f"Подтвердить оплату заказа #{order_id}", callback_data=f"admin_confirm_{order_id}"))

        notify_admin(f"Пользователь @{call.from_user.username or call.from_user.first_name} подтвердил оплату заказа #{order_id}, сумма: {format_currency(order['total'])}", reply_markup=markup)
        bot.answer_callback_query(call.id)
        return

    # Подтверждение оплаты админом
    if data.startswith("admin_confirm_") and user_id == ADMIN_CHAT_ID:
        order_id = int(data.split("_")[-1])
        order = orders.get(order_id)
        if not order:
            bot.answer_callback_query(call.id, "Заказ не найден", show_alert=True)
            return
        if order["status"] != "waiting_admin_confirmation":
            bot.answer_callback_query(call.id, "Заказ уже подтвержден или отменен", show_alert=True)
            return
        order["status"] = "paid"
        bot.answer_callback_query(call.id, f"Оплата заказа #{order_id} подтверждена")
        buyer_id = order["user_id"]
        lang_buyer = user_language.get(buyer_id, "ru")
        bot.send_message(buyer_id, t("pay_confirmed", lang_buyer))

        # Обновление статистики по рефералам
        referrer = None
        for ref, referred_list in referrals.items():
            if buyer_id in referred_list:
                referrer = ref
                break
        if referrer:
            user_spending[referrer] = user_spending.get(referrer, 0) + order["total"]
            if user_spending[referrer] >= 4100:
                lang_ref = user_language.get(referrer, "ru")
                bot.send_message(referrer, t("referral_notify", lang_ref).format(sum=user_spending[referrer]))

        return
        
     # --- Запрос на отзыв ---
waiting_for_review = set()  # user_id, кто сейчас пишет отзыв

@bot.message_handler(func=lambda m: m.from_user.id in waiting_for_review)
def handle_review_message(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, "ru")
    text = message.text.strip()
    if not text:
        bot.reply_to(message, t("review_prompt", lang))
        return
    # Добавляем отзыв в список, approved=False
    reviews.append({"user_id": user_id, "text": text, "approved": False})
    waiting_for_review.remove(user_id)
    bot.reply_to(message, t("review_added", lang))
    # Уведомляем админа с кнопками модерации
    idx = len(reviews) - 1
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Показать", callback_data=f"show_review_{idx}"),
        types.InlineKeyboardButton("Удалить", callback_data=f"del_review_{idx}")
    )
    notify_admin(f"Новый отзыв от @{message.from_user.username or message.from_user.first_name}:\n\n{text}", reply_markup=markup)

# --- Запрос на отзыв ---
waiting_for_review = set()  # user_id, кто сейчас пишет отзыв

@bot.message_handler(func=lambda m: m.from_user.id in waiting_for_review)
def handle_review_message(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, "ru")
    text = message.text.strip()
    if not text:
        bot.reply_to(message, t("review_prompt", lang))
        return
    # Добавляем отзыв в список, approved=False
    reviews.append({"user_id": user_id, "text": text, "approved": False})
    waiting_for_review.remove(user_id)
    bot.reply_to(message, t("review_added", lang))
    # Уведомляем админа с кнопками модерации
    idx = len(reviews) - 1
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Одобрить", callback_data=f"approve_review_{idx}"),
        types.InlineKeyboardButton("Удалить", callback_data=f"delete_review_{idx}")
    )
    notify_admin(f"Новый отзыв от @{message.from_user.username or message.from_user.first_name}:\n\n{text}", reply_markup=markup)

# --- Мои заказы ---
def user_orders_menu(user_id):
    lang = user_language.get(user_id, "ru")
    user_orders = [o for o in orders.values() if o["user_id"] == user_id]
    if not user_orders:
        return t("orders_empty", lang), None
    text = "Ваши заказы:\n\n"
    markup = types.InlineKeyboardMarkup(row_width=1)
    for o in user_orders:
        status = t("order_status_paid", lang) if o["status"] == "paid" else t("order_status_completed", lang) if o["status"] == "completed" else o["status"]
        text += f"#{o['id']} — {format_currency(o['total'])} — {status}\n"
        if o["status"] == "paid":
            markup.add(types.InlineKeyboardButton(f"{t('confirm_received', lang)} #{o['id']}", callback_data=f"confirm_received_{o['id']}"))
    markup.add(types.InlineKeyboardButton(t("back", lang), callback_data="back_main"))
    return text, markup

@bot.callback_query_handler(func=lambda call: call.data.startswith("my_orders"))
def my_orders_handler(call):
    user_id = call.from_user.id
    lang = user_language.get(user_id, "ru")
    text, markup = user_orders_menu(user_id)
    if markup:
        bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
    else:
        bot.edit_message_text(text, user_id, call.message.message_id)
    bot.answer_callback_query(call.id)

# --- Подтверждение получения ---
@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_received_"))
def confirm_received_handler(call):
    user_id = call.from_user.id
    lang = user_language.get(user_id, "ru")
    order_id = int(call.data.split("_")[-1])
    order = orders.get(order_id)
    if not order or order["user_id"] != user_id:
        bot.answer_callback_query(call.id, "Заказ не найден", show_alert=True)
        return
    if order["status"] != "paid":
        bot.answer_callback_query(call.id, "Заказ нельзя подтвердить", show_alert=True)
        return
    order["status"] = "completed"
    bot.edit_message_text(f"Заказ #{order_id} {t('order_status_completed', lang)}", user_id, call.message.message_id)
    bot.answer_callback_query(call.id, "Спасибо за подтверждение!")
    
    import hashlib

# --- Получить или создать реферальную ссылку для пользователя ---
def get_referral_link(user_id):
    base_url = "https://t.me/your_bot_username?start="
    # Например, хэш или просто user_id для уникальной ссылки
    ref_code = str(user_id)
    return base_url + ref_code

# --- Добавить реферала при старте ---
@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, "ru")
    
    # Проверяем наличие параметра start для реферала
    if message.text and len(message.text.split()) > 1:
        ref_code = message.text.split()[1]
        try:
            referrer_id = int(ref_code)
            if referrer_id != user_id:
                referrals.setdefault(referrer_id, set()).add(user_id)
        except ValueError:
            pass
    
    if user_id not in user_language:
        # Предлагаем выбрать язык (пример)
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("Русский 🇷🇺", callback_data="set_lang_ru"),
            types.InlineKeyboardButton("Українська 🇺🇦", callback_data="set_lang_ua")
        )
        bot.send_message(user_id, "Выберите язык / Оберіть мову", reply_markup=markup)
    else:
        send_main_menu(user_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("set_lang_"))
def set_language(call):
    user_id = call.from_user.id
    lang_code = call.data.split("_")[-1]
    user_language[user_id] = lang_code
    bot.answer_callback_query(call.id, f"Язык установлен: {'Русский' if lang_code == 'ru' else 'Українська'}")
    send_main_menu(user_id)

# --- Показать статистику рефералов ---
def referral_menu_markup(user_id):
    lang = user_language.get(user_id, "ru")
    ref_list = referrals.get(user_id, set())
    count = len(ref_list)
    spent = user_spending.get(user_id, 0)

    text = (f"Вы привели: {count} человек\n"
            f"Общая сумма покупок ваших рефералов: {format_currency(spent)}\n\n"
            f"Ваша реферальная ссылка:\n{get_referral_link(user_id)}")

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(t("back", lang), callback_data="back_main"))
    return text, markup

@bot.message_handler(func=lambda m: m.text == "👥 Реферальная система")
def referral_system_handler(message):
    user_id = message.from_user.id
    text, markup = referral_menu_markup(user_id)
    bot.send_message(user_id, text, reply_markup=markup)

# --- Обновление суммы покупок у рефералов при подтверждении оплаты ---
def update_referral_spending(user_id, amount):
    # Найти, кто пригласил user_id
    for referrer, refs in referrals.items():
        if user_id in refs:
            user_spending[referrer] = user_spending.get(referrer, 0) + amount
            # Проверяем достижение порога 4100
            if user_spending[referrer] >= 4100:
                lang = user_language.get(referrer, "ru")
                text = t("referral_notify", lang).format(sum=user_spending[referrer])
                bot.send_message(referrer, text)

# --- Вызов update_referral_spending() при подтверждении оплаты ---
# В обработчике подтверждения оплаты нужно добавить:
# update_referral_spending(order["user_id"], order["total"])

# --- Обработка отзывов ---
def reviews_menu_markup(lang):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("Оставить отзыв", callback_data="leave_review"),
        types.InlineKeyboardButton("Посмотреть отзывы", callback_data="view_reviews"),
        types.InlineKeyboardButton(t("back", lang), callback_data="back_main")
    )
    return markup

def view_reviews_text(lang):
    approved_reviews = [r for r in reviews if r.get("approved")]
    if not approved_reviews:
        return "Пока нет отзывов." if lang == "ru" else "Поки немає відгуків."
    text = ""
    for i, review in enumerate(approved_reviews, 1):
        text += f"{i}. {review['text']}\n\n"
    return text

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    lang = user_language.get(user_id, "ru")
    data = call.data

    # ... здесь идут предыдущие обработчики ...

    if data == "reviews_menu":
        bot.edit_message_text("Отзывы:" if lang == "ru" else "Відгуки:", user_id, call.message.message_id, reply_markup=reviews_menu_markup(lang))
        bot.answer_callback_query(call.id)
        return

    if data == "leave_review":
        msg = bot.send_message(user_id, t("review_prompt", lang))
        bot.register_next_step_handler(msg, process_review_step)
        bot.answer_callback_query(call.id)
        return

    if data == "view_reviews":
        text = view_reviews_text(lang)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t("back", lang), callback_data="reviews_menu"))
        bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id)
        return

    # Админские кнопки для управления отзывами
    if data.startswith("approve_review_") and user_id == ADMIN_CHAT_ID:
        idx = int(data.split("_")[-1])
        if 0 <= idx < len(reviews):
            reviews[idx]["approved"] = True
            bot.answer_callback_query(call.id, "Отзыв одобрен")
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        else:
            bot.answer_callback_query(call.id, "Отзыв не найден", show_alert=True)
        return

    if data.startswith("delete_review_") and user_id == ADMIN_CHAT_ID:
        idx = int(data.split("_")[-1])
        if 0 <= idx < len(reviews):
            reviews.pop(idx)
            bot.answer_callback_query(call.id, "Отзыв удалён")
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        else:
            bot.answer_callback_query(call.id, "Отзыв не найден", show_alert=True)
        return

def process_review_step(message):
    user_id = message.from_user.id
    text = message.text
    reviews.append({"user_id": user_id, "text": text, "approved": False})
    bot.send_message(user_id, t("review_added", user_language.get(user_id, "ru")))
    # Уведомление админу с кнопками одобрения/удаления
    markup = types.InlineKeyboardMarkup()
    idx = len(reviews) - 1
    markup.add(
        types.InlineKeyboardButton("Показать отзыв", callback_data=f"approve_review_{idx}"),
        types.InlineKeyboardButton("Удалить отзыв", callback_data=f"delete_review_{idx}")
    )
    notify_admin(f"Новый отзыв от пользователя @{message.from_user.username or message.from_user.first_name}:\n\n{text}", reply_markup=markup)
    
    # --- Реферальная система ---

def referral_menu_markup(lang):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📊 Мои рефералы", callback_data="referral_stats"),
        types.InlineKeyboardButton(t("back", lang), callback_data="back_main")
    )
    return markup

@bot.message_handler(func=lambda message: message.text in ["👥 Реферальная система", "Реферальная система", "Referral system"])
def referral_menu(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, "ru")
    bot.send_message(user_id, "Реферальная система", reply_markup=referral_menu_markup(lang))

@bot.callback_query_handler(func=lambda call: call.data.startswith("referral_"))
def referral_callback_handler(call):
    user_id = call.from_user.id
    lang = user_language.get(user_id, "ru")
    data = call.data

    if data == "referral_stats":
        # Получаем список рефералов и их сумму покупок
        refs = referrals.get(user_id, [])
        total_spent = user_spending.get(user_id, 0)

        text = f"Вы пригласили {len(refs)} пользователей.\nОбщая сумма покупок ваших рефералов: {total_spent} грн.\n\n"
        text += f"Ваша реферальная ссылка:\nhttps://t.me/YourBotUsername?start={user_id}\n\n"
        text += ("🎁 При достижении суммы 4100 грн вы получаете подарок — любую жидкость или два картриджа на выбор!\n"
                 "Спасибо, что остаетесь с нами!")

        bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=referral_menu_markup(lang))
        bot.answer_callback_query(call.id)
        return

    if data == "back_main":
        bot.edit_message_text(t("main_menu", lang), user_id, call.message.message_id, reply_markup=main_menu_markup(lang))
        bot.answer_callback_query(call.id)
        return

# --- При регистрации пользователя с реферальным кодом ---
@bot.message_handler(commands=["start"])
def start_handler(message):
    user_id = message.from_user.id
    lang = "ru"  # Можно расширить выбор языка
    user_language[user_id] = lang

    args = message.text.split()
    if len(args) > 1:
        ref_id_str = args[1]
        try:
            ref_id = int(ref_id_str)
            if ref_id != user_id:
                # Добавляем реферала
                referrals.setdefault(ref_id, set()).add(user_id)
        except Exception:
            pass

    bot.send_message(user_id, t("main_menu", lang), reply_markup=main_menu_markup(lang))

# --- Функция обновления трат рефералов при подтверждении оплаты ---
def update_referral_spending(purchaser_id, amount):
    for referrer, referred_set in referrals.items():
        if purchaser_id in referred_set:
            current_spent = user_spending.get(referrer, 0)
            user_spending[referrer] = current_spent + amount

            # Проверка на подарок
            if user_spending[referrer] >= 4100:
                lang = user_language.get(referrer, "ru")
                bot.send_message(referrer, t("referral_notify", lang).format(sum=user_spending[referrer]))

# Вызывать update_referral_spending при подтверждении оплаты админом

# --- Меню Мои заказы ---
def my_orders_menu_markup(user_id, lang):
    markup = types.InlineKeyboardMarkup(row_width=1)
    user_orders = [order for order in orders.values() if order["user_id"] == user_id]
    if not user_orders:
        markup.add(types.InlineKeyboardButton(t("back", lang), callback_data="back_main"))
        return markup

    for order in user_orders:
        status = order["status"]
        total = format_currency(order["total"])
        text = f"Заказ #{order['id']}: {total}\nСтатус: "
        if status == "paid":
            text += t("order_status_paid", lang)
        elif status == "completed":
            text += t("order_status_completed", lang)
        else:
            text += status

        # Кнопка подтверждения получения (если оплачено, но не завершено)
        buttons = []
        if status == "paid":
            buttons.append(types.InlineKeyboardButton(t("confirm_received", lang), callback_data=f"confirm_receive_{order['id']}"))
        buttons.append(types.InlineKeyboardButton(t("back", lang), callback_data="back_main"))

        for btn in buttons:
            markup.add(btn)
    return markup

@bot.message_handler(func=lambda message: message.text in ["📦 Мои заказы", "Мои заказы"])
def my_orders_handler(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, "ru")
    user_orders = [order for order in orders.values() if order["user_id"] == user_id]
    if not user_orders:
        bot.send_message(user_id, t("orders_empty", lang), reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(t("back", lang)))
        return
    bot.send_message(user_id, "Ваши заказы:", reply_markup=my_orders_menu_markup(user_id, lang))

@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_receive_"))
def confirm_receive_callback(call):
    user_id = call.from_user.id
    lang = user_language.get(user_id, "ru")
    order_id = int(call.data.split("_")[-1])

    order = orders.get(order_id)
    if order and order["user_id"] == user_id:
        if order["status"] == "paid":
            order["status"] = "completed"
            bot.answer_callback_query(call.id, "Заказ подтвержден как полученный!")
            bot.edit_message_text(f"Заказ #{order_id} {t('order_status_completed', lang)}", user_id, call.message.message_id)
        else:
            bot.answer_callback_query(call.id, "Статус заказа не позволяет подтвердить получение.")
    else:
        bot.answer_callback_query(call.id, "Заказ не найден.")

@bot.callback_query_handler(func=lambda call: call.data == "back_main")
def back_main_handler(call):
    user_id = call.from_user.id
    lang = user_language.get(user_id, "ru")
    bot.edit_message_text(t("main_menu", lang), user_id, call.message.message_id, reply_markup=main_menu_markup(lang))
    bot.answer_callback_query(call.id)
    
    # --- Хранение состояний пользователей для отзывов ---
user_review_state = {}  # user_id: True если пользователь пишет отзыв

# --- Кнопки для отзывов ---
def reviews_menu_markup(lang):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("✍️ " + ("Оставить отзыв" if lang == "ru" else "Залишити відгук"), callback_data="review_add"),
        types.InlineKeyboardButton("📖 " + ("Посмотреть отзывы" if lang == "ru" else "Переглянути відгуки"), callback_data="review_view"),
        types.InlineKeyboardButton(t("back", lang), callback_data="back_main")
    )
    return markup

# --- Обработка входа в раздел отзывов ---
@bot.message_handler(func=lambda message: message.text in ["⭐ Отзывы", "Отзывы", "⭐ Відгуки", "Відгуки"])
def reviews_menu_handler(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, "ru")
    bot.send_message(user_id, ("Отзывы" if lang == "ru" else "Відгуки"), reply_markup=reviews_menu_markup(lang))

# --- Начало добавления отзыва ---
@bot.callback_query_handler(func=lambda call: call.data == "review_add")
def review_add_start(call):
    user_id = call.from_user.id
    lang = user_language.get(user_id, "ru")
    user_review_state[user_id] = True
    bot.send_message(user_id, t("review_prompt", lang))
    bot.answer_callback_query(call.id)

# --- Прием текста отзыва ---
@bot.message_handler(func=lambda message: user_review_state.get(message.from_user.id, False))
def review_receive(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, "ru")
    text = message.text.strip()
    if len(text) < 5:
        bot.send_message(user_id, ("Отзыв слишком короткий, попробуйте еще раз." if lang == "ru" else "Відгук занадто короткий, спробуйте ще раз."))
        return
    reviews.append({"user_id": user_id, "text": text, "approved": False})
    user_review_state[user_id] = False
    bot.send_message(user_id, t("review_added", lang))
    # Уведомить администратора
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("✔️ Одобрить", callback_data=f"review_approve_{len(reviews)-1}"),
        types.InlineKeyboardButton("❌ Удалить", callback_data=f"review_delete_{len(reviews)-1}")
    )
    admin_text = f"Новый отзыв от пользователя {user_id}:\n\n{text}"
    notify_admin(admin_text, reply_markup=markup)

# --- Модерация отзывов ---
@bot.callback_query_handler(func=lambda call: call.data.startswith("review_approve_") or call.data.startswith("review_delete_"))
def review_moderation_handler(call):
    data = call.data
    idx = int(data.split("_")[-1])
    if idx < 0 or idx >= len(reviews):
        bot.answer_callback_query(call.id, "Отзыв не найден.")
        return
    if call.from_user.id != ADMIN_CHAT_ID:
        bot.answer_callback_query(call.id, "У вас нет прав на модерацию.")
        return

    if data.startswith("review_approve_"):
        reviews[idx]["approved"] = True
        bot.answer_callback_query(call.id, "Отзыв одобрен.")
        bot.edit_message_reply_markup(ADMIN_CHAT_ID, call.message.message_id, reply_markup=None)
    elif data.startswith("review_delete_"):
        reviews.pop(idx)
        bot.answer_callback_query(call.id, "Отзыв удалён.")
        bot.edit_message_reply_markup(ADMIN_CHAT_ID, call.message.message_id, reply_markup=None)

# --- Просмотр одобренных отзывов ---
def get_approved_reviews_text(lang):
    approved = [r for r in reviews if r["approved"]]
    if not approved:
        return ("Пока нет отзывов." if lang == "ru" else "Поки немає відгуків.")
    texts = []
    for r in approved:
        texts.append(f"⭐ {r['text']}")
    return "\n\n".join(texts)

@bot.callback_query_handler(func=lambda call: call.data == "review_view")
def review_view_handler(call):
    user_id = call.from_user.id
    lang = user_language.get(user_id, "ru")
    text = get_approved_reviews_text(lang)
    bot.send_message(user_id, text)
    bot.answer_callback_query(call.id)
    
    # --- Реферальная система ---
def get_referral_link(user_id):
    return f"https://t.me/YourBotUsername?start=ref{user_id}"

def show_referral_menu(user_id, lang):
    referred = referrals.get(user_id, [])
    total_spent = user_spending.get(user_id, 0)
    text = (f"👥 Вы пригласили: {len(referred)} человек\n"
            f"💰 Сумма покупок ваших рефералов: {total_spent} грн\n\n"
            f"Ваша реферальная ссылка:\n"
            f"<a href='{get_referral_link(user_id)}'>Перейти по ссылке</a>")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(t("back", lang), callback_data="back_main"))
    bot.send_message(user_id, text, reply_markup=markup, parse_mode="HTML")

# --- Обработка подтверждения получения заказа ---
def confirm_order_received(order_id, user_id, lang):
    order = orders.get(order_id)
    if not order or order["user_id"] != user_id:
        bot.send_message(user_id, "Заказ не найден")
        return
    if order["status"] != "paid":
        bot.send_message(user_id, "Заказ нельзя подтвердить")
        return
    order["status"] = "completed"
    bot.send_message(user_id, t("order_status_completed", lang))
    
# --- Обработка команд и колбеков для рефералов и заказов ---
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    lang = user_language.get(user_id, "ru")
    data = call.data

    # Обработка возврата в главное меню
    if data == "back_main":
        bot.send_message(user_id, t("main_menu", lang), reply_markup=main_menu_markup(lang))
        bot.answer_callback_query(call.id)
        return

    # Реферальная система
    if data == "referral_system":
        show_referral_menu(user_id, lang)
        bot.answer_callback_query(call.id)
        return

    # Подтверждение получения заказа
    if data.startswith("confirm_received_"):
        order_id = int(data.split("_")[-1])
        confirm_order_received(order_id, user_id, lang)
        bot.answer_callback_query(call.id)
        return

    # Подтверждение оплаты админом
    if data.startswith("admin_confirm_") and user_id == ADMIN_CHAT_ID:
        order_id = int(data.split("_")[-1])
        order = orders.get(order_id)
        if not order:
            bot.answer_callback_query(call.id, "Заказ не найден", show_alert=True)
            return
        if order["status"] != "waiting_admin_confirmation":
            bot.answer_callback_query(call.id, "Заказ уже подтвержден или отменён", show_alert=True)
            return
        order["status"] = "paid"
        bot.answer_callback_query(call.id, f"Оплата заказа #{order_id} подтверждена")

        user_order_id = order["user_id"]
        bot.send_message(user_order_id, t("pay_confirmed", user_language.get(user_order_id, "ru")))

        # Начисление бонусов рефералу
        referrer = None
        for ref, referred_list in referrals.items():
            if user_order_id in referred_list:
                referrer = ref
                break
        if referrer:
            user_spending[referrer] = user_spending.get(referrer, 0) + order["total"]
            total_spent = user_spending[referrer]
            if total_spent >= 4100:
                bot.send_message(referrer, t("referral_notify", user_language.get(referrer, "ru")).format(sum=total_spent))
        return

    # Здесь можно добавить обработку других колбеков...

# --- Обработка команды /start с реферальным кодом ---
@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, "ru")

    # Парсим реферальный код если есть
    args = message.text.split()
    if len(args) > 1 and args[1].startswith("ref"):
        ref_id = int(args[1][3:])
        if ref_id != user_id:
            referrals.setdefault(ref_id, []).append(user_id)

    # Приветствие
    bot.send_message(user_id, t("main_menu", lang), reply_markup=main_menu_markup(lang))

# --- Запуск бота ---
if __name__ == "__main__":
    print("Бот запущен")
    bot.infinity_polling())


