import time

from threading import Thread

from call_center.src.actors.actors_creator import ActorsCreator
from call_center.src.actors.agents_stats_inspector import AgentsStatsInspector
from call_center.src.common.call_journal import CallJournal
from call_center.src.common.decorators import log_crash


CALL_CENTER_TIMEOUT = 20  # seconds for agents to handle all consumers


class CallCenterOrchestrator:
    consumer_threads = []

    @staticmethod
    @log_crash
    def concurrently_orchestrate():
        """
        Orchestrate a real world simulation of consumers and agents interactions.
        The consumers call the agents concurrently.
        The agents respond to the calls if not already in a call.
        :return: None
        """
        start_time = time.time()
        CallCenterOrchestrator._start_consumers()

        time.sleep(CALL_CENTER_TIMEOUT)  # Wait for the consumers and agents to interact

        CallCenterOrchestrator._stop_consumers()
        ActorsCreator().stop_all_agents()

        CallJournal.dump_call_report()
        AgentsStatsInspector.dump_all_actors()

        AgentsStatsInspector.display_tree_structure("call_center")
        print(f"--- {time.time() - start_time} seconds ---")

    @staticmethod
    def _start_consumers():
        """
        Start the consumer threads.
        Consumers concurrently call the agents.
        :return: None
        """
        CallCenterOrchestrator.consumer_threads = [
            Thread(target=consumer.call, args=[None])
            for consumer in ActorsCreator().consumers
        ]
        for consumer_thread in CallCenterOrchestrator.consumer_threads:
            consumer_thread.start()

    @staticmethod
    def _stop_consumers():
        """
        Stop the consumer threads.
        :return: None
        """
        for consumer_thread in CallCenterOrchestrator.consumer_threads:
            consumer_thread.join()
