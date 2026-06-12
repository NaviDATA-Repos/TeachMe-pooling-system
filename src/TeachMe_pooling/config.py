"""Constants for the MATHANX pooling system."""

from __future__ import annotations

# ── CONFIG: constants & fixed lookup tables ────────────────────────────────
SOCIO_COLS = [
    "Model",
    "mode",
    "gender",
    "age",
    "sexual_orientation",
    "city",
    "employment_status",
    "education",
    "parent_1_education",
    "parent_2_education",
    "marital_status",
    "children",
    "migration_status",
    "religious_beliefs",
    "hobbies",
    "fav_subjects",
    "hat_subjects",
    "ocean_openness_level",
    "ocean_conscientiousness_level",
    "ocean_extraversion_level",
    "ocean_agreeableness_level",
    "ocean_neuroticism_level",
]

TOPIC_OPTIONS = [
    "Math Relationship",
    "Math Anxiety",
    "AI for Math Learning",
    "Solving Equations",
    "Stationary Points",
    "PCA",
    "LLMs in Education",
]

VIEW_MODES = ["Topics", "Psy. Scales", "Networks", "Quizzes"]

# Sidebar filter groups — also reused to group the persona card by category.
FILTER_GROUPS = {
    "LLMs / Modality": ["Model", "mode"],
    "Demographics": [
        "gender",
        "age",
        "sexual_orientation",
        "city",
        "religious_beliefs",
        "marital_status",
        "children",
        "migration_status",
    ],
    "Job & Education": [
        "employment_status",
        "education",
        "parent_1_education",
        "parent_2_education",
        "fav_subjects",
        "hat_subjects",
    ],
    "Psychological Profile": [
        "ocean_openness_level",
        "ocean_conscientiousness_level",
        "ocean_extraversion_level",
        "ocean_agreeableness_level",
        "ocean_neuroticism_level",
        "hobbies",
    ],
}

# Topic prompts and the dataframe columns that hold each topic response.
TOPIC_QUESTIONS = {
    "Math Relationship":    "What is your relationship with mathematics?",
    "Math Anxiety":         "Do you ever get anxious when thinking about mathematics?",
    "AI for Math Learning": "Did you ever use AI to support your math learning in the last year? If yes, how was your experience?",
    "Solving Equations":    "How would you explain, step by step, how to solve a second order algebraic equation?",
    "Stationary Points":    "How would you explain, step by step, how to find the stationary points of an equation y = f(x)?",
    "PCA":                  "Briefly, how do you perform a Principal Component Analysis? Should I get anxious about its mathematics?",
    "LLMs in Education":    "According to you, how can LLMs be used to innovate math learning in schools and universities?",
}

TOPIC_COLS = {
    "Math Relationship":    "answer_text_1",
    "Math Anxiety":         "answer_text_2",
    "AI for Math Learning": "answer_text_3",
    "Solving Equations":    "answer_text_4",
    "Stationary Points":    "answer_text_5",
    "PCA":                  "answer_text_6",
    "LLMs in Education":    "answer_text_7",
}

# Psychometric scales items count
SCALE_ITEMS = {
    "maes":  9,
    "amas":  9,
    "mseaq": 28,
}

# Call 4 — problem solving
QUIZ_ITEMS = 18

# ── Data-fetch configuration ───────────────────────────────────────────────
DATA_VERSION = "v1.0"
DATA_TAG = "data-v1.0"
DATA_FILENAME = "df_pooling_system.parquet"
RELEASE_URL = (
    "https://github.com/NaviDATA-Repos/TeachMe-pooling-system"
    f"/releases/download/{DATA_TAG}/{DATA_FILENAME}"
)
EXPECTED_SHA256: str | None = (
    "1f4b31923c84c1ca134be5c67b854b8c135ce4273812757bcb10dbce8bff3fcb"
)