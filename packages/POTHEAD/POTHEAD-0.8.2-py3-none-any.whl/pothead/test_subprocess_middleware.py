import io
import os
import pytest
import signal
import sys
import traceback
from typing import Any, Callable, cast, Dict, Iterable, TextIO
from unittest import TestCase
import werkzeug
from werkzeug.datastructures import Headers
from werkzeug.test import Client

from .subprocess_middleware import SubprocessMiddleware
from .wsgi_typing import (
    Environ,
    ExcInfo,
    StartResponse,
)

# Used for testing that only gets initialized once in the forkserver
# process, and not once per spawned subprocess.
TEST_GLOBAL_VAR = os.getpid()


def assertActiveException() -> ExcInfo:
    exc_info = sys.exc_info()
    assert exc_info[0] is not None
    assert exc_info[1] is not None
    assert exc_info[2] is not None
    return exc_info


# This function executes inside the spawned subprocess
def wrapped_app(environ: Environ, start_response: StartResponse) -> Iterable[bytes]:
    # Separate code path for tests that do not read request payload
    if environ["PATH_INFO"] == "/test_success_app_does_not_read_payload":
        start_response("200 OK", [], None)
        yield b"This is a successful response"
    else:
        request = werkzeug.Request(cast(Dict[str, Any], environ))
        assert request.is_multiprocess

        if request.path == "/test_success_with_request_and_response_payloads":
            assert request.data == b"Non-UTF8 binary payload: \x80"
            start_response("200 OK", [("key1", "value1"), ("key2", "value2")], None)
            yield b"This is a "
            yield b"non-UTF8 success response: \x80"
        elif request.path == "/test_success_with_payload_and_cpu_reservation_reset":
            start_response("200 OK", [], None)
            assert "RESET_CPU_RESERVATION" in environ
            reset_cpu_reservation = cast(
                Callable[[int], None], environ["RESET_CPU_RESERVATION"]
            )
            yield b"This is a "
            reset_cpu_reservation(7)
            yield b"successful response"
        elif (
            request.path == "/test_no_cpu_reservation_reset_if_none_in_original_request"
        ):
            assert "RESET_CPU_RESERVATION" not in environ
            start_response("200 OK", [], None)
            yield b"This is a successful response"
        elif request.path == "/test_success_with_no_response_payload":
            start_response("200 OK", [], None)
        elif request.path == "/test_failed_request_with_wsgi_error_output":
            wsgi_errors = cast(TextIO, environ.get("wsgi.errors"))
            wsgi_errors.write("First error output\n")
            start_response("500 Internal Server Error", [], None)
            wsgi_errors.write("Second error output\n")
        elif request.path == "/test_exception_raised_in_wrapped_app":

            def a_function_in_the_wrapped_app_callstack():
                raise Exception("This is an exception message")

            a_function_in_the_wrapped_app_callstack()
        elif request.path == "/test_exception_returned_from_start_response":

            def a_function_in_the_wrapped_app_callstack():
                try:
                    raise Exception("This is an exception message")
                except Exception:
                    exc_info = assertActiveException()
                    start_response(
                        "500 Internal Server Error",
                        [("key1", "value1"), ("key2", "value2")],
                        exc_info,
                    )

            a_function_in_the_wrapped_app_callstack()
        elif request.path == "/test_wrapped_app_dies_from_signal":
            os.kill(os.getpid(), signal.SIGKILL)
        elif request.path == "/test_globals_not_reinitialized_for_each_request":
            start_response("200 OK", [], None)
            yield f"TEST_GLOBAL_VAR: {TEST_GLOBAL_VAR}".encode("utf-8")
        else:
            assert False, f"Unknown test endpoint path: {request.path}"


class SubprocessMiddlewareTest(TestCase):
    def test_success_with_request_and_response_payloads(self):
        client = Client(SubprocessMiddleware(wrapped_app))
        response = client.post(
            "/test_success_with_request_and_response_payloads",
            data=b"Non-UTF8 binary payload: \x80",
        )

        assert response.status == "200 OK"
        assert response.headers == Headers(
            [
                ("key1", "value1"),
                ("key2", "value2"),
            ]
        )
        assert [b for b in response.response] == [
            b"This is a ",
            b"non-UTF8 success response: \x80",
        ]

    def test_success_app_does_not_read_payload(self):
        client = Client(SubprocessMiddleware(wrapped_app))
        large_payload_data = bytearray(20 * 1024 * 1024)
        response = client.post(
            "/test_success_app_does_not_read_payload",
            data=bytes(large_payload_data),
        )

        assert response.status == "200 OK"
        assert [b for b in response.response] == [b"This is a successful response"]

    def test_success_with_payload_and_cpu_reservation_reset(self):
        reset_cpu_calls = []

        def reset_cpu_reservation_callback(num_cpus: int):
            reset_cpu_calls.append(num_cpus)

        client = Client(SubprocessMiddleware(wrapped_app))
        response = client.post(
            "/test_success_with_payload_and_cpu_reservation_reset",
            environ_overrides={"RESET_CPU_RESERVATION": reset_cpu_reservation_callback},
        )

        assert response.status == "200 OK"
        assert [b for b in response.response] == [b"This is a ", b"successful response"]
        assert reset_cpu_calls == [7]

    def test_no_cpu_reservation_reset_if_none_in_original_request(self):
        client = Client(SubprocessMiddleware(wrapped_app))
        response = client.post(
            "/test_no_cpu_reservation_reset_if_none_in_original_request",
        )

        assert response.status == "200 OK"
        assert [b for b in response.response] == [b"This is a successful response"]

    def test_failed_request_with_wsgi_error_output(self):
        client = Client(SubprocessMiddleware(wrapped_app))

        error_output = io.StringIO()
        response = client.post(
            "/test_failed_request_with_wsgi_error_output",
            environ_overrides={"wsgi.errors": error_output},
        )

        assert response.status == "500 Internal Server Error"
        assert [b for b in response.response] == []
        assert error_output.getvalue() == "First error output\nSecond error output\n"

    def test_exception_raised_in_wrapped_app(self):
        client = Client(SubprocessMiddleware(wrapped_app))

        with pytest.raises(Exception) as pytest_exc_info:
            client.post("/test_exception_raised_in_wrapped_app")

        exc_msg = pytest_exc_info.value.args[0]
        exc_traceback = "\n".join(traceback.format_tb(pytest_exc_info.tb))
        assert "This is an exception message" in exc_msg
        assert "test_subprocess_middleware.py" in exc_traceback
        assert "a_function_in_the_wrapped_app_callstack" in exc_traceback

    def test_exception_returned_from_start_response(self):
        client = Client(SubprocessMiddleware(wrapped_app))

        with pytest.raises(Exception) as pytest_exc_info:
            client.post("/test_exception_returned_from_start_response")

        exc_msg = pytest_exc_info.value.args[0]
        exc_traceback = "\n".join(traceback.format_tb(pytest_exc_info.tb))
        assert "This is an exception message" in exc_msg
        assert "test_subprocess_middleware.py" in exc_traceback
        assert "a_function_in_the_wrapped_app_callstack" in exc_traceback

    def test_wrapped_app_dies_from_signal(self):
        client = Client(SubprocessMiddleware(wrapped_app))

        with pytest.raises(Exception) as pytest_exc_info:
            client.post("/test_wrapped_app_dies_from_signal")

        exc_msg = pytest_exc_info.value.args[0]
        assert "Failed to read from WSGI request subprocess!" in exc_msg

    def test_globals_not_reinitialized_for_each_request(self):
        client = Client(SubprocessMiddleware(wrapped_app))

        response1 = client.post("/test_globals_not_reinitialized_for_each_request")
        response2 = client.post("/test_globals_not_reinitialized_for_each_request")

        response1_data = [b for b in response1.response]
        response2_data = [b for b in response2.response]

        assert response1_data[0].startswith(b"TEST_GLOBAL_VAR:")
        assert response1_data == response2_data
