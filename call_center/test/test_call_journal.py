from call_center.src.actors.consumer import Consumer
from call_center.src.common.call_journal import CallJournal
from call_center.src.common.person import (
    AGE,
    STATE,
    KIDS_COUNT,
    CARS_COUNT,
    INSURANCE_OPERATION,
    INCOME,
    PHONE_NUMBER,
    AVAILABLE,
)

DUMMY_CONSUMER = Consumer(
    personal_info={
        AGE: 1,
        STATE: "",
        KIDS_COUNT: -1,
        CARS_COUNT: -1,
        INSURANCE_OPERATION: "INEXISTENT OPERATION",
        INCOME: -1,
        PHONE_NUMBER: "",
        AVAILABLE: True,
    }
)


def test_call_journal_do_not_raise():
    CallJournal.save_call_report(DUMMY_CONSUMER, DUMMY_CONSUMER)
    CallJournal.dump_call_report()


def test_call_journal_appends_call_log():
    CallJournal.call_journal = []
    CallJournal.save_call_report(DUMMY_CONSUMER, DUMMY_CONSUMER)
    assert len(CallJournal.call_journal) == 1
