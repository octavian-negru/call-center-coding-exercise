import random
from time import sleep

from call_center.src.common.person import Person


class Consumer(Person):
    """
    Class modelling a person which can interact with an agent
    """

    def call(self):
        # avoiding circular imports
        from call_center.src.routers.phone_call_router import PhoneCallRouter

        PhoneCallRouter.call_agent(self)

    def respond(self, caller: Person):
        self.available = False  # call accepted
        print(f"Consumer responded to the call. Consumer: {self} Person: {caller}")
        sleep(random.uniform(0.05, 0.3))  # Simulation of the call taking place
        #  The consumers don't save the call report, it's not their responsibility
        self.available = True

    def accepts_call(self) -> bool:
        # Consumers have a chance of being busy of ~80%
        return random.randint(0, 100) < 20
