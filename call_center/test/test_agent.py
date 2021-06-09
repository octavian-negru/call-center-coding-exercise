import pytest

from call_center.src.actors.actors_creator import BUY
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
)


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
    agent = InsuranceAgent(
        personal_info={
            AGE: 35,
            STATE: "Michigan",
            KIDS_COUNT: 3,
            CARS_COUNT: 2,
            INSURANCE_OPERATION: BUY,
            INCOME: 1000,
            PHONE_NUMBER: "0123456789",
            AVAILABLE: True,
        },
        call_acceptance_criteria=call_acceptance_criteria,
    )
    assert expected == agent.accepts_call_from(
        Consumer(
            personal_info={
                AGE: 35,
                STATE: "Michigan",
                KIDS_COUNT: 3,
                CARS_COUNT: 2,
                INSURANCE_OPERATION: BUY,
                INCOME: 1000,
                PHONE_NUMBER: "0123456789",
                AVAILABLE: True,
            }
        )
    )


@pytest.mark.parametrize(
    "consumer",
    [
        [],
        Consumer(
            personal_info={
                AGE: 35,
                STATE: "Michigan",
                KIDS_COUNT: 3,
                CARS_COUNT: 2,
                INSURANCE_OPERATION: BUY,
                INCOME: 1000,
                PHONE_NUMBER: "0123456789",
                AVAILABLE: True,
            }
        ),
    ],
)
def test_agent_respond_do_not_raise(consumer):
    InsuranceAgent(
        personal_info={
            AGE: 35,
            STATE: "Michigan",
            KIDS_COUNT: 3,
            CARS_COUNT: 2,
            INSURANCE_OPERATION: BUY,
            INCOME: 1000,
            PHONE_NUMBER: "0123456789",
            AVAILABLE: True,
        },
        call_acceptance_criteria=[],
    ).respond(consumer)
