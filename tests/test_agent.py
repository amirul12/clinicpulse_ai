"""Integration skeleton for ClinicPulse AI."""

import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types

from clinicpulse.agent import root_agent


async def main() -> None:
    """Executes a placeholder conversation until real logic lands."""

    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name="clinicpulse",
        user_id="demo_user",
        session_id="demo_session",
    )
    runner = Runner(
        agent=root_agent,
        app_name="clinicpulse",
        session_service=session_service,
    )

    queries = [
        "Patient Jane Doe is here with shortness of breath",
        "Symptoms began 2 days ago",
        "No further questions",
    ]

    for query in queries:
        print(f">>> {query}")
        async for event in runner.run_async(
            user_id="demo_user",
            session_id="demo_session",
            new_message=genai_types.Content(
                role="user",
                parts=[genai_types.Part.from_text(text=query)],
            ),
        ):
            if event.is_final_response() and event.content and event.content.parts:
                print(event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(main())
