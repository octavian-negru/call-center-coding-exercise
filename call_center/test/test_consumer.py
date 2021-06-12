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


def test_consumer_do_not_raise():
    consumer = Consumer(
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

    consumer.call(None)
    consumer.accepts_call_from(None)
    consumer.respond(consumer)
