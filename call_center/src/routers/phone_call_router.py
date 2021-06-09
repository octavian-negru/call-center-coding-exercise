import random

from call_center.src.actors.agent import InsuranceAgent
from call_center.src.common.person import AVAILABLE, Person
from call_center.src.actors.actors_creator import ActorsCreator
from call_center.src.actors.consumer import Consumer


class PhoneCallRouter:
    @staticmethod
    def find_someone(
        actor_type, match_condition=lambda x: x if x[AVAILABLE] is True else None
    ) -> Person:
        actors_to_find = {
            InsuranceAgent: ActorsCreator().agents,
            Consumer: ActorsCreator().consumers,
        }
        available_actors = list(
            filter(
                lambda x: x if x[AVAILABLE] is True else None,
                actors_to_find[actor_type],
            )
        )
        matched_persons = list(filter(match_condition, available_actors))
        # Filtering Nones because user might provide a lambda as a filtering callback.
        # Oftentimes lambdas have an `else None` clause
        matched_persons = list(filter(None, matched_persons))
        return random.choice(matched_persons) if matched_persons else None

    @staticmethod
    def call_agent(caller: Consumer) -> Person:
        found_agent = PhoneCallRouter.find_someone(InsuranceAgent)
        if found_agent:
            if found_agent.accepts_call_from(caller):
                found_agent.respond(caller)
            else:
                found_agent.voice_mail.append(caller)
