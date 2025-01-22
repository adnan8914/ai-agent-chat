from typing import Dict, Any
from langgraph.graph import StateGraph
from ..models.embedding_model import EmbeddingModel
from ..models.llm_model import LLMModel
from ..tools.web_search import WebSearchTool
from ..tools.email_writer import EmailWriter
from ..tools.customer_support import CustomerSupport
from ..tools.personal_assist import PersonalAssistant
from ..tools.content_creator import ContentCreator

class AgentWorkflow:
    def __init__(self):
        self.embedding_model = EmbeddingModel()
        self.llm_model = LLMModel()
        self.tools = {
            "web_search": WebSearchTool(),
            "email": EmailWriter(),
            "customer_support": CustomerSupport(),
            "personal_assist": PersonalAssistant(),
            "content_creator": ContentCreator()
        }
        
    def build_workflow(self) -> StateGraph:
        """
        Build the LangGraph workflow
        """
        # Initialize the graph
        graph = StateGraph()
        
        # Add nodes
        graph.add_node("process_input", self._process_input)
        graph.add_node("analyze_input", self._analyze_input)
        graph.add_node("route_to_tool", self._route_to_tool)
        graph.add_node("execute_tool", self._execute_tool)
        graph.add_node("generate_response", self._generate_response)
        
        # Define edges
        graph.add_edge("process_input", "analyze_input")
        graph.add_edge("analyze_input", "route_to_tool")
        graph.add_edge("route_to_tool", "execute_tool")
        graph.add_edge("execute_tool", "generate_response")
        
        return graph.compile()
    
    def _process_input(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process initial input and generate embeddings
        """
        input_text = state["input"]
        embeddings = self.embedding_model.get_embeddings(input_text)
        state["embeddings"] = embeddings
        return state
    
    def _analyze_input(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze input to determine intent and sentiment
        """
        input_text = state["input"]
        sentiment = self.embedding_model.get_sentiment(input_text)
        
        # Determine intent using LLM
        intent_prompt = f"Determine the intent of: {input_text}"
        intent = self.llm_model.generate({"input": intent_prompt})
        
        state["analysis"] = {
            "sentiment": sentiment,
            "intent": intent
        }
        return state
    
    def _route_to_tool(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route to appropriate tool based on analysis
        """
        intent = state["analysis"]["intent"]
        
        # Map intent to tool
        tool_mapping = {
            "search": "web_search",
            "email": "email",
            "support": "customer_support",
            "assist": "personal_assist",
            "content": "content_creator"
        }
        
        selected_tool = "personal_assist"  # default
        for intent_key, tool_name in tool_mapping.items():
            if intent_key in intent.lower():
                selected_tool = tool_name
                break
                
        state["selected_tool"] = selected_tool
        return state
    
    def _execute_tool(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute selected tool
        """
        tool_name = state["selected_tool"]
        tool = self.tools[tool_name]
        
        # Prepare tool input
        tool_input = {
            "query": state["input"],
            "context": {
                "sentiment": state["analysis"]["sentiment"],
                "intent": state["analysis"]["intent"]
            }
        }
        
        # Execute tool
        if tool_name == "customer_support":
            result = tool.handle_inquiry(tool_input["query"], tool_input["context"])
        elif tool_name == "personal_assist":
            result = tool.process_request(tool_input["query"], tool_input["context"])
        elif tool_name == "email":
            result = tool.compose_email(tool_input["context"])
        elif tool_name == "content_creator":
            result = tool.create_content(tool_input["query"], "general")
        else:
            result = tool.search(tool_input["query"])
            
        state["tool_result"] = result
        return state
    
    def _generate_response(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate final response using LLM
        """
        tool_result = state["tool_result"]
        
        # Prepare response prompt
        prompt = (
            f"Based on the tool result: {tool_result}\n"
            f"Generate a natural response for the user's input: {state['input']}"
        )
        
        response = self.llm_model.generate({"input": prompt})
        state["response"] = response
        return state 