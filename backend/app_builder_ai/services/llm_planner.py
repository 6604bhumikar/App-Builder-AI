from app_builder_ai.core.config import settings


class LlmPlanner:
    """Optional LangChain planner adapter.

    The generator remains deterministic without an API key. When configured, this adapter can enrich
    the summary while the validated workflow still owns the final tool calls.
    """

    def is_enabled(self) -> bool:
        return bool(settings.openai_api_key)

    def summarize(self, prompt: str) -> str:
        if not self.is_enabled():
            return prompt.strip()

        try:
            from langchain_core.prompts import ChatPromptTemplate
            from langchain_openai import ChatOpenAI
        except ImportError:
            return prompt.strip()

        template = ChatPromptTemplate.from_messages(
            [
                ("system", "Summarize the requested app as one concise product brief."),
                ("human", "{prompt}"),
            ]
        )
        model = ChatOpenAI(model=settings.llm_model, api_key=settings.openai_api_key)
        response = (template | model).invoke({"prompt": prompt})
        return getattr(response, "content", prompt).strip()
