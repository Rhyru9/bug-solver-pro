#!/usr/bin/env python3
"""Isolated synthetic ASGI probe: normal output filtering versus direct Response.

Run with the project's existing interpreter when FastAPI is already installed.
No network, disk writes, package installs, production inputs, or external effects.
"""

import asyncio
import json
import sys


async def request(app, path):
    messages = []
    delivered = False

    async def receive():
        nonlocal delivered
        if not delivered:
            delivered = True
            return {"type": "http.request", "body": b"", "more_body": False}
        await asyncio.Event().wait()

    async def send(message):
        messages.append(message)

    scope = {
        "type": "http", "asgi": {"version": "3.0"}, "http_version": "1.1",
        "method": "GET", "scheme": "http", "path": path,
        "raw_path": path.encode("ascii"), "root_path": "", "query_string": b"",
        "headers": [], "client": ("fixture", 1), "server": ("fixture", 80),
    }
    await asyncio.wait_for(app(scope, receive, send), timeout=5)
    status = next(message["status"] for message in messages if message["type"] == "http.response.start")
    body = b"".join(message.get("body", b"") for message in messages
                    if message["type"] == "http.response.body")
    return {"status": status, "body": json.loads(body)}


async def probe():
    import fastapi
    import pydantic
    import starlette
    from fastapi import FastAPI
    from fastapi.encoders import jsonable_encoder
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel

    class PublicOutput(BaseModel):
        id: int

    payload = {"id": 1, "internal_marker": "synthetic-only"}
    app = FastAPI()

    @app.get("/normal", response_model=PublicOutput)
    def normal():
        return dict(payload)

    @app.get("/direct", response_model=PublicOutput)
    def direct():
        return JSONResponse(content=dict(payload))

    @app.get("/explicit-output", response_model=PublicOutput)
    def explicit_output():
        return JSONResponse(content=jsonable_encoder(PublicOutput(**payload)))

    results = {path: await request(app, path)
               for path in ("/normal", "/direct", "/explicit-output")}
    expected = {
        "/normal": {"status": 200, "body": {"id": 1}},
        "/direct": {"status": 200, "body": payload},
        "/explicit-output": {"status": 200, "body": {"id": 1}},
    }
    if results != expected:
        raise AssertionError(f"Probe prediction contradicted: {results!r}")
    return {
        "kind": "synthetic_runtime_probe",
        "versions": {"python": sys.version.split()[0], "fastapi": fastapi.__version__,
                     "pydantic": pydantic.__version__, "starlette": starlette.__version__},
        "results": results,
        "conclusion": "Normal response filtering ran; direct Response bypassed it; explicit output DTO excluded the extra field.",
        "limits": "Local ASGI fixtures only; no production incident, network server, streaming, middleware, provider, or other-version validation.",
    }


def main():
    try:
        result = asyncio.run(probe())
    except ImportError as error:
        print(f"Probe requires FastAPI in this interpreter: {error}", file=sys.stderr)
        return 2
    except (AssertionError, asyncio.TimeoutError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
