from crewai import Task
from textwrap import dedent


class MealPlannerTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def meal_generation_task(self, agent, meal_type, input_criteria):
        return Task(
            description=dedent(
                f"""
            Do something as part of task 1

            {self.__tip_section()}

            Generate 10 unique {meal_type} meal ideas that meet the {input_criteria}. 
            For each idea, list ingredients with precise amounts, for one portion.
        """
            ),
            expected_output="A JSON array of 10 meal objects, each with name, ingredients, and amounts.",
            agent=agent,
            async_execution=True,
        )

    def reporting_task(self, agent, meal_plan_task):
        return Task(
            description=dedent(
                f"""
            {self.__tip_section()}

            Compile the meal plan results into a detailed report in a HTML file.
        """
            ),
            expected_output="An HTML file with the results in the following format:"
            "The Meal Type (e.g., Breakfast, Lunch, Dinner)"
            "- Meal Name"
            "- Ingredients and Measurements",
            agent=agent,
            context=meal_plan_task,
            output_file="./meal_plan.html",
        )
