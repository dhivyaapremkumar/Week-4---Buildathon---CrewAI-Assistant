from crewai import Task, Crew, Process

from agents import (
    greeting_agent,
    search_agent,
    logger_agent,
)
def run_crew(user_query):
        greeting_task = Task(
        description=f"""
        The user asked:

        {user_query}

        Welcome the user professionally.
        Acknowledge the user's query.
        Inform the user that the Search Agent will search the web.

        Do not answer the question.
        """,
        expected_output="A professional greeting.",
        agent=greeting_agent
    )
        search_task = Task(
    description=f"""
    IMPORTANT:

    Use the user's query EXACTLY as given.

    User Query:
    {user_query}

    Do not modify the query.

    Do not add any year.

    Do not add additional keywords.

    Use the Google Search Tool with the exact query.

    After retrieving the search results,
    summarize them professionally.
    """,

    expected_output="A summarized web search result.",

    agent=search_agent,

    context=[greeting_task]
)
        logger_task = Task(
        description="""
        Create a clean execution report.

        Include:
        - Greeting Agent output
        - Search Agent output

        Format it professionally.
        """,
        expected_output="Formatted execution log.",
        agent=logger_agent,
        context=[
            greeting_task,
            search_task
        ]
    )
        crew = Crew(
        agents=[
            greeting_agent,
            search_agent,
            logger_agent
        ],
        tasks=[
            greeting_task,
            search_task,
            logger_task
        ],
        process=Process.sequential,
        verbose=True
    )
        result = crew.kickoff()
        return {
    "success": True,
    "query": user_query,

    "greeting_output": greeting_task.output.raw,

    "search_output": search_task.output.raw,

    "logger_output": logger_task.output.raw,

    "final_output": result.raw
}
  