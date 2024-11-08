from transitions import Machine

class Orchestrator:
    states = ["init_startup", "in_startup_processing", "active", "init_shutdown", "in_shutdown_processing", "inactive"]

    def __init__(self):
        self.machine = Machine(model=self, states=Orchestrator.states, initial="inactive")
        # Определение переходов
        self.machine.add_transition(trigger="startup", source="inactive", dest="init_startup")
        self.machine.add_transition(trigger="processing_startup", source="init_startup", dest="in_startup_processing")
        self.machine.add_transition(trigger="activate", source="in_startup_processing", dest="active")
        self.machine.add_transition(trigger="shutdown", source="active", dest="init_shutdown")
        self.machine.add_transition(trigger="processing_shutdown", source="init_shutdown", dest="in_shutdown_processing")
        self.machine.add_transition(trigger="deactivate", source="in_shutdown_processing", dest="inactive")

    def get_state(self):
        return self.state

