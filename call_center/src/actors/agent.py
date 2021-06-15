import random
from threading import Thread
from time import sleep
from typing import List

from call_center.src.actors.consumer import Consumer
from call_center.src.common.call_journal import CallJournal
from call_center.src.common.person import Person


class InsuranceAgent(Person):
    """
    Class modelling an insurance agent which can interact with a consumer
    """

    def __init__(self, personal_info: dict, call_acceptance_criteria: List[dict]):
        super().__init__(personal_info)

        # The criteria for accepting the call. Each agent accepts some specific consumers.
        self.call_acceptance_criteria = call_acceptance_criteria

        # Agent is in working state. self.active is used by the voice mail thread.
        self.active = True

        # Thread for periodically reading voice mail messages
        self.polling_thread: Thread = Thread(target=self._poll_voice_mail)

        # Start looking for voice mail messages
        self._start_polling_voice_mail()

    def __del__(self):
        self.stop_activity()

    def stop_activity(self):
        self.active = False
        self.polling_thread.join()

    def get_personal_data(self) -> dict:
        """
        Getter method for Agent's stats
        :return: dict containing the stats at the moment of calling
        """
        personal_data = super().get_personal_data()
        call_acceptance_criteria = {
            "accepts_calls_from_any_of": self.call_acceptance_criteria
        }
        return {**personal_data, **call_acceptance_criteria}

    def accepts_call_from(self, caller: Person) -> bool:
        """
        Checker method for evaluating if self can pick the call.
        :param caller: Person who's calling
        :return: bool indicating if self is able to respond
        """
        criteria_matched = []
        for acceptance_criterion in self.call_acceptance_criteria:
            criteria_matched.append(
                InsuranceAgent._match_acceptance_criterion(acceptance_criterion, caller)
            )
        if any(criteria_matched):
            return True
        return False

    def call(self, person_to_call: Person):
        """
        Directly contact a person.
        :param person_to_call: The person which is to be contacted. The person must accept the call before.
        :return: None
        """
        person_to_call.respond(self)

    def respond(self, caller: Person):
        """
        Respond to a calling person.
        :param caller: Person object with a call request
        :return:
        """
        self.available = False  # call accepted
        print(
            f"InsuranceAgent responded. Agent: {self.id} Caller type: {type(caller).__name__}, Caller ID: {caller.id}"
        )
        self.received_calls_count += 1

        call_duration = random.uniform(0.05, 0.3)
        sleep(call_duration)  # Simulation of the call taking place

        CallJournal.save_call_report(caller=caller, callee=self)
        sleep(random.uniform(0, 0.03))  # Take a little break after the call

        self.available = True

    def put_voice_mail_msg(self, caller: Person):
        """
        Insert into the voice mail the person who wanted to contact self.
        As a side effect, the method increments the voice mail counter.
        :param caller: the caller object
        :return:  None
        """
        self.voice_mail.append(caller)
        self.received_voice_mail_msgs_count += 1

    @staticmethod
    def _match_acceptance_criterion(acceptance_criterion: dict, caller: Person) -> bool:
        """
        Evaluate if the caller matches the current acceptance_criterion.
        The acceptance criteria are used for evaluating if an Agent is able to pick a call from a specific Person.
        :param acceptance_criterion: dictionary describing an acceptance criterion
        :param caller: the Person who is to be matched with the provided acceptance_criterion
        :return: bool
        """
        person_attribute = acceptance_criterion["person_attribute"]
        comparison_operator = acceptance_criterion["comparison_operator"]
        if comparison_operator == "<":
            if caller[person_attribute] < acceptance_criterion["value"]:
                return True
        elif comparison_operator == ">":
            if caller[person_attribute] > acceptance_criterion["value"]:
                return True
        return False

    def _start_polling_voice_mail(self):
        """
        Initializer for the internal voice mail reading thread
        :return: None
        """
        self.polling_thread.start()

    def _poll_voice_mail(self):
        """
        The voice mail polling thread method.
        When an Agent is active and has no call to pick at some certain time,
        then the agent calls back the customers which may have called him in the past.
        :return: None
        """
        while self.active:
            if self.available and len(self.voice_mail):

                # Select the oldest message in voice mail
                consumer_to_call: Consumer = self.voice_mail.pop(0)

                if consumer_to_call.accepts_call_from(self):
                    self.call(consumer_to_call)
                    CallJournal.save_call_report(caller=self, callee=consumer_to_call)
                else:
                    # Call couldn't take place, add back to voice mail
                    self.voice_mail.append(consumer_to_call)
            # Sleep between polls, due to GIL. Let the interpreter switch `attention` to other threads.
            sleep(0.001)
