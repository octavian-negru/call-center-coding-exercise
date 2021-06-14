import random

from typing import List

from faker import Faker

from call_center.src.actors.agent import InsuranceAgent
from call_center.src.actors.consumer import Consumer
from call_center.src.common.person import (
    AGE,
    AVAILABLE,
    INSURANCE_OPERATION,
    PHONE_NUMBER,
    INCOME,
    CARS_COUNT,
    KIDS_COUNT,
    STATE,
    RENT,
    BUY,
)
from call_center.src.common.singleton_meta import SingletonMeta

CONSUMER_COUNT = 1000
AGENTS_COUNT = 20
FAKE = Faker("en_US")


class ActorsCreator(metaclass=SingletonMeta):
    """
    Singleton class which acts as a container for both Agents and Consumers.
    In a real-world scenario, we would have a database containing both actors/consumers.
    This is a replacement, for the sake of example.
    """

    def __init__(self):
        self.consumers = ActorsCreator.create_consumers()
        self.agents = ActorsCreator.create_agents()

    def __del__(self):
        self.stop_all_agents()

    @staticmethod
    def create_consumers() -> List[Consumer]:
        """
        Create the consumers. Consumers are created with randomized attributes.
        :return: A new list of Consumer.
        """
        consumers = []
        for consumer in range(CONSUMER_COUNT):
            consumers.append(
                Consumer(
                    {
                        AGE: FAKE.random_int(min=0, max=120),
                        STATE: FAKE.state(),
                        KIDS_COUNT: FAKE.random_int(min=0, max=12),
                        CARS_COUNT: FAKE.random_int(min=0, max=10),
                        INSURANCE_OPERATION: random.choice((RENT, BUY)),
                        INCOME: FAKE.random_int(min=0, max=99999999999),
                        PHONE_NUMBER: FAKE.phone_number(),
                        AVAILABLE: True,
                    }
                )
            )
        return consumers

    @staticmethod
    def create_agents() -> List[InsuranceAgent]:
        """
        Create the InsuranceAgents. Consumers are created with randomized attributes.
        :return: A new list of InsuranceAgent.
        """
        agents = []
        for consumer in range(AGENTS_COUNT):
            insurance_agent = InsuranceAgent(
                personal_info={
                    AGE: FAKE.random_int(min=0, max=120),
                    STATE: FAKE.state(),
                    KIDS_COUNT: FAKE.random_int(min=0, max=12),
                    CARS_COUNT: FAKE.random_int(min=0, max=10),
                    INSURANCE_OPERATION: random.choice((RENT, BUY)),
                    INCOME: FAKE.random_int(min=0, max=1000000),
                    PHONE_NUMBER: FAKE.phone_number(),
                    AVAILABLE: True,
                },
                call_acceptance_criteria=[
                    {
                        "person_attribute": AGE,
                        "comparison_operator": random.choice(("<", ">")),
                        "value": FAKE.random_int(
                            min=0,
                            max=120,
                        ),
                    },
                    {
                        "person_attribute": INCOME,
                        "comparison_operator": random.choice(("<", ">")),
                        "value": FAKE.random_int(
                            min=0,
                            max=1000000,
                        ),
                    },
                    {
                        "person_attribute": KIDS_COUNT,
                        "comparison_operator": random.choice(("<", ">")),
                        "value": FAKE.random_int(
                            min=0,
                            max=12,
                        ),
                    },
                    {
                        "person_attribute": CARS_COUNT,
                        "comparison_operator": random.choice(("<", ">")),
                        "value": FAKE.random_int(
                            min=0,
                            max=12,
                        ),
                    },
                    {
                        "person_attribute": INSURANCE_OPERATION,
                        "comparison_operator": random.choice(("<", ">")),
                        "value": random.choice((RENT, BUY)),
                    },
                ],
            )
            agents.append(insurance_agent)
        return agents

    def stop_all_agents(self):
        """
        Gracefully stop all agents threads on self deletion.
        To find more on agents' threads, see agent.py
        :return:
        """
        for agent in self.agents:
            if agent.available:
                agent.stop_activity()
