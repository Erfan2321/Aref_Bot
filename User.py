class User:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.firstname = None
        self.lastname = None
        self.phone = None
        self.grade = None
        self.field = None
        self.city = None

    def to_dict(self):
        return {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "phone": self.phone,
            "grade": self.grade,
            "field": self.field,
            "city": self.city,
        }

    def __str__(self):
        text = "👤 پروفایل شما:\n"
        for key, value in self.to_dict().items():
            text += f"- {key}: {value or '❌'}\n"
        return text
