from enum import Enum


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.firstname = None
        self.lastname = None
        self.phone = None
        self.grade = None
        self.field = None
        self.city = None

    def __str__(self):

        print(self.firstname)
        print(self.lastname)
        print(self.phone)

        return (
            f"👤 پروفایل شما:\n"
            f"- نام: {self.firstname or '❌'}\n"
            f"- نام خانوادگی: {self.lastname or '❌'}\n"
            f"- شماره تماس: {self.phone or '❌'}\n"
            f"- پایه تحصیلی: {self.grade or '❌'}\n"
            f"- رشته تحصیلی: {self.field or '❌'}\n"
            f"- شهر: {self.city or '❌'}"
        )

class UserField(Enum):
    firstname = "firstname"
    lastname = "lastname"
    phone = "phone"
    grade = "grade"
    field = "field"
    city = "city"