from typing import Any, Callable, Dict, TypeVar
from functools import wraps
from .logger import CustomLogger
import streamlit as st

T = TypeVar('T')
logger = CustomLogger("error_handler")

class AIAgentError(Exception):
    """Base exception class for AI Agent errors"""
    pass

class ModelError(AIAgentError):
    """Errors related to model operations"""
    pass

class ToolError(AIAgentError):
    """Errors related to tool operations"""
    pass

class WorkflowError(AIAgentError):
    """Errors related to workflow operations"""
    pass

def handle_model_errors(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator to handle model-related errors"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> T:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Model error in {func.__name__}: {str(e)}")
            raise ModelError(f"Error in model operation: {str(e)}")
    return wrapper

def handle_tool_errors(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator to handle tool-related errors"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> T:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Tool error in {func.__name__}: {str(e)}")
            raise ToolError(f"Error in tool operation: {str(e)}")
    return wrapper

def handle_workflow_errors(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator to handle workflow-related errors"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> T:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Workflow error in {func.__name__}: {str(e)}")
            raise WorkflowError(f"Error in workflow operation: {str(e)}")
    return wrapper

def handle_agent_error(error: Exception) -> None:
    """Handle errors from the AI agent gracefully"""
    st.error(f"An error occurred: {str(error)}")
    st.warning("Please try again or contact support if the problem persists.") 