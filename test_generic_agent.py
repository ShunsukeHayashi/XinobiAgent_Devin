"""
Test script for the GenericAgent implementation.
"""

import asyncio
from app.examples.generic_agent_example import run_generic_agent_example


async def test():
    """Run a simple test of the GenericAgent."""
    print('Running test with simplified goal...')
    await run_generic_agent_example('Print Hello World')


if __name__ == "__main__":
    asyncio.run(test())
