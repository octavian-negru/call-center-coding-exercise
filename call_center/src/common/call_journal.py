import os
from typing import List

from call_center.src.common.person import Person

CALL_CENTER_STATS_PATH = os.path.join("call_center", "stats")


class CallJournal:
    """
    Class which encapsulates the call report.
    """

    call_count = 0
    call_journal: List[str] = []
    call_stats: List[dict] = []

    @staticmethod
    def save_call_report(caller: Person, callee: Person):
        """
        In-memory save (for performance purposes) the two correspondents.
        As a side effect, this method increments the call_count and appends a line to the call_journal.
        :param caller: the Person which initiated the call
        :param callee: the called Person
        :return: None
        """
        CallJournal.call_count += 1
        print(f"Call count: {CallJournal.call_count}")
        call_log_line = (
            f"Caller ID: {caller.id}, caller type: {type(caller).__name__}, callee ID: {callee.id}, callee type: {type(callee).__name__}"
            + os.linesep
        )
        CallJournal.call_journal.append(call_log_line)

    @staticmethod
    def dump_call_report():
        """
        Locally write a file with who called and who responded.
        :return: None
        """
        call_summary_file = os.path.join(CALL_CENTER_STATS_PATH, "Call_summary.txt")
        os.makedirs(os.path.dirname(call_summary_file), exist_ok=True)
        with open(call_summary_file, "w") as call_summary_file:
            # https://stackoverflow.com/questions/11983938/python-appending-to-same-file-from-multiple-threads
            call_summary_file.write("".join(CallJournal.call_journal))
