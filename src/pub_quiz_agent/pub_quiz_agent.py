from dotenv import load_dotenv
import json
import sys
from pathlib import Path
import asyncio
from agents import (
    Agent,
    Runner,
    RunResult,
    RunContextWrapper
)

SRC_ROOT: Path = Path(__file__).parent.parent # this is the src/ folder
sys.path.insert(0, str(SRC_ROOT))
from pub_quiz_agent.pub_quiz_agent_models import Question, Questions, QuestionsGeneratorInput

AGENT_INSTRUCTIONS: str = """
You are an expert Pub Trivia Question Generator. Your task is to generate a batch of high-quality, engaging multiple-choice trivia questions based on the user's provided input.

### INPUT PARAMETERS
You will receive:
1. `number_of_questions`: The total number of `Question` objects to generate.
2. `theme`: The primary theme or subject focus for the generated trivia batch.

### CORE INSTRUCTIONS
1. **Quantity**: You MUST generate exactly the requested `number_of_questions`.
2. **Theme Alignment**: Ensure every question ties into or strongly aligns with the provided `theme`.
3. **Question Rules**:
   - Keep the question body concise (1-2 sentences max).
   - Questions should feel like classic pub trivia: fun, challenging, and clear.
4. **Choices & Correct Answer**:
   - Provide realistic multiple-choice options (typically 4 choices).
   - Ensure EXACTLY ONE option is correct.
   - Set `answer_idx` to the zero-based index (0, 1, 2, ...) corresponding to the correct answer in your `choices` list.
   - Distractors must be plausible and well-researched to make the quiz challenging.
5. **Categorization**:
   - Map each question to the most accurate topic from the strict `Literal` enum list provided in the schema (`HISTORY`, `GEOGRAPHY`, `CINEMA`, `SCIENCE_AND_TECNOLOGY`, `SPORTS`, `MUSIC`, `LITURATURE`, `CUISINE`, `POPULAR_CULTURE`, `GAMING`, `MYTHOLOGY`, `OTHER`).
   - *Note*: Keep literal spelling intact (`SCIENCE_AND_TECNOLOGY`, `LITURATURE`).
6. **Tags**:
   - Include 1-3 short (1-2 word) tags per question to enable downstream filtering by the Quizmaster Agent (e.g., "sci fi", "famous buildings", "80s music").

### CONSTRAINTS
- Return ONLY data matching the `Questions` output schema.
- Do not add conversational fluff or explanatory text outside the structured output.
"""

def get_question_generator_agent()->Agent:
    return Agent[QuestionsGeneratorInput](
        name="question_generator_agent",
        instructions=AGENT_INSTRUCTIONS,
        model="gpt-4o",
        output_type=Questions,
    )

load_dotenv()

class QuestionGeneratorAgent:
    async def run_workflow(self, input_context: QuestionsGeneratorInput)->Questions:
        my_agent: Agent[QuestionsGeneratorInput] = get_question_generator_agent()
        run_result: RunResult = await Runner.run(
            starting_agent=my_agent,
            context=input_context,
            input=f"Generate {input_context.number_of_questions} questions fitting the theme: {input_context.theme}."
        )
        return run_result.final_output_as(Questions)

async def main():

    input_ctx: QuestionsGeneratorInput  = QuestionsGeneratorInput(
        number_of_questions=20,
        theme="Late 1990s and early 2000s Internet culture"
    )

    questions: Questions = await QuestionGeneratorAgent().run_workflow(input_ctx)

    # save jsons
    out_json: str = questions.model_dump_json(indent=2)
    schema_str: str = json.dumps(Questions.model_json_schema(), indent=2)
    with open("schema.json", 'w') as f:
        f.write(schema_str)
    with open("example_questions.json", 'w') as f:
        f.write(out_json)

    
if __name__ == "__main__":
    asyncio.run(main())


