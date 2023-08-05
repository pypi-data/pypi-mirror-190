from logging import getLogger
from helios.instrumentation.base import HeliosBaseInstrumentor

_LOG = getLogger(__name__)


class HeliosAioPikaInstrumentor(HeliosBaseInstrumentor):
    MODULE_NAME = 'helios.aio_pika_instrumentation'
    INSTRUMENTOR_NAME = 'AioPikaInstrumentor'

    def __init__(self):
        super().__init__(self.MODULE_NAME, self.INSTRUMENTOR_NAME)

    def instrument(self, tracer_provider=None, **kwargs):
        if self.get_instrumentor() is None:
            return

        self.get_instrumentor().instrument(tracer_provider=tracer_provider)
