# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for the ParallelAgent."""

import asyncio
from typing import AsyncGenerator

from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.agents.parallel_agent import ParallelAgent
from google.adk.events import Event
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types
import pytest
from typing_extensions import override


class _TestingAgent(BaseAgent):

  delay: float = 0
  """The delay before the agent generates an event."""

  @override
  async def _run_async_impl(
      self, ctx: InvocationContext
  ) -> AsyncGenerator[Event, None]:
    await asyncio.sleep(self.delay)
    yield Event(
        author=self.name,
        branch=ctx.branch,
        invocation_id=ctx.invocation_id,
        content=types.TextContent(
            parts=[types.Part(text=f'Hello, async {self.name}!')]
        ),
    )


async def _create_parent_invocation_context(
    test_name: str, agent: BaseAgent
) -> InvocationContext:
  session_service = InMemorySessionService()
  session = await session_service.create_session(
      app_name='test_app', user_id='test_user'
  )
  return InvocationContext(
      invocation_id=f'{test_name}_invocation_id',
      agent=agent,
      session=session,
      session_service=session_service,
  )


@pytest.mark.asyncio
async def test_run_async(request: pytest.FixtureRequest):
  agent1 = _TestingAgent(
      name=f'{request.function.__name__}_test_agent_1',
      delay=0.5,
  )
  agent2 = _TestingAgent(name=f'{request.function.__name__}_test_agent_2')
  parallel_agent = ParallelAgent(
      name=f'{request.function.__name__}_test_parallel_agent',
      sub_agents=[
          agent1,
          agent2,
      ],
  )
  parent_ctx = await _create_parent_invocation_context(
      request.function.__name__, parallel_agent
  )
  events = [e async for e in parallel_agent.run_async(parent_ctx)]

  assert len(events) == 2
  # agent2 generates an event first, then agent1. Because they run in parallel
  # and agent1 has a delay.
  assert events[0].author == agent2.name
  assert events[1].author == agent1.name
  assert events[0].branch.endswith(agent2.name)
  assert events[1].branch.endswith(agent1.name)
  assert events[0].content.parts[0].text == f'Hello, async {agent2.name}!'
  assert events[1].content.parts[0].text == f'Hello, async {agent1.name}!'
