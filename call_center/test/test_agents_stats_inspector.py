import os
from unittest.mock import Mock

import pytest

from call_center.src.actors.agents_stats_inspector import AgentsStatsInspector


def test_dump_all_actors_do_not_raise():
    AgentsStatsInspector.dump_all_actors()


def test_display_tree_structure_do_not_raise():
    AgentsStatsInspector.display_tree_structure(os.getcwd())


def test_agents_load_counts_available_agents():
    dummy_agent1 = Mock()
    dummy_agent1.available = True

    assert "Available agents: 1/1" == AgentsStatsInspector.inspect_agents_load(
        [dummy_agent1]
    )

    dummy_agent2 = Mock()
    dummy_agent2.available = False

    assert "Available agents: 0/1" == AgentsStatsInspector.inspect_agents_load(
        [dummy_agent2]
    )


def test_if_agents_pool_have_wrong_type_an_exception_raises():
    with pytest.raises(TypeError):
        AgentsStatsInspector.inspect_agents_load(None)
