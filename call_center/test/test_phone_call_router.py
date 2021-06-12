import pytest

from call_center.src.actors.agent import InsuranceAgent
from call_center.src.actors.consumer import Consumer
from call_center.src.common.person import (
    AVAILABLE,
    INSURANCE_OPERATION,
    RENT,
    BUY,
)
from call_center.src.routers.phone_call_router import PhoneCallRouter


@pytest.mark.parametrize(
    "filter_condition, tested_field_name, expected_value",
    [
        (
            lambda x: x if x[INSURANCE_OPERATION] == RENT else None,
            INSURANCE_OPERATION,
            RENT,
        ),
        (
            lambda x: x if x[INSURANCE_OPERATION] == BUY else None,
            INSURANCE_OPERATION,
            BUY,
        ),
        (lambda x: x if x[AVAILABLE] == True else None, AVAILABLE, True),
        (
            lambda x: x if x[INSURANCE_OPERATION] == RENT else None,
            AVAILABLE,
            True,
        ),
        (
            lambda x: x if x[INSURANCE_OPERATION] == RENT else None,
            INSURANCE_OPERATION,
            RENT,
        ),
        (
            lambda x: x if x[INSURANCE_OPERATION] == BUY else None,
            AVAILABLE,
            True,
        ),
        (
            lambda x: x if x[INSURANCE_OPERATION] == BUY else None,
            INSURANCE_OPERATION,
            BUY,
        ),
    ],
)
def test_find_someone_returns_expected_actor(
    filter_condition, tested_field_name, expected_value
):
    # Because agents/consumers are generated with Faker, sometimes no agents `escape` the filtering condition
    # TODO: create agents/consumers in a deterministic way
    insurance_agent = PhoneCallRouter.find_someone(InsuranceAgent, filter_condition)
    if insurance_agent:
        assert insurance_agent[tested_field_name] == expected_value

    consumer = PhoneCallRouter.find_someone(Consumer, filter_condition)
    if consumer:
        assert consumer[tested_field_name] == expected_value


@pytest.mark.parametrize(
    "filter_condition",
    [
        lambda x: x
        if x[INSURANCE_OPERATION] == "NOT EXISTING INSURANCE OPERATION"
        else None,
    ],
)
def test_find_someone_returns_None_if_not_found(filter_condition):
    assert PhoneCallRouter.find_someone(InsuranceAgent, filter_condition) is None
    assert PhoneCallRouter.find_someone(Consumer, filter_condition) is None


def test_default_match_condition_is_used():
    assert PhoneCallRouter.find_someone(InsuranceAgent)[AVAILABLE] == True
    assert PhoneCallRouter.find_someone(Consumer)[AVAILABLE] == True


@pytest.mark.parametrize(
    "incorrect_filter_condition",
    [
        (lambda x: x if x["not_existing_key"] is None else None),
    ],
)
def test_find_someone_fails(incorrect_filter_condition):
    with pytest.raises(AttributeError):
        PhoneCallRouter.find_someone(InsuranceAgent, incorrect_filter_condition)


def test_call_agent_do_not_fail():
    random_consumer = PhoneCallRouter.find_someone(Consumer, lambda x: x)
    PhoneCallRouter.call_agent(random_consumer)
