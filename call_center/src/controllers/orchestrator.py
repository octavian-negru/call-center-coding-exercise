import time

from call_center.src.actors.actors_creator import ActorsCreator


class CallCenterOrchestrator:
    @staticmethod
    def orchestrate():
        start_time = time.time()
        for consumer in ActorsCreator().consumers:
            consumer.call()
        print(f"--- {time.time() - start_time} seconds ---")