from transformers import pipeline

# Load HuggingFace pipelines
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
summarizer_pipeline = pipeline("summarization", model="t5-small", device=-1)


class Agent:
    """
    A flexible legal agent that can perform QA or summarization based on the specified task.
    """
    def __init__(self, system_msg=None, recipient="user", task="qa"):
        self.system_msg = system_msg.strip() if system_msg else ""
        self.recipient = recipient
        self.task = task

    def respond(self, query="", context=""):
        """
        Generate a response based on task type.
        - For 'qa': Answer questions using provided context
        - For 'summarization': Generate summary of the context
        """
        try:
            if self.task == "qa":
                if not context.strip():
                    return "Sorry, I need some context to answer that."
                full_context = f"{self.system_msg}\n{context}".strip()
                full_context = full_context[:3500]  # Prevent overloading input
                result = qa_pipeline(question=query.strip(), context=full_context)
                return result.get('answer', 'Sorry, I could not find a clear answer.')

            elif self.task == "summarization":
                full_input = f"{self.system_msg}\n{context}".strip()
                result = summarizer_pipeline(full_input, max_length=512, min_length=80, do_sample=False)
                return result[0]['summary_text']

            else:
                return "❌ Unsupported task type."

        except Exception as e:
            return f"⚠️ Error: {str(e)}"

# === Predefined Agents ===

questioner = Agent(
    task="qa",
    system_msg="""
You are Law Justifier, an AI-powered legal assistant specializing in Indian law.
You answer user questions based only on the context provided.
Use simple, accurate legal language and avoid speculation.
"""
)

tone_analyzer = Agent(
    task="qa",
    system_msg="""
You are a tone analysis expert.
Based on the provided legal document, assess whether the tone is formal, aggressive,
conciliatory, neutral, or mixed. Justify your analysis briefly.
"""
)

summarizer = Agent(
    task="summarization",
    system_msg="""
You are a legal document summarizer. Summarize the legal text clearly, focusing on:
- Purpose of the document
- Legal obligations and rights
- Key clauses (e.g., data use, liabilities, terms)
- Summary of implications for the reader
"""
)
