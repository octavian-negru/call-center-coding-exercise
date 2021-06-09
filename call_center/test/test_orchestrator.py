from call_center.src.controllers.orchestrator import CallCenterOrchestrator


def test_orchestrator_do_not_raise():
    CallCenterOrchestrator.orchestrate()
