import abc
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
RENT = "rent"
BUY = "buy"

NotImplementedErrorMsg = "Subclasses should implement this method!"


class Person(abc.ABC):
    """
    Abstract Base Class for agents and consumers.
    """

    def __init__(self, personal_info: dict):
        self.id = str(uuid.uuid4()).replace("-", "")
        self.age = personal_info[AGE]
        self.state = personal_info[STATE]
        self.kids_count = personal_info[KIDS_COUNT]
        self.cars_count = personal_info[CARS_COUNT]
        self.income = personal_info[INCOME]
        self.phone_number = personal_info[PHONE_NUMBER]
        self.insurance_operation = personal_info[INSURANCE_OPERATION]
        self.available = personal_info[AVAILABLE]
        self.voice_mail = []
        self.received_voice_mail_msgs_count = 0
        self.received_calls_count = 0

    def __getitem__(self, item):
        return getattr(self, item)  # Allowing iteration in a List[Person]

    def __repr__(self):
        return str(self.get_personal_data())

    def get_personal_data(self) -> dict:
        """
        Utility method to get all Person's stats at once.
        :return: dict with the self state.
        """
        return {
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
            "received_voice_mail_msgs_count": self.received_voice_mail_msgs_count,
            "received_calls_count": self.received_calls_count,
        }

    @abc.abstractmethod
    def accepts_call_from(self, caller) -> bool:
        """
        Method to inspect various caller properties before responding to the call.
        :param caller: Person who is calling
        :return: bool
        """
        raise NotImplementedError(NotImplementedErrorMsg)

    @abc.abstractmethod
    def call(self, person):
        """
        Call another person.
        :param person: Person who is called.
        :return: None
        """
        raise NotImplementedError(NotImplementedErrorMsg)

    @abc.abstractmethod
    def respond(self, caller):
        """
        Respond to the caller Person and start the actual call.
        :param caller: caller Person
        :return: None
        """
        raise NotImplementedError(NotImplementedErrorMsg)
