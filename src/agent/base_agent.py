from typing import Dict, Any, List
from pydantic import BaseModel, Field
from langgraph.graph import Graph, StateGraph
from ..models.embedding_model import EmbeddingModel
from ..models.llm_model import LLMModel
from ..memory.buffer import WindowBuffer

class AgentState(BaseModel):
    input: str
    input_type: str
    embeddings: List[float] = Field(default_factory=list)
    sentiment: Dict[str, Any] = {}
    response: str = ""
    memory: List[Dict[str, str]] = []

class AIAgent:
    def __init__(self):
        self.embedding_model = EmbeddingModel()
        self.llm_model = LLMModel()
        self.memory = WindowBuffer()
        self.graph = self._build_graph()
        
    def _build_graph(self) -> StateGraph:
        """
        Build the LangGraph workflow
        """
        # Initialize the graph with Pydantic schema
        graph = StateGraph(AgentState)
        
        # Add nodes
        graph.add_node("process_input", self._process_input)
        graph.add_node("analyze_sentiment", self._analyze_sentiment)
        graph.add_node("route_to_tool", self._route_to_tool)
        graph.add_node("generate_response", self._generate_response)
        
        # Define edges
        graph.add_edge("process_input", "analyze_sentiment")
        graph.add_edge("analyze_sentiment", "route_to_tool")
        graph.add_edge("route_to_tool", "generate_response")
        
        # Set entry and end points
        graph.set_entry_point("process_input")
        graph.set_finish_point("generate_response")
        
        return graph.compile()
    
    def _process_input(self, state: AgentState) -> AgentState:
        """
        Process user input (text or audio)
        """
        input_type = state.input_type
        input_data = state.input
        
        if input_type == "audio":
            # Convert audio to text (implement speech_to_text logic)
            pass
            
        # Get embeddings
        embeddings = self.embedding_model.get_embeddings(input_data)
        state.embeddings = embeddings
        return state
    
    def _analyze_sentiment(self, state: AgentState) -> AgentState:
        """
        Analyze sentiment of the input
        """
        sentiment = self.embedding_model.get_sentiment(state.input)
        state.sentiment = sentiment
        return state
    
    def _route_to_tool(self, state: AgentState) -> AgentState:
        """
        Route to appropriate tool based on input and sentiment
        """
        # Implement tool routing logic
        return state
    
    def _generate_response(self, state: AgentState) -> AgentState:
        """
        Generate final response
        """
        # Generate response using LLM
        response = self.llm_model.generate(state.dict())
        state.response = response
        return state
    
    def process(self, user_input: str, input_type: str = "text") -> Dict[str, Any]:
        """
        Process user input and return response
        """
        initial_state = AgentState(
            input=user_input,
            input_type=input_type,
            memory=self.memory.get_context()
        )
        
        # Use invoke instead of run
        final_state = self.graph.invoke(initial_state)
        self.memory.add(user_input, final_state["response"])
        
        # Return the dictionary directly since final_state is already a dict
        return dict(final_state) 