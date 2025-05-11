import os
import openai
from crewai import Crew, Process

from textwrap import dedent
from agents import MealPlannerAgents
from tasks import MealPlannerTasks

openai.api_key = os.getenv("OPENAI_API_KEY")

MEAL_TYPES = ["breakfast", "lunch", "dinner", "snack"]


class MealPlannerCrew:
    def __init__(self, input_criteria, nutritional_requirements):
        self.input_criteria = input_criteria
        self.nutritional_requirements = nutritional_requirements

    def run(self):
        agents = MealPlannerAgents()
        tasks = MealPlannerTasks()

        meal_idea_agent = agents.meal_idea_agent()
        nutrition_agent = agents.nutrition_agent()
        meal_planning_agent = agents.meal_planner_agent()
        frontend_agent = agents.frontend_agent()

        meal_generation_tasks = [
            tasks.meal_generation_task(
                meal_idea_agent,
                meal_type,
                self.input_criteria,
            )
            for meal_type in MEAL_TYPES
        ]

        nutrition_value_task = tasks.nutrition_value_task(
            nutrition_agent, meal_generation_tasks
        )

        meal_planning_task = tasks.meal_planning_task(
            meal_planning_agent, nutrition_value_task, self.nutritional_requirements
        )

        reporting_task = tasks.reporting_task(frontend_agent, meal_planning_task)

        crew = Crew(
            agents=[meal_idea_agent, nutrition_agent, meal_planning_agent, frontend_agent],
            tasks=meal_generation_tasks + [nutrition_value_task, meal_planning_task, reporting_task],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()
        return result


if __name__ == "__main__":
    print("## Welcome to the Meal Planner")
    print("-------------------------------")
    # input_dietary = input(dedent("""Do you have any dietary requirements?"""))
    # input_exclusions = input(dedent("""What foods do you dislike?"""))

    input_dietary = "Gluten-free"
    input_exclusions = "Mushrooms"

    our_input_criteria = f"""
    Dietary requirements are: {input_dietary}
    Food exclusions are: {input_exclusions}
    """

    our_nutritional_requirements = f"""
    2,650 calories/day
    160 grams/day protein
    75 grams/day fat
    350 grams/day carbohydrates
    60 grams/day sugar
    25 grams/day saturated fat
    """

    meal_plan_crew = MealPlannerCrew(our_input_criteria, our_nutritional_requirements)
    meal_plan_result = meal_plan_crew.run()
    print("\n\n########################")
    print("## Here is you Meal Planner Crew results:")
    print("########################\n")
    print(meal_plan_result)
