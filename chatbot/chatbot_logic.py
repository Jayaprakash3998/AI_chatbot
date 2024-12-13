# chatbot_logic.py

from langchain.prompts import PromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_core.output_parsers import StrOutputParser
import json
from operator import itemgetter
from guardrails import guardrails

class Chatbot:
    def __init__(self, model_name="llama3.2-vision"):
        """
        Initialize the chatbot with the specified model.
        """
        self.ollama_llm = Ollama(model=model_name, format="json")
        self.prompt_data ="""
        You're 'Gobal' a highly advanced and helpful AI assistant. You're role is to understand the user's query, context and provide a helpful response. You can ask follow-up questions to clarify the user's query if needed.
        Only provide precise and accurate information. Do not provide any personal, sensitive, Biased or harmful information.
        STRICTLY stick to the Output structure provided
        chat_context: {chat_context}
        user query: {user_query}
        output: {output}
        """
        self.prompt_template = PromptTemplate.from_template(self.prompt_data)
        self.output_parser = StrOutputParser()
        self.guardrail = guardrails()
        
        
    def get_response(self, user_input, context=None):
        
        user_input_query = user_input
        context = context
        
        chat_context = f"""
        The chat_context is: {context}
        """
        user_query = f"""
        The user query is: {user_input_query}
        """
        
        output = """{"chat_response": "obtained chat response"}"""
        
        user_intent = self.guardrail.get_intent(user_input_query)
        
        if user_intent == "Yes":
            return "Sorry , I'm not able to provide a response regarding political, harmful, legal and health related topics."
        
        

        # Format the conversation context
        formatted_context = "\n".join([f"User: {q}\nAssistant: {a}" for q, a in context])
        
        # Chain:
        
        chain = (
            {"chat_context": itemgetter("chat_context"),
             "user_query": itemgetter("user_query"),
             "output": itemgetter("output")}
            |self.prompt_template
            |self.ollama_llm
            |self.output_parser
        )

        # Invoke the chain
        response = chain.invoke({"chat_context": formatted_context, "user_query": user_query, "output": output})
        response = json.loads(response)
        response_text = response["chat_response"]
        response_text = str(response_text)
        return response_text
