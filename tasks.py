from crewai import Task
from textwrap import dedent

PER_MEAL_CALORIE = {
    "breakfast": (600, 800),
    "lunch": (600, 800),
    "dinner": (600, 800),
    "snack": (200, 400),
}


class MealPlannerTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def batch_meal_generation_task(self, agent, meal_types, input_criteria):
        return Task(
            description=dedent(f"""
                {self.__tip_section()}

                You will generate 50 unique meal ideas **for each** of the following meal types:
                {', '.join(meal_types)}.  

                Requirements for **each** meal idea:
                - Calories between:
                    - Breakfast: {PER_MEAL_CALORIE['breakfast'][0]}–{PER_MEAL_CALORIE['breakfast'][1]} 
                    - Lunch: {PER_MEAL_CALORIE['lunch'][0]}–{PER_MEAL_CALORIE['lunch'][1]} 
                    - Dinner: {PER_MEAL_CALORIE['dinner'][0]}–{PER_MEAL_CALORIE['dinner'][1]} 
                    - Snack: {PER_MEAL_CALORIE['snack'][0]}–{PER_MEAL_CALORIE['snack'][1]} 
                - **Strictly** meet the dietary requirements and exclusions: {input_criteria}  
                - List ingredients with precise amounts for one portion.
                - Provide concise instructions for the recipe. 

                **Instruction:**  
                1. For each meal type in that list, produce a sub‐array of 50 JSON objects  
                2. Merge all sub‐arrays into one top‐level JSON array  
                3. Write the combined JSON array to `./meal_output_files/all_meal_ideas.json`
            """),
            expected_output="A single JSON array of 200 meal objects (50 per type), written to all_meal_ideas.json",
            agent=agent,
            async_execution=False,
            output_file="./meal_output_files/all_meal_ideas.json",
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
            context=[meal_plan_task],
            output_file="./meal_output_files/meal_ideas_with_cals.json",
        )

    def meal_planning_task(self, agent, enriched_meals_task, nutrition_requirements):
        return Task(
            description=dedent(
                f"""
                {self.__tip_section()}
                
                Using the nutritional data from `enriched_meals_task`, assemble a **7-day** meal plan (Monday–Sunday) 
                with **three meals** (breakfast, lunch, dinner) and **one or two snacks per day** that collectively meet 
                the daily nutritional targets **{nutrition_requirements}**, within a **±10%** tolerance.
                **YOU MUST SCALE UP MEAL(S) TO ENSURE THAT THE NUTRITIONAL TARGETS ARE MET**
                """
            ),
            expected_output=(
                "A JSON object with keys Monday…Sunday, each containing sub-keys "
                "`breakfast`, `lunch`, `dinner`, and `snacks` (an array of 1–2 items), "
                "with calorie and macro information for each meal. Also a 'total' key that has the total "
                "calorie and macro information for the day"
            ),
            agent=agent,
            context=[enriched_meals_task],
            output_file="./meal_output_files/meal_plan.json",
        )

    def reporting_task(self, agent, meals_planned_task):
        return Task(
            description=dedent(f"""
                {self.__tip_section()}
    
                Using the provided HTML skeleton (doctype, head, body, styles), insert a 
                `<section class="day-section" id="{{day}}">` for each day (Monday–Sunday).
                Within each section:
                  1. Add `<h2>{{day}}</h2>`.
                  2. For each meal type (breakfast, lunch, dinner), insert a 
                     `<div class="meal" data-type="{{meal_type}}">` containing:
                       - `<h3>{{meal_type.title()}}: {{meal.name}}</h3>`
                       - `<ul>` of `<li>{{ingredient}}: {{amount}}</li>`
                       - `<p class="instructions">{{meal.instructions}}</p> — the cooking or prep instructions`
                       - `<p class="meal-calories">Calories: {{meal.calories}}</p> — per-meal calorie info`
                       
                     Close `</div>`.
                  3. If snacks exist, create `<aside class="snacks">` with a `<ul>`.
                  4. Append a `<table class="nutrition-table">` summarizing that day’s totals:
                     | Nutrient        | Amount                     |
                     |-----------------|----------------------------|
                     | Calories        | {{totals.calories}}        |
                     | Protein (g)     | {{totals.protein}}         |
                     | Carbs (g)       | {{totals.carbs}}           |
                     | Sugars (g)      | {{totals.sugar}}           |
                     | Fat (g)         | {{totals.fat}}             |
                     | Sat Fat(g)      | {{totals.saturatedfat}}    |
                         
                Ensure proper closing of all HTML tags.
            """),
            expected_output=dedent("""
                A valid HTML file matching the skeleton, with:
                - Seven `<section>` blocks for each day.
                - Nested `<div>` for meals and `<aside>` for snacks.
                - A `<table>` summarizing daily nutrition.
            """),
            agent=agent,
            context=[meals_planned_task],
            output_file="./meal_output_files/meal_plan.html",
        )
