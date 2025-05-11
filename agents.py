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
                f"""Generate 40 meal ideas for a given meal type that satisfy 
                a set of requirements. You should provide ingredients and amounts for one portion."""
            ),
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4_1_MINI,
        )

    def nutrition_agent(self):
        return Agent(
            role="Nutrition Expert",
            backstory=dedent(
                f"""You are a Nutrition Expert with a deep understanding of calories, food macros, and nutrition."""
            ),
            goal=dedent(
                f"""For a set of meals, calculate for each the:
                    total calories, total carbohydrates, total carbohydrates that sugar, total fat, 
                    total saturated fats, total protein """
            ),
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4_1_MINI,
        )

    def meal_planner_agent(self):
        return Agent(
            role="Meal Planning Expert",
            backstory=dedent(
                f"""You are a Meal Planning Expert who can construct weekly meal plans that meet 
                calorie and macronutrient requirements,"""
            ),
            goal=dedent(
                f"""For a given set of meal options and calorie and macronutrient daily requirements, 
                create a meal plan for one week that contains breakfast, lunch, and dinner and includes two snacks."""
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
