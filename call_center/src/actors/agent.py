import os
import random
from threading import Lock, Thread
from time import sleep
from typing import List

from call_center.src.actors.consumer import Consumer
from call_center.src.common.person import Person

mutex = Lock()


class InsuranceAgent(Person):
    """
    Class modelling an insurance agent which can interact with a consumer
    """

    def __init__(self, personal_info: dict, call_acceptance_criteria: List[dict]):
        super().__init__(personal_info)
        self.call_acceptance_criteria = call_acceptance_criteria
        self.active = True
        self.polling_thread = Thread(target=self._poll_voice_mail, daemon=True)
        self._start_polling_voice_mail()

    def __del__(self):
        self.active = False
        self.polling_thread.join()

    def call(self):
        # pop from voice mail and call to the ID
        pass

    def respond(self, caller: Person):
        self.available = False  # call accepted
        print(f"InsuranceAgent responded to the call. Agent: {self} Person: {caller}")
        sleep(random.uniform(0.05, 0.3))  # Simulation of the call taking place
        self._save_call_report()

        sleep(random.uniform(0, 0.03))  # Take a little break after the call
        self.available = True

    def _save_call_report(self):
        file_path = os.path.join("call_center", "stats", "Call_summary.csv")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "a") as call_summary_file:
            # https://stackoverflow.com/questions/11983938/python-appending-to-same-file-from-multiple-threads
            mutex.acquire()
            import uuid

            # TODO: add here real information
            # TODO: it may be feasible to have another class which will write the call report to a CSV file.
            call_summary_file.write(str(uuid.uuid4()) + "\n")
            mutex.release()

    def accepts_call_from(self, caller: Person) -> bool:
        criteria_matched = []
        for acceptance_criterion in self.call_acceptance_criteria:
            criteria_matched.append(
                InsuranceAgent._check_acceptance_criterion(acceptance_criterion, caller)
            )
        if any(criteria_matched):
            return True
        return False  # Cannot accept call if acceptance_criteria not set.

    @staticmethod
    def _check_acceptance_criterion(acceptance_criterion: dict, caller: Person) -> bool:
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
        self.polling_thread.start()

    def _poll_voice_mail(self):
        while self.active:
            if self.available and len(self.voice_mail):
                # Select the oldest message in voice mail
                consumer_to_call: Consumer = self.voice_mail.pop(0)
                if consumer_to_call.accepts_call():
                    consumer_to_call.respond(self)
                    self._save_call_report()
                else:
                    # Call couldn't take place, add back to voice mail
                    self.voice_mail.append(consumer_to_call)
            sleep(0.05)  # Sleep between polls
