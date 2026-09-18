# src/pub_quiz_agent/pub_quiz_models.py

from pydantic import BaseModel, Field, computed_field
from uuid import uuid4
from typing import Literal

class Question(BaseModel):

    """
    A model representing one pub trivia question
    """

    question: str = Field(..., description="A multiple choice pub trivia question. Max 1-2 sentences.")
    choices: list[str] = Field(..., description="A list of possible answers to the question. *EXACTLY ONE* choice must be the correct answer. The others should should be incorrect but also seem feasible.")
    answer_idx: int = Field(..., description="The zero-based index of the correct item from the choices list.")
    topic: Literal[
        "HISTORY",
        "GEOGRAPHY",
        "CINEMA",
        "SCIENCE_AND_TECNOLOGY",
        "SPORTS",
        "MUSIC",
        "LITURATURE",
        "CUISINE",
        "POPULAR_CULTURE",
        "GAMING",
        "MYTHOLOGY",
        "OTHER"
    ] = Field(..., description="The category that best fits the question's main topic.")
    tags: list[str] = Field(..., description="A list of  1-2 word tags that help further characterize the topic of the question. Examples: 'sci fi', 'famous buildings', 'deceased people', 'cinematic villians', 'robots', 'medicine', 'business' etc. These tags will help the quiz-master agent look up thematically appropriate questions for a given theme.")

    @computed_field
    @property
    def question_uuid_string(self)->str:
        return str(uuid4())

class Questions(BaseModel):
    """
    A model representing a collection of questions to be added to a trivia database
    """
    questions: list[Question] = Field(..., description="A list of Questions")

class QuestionsGeneratorInput(BaseModel):
    number_of_questions: int
    theme: str
