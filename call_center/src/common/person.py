import abc
import json
import uuid

# Person attributes constants
AGE = "age"
AVAILABLE = "available"
CARS_COUNT = "cars_count"
INCOME = "income"
INSURANCE_OPERATION = "insurance_operation"
KIDS_COUNT = "kids_count"
PHONE_NUMBER = "phone_number"
STATE = "state"
VOICE_MAIL = "voice_mail"

NotImplementedErrorMsg = "Subclasses should implement this method!"


class Person(abc.ABC):
    """
    Person abstract class.
    Various actors which represent human beings implement this.
    """

    def __init__(self, personal_info: dict):
        self.id = uuid.uuid4()
        self.age = personal_info[AGE]
        self.state = personal_info[STATE]
        self.kids_count = personal_info[KIDS_COUNT]
        self.cars_count = personal_info[CARS_COUNT]
        self.income = personal_info[INCOME]
        self.phone_number = personal_info[PHONE_NUMBER]
        self.insurance_operation = personal_info[INSURANCE_OPERATION]
        self.available = personal_info[AVAILABLE]
        self.voice_mail = []

    def __getitem__(self, item):
        return getattr(self, item)

    def __repr__(self):
        return str(
            {
                "type": type(self).__name__,
                "id": str(self.id),
                AGE: self.age,
                STATE: self.state,
                KIDS_COUNT: self.kids_count,
                CARS_COUNT: self.cars_count,
                INCOME: self.income,
                PHONE_NUMBER: self.phone_number,
                INSURANCE_OPERATION: self.insurance_operation,
                AVAILABLE: self.available,
                VOICE_MAIL: self.voice_mail,
            }
        )

    def get_personal_data(self) -> dict:
        return {
            "id": str(self.id),
            AGE: self.age,
            STATE: self.state,
            KIDS_COUNT: self.kids_count,
            CARS_COUNT: self.cars_count,
            INCOME: self.income,
            PHONE_NUMBER: self.phone_number,
            INSURANCE_OPERATION: self.insurance_operation,
            AVAILABLE: self.available,
            VOICE_MAIL: self.voice_mail,
        }

    @abc.abstractmethod
    def call(self):
        raise NotImplementedError(NotImplementedErrorMsg)

    @abc.abstractmethod
    def respond(self, caller):
        raise NotImplementedError(NotImplementedErrorMsg)
