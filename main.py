import os
import openai
from crewai import Crew, Process

from textwrap import dedent
import tkinter as tk
from tkinter import messagebox, font
from tkinter import ttk

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

        meal_generation_tasks = tasks.batch_meal_generation_task(
                meal_idea_agent,
                meal_types=MEAL_TYPES,
                input_criteria=self.input_criteria,
            )

        nutrition_value_task = tasks.nutrition_value_task(
            nutrition_agent, meal_generation_tasks
        )

        meal_planning_task = tasks.meal_planning_task(
            meal_planning_agent, nutrition_value_task, self.nutritional_requirements
        )

        reporting_task = tasks.reporting_task(frontend_agent, meal_planning_task)

        crew = Crew(
            agents=[meal_idea_agent, nutrition_agent, meal_planning_agent, frontend_agent],
            tasks=[meal_generation_tasks, nutrition_value_task, meal_planning_task, reporting_task],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()
        return result


def run_meal_planner():
    input_dietary = dietary_entry.get()
    input_exclusions = exclusions_entry.get()

    nutritional_requirements = f"""
    2,650 calories/day
    160 grams/day protein
    75 grams/day fat
    350 grams/day carbohydrates
    60 grams/day sugar
    25 grams/day saturated fat
    """

    input_criteria = f"""
    Dietary requirements are: {input_dietary}
    Food exclusions are: {input_exclusions}
    """

    meal_plan_crew = MealPlannerCrew(input_criteria, nutritional_requirements)
    meal_plan_result = meal_plan_crew.run()
    print("\n\n########################")
    print("## Here is you Meal Planner Crew results:")
    print("########################\n")
    print(meal_plan_result)
    messagebox.showinfo("Meal Planner", "Meal plan is generated!\nCheck your output files.")

    root.destroy()


if __name__ == "__main__":
    print("## Welcome to the Meal Planner")
    print("-------------------------------")

    root = tk.Tk()
    root.title("Meal Planner")

    tk.Label(root, text="Do you have any dietary requirements?").grid(row=0, column=0, padx=10, pady=5)
    dietary_entry = tk.Entry(root, width=40)
    dietary_entry.grid(row=0, column=1)

    tk.Label(root, text="What foods do you dislike?").grid(row=1, column=0, padx=10, pady=5)
    exclusions_entry = tk.Entry(root, width=40)
    exclusions_entry.grid(row=1, column=1)

    run_button = tk.Button(root, text="Run Meal Planner", command=run_meal_planner)
    run_button.grid(row=2, column=0, columnspan=2, pady=10)

    root.mainloop()
