import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

import streamlit as st
from src.agent.base_agent import AIAgent
from src.utils.error_handlers import handle_agent_error
from src.utils.analytics import ConversationAnalytics
from src.utils.cache import CacheManager
import plotly.express as px
import time

class StreamlitApp:
    def __init__(self):
        self.initialize_session_state()
        self.agent = AIAgent()
        self.analytics = ConversationAnalytics()
        self.cache = CacheManager()
        
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
            
    def run(self):
        """Run the Streamlit application"""
        # Render sidebar first
        self.render_sidebar()
        
        # Main content
        st.title("AI Agent Chat Interface")
        
        # Initialize agent
        self.initialize_agent()
        
        # Initialize chat history
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        # Add tabs to the interface
        tab1, tab2, tab3 = st.tabs(["Chat", "Analytics", "Settings"])
        
        with tab1:
            self.render_chat_interface()
            
        with tab2:
            self.render_analytics()
            
        with tab3:
            self.render_settings()
    
    def initialize_agent(self):
        """Initialize the AI agent if not already in session state"""
        if 'agent' not in st.session_state:
            with st.spinner('Initializing AI Agent...'):
                st.session_state.agent = self.agent
        
    def process_input(self, user_input: str) -> dict:
        """Process user input through the agent"""
        try:
            response = self.agent.process(user_input)
            return response
        except Exception as e:
            st.error(f"Error processing input: {str(e)}")
            return {"response": "I encountered an error processing your request."}
    
    def render_analytics(self):
        """Render analytics dashboard"""
        st.header("Conversation Analytics")
        
        # Get analytics data
        report = self.analytics.get_analytics_report()
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Conversations", report['metrics']['total_conversations'])
        with col2:
            st.metric("Avg Processing Time", f"{report['metrics']['avg_processing_time']:.2f}s")
        with col3:
            st.metric("Most Used Tool", max(report['tool_usage'], key=report['tool_usage'].get))
        
        # Tool usage chart
        fig_tools = px.pie(
            values=list(report['tool_usage'].values()),
            names=list(report['tool_usage'].keys()),
            title="Tool Usage Distribution"
        )
        st.plotly_chart(fig_tools)
        
        # Sentiment distribution
        fig_sentiment = px.bar(
            x=list(report['sentiment_distribution'].keys()),
            y=list(report['sentiment_distribution'].values()),
            title="Sentiment Distribution"
        )
        st.plotly_chart(fig_sentiment)
    
    def render_settings(self):
        """Render settings interface"""
        st.header("Settings")
        
        # Model settings
        st.subheader("Model Configuration")
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
        max_length = st.slider("Max Response Length", 50, 500, 200)
        
        # Tool settings
        st.subheader("Tool Settings")
        enabled_tools = st.multiselect(
            "Enabled Tools",
            ["Web Search", "Email Writing", "Customer Support", 
             "Personal Assistant", "Content Creation"],
            default=["Web Search", "Email Writing", "Customer Support"]
        )
        
        # Cache settings
        st.subheader("Cache Settings")
        cache_enabled = st.toggle("Enable Response Caching", value=True)
        if cache_enabled:
            cache_duration = st.number_input(
                "Cache Duration (minutes)",
                min_value=1,
                max_value=1440,
                value=60
            )

    def render_chat_interface(self):
        """Render the chat interface"""
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Chat input
        if prompt := st.chat_input("What would you like to know?"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.write(prompt)
            
            # Get AI response
            try:
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = self.process_input(prompt)
                        st.write(response["response"])
                        
                # Add assistant response to chat history
                st.session_state.messages.append(
                    {"role": "assistant", "content": response["response"]}
                )
                
            except Exception as e:
                handle_agent_error(e)

    def render_sidebar(self):
        """Render the sidebar"""
        with st.sidebar:
            st.title("AI Agent Dashboard")
            
            # Initialize messages if not in session state
            if 'messages' not in st.session_state:
                st.session_state.messages = []
            
            # User info section
            st.subheader("Session Info")
            total_messages = len(st.session_state.messages)
            st.info(f"Messages in conversation: {total_messages}")
            
            # Quick actions
            st.subheader("Quick Actions")
            if st.button("Clear Chat History"):
                st.session_state.messages = []
                st.rerun()
                
            if st.button("Export Conversation"):
                st.download_button(
                    "Download Chat",
                    data=str(st.session_state.messages),
                    file_name="conversation.txt",
                    mime="text/plain"
                )
            
            # Model info
            st.subheader("Model Information")
            st.markdown("""
            - **Model**: NVIDIA AI LLM
            - **Context Window**: 4096 tokens
            - **Temperature**: 0.7
            """)
            
            # Help section
            with st.expander("Help & Tips"):
                st.markdown("""
                - Use clear, specific questions
                - You can ask follow-up questions
                - The agent remembers conversation context
                - Use the settings tab to customize behavior
                """)

if __name__ == "__main__":
    app = StreamlitApp()
    app.run() 