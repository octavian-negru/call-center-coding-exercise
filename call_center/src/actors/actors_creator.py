import csv
import os
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
    Person,
)
from call_center.src.common.singleton_meta import SingletonMeta

CONSUMER_COUNT = 1000
AGENTS_COUNT = 20
FAKE = Faker("en_US")
RENT = "rent"
BUY = "buy"


class ActorsCreator(metaclass=SingletonMeta):
    """
    Singleton class which acts as a container for both Agents and Consumers.
    In a real-world scenario, we would have a database containing both actors/consumers.
    This is a replacement, for the sake of example.
    """

    def __init__(self):
        self.consumers = ActorsCreator.create_consumers()
        self.agents = ActorsCreator.create_agents()
        self._dump_actors(self.consumers)
        self._dump_actors(self.agents)

    @staticmethod
    def create_consumers() -> List[Consumer]:
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

    def _dump_actors(self, actors: List[Person]):
        if actors:
            actor_class_name = type(actors[0]).__name__
            file_name = f"{actor_class_name}.csv"
            file_path = os.path.join("call_center", "stats", file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, "w") as actors_file:
                csv_rows = actors[0].get_personal_data().keys()
                dict_writer = csv.DictWriter(actors_file, csv_rows)
                dict_writer.writeheader()
                dict_writer.writerows([actor.get_personal_data() for actor in actors])
