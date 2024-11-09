from transitions import Machine
from runner.runner import logger


class Orchestrator:
    """
    Класс для управления состояниями с помощью конечного автомата.
    `Orchestrator` реализует переключение между состояниями и автоматизирует
    процессы активации и деактивации различных режимов.

    Состояния:
        - "init_startup": Начальная инициализация.
        - "in_startup_processing": Процесс инициализации завершен, идет подготовка к активному состоянию.
        - "active": Активное состояние.
        - "init_shutdown": Инициализация завершения работы.
        - "in_shutdown_processing": Процесс завершения работы.
        - "inactive": Неактивное состояние.

    Атрибуты:
        machine (Machine): Экземпляр конечного автомата для управления переходами состояний.
        states (list): Список возможных состояний.
    """

    states = ["init_startup", "in_startup_processing", "active", "init_shutdown", "in_shutdown_processing", "inactive"]

    def __init__(self):
        """
        Инициализирует Orchestrator с начальными состояниями и переходами между ними.

        Переходы:
            - "startup" переводит из состояния "inactive" в "init_startup".
            - "processing_startup" переводит из состояния "init_startup" в "in_startup_processing".
            - "activate" переводит из состояния "in_startup_processing" в "active".
            - "shutdown" переводит из состояния "active" в "init_shutdown".
            - "processing_shutdown" переводит из состояния "init_shutdown" в "in_shutdown_processing".
            - "deactivate" переводит из состояния "in_shutdown_processing" в "inactive".
        """
        self.machine = Machine(model=self, states=Orchestrator.states, initial="inactive")
        self.machine.add_transition(trigger="startup", source="inactive", dest="init_startup")
        self.machine.add_transition(trigger="processing_startup", source="init_startup", dest="in_startup_processing")
        self.machine.add_transition(trigger="activate", source="in_startup_processing", dest="active")
        self.machine.add_transition(trigger="shutdown", source="active", dest="init_shutdown")
        self.machine.add_transition(trigger="processing_shutdown", source="init_shutdown", dest="in_shutdown_processing")
        self.machine.add_transition(trigger="deactivate", source="in_shutdown_processing", dest="inactive")
        logger.info("Orchestrator initialized with state: 'inactive'")

    def get_state(self):
        """
        Возвращает текущее состояние объекта `Orchestrator`.

        Возвращает:
            str: Текущее состояние автомата.
        """
        logger.debug(f"Current state: {self.state}")
        return self.state

    def change_state(self, new_state):
        """
        Изменяет текущее состояние, вызывая соответствующий триггер для перехода.

        Параметры:
            new_state (str): Новое состояние, к которому нужно перейти.

        Исключения:
            Выводит ошибку, если при изменении состояния произошла ошибка.

        Примечание:
            Если текущее состояние уже соответствует `new_state`, то переход не выполняется.
        """
        # Сопоставление состояний с триггерами
        triggers = {
            "init_startup": self.startup,
            "in_startup_processing": self.processing_startup,
            "active": self.activate,
            "init_shutdown": self.shutdown,
            "in_shutdown_processing": self.processing_shutdown,
            "inactive": self.deactivate,
        }

        if new_state not in triggers:
            logger.error(f"Invalid target state: {new_state}")
            return

        if self.state == new_state:
            logger.info(f"Already in target state: {new_state}")
            return

        try:
            logger.info(f"Changing state from '{self.state}' to '{new_state}'")
            triggers[new_state]()
            logger.info(f"State changed to: {self.state}")
        except Exception as e:
            logger.error(f"Error during state change to '{new_state}': {e}")
