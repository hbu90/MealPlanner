from crewai import Task
from textwrap import dedent


class MealPlannerTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def meal_generation_task(self, agent, meal_type, input_criteria):
        return Task(
            description=dedent(
                f"""
            {self.__tip_section()}

            Generate 40 unique {meal_type} meal ideas that meet the {input_criteria}.
            Note that dietary requirements should be met and any food exclusions mentioned should not be used. 
            For each idea, list ingredients with precise amounts, for one portion.
        """
            ),
            expected_output="A JSON array of 40 meal objects, each with name, ingredients, and amounts.",
            agent=agent,
            async_execution=True,
            output_file="./meal_ideas.json",
        )

    def nutrition_value_task(self, agent, meal_plan_task):
        return Task(
            description=dedent(
                f"""

            {self.__tip_section()}

            Examine each meal given in the JSON array and append additional information for:
            total calories, total carbohydrates, total carbohydrates that sugar, total fat, 
            total saturated fats, total protein 
            
        """
            ),
            expected_output="An updated JSON array that contains the total nutritional values.",
            agent=agent,
            context=meal_plan_task,
            output_file="./meal_ideas_with_cals.json",
        )

    def meal_planning_task(self, agent, enriched_meals_task, nutrition_requirements):
        return Task(
            description=dedent(
                f"""
                {self.__tip_section()}
                
                Using the nutritional data with the generated meal ideas, 
                consider the daily nutritional requirements {nutrition_requirements} 
                and plan a meal plan for one week that contains breakfast, lunch, and dinner and up to two snacks.
                There can be one or zero snacks.
                """
            ),
            expected_output="A JSON array that has meal entries for every day of the week (Monday to Sunday) and "
            "entries for the meals breakfast, lunch, snacks, and dinner. Include calorie information.",
            agent=agent,
            context=[enriched_meals_task],
            output_file="./meal_plan.json",
        )

    def reporting_task(self, agent, meals_planned_task):
        return Task(
            description=dedent(
                f"""
            {self.__tip_section()}

            Compile the meal plan results into a detailed report in a HTML file.
        """
            ),
            expected_output="An HTML file with the results in the following format:"
            "The Day of the Week"
            "The Meal Type (e.g., Breakfast, Lunch, Dinner)"
            "- Meal Name"
            "   - Ingredients and Measurements"
            "   - Nutritional Values (calories, protein, fats, etc)",
            agent=agent,
            context=[meals_planned_task],
            output_file="./meal_plan.html",
        )
