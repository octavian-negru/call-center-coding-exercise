from call_center.src.actors.agents_stats_inspector import AgentsStatsInspector


def test_dump_all_actors_do_not_raise():
    AgentsStatsInspector.dump_all_actors()


def test_display_tree_structure_do_not_raise():
    AgentsStatsInspector.display_tree_structure("")


def test_all_agents_are_available():
    assert "Available agents: 20/20" == AgentsStatsInspector.inspect_agents_load()
