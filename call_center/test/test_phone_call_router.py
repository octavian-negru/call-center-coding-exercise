from unittest.mock import Mock

import pytest

from call_center.src.actors.actors_creator import ActorsCreator
from call_center.src.routers.phone_call_router import PhoneCallRouter


def test_agent_responds_if_is_available_and_accepts_call():
    dummy_agent = Mock()
    dummy_agent.available = True
    dummy_agent.accepts_call_from = lambda x: True

    PhoneCallRouter.call_agent(ActorsCreator().consumers[0], [dummy_agent])
    dummy_agent.respond.assert_called()


def test_agent_receives_voice_mail_message_if_not_available():
    dummy_agent = Mock()
    dummy_agent.available = False

    PhoneCallRouter.call_agent(ActorsCreator().consumers[0], [dummy_agent])
    dummy_agent.put_voice_mail_msg.assert_called()


def test_if_agents_pool_not_provided_an_exception_raises():
    with pytest.raises(IndexError):
        PhoneCallRouter.call_agent(ActorsCreator().consumers[0], [])
