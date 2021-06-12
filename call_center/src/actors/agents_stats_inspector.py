import csv
import os
from typing import List

from call_center.src.actors.actors_creator import ActorsCreator
from call_center.src.common.call_journal import CALL_CENTER_STATS_PATH
from call_center.src.common.person import Person


class AgentsStatsInspector:
    @staticmethod
    def inspect_agents_load():
        """
        Utility method to check how many Agents have work assigned.
        Returns the stats at the moment of calling.
        :return: string, e.g. Available agents: 10/20
        """
        all_agents = ActorsCreator().agents
        available_agents = [agent for agent in all_agents if agent.available]
        return f"Available agents: {len(available_agents)}/{len(all_agents)}"

    @staticmethod
    def display_tree_structure(path_to_display):
        """
        https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
        Log the structure of the local Docker container.
        Useful for debugging.
        :param path_to_display: Path to log
        :return: None
        """
        print(f"Displaying tree of {path_to_display}")
        for root, dirs, files in os.walk(path_to_display):
            level = root.replace(path_to_display, "").count(os.sep)
            indent = " " * 4 * (level)
            print("{}{}/".format(indent, os.path.basename(root)))
            subindent = " " * 4 * (level + 1)
            for f in files:
                print("{}{}".format(subindent, f))

    @staticmethod
    def dump_all_actors():
        """
        Utility method to dump all agents/consumers to a csv file.
        :return: None
        """
        AgentsStatsInspector._dump_actors(ActorsCreator().agents)
        AgentsStatsInspector._dump_actors(ActorsCreator().consumers)

    @staticmethod
    def _dump_actors(actors: List[Person]):
        """
        Utility method to dump specific actors informations.
        The method dumps a CSV file named as the first actor type.
        E.g. for an object of type Consumer, the file name is Consumer.csv
        The CSV lines contain the data returned by get_personal_data() method,
        which is called for all actors from the list.
        :param actors:
        :return:
        """
        if actors:
            actor_class_name = type(actors[0]).__name__
            actors_file_name = f"{actor_class_name}.csv"
            actors_file_path = os.path.join(CALL_CENTER_STATS_PATH, actors_file_name)
            os.makedirs(os.path.dirname(actors_file_path), exist_ok=True)

            with open(actors_file_path, "w") as actors_file:
                csv_rows = actors[0].get_personal_data().keys()
                dict_writer = csv.DictWriter(actors_file, csv_rows)
                dict_writer.writeheader()
                dict_writer.writerows([actor.get_personal_data() for actor in actors])
