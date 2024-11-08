from transitions import Machine

class Orchestrator:
    states = ["init_startup", "in_startup_processing", "active", "init_shutdown", "in_shutdown_processing", "inactive"]

    def __init__(self):
        self.machine = Machine(model=self, states=Orchestrator.states, initial="inactive")
        self.machine.add_transition(trigger="startup", source="inactive", dest="init_startup")
        self.machine.add_transition(trigger="processing_startup", source="init_startup", dest="in_startup_processing")
        self.machine.add_transition(trigger="activate", source="in_startup_processing", dest="active")
        self.machine.add_transition(trigger="shutdown", source="active", dest="init_shutdown")
        self.machine.add_transition(trigger="processing_shutdown", source="init_shutdown", dest="in_shutdown_processing")
        self.machine.add_transition(trigger="deactivate", source="in_shutdown_processing", dest="inactive")

    def get_state(self):
        return self.state

    def change_state(self, new_state):
        # Сопоставление состояний с триггерами
        triggers = {
            "init_startup": self.startup,
            "in_startup_processing": self.processing_startup,
            "active": self.activate,
            "init_shutdown": self.shutdown,
            "in_shutdown_processing": self.processing_shutdown,
            "inactive": self.deactivate,
        }
        if new_state in triggers:
            try:
                triggers[new_state]()  # Запуск соответствующего триггера
            except Exception as e:
                print("Ошибка при изменении состояния:", str(e))
