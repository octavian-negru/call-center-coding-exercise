from call_center.src.actors.actors_creator import (
    ActorsCreator,
    CONSUMER_COUNT,
    AGENTS_COUNT,
)


def test_actors_creator_creates_expected_number_of_actors():
    actors_creator = ActorsCreator()
    assert len(actors_creator.consumers) == CONSUMER_COUNT
    assert len(actors_creator.agents) == AGENTS_COUNT


def test_actors_creator_is_singleton():
    assert id(ActorsCreator()) == id(ActorsCreator())
