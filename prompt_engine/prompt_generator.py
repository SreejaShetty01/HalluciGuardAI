"""
Prompt Engineering Generator
Generates Zero-Shot, Few-Shot, Chain-of-Thought, and Role-Based prompt variants.
"""


class PromptGenerator:
    """Generates multiple prompt engineering variants for a given query."""

    EXAMPLES = [
        {
            "q": "What is hypertension?",
            "a": "Hypertension (high blood pressure) is a chronic condition where arterial blood pressure persistently "
                 "exceeds 130/80 mmHg. It is caused by factors including genetics, high-sodium diet, obesity, stress, "
                 "and sedentary lifestyle. It significantly increases risk of heart disease, stroke, kidney failure, "
                 "and vision loss. Treatment involves lifestyle changes and antihypertensive medications."
        },
        {
            "q": "What is photosynthesis?",
            "a": "Photosynthesis is the biological process by which chlorophyll-containing organisms (plants, algae, "
                 "cyanobacteria) convert light energy, carbon dioxide, and water into glucose and oxygen. The overall "
                 "equation is: 6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂. It occurs in two stages: light-dependent "
                 "reactions (in thylakoids) and the Calvin cycle (in stroma)."
        },
        {
            "q": "What is machine learning?",
            "a": "Machine learning (ML) is a subset of artificial intelligence where systems learn patterns from data "
                 "to make predictions or decisions without being explicitly programmed. Key paradigms include "
                 "supervised learning (labeled data), unsupervised learning (unlabeled data), and reinforcement "
                 "learning (reward-based). Common algorithms: linear regression, decision trees, neural networks, SVMs."
        },
    ]

    def __init__(self, query: str):
        self.query = query.strip()

    def generate_zero_shot(self) -> str:
        return (
            f"Answer the following question accurately and concisely based on verified facts.\n\n"
            f"Question: {self.query}\n\n"
            f"Answer:"
        )

    def generate_few_shot(self) -> str:
        examples_text = ""
        for i, ex in enumerate(self.EXAMPLES, 1):
            examples_text += f"\nExample {i}:\nQ: {ex['q']}\nA: {ex['a']}\n"

        return (
            f"You are a knowledgeable assistant. Study these example question-answer pairs for style and accuracy:\n"
            f"{examples_text}\n"
            f"Now answer this question with the same clarity, accuracy, and level of detail:\n\n"
            f"Q: {self.query}\n"
            f"A:"
        )

    def generate_chain_of_thought(self) -> str:
        return (
            f"Let's work through this question step by step to ensure an accurate, well-reasoned answer.\n\n"
            f"Question: {self.query}\n\n"
            f"Step-by-step reasoning:\n\n"
            f"Step 1 — Identify what is being asked:\n"
            f"The question asks about: {self.query}\n\n"
            f"Step 2 — Recall relevant domain knowledge:\n"
            f"[Identify and list the key concepts, facts, definitions, or mechanisms involved]\n\n"
            f"Step 3 — Organize information logically:\n"
            f"[Structure the facts from foundational to specific]\n\n"
            f"Step 4 — Verify for accuracy:\n"
            f"[Check that each claim is grounded in established knowledge, not speculation]\n\n"
            f"Step 5 — Formulate the final answer:\n"
            f"Based on the above reasoning, the complete and accurate answer is:\n"
        )

    def generate_role_based(self) -> str:
        return (
            f"You are a distinguished professor and subject matter expert with a PhD from a top-tier research "
            f"university and 30+ years of academic and practical experience. You have published peer-reviewed "
            f"research and are known internationally for your precision and accuracy.\n\n"
            f"Your strict guidelines:\n"
            f"• Only state verifiable facts — never guess or fabricate data\n"
            f"• If uncertain about a specific detail, explicitly state 'I am not certain about...'\n"
            f"• Provide concise but comprehensive explanations\n"
            f"• Use precise scientific/technical language with brief definitions when needed\n"
            f"• Never invent statistics, dates, names, or citations\n"
            f"• Structure your answer with key points\n\n"
            f"As this expert, please answer the following question:\n\n"
            f"Question: {self.query}\n\n"
            f"Expert Answer:"
        )

    def generate_all(self) -> dict:
        return {
            'zero_shot': {
                'label': 'Zero-Shot',
                'prompt': self.generate_zero_shot(),
                'description': 'Direct question with no examples. Tests baseline model factual accuracy.',
                'color': '#6366f1',
                'icon': 'fa-bolt',
            },
            'few_shot': {
                'label': 'Few-Shot',
                'prompt': self.generate_few_shot(),
                'description': 'Provides 3 curated high-quality examples before posing the question.',
                'color': '#10b981',
                'icon': 'fa-clone',
            },
            'chain_of_thought': {
                'label': 'Chain-of-Thought',
                'prompt': self.generate_chain_of_thought(),
                'description': 'Forces structured step-by-step reasoning before answering.',
                'color': '#f59e0b',
                'icon': 'fa-link',
            },
            'role_based': {
                'label': 'Role-Based',
                'prompt': self.generate_role_based(),
                'description': 'Expert persona with strict factual accuracy constraints.',
                'color': '#ef4444',
                'icon': 'fa-user-tie',
            },
        }
