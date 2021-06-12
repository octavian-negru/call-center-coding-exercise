import pytest

from call_center.src.actors.agent import InsuranceAgent
from call_center.src.actors.consumer import Consumer
from call_center.src.common.person import (
    AGE,
    STATE,
    KIDS_COUNT,
    CARS_COUNT,
    INSURANCE_OPERATION,
    INCOME,
    PHONE_NUMBER,
    AVAILABLE,
    BUY,
)

DUMMY_PERSONAL_INFO = {
    AGE: 1,
    STATE: "",
    KIDS_COUNT: -1,
    CARS_COUNT: -1,
    INSURANCE_OPERATION: "INEXISTENT OPERATION",
    INCOME: -1,
    PHONE_NUMBER: "",
    AVAILABLE: True,
}


@pytest.mark.parametrize(
    "call_acceptance_criteria, expected",
    [
        ([], False),
        ({}, False),
        (
            [
                {
                    "person_attribute": AGE,
                    "comparison_operator": "<",
                    "value": 30,
                }
            ],
            False,
        ),
        (
            [
                {
                    "person_attribute": AGE,
                    "comparison_operator": ">",
                    "value": 30,
                }
            ],
            True,
        ),
        (
            [
                {
                    "person_attribute": KIDS_COUNT,
                    "comparison_operator": "<",
                    "value": 5,
                }
            ],
            True,
        ),
        (
            [
                {
                    "person_attribute": KIDS_COUNT,
                    "comparison_operator": ">",
                    "value": 5,
                }
            ],
            False,
        ),
        (
            [
                {
                    "person_attribute": CARS_COUNT,
                    "comparison_operator": "<",
                    "value": 3,
                }
            ],
            True,
        ),
        (
            [
                {
                    "person_attribute": CARS_COUNT,
                    "comparison_operator": ">",
                    "value": 3,
                }
            ],
            False,
        ),
        (
            [
                {
                    "person_attribute": INCOME,
                    "comparison_operator": "<",
                    "value": 1500,
                }
            ],
            True,
        ),
        (
            [
                {
                    "person_attribute": INCOME,
                    "comparison_operator": ">",
                    "value": 1500,
                }
            ],
            False,
        ),
        # TODO: add support for non numerical comparisons
    ],
)
def test_agent_accepts_call(call_acceptance_criteria, expected):
    personal_info = {
        AGE: 35,
        STATE: "Michigan",
        KIDS_COUNT: 3,
        CARS_COUNT: 2,
        INSURANCE_OPERATION: BUY,
        INCOME: 1000,
        PHONE_NUMBER: "0123456789",
        AVAILABLE: True,
    }
    agent = InsuranceAgent(
        personal_info=personal_info,
        call_acceptance_criteria=call_acceptance_criteria,
    )
    assert expected == agent.accepts_call_from(Consumer(personal_info=personal_info))
    agent.stop_activity()


def test_agent_respond_do_not_raise():
    agent = InsuranceAgent(
        personal_info=DUMMY_PERSONAL_INFO,
        call_acceptance_criteria=[],
    )
    agent.respond(Consumer(personal_info=DUMMY_PERSONAL_INFO))
    agent.stop_activity()


def test_agent_call_count_is_increased_after_call():
    agent = InsuranceAgent(
        personal_info=DUMMY_PERSONAL_INFO,
        call_acceptance_criteria=[],
    )
    expected_received_calls = agent.received_calls_count + 1
    agent.respond(Consumer(personal_info=DUMMY_PERSONAL_INFO))
    agent.stop_activity()

    assert expected_received_calls == agent.received_calls_count


def test_put_voice_mail_msg_increases_msgs_count():
    agent = InsuranceAgent(
        personal_info=DUMMY_PERSONAL_INFO,
        call_acceptance_criteria=[],
    )
    expected_received_calls = agent.received_voice_mail_msgs_count + 1
    agent.put_voice_mail_msg(Consumer(personal_info=DUMMY_PERSONAL_INFO))
    agent.stop_activity()

    assert expected_received_calls == agent.received_voice_mail_msgs_count
