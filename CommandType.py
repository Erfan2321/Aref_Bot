import enum

class CommandType(enum.Enum):
    """
    اینجا همه‌ی نوع‌های دستور/کوئری تعریف میشن.
    مقدارش هم همون چیزی میشه که داخل callback_data ذخیره می‌کنیم.
    """

    SET_FIRSTNAME = "set_firstname"
    SET_LASTNAME = "set_lastname"
    SET_PHONE = "set_phone"
    SET_GRADE = "set_grade"
    SET_FIELD = "set_field"
    SET_CITY = "set_city"
    SHOW_PROFILE = "show_profile"

