import pytest
import asyncio

"""
This conftest.py is used for shared fixtures across tests.
pytest-asyncio handles event loop management for async tests automatically.

Example shared fixture (can be uncommented and adapted):
# @pytest.fixture(scope='session')
# def event_loop():
#     """Create an instance of the default event loop for the session."""
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()
"""
