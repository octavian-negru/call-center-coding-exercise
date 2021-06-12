import random

from call_center.src.actors.agent import InsuranceAgent
from call_center.src.actors.agents_stats_inspector import AgentsStatsInspector
from call_center.src.common.person import AVAILABLE, Person
from call_center.src.actors.actors_creator import ActorsCreator
from call_center.src.actors.consumer import Consumer


class PhoneCallRouter:
    """
    Class which assigns consumers to agents, based on their availability.
    """

    @staticmethod
    def find_someone(
        actor_type, match_condition=lambda x: x if x[AVAILABLE] is True else None
    ) -> Person:
        """
        Find an agent/consumer which corresponds to the provided match_condition.
        If a match condition is not provided, the agents/consumers are filtered based on their availability.
        :param actor_type: type of the actor. Used to select the correct pool of actors.
        :param match_condition: function which does the filtering in the actors' pool
        :return:
        """
        actors_to_find = {
            InsuranceAgent: ActorsCreator().agents,
            Consumer: ActorsCreator().consumers,
        }
        matched_persons = list(filter(match_condition, actors_to_find[actor_type]))
        # Filtering Nones because user might provide a lambda as a filtering callback.
        # Oftentimes lambdas have an `else None` clause
        matched_persons = list(filter(None, matched_persons))
        return random.choice(matched_persons) if matched_persons else None

    @staticmethod
    def call_agent(caller: Consumer):
        """
        The public method of the call center.
        The consumers must call this method in order to contact an agent.
        :param caller: the consumer which wants to talk to an agent
        :return: None
        """
        print(f"Calling agent. Caller: {caller.id}")
        print(AgentsStatsInspector.inspect_agents_load())

        matched_agents = [
            agent for agent in ActorsCreator().agents if agent.accepts_call_from(caller)
        ]
        found_agent = random.choice(matched_agents)
        if found_agent:
            if found_agent.available:
                print(f"Agent {found_agent.id} accepted call.")
                found_agent.respond(caller)
            elif found_agent.available is False:
                print(f"Agent {found_agent.id} accepted call but is busy now.")
                found_agent.put_voice_mail_msg(caller)
        else:
            PhoneCallRouter.call_agent(caller)
