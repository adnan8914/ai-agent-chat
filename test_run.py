import streamlit as st
from src.agent.base_agent import AIAgent
from src.utils.logger import CustomLogger

# Initialize logger
logger = CustomLogger("test_run")

def test_components():
    """Test if all components are working"""
    try:
        # Initialize agent
        logger.info("Initializing AI Agent...")
        agent = AIAgent()
        
        # Test with a simple query
        test_input = "Can you help me find information about artificial intelligence?"
        logger.info(f"Testing with input: {test_input}")
        
        # Process the query
        response = agent.process(test_input)
        
        logger.info("Test completed successfully!")
        return response
        
    except Exception as e:
        logger.error(f"Error during test: {str(e)}")
        raise

if __name__ == "__main__":
    test_components() 