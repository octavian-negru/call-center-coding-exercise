import os
import sys

import pytest

# PYTHONPATH setup for pytest
# https://stackoverflow.com/questions/10253826/path-issue-with-pytest-importerror-no-module-named-yadayadayada
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "..", ".."))

from call_center.src.actors.actors_creator import ActorsCreator


@pytest.fixture(autouse=True, scope="function")
def stop_agents():
    ActorsCreator().stop_all_agents()
