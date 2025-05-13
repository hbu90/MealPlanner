from crewai import Task
from textwrap import dedent

PER_MEAL_CALORIE = {
    "breakfast": (600, 800),
    "lunch":     (600, 800),
    "dinner":    (600, 800),
    "snack":     (200, 400),
}


class MealPlannerTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def meal_generation_task(self, agent, meal_type, input_criteria):
        return Task(
            description=dedent(
                f"""
            {self.__tip_section()}

            Generate 40 unique {meal_type} meal ideas that meet the {input_criteria}. 
            **Each meal must contain between {PER_MEAL_CALORIE[meal_type][0]} and \
            {PER_MEAL_CALORIE[meal_type][1]} calories.**  
            Note that dietary requirements should be met and any food exclusions mentioned should not be used. 
            For each idea, list ingredients with precise amounts, for one portion.
        """
            ),
            expected_output="A JSON array of 40 meal objects, each with the meal type, name, ingredients, and amounts.",
            agent=agent,
            async_execution=True,
            output_file=f"./meal_ideas_{meal_type}.json",
        )

    def aggregate_meal_ideas_task(self, agent):
        return Task(
            description="""
                Read ./meal_ideas_breakfast.json, lunch, dinner, snack;
                concatenate into one JSON array and write to ./all_meal_ideas.json
            """,
            expected_output="A single JSON array of all meal ideas.",
            agent=agent,
            context=[],
            output_file="./all_meal_ideas.json",
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
                
                Using the nutritional data from `enriched_meals_task`, assemble a **7-day** meal plan (Monday–Sunday) 
                with **three meals** (breakfast, lunch, dinner) and **up to two snacks per day** that collectively meet 
                the daily nutritional targets **{nutrition_requirements}**, within a **±10%** tolerance.
                """
            ),
            expected_output=(
                "A JSON object with keys Monday…Sunday, each containing sub-keys "
                "`breakfast`, `lunch`, `dinner`, and `snacks` (an array of 0–2 items), "
                "with calorie and macro information for each meal."
            ),
            agent=agent,
            context=[enriched_meals_task],
            output_file="./meal_files/meal_plan.json",
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
