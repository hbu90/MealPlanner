from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI


class MealPlannerAgents:
    def __init__(self):
        self.OpenAIGPT4_1_MINI = ChatOpenAI(model_name="gpt-4.1-mini", temperature=0.7)
        self.OpenAIGPT4_1_NANO = ChatOpenAI(model_name="gpt-4.1-nano", temperature=0.7)
        self.OpenAIGPT4_o = ChatOpenAI(model_name="gpt-4o", temperature=0.7)
        self.OpenAIGPT4_1 = ChatOpenAI(model_name="gpt-4.1", temperature=0.7)

    def meal_idea_agent(self):
        return Agent(
            role="Meal Idea Generator",
            backstory=dedent(
                f"You are a Head Chef tasked with producing meal ideas in batches. Given a list of meal types, "
                f"iterate over each type and generate 50 JSON-formatted meal objects. "
                f"At the end, merge all results into one JSON array and save to the specified output file."
            ),
            goal=dedent(
                f"""Generate 50 meal ideas for a given meal type that satisfy 
                a set of requirements. You should provide ingredients and amounts for one portion."""
            ),
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4_1,
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
            llm=self.OpenAIGPT4_1,
        )

    def meal_planner_agent(self):
        return Agent(
            role="Meal Planning Expert",
            backstory=dedent(
                f"""You are a Meal Planning Expert who can construct weekly meal plans that meet 
                calorie and macronutrient requirements."""
            ),
            goal=dedent(
                f"""For a given set of meal options and calorie and macronutrient daily requirements, 
                create a meal plan for one week that contains breakfast, lunch, and dinner 
                and includes one or two snacks."""
            ),
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4_1,
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
            llm=self.OpenAIGPT4_1,
        )
