import uvicorn
from fastapi import FastAPI
from endpoints import endpoints_register
from db import create_db
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


@asynccontextmanager
async def main(app: FastAPI):
    await create_db()
    yield

app = FastAPI(lifespan=main)

resource = Resource.create({
    "service.name": "user-registration-service"
})

provider = TracerProvider(resource=resource)

exporter = OTLPSpanExporter(
    endpoint="http://jaeger:4317",
    insecure=True
)

provider.add_span_processor(
    BatchSpanProcessor(exporter)
)

trace.set_tracer_provider(provider)

FastAPIInstrumentor.instrument_app(app)

endpoints_register(app)

Instrumentator().instrument(app).expose(app)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)