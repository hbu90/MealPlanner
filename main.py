import os
import openai
from crewai import Crew, Process

from textwrap import dedent
from agents import MealPlannerAgents
from tasks import MealPlannerTasks

openai.api_key = os.getenv("OPENAI_API_KEY")

MEAL_TYPES = ["breakfast", "lunch", "dinner", "snack"]


class MealPlannerCrew:
    def __init__(self, input_criteria):
        self.input_criteria = input_criteria

    def run(self):
        agents = MealPlannerAgents()
        tasks = MealPlannerTasks()

        meal_idea_agent = agents.meal_idea_agent()
        nutrition_agent = agents.nutrition_agent()
        frontend_agent = agents.frontend_agent()

        meal_generation_tasks = [
            tasks.meal_generation_task(
                meal_idea_agent,
                meal_type,
                self.input_criteria,
            )
            for meal_type in MEAL_TYPES
        ]

        nutrition_value_task = tasks.nutrition_value_task(nutrition_agent, meal_generation_tasks)

        reporting_task = tasks.reporting_task(frontend_agent, nutrition_value_task)

        crew = Crew(
            agents=[meal_idea_agent, nutrition_agent, frontend_agent],
            tasks=meal_generation_tasks + [nutrition_value_task, reporting_task],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()
        return result


if __name__ == "__main__":
    print("## Welcome to the Meal Planner")
    print("-------------------------------")
    input_dietary = input(dedent("""Do you have any dietary requirements?"""))
    input_exclusions = input(dedent("""What foods do you dislike?"""))

    our_input_criteria = f"""
    Dietary requirements are: {input_dietary}
    Food exclusions are: {input_exclusions}
    """

    meal_plan_crew = MealPlannerCrew(our_input_criteria)
    meal_plan_result = meal_plan_crew.run()
    print("\n\n########################")
    print("## Here is you Meal Planner Crew results:")
    print("########################\n")
    print(meal_plan_result)
