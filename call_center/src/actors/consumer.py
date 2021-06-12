import random
from time import sleep

from call_center.src.common.person import Person


class Consumer(Person):
    """
    Class modelling a person which can interact with an agent
    """

    def accepts_call_from(self, caller: Person) -> bool:
        """
        As stated in the project requirements, the Consumer have a chance of being busy of ~80%.
        :param caller: ignored caller Person
        :return:
        """
        return random.randint(0, 100) < 20

    def call(self, person_to_call: Person):
        """
        Call an agent through PhoneCallRouter.
        :param person_to_call: person to be called. Param provided by the Person ABC.
        :return: None
        """
        from call_center.src.routers.phone_call_router import (
            PhoneCallRouter,
        )  # avoiding circular imports

        PhoneCallRouter.call_agent(self)

    def respond(self, caller: Person):
        """
        Respond to the caller Person.
        As a side effect, the received calls counter is incremented.
        :param caller:
        :return: None
        """
        self.available = False  # call accepted
        print(
            f"Consumer responded. Consumer: {self.id} Caller type: {type(caller).__name__}, Caller ID: {caller.id}"
        )
        self.received_calls_count += 1

        call_duration = random.uniform(0.05, 0.3)
        sleep(call_duration)  # Simulation of the call taking place

        #  The consumers don't save the call report, it's not their responsibility
        self.available = True
