# guardrails file to understand user intent


from langchain.prompts import PromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_core.output_parsers import StrOutputParser
import json
from operator import itemgetter


class guardrails:
    def __init__(self, model_name="llama3.2-vision"):
        """
        Initialize the chatbot with the specified model.
        """
        self.ollama_llm = Ollama(model=model_name, format="json")
        self.prompt_data ="""
        You're 'Gobal' a highly advanced and helpful AI assistant. You're role is to understand the user's query and identify the  user's intent and topic.
        STRICTLY stick to the Output structure provided
        restricted intent: {restricted_intent}
        user query: {user_query}
        output: {output}
        """
        self.prompt_template = PromptTemplate.from_template(self.prompt_data)
        self.output_parser = StrOutputParser()
        
        
    def get_intent(self, user_input, sensitive_topic=None):
        
        
        SENSITIVE_TOPICS = ["sexual", "violence", "politics", "healthcare", "legal","harmful", "war", "hate speech"]
        sensitive_topic = json.dumps(SENSITIVE_TOPICS)
        
        user_input_query = user_input
        #context = context
        
        restricted_intent = f"""
        The restricted user intents and topics are: {sensitive_topic}
        if the user intent pr topic is not in the restricted intents, then the output should be: "No", else the output should be: "Yes"
        """
        user_query = f"""
        The user query is: {user_input_query}
        """
        
        output = """{"restricted_intent": "Yes"/"No"}"""
        
        # Chain:
        
        chain = (
            {"restricted_intent": itemgetter("restricted_intent"),
            "user_query": itemgetter("user_query"),
            "output": itemgetter("output")}
            |self.prompt_template
            |self.ollama_llm
            |self.output_parser
        )

        # Invoke the chain
        response = chain.invoke({"restricted_intent": restricted_intent, "user_query": user_query, "output": output})
        response = json.loads(response)
        response_text = response["restricted_intent"]
        response_text = str(response_text)
        return response_text
