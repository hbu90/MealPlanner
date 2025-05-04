from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI


class MealPlannerAgents:
    def __init__(self):
        self.OpenAIGPT4_1_MINI = ChatOpenAI(model_name="gpt-4.1-mini", temperature=0.7)
        self.OpenAIGPT4_1_NANO = ChatOpenAI(model_name="gpt-4.1-nano", temperature=0.7)

    def meal_idea_agent(self):
        return Agent(
            role="Meal Idea Generator",
            backstory=dedent(
                f"""You are a creative Head Chef with a deep understanding of recipes and nutrition."""
            ),
            goal=dedent(
                f"""Generate 5 meal ideas for a given meal type that satisfy 
                a set of requirements. You should provide ingredients and amounts for one portion."""
            ),
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4_1_MINI,
        )

    def frontend_agent(self):
        return Agent(
            role="Senior AI Frontend Engineer",
            backstory=dedent(
                f"""You are a competent frontend engineer writing HTML and CSS 
            with decades of experience."
            "You have also been working with AI for decades and understand it well."""
            ),
            goal=dedent(f"""Compile the results into a HTML file."""),
            verbose=True,
            llm=self.OpenAIGPT4_1_NANO,
        )
