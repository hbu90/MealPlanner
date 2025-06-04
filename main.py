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

    try:
        cals = int(calories_entry.get().strip())
        protein = int(protein_entry.get().strip())
        fat = int(fat_entry.get().strip())
        carbs = int(carbs_entry.get().strip())
        sugar = int(sugar_entry.get().strip())
        sat_fat = int(sat_fat_entry.get().strip())
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid integers for all nutritional fields.")
        return

    nutritional_requirements = f"""
    {cals:,} calories/day
    {protein:,} grams/day protein
    {fat:,} grams/day fat
    {carbs:,} grams/day carbohydrates
    {sugar:,} grams/day sugar
    {sat_fat:,} grams/day saturated fat
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

    tk.Label(root, text="Calories per day:").grid(row=2, column=0, padx=10, pady=3, sticky="e")
    calories_entry = tk.Entry(root, width=15)
    calories_entry.insert(0, "2650")  # optional default
    calories_entry.grid(row=2, column=1, sticky="w", padx=10, pady=3)

    tk.Label(root, text="Protein (g/day):").grid(row=3, column=0, padx=10, pady=3, sticky="e")
    protein_entry = tk.Entry(root, width=15)
    protein_entry.insert(0, "160")
    protein_entry.grid(row=3, column=1, sticky="w", padx=10, pady=3)

    tk.Label(root, text="Fat (g/day):").grid(row=4, column=0, padx=10, pady=3, sticky="e")
    fat_entry = tk.Entry(root, width=15)
    fat_entry.insert(0, "75")
    fat_entry.grid(row=4, column=1, sticky="w", padx=10, pady=3)

    tk.Label(root, text="Carbs (g/day):").grid(row=5, column=0, padx=10, pady=3, sticky="e")
    carbs_entry = tk.Entry(root, width=15)
    carbs_entry.insert(0, "350")
    carbs_entry.grid(row=5, column=1, sticky="w", padx=10, pady=3)

    tk.Label(root, text="Sugar (g/day):").grid(row=6, column=0, padx=10, pady=3, sticky="e")
    sugar_entry = tk.Entry(root, width=15)
    sugar_entry.insert(0, "60")
    sugar_entry.grid(row=6, column=1, sticky="w", padx=10, pady=3)

    tk.Label(root, text="Sat. Fat (g/day):").grid(row=7, column=0, padx=10, pady=3, sticky="e")
    sat_fat_entry = tk.Entry(root, width=15)
    sat_fat_entry.insert(0, "25")
    sat_fat_entry.grid(row=7, column=1, sticky="w", padx=10, pady=3)

    run_button = tk.Button(root, text="Run Meal Planner", command=run_meal_planner)
    run_button.grid(row=8, column=0, columnspan=2, pady=15)

    root.mainloop()
