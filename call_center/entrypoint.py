import os
import sys

# PYTHONPATH setup for setting the paths in the Docker container
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, ".."))

from src.controllers.orchestrator import CallCenterOrchestrator


CallCenterOrchestrator.concurrently_orchestrate()
