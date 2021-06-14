import random

from call_center.src.actors.agents_stats_inspector import AgentsStatsInspector
from call_center.src.actors.actors_creator import ActorsCreator
from call_center.src.actors.consumer import Consumer


class PhoneCallRouter:
    """
    Class which assigns consumers to agents, based on their availability.
    """

    @staticmethod
    def call_agent(caller: Consumer, agents_pool=ActorsCreator().agents):
        """
        The public method of the call center.
        The consumers must call this method in order to contact an agent.
        :param caller: the consumer which wants to talk to an agent
        :param agents_pool: agents list from which an agent is selected to respond
        :return: None
        """
        print(f"Calling agent. Caller: {caller.id}")
        print(AgentsStatsInspector.inspect_agents_load())

        matched_agents = [
            agent for agent in agents_pool if agent.accepts_call_from(caller)
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
