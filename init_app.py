import streamlit as st
from src.agent.base_agent import AIAgent
from src.utils.user_management import UserManager
from src.utils.personalization import PersonalizationEngine
from src.utils.ab_testing import ABTestingSystem
from src.utils.cache import CacheManager
from src.utils.analytics import ConversationAnalytics
from src.utils.feedback import FeedbackSystem
import plotly.express as px
import time
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
import json
import speech_recognition as sr
from speech_recognition import Recognizer, Microphone
import pyttsx3
from streamlit_ace import st_ace
from datetime import datetime
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import io

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'agent' not in st.session_state:
        st.session_state.agent = AIAgent()
    if 'user_manager' not in st.session_state:
        st.session_state.user_manager = UserManager()
    if 'personalization' not in st.session_state:
        st.session_state.personalization = PersonalizationEngine()
    if 'ab_testing' not in st.session_state:
        st.session_state.ab_testing = ABTestingSystem()
    if 'cache' not in st.session_state:
        st.session_state.cache = CacheManager()
    if 'analytics' not in st.session_state:
        st.session_state.analytics = ConversationAnalytics()
    if 'feedback' not in st.session_state:
        st.session_state.feedback = FeedbackSystem()
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'session_count' not in st.session_state:
        st.session_state.session_count = 0

def main():
    initialize_session_state()
    
    # If user is not logged in, show login/register page
    if not st.session_state.user:
        show_auth_page()
    else:
        show_main_app()

def show_auth_page():
    """Show authentication page"""
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.header("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            result = st.session_state.user_manager.authenticate(username, password)
            if result:
                st.session_state.user = result['user']
                st.session_state.session_count += 1  # Increment session count
                st.rerun()
            else:
                st.error("Invalid credentials")
    
    with tab2:
        st.header("Register")
        new_username = st.text_input("Username", key="reg_username")
        new_password = st.text_input("Password", type="password", key="reg_password")
        email = st.text_input("Email", key="reg_email")
        
        if st.button("Register"):
            try:
                result = st.session_state.user_manager.register_user(
                    new_username, new_password, email
                )
                st.session_state.user = result
                st.success("Registration successful! Please login.")
            except ValueError as e:
                st.error(str(e))

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def show_main_app():
    """Show main application interface"""
    # Configure page
    st.set_page_config(
        page_title="AI Assistant",
        page_icon="🤖",
        layout="wide"
    )

    # Enhanced Custom CSS
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
        
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
            font-family: 'Poppins', sans-serif;
        }
        
        .chat-message {
            padding: 1.5rem;
            border-radius: 1rem;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s ease;
        }
        
        .chat-message:hover {
            transform: translateY(-2px);
        }
        
        .user-message {
            background: linear-gradient(135deg, #6B9FFF 0%, #4C8DFF 100%);
            color: white;
        }
        
        .assistant-message {
            background: linear-gradient(135deg, #F5F7FF 0%, #E8ECFD 100%);
        }
        
        .sidebar-content {
            padding: 2rem;
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(10px);
        }
        
        .metrics-card {
            background: white;
            padding: 1.5rem;
            border-radius: 1rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        
        .metrics-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }
        
        .suggestion-chip {
            background: linear-gradient(135deg, #FF6B6B 0%, #FF4B4B 100%);
            color: white;
            border: none;
            border-radius: 20px;
            padding: 10px 20px;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .suggestion-chip:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        .app-title {
            text-align: center;
            background: linear-gradient(135deg, #FF6B6B 0%, #FF4B4B 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            padding: 1rem;
            font-size: 2rem;
            font-weight: bold;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .stButton>button {
            border-radius: 20px;
            padding: 10px 24px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        .chat-container {
            padding: 2rem;
            border-radius: 1rem;
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #FF4B4B;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #FF6B6B;
        }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar with enhanced styling
    with st.sidebar:
        # Replace image with styled title
        st.markdown('<div class="app-title">🤖 AI Assistant</div>', unsafe_allow_html=True)
        st.title(f"Welcome, {st.session_state.user['username']}")
        st.divider()
        
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        # Navigation
        selected = option_menu(
            "Main Menu",
            ["Chat", "Analytics", "Settings"],
            icons=['chat', 'graph-up', 'gear'],
            menu_icon="cast",
            default_index=0,
        )
        
        # User stats
        st.subheader("Your Stats")
        col1, col2 = st.columns(2)
        with col1:
            message_count = len(st.session_state.messages) if 'messages' in st.session_state else 0
            st.metric("Messages", message_count)
        with col2:
            session_count = st.session_state.session_count if 'session_count' in st.session_state else 1
            st.metric("Sessions", session_count)
            
        st.divider()
        if st.button("Logout", type="secondary"):
            st.session_state.user = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content area
    if selected == "Chat":
        show_chat_interface()
    elif selected == "Analytics":
        show_analytics()
    else:
        show_settings()

def show_chat_interface():
    """Enhanced chat interface with additional features"""
    # Load Lottie animations
    chat_animation = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_u25cckyh.json")
    
    # Header with animation
    col1, col2 = st.columns([3, 1])
    with col1:
        st.header("💬 AI Assistant")
    with col2:
        if chat_animation:
            st_lottie(chat_animation, height=100, key="chat_animation")
    
    # Chat container with enhanced styling
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Message history
        for message in st.session_state.messages:
            with st.chat_message(
                message["role"],
                avatar="🧑" if message["role"] == "user" else "🤖"
            ):
                st.markdown(message["content"])
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area with enhanced styling
    with st.container():
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            user_input = st.chat_input("Type your message...", key="chat_input")
        with col2:
            if st.button("❓ Help", key="help_btn", use_container_width=True):
                show_help_modal()
        with col3:
            if st.button("🔄 Clear", key="clear_btn", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
    
    # Suggestion chips with enhanced styling
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🎯 Quick Start", key="start_btn"):
            process_chat_input("What can you help me with?")
    with col2:
        if st.button("😄 Tell a Joke", key="joke_btn"):
            process_chat_input("Tell me a joke")
    with col3:
        if st.button("💻 Coding Help", key="code_btn"):
            process_chat_input("What programming topics can you help with?")
    with col4:
        if st.button("🤖 About AI", key="ai_btn"):
            process_chat_input("Explain what AI is")

    # Add feature tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Voice", "Files", "Code", "Export"])
    
    with tab1:
        add_voice_controls()
    
    with tab2:
        add_file_processing()
    
    with tab3:
        add_code_editor()
    
    with tab4:
        add_export_options()

def add_voice_controls():
    try:
        import sounddevice as sd
        import numpy as np
        import scipy.io.wavfile as wav
        import speech_recognition as sr
        import pyttsx3
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎤 Voice Input"):
                try:
                    # Voice input code...
                    status_placeholder = st.empty()
                    status_placeholder.info("🎤 Recording will start in 3 seconds...")
                    time.sleep(1)
                    
                    duration = 5
                    fs = 44100
                    status_placeholder.info("🎤 Recording... Speak now!")
                    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
                    sd.wait()
                    
                    virtual_file = io.BytesIO()
                    recording = recording.flatten()
                    wav.write(virtual_file, fs, recording)
                    virtual_file.seek(0)
                    
                    recognizer = sr.Recognizer()
                    with sr.AudioFile(virtual_file) as source:
                        audio = recognizer.record(source)
                        text = recognizer.recognize_google(audio)
                        
                    if text:
                        status_placeholder.success(f"Recognized: {text}")
                        process_chat_input(text)
                    else:
                        status_placeholder.error("No speech detected. Please try again.")
                        
                except Exception as e:
                    st.error(f"Voice input error: {str(e)}")
                    
        with col2:
            if st.button("🔊 Read Response"):
                try:
                    if st.session_state.messages:
                        last_response = st.session_state.messages[-1]['content']
                        engine = pyttsx3.init()
                        engine.say(last_response)
                        engine.runAndWait()
                except Exception as e:
                    st.error("Could not process text-to-speech.")
                    
    except ImportError:
        st.warning("Voice features are not available. Please install required dependencies.")

def show_analytics():
    """Enhanced analytics dashboard"""
    st.title("📊 Analytics Dashboard")
    
    # Get analytics data
    analytics_data = st.session_state.analytics.get_analytics_report()
    
    # Summary metrics
    st.markdown("### Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        display_metric_card("Total Users", analytics_data['metrics']['total_users'], "👥")
    with col2:
        display_metric_card("Active Sessions", analytics_data['metrics']['active_sessions'], "📱")
    with col3:
        display_metric_card("Avg Response Time", f"{analytics_data['metrics']['avg_response_time']:.2f}s", "⚡")
    with col4:
        display_metric_card("Total Messages", len(st.session_state.messages), "💬")
    
    # Charts in tabs
    tab1, tab2, tab3 = st.tabs(["Activity", "Usage", "Performance"])
    
    with tab1:
        st.plotly_chart(create_activity_chart(analytics_data), use_container_width=True)
    with tab2:
        st.plotly_chart(create_usage_chart(analytics_data), use_container_width=True)
    with tab3:
        st.plotly_chart(create_performance_chart(analytics_data), use_container_width=True)

def display_metric_card(title, value, icon):
    st.markdown(f"""
        <div class="metrics-card">
            <h3>{icon} {title}</h3>
            <h2>{value}</h2>
        </div>
    """, unsafe_allow_html=True)

# Add helper functions for charts
def create_activity_chart(data):
    return px.line(
        data['activity_data'],
        x='timestamp',
        y='count',
        title="User Activity Over Time",
        template="plotly_white"
    )

def create_usage_chart(data):
    return px.pie(
        values=list(data['tool_usage'].values()),
        names=list(data['tool_usage'].keys()),
        title="Tool Usage Distribution",
        hole=0.4
    )

def create_performance_chart(data):
    """Create performance metrics chart"""
    performance_data = {
        'Metric': ['Response Time', 'Success Rate', 'User Rating'],
        'Value': [
            data['metrics']['avg_response_time'],
            0.95,  # Example success rate
            4.5    # Example user rating
        ]
    }
    
    fig = px.bar(
        performance_data,
        x='Metric',
        y='Value',
        title="Performance Metrics",
        template="plotly_white"
    )
    
    fig.update_layout(
        yaxis_title="Score",
        showlegend=False
    )
    
    return fig

def show_settings():
    """Show settings interface"""
    st.header("Settings")
    
    # User preferences
    st.subheader("User Preferences")
    communication_style = st.selectbox(
        "Communication Style",
        ["Professional", "Casual", "Technical"],
        index=0
    )
    
    detail_level = st.select_slider(
        "Response Detail Level",
        options=["Brief", "Balanced", "Detailed"],
        value="Balanced"
    )
    
    # Model settings
    st.subheader("Model Configuration")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    max_length = st.slider("Max Response Length", 50, 500, 200)
    
    # Save settings button
    if st.button("Save Settings"):
        # Update user preferences
        st.session_state.personalization.update_preferences(
            st.session_state.user['id'],
            {
                'communication_style': communication_style,
                'detail_level': detail_level,
                'temperature': temperature,
                'max_length': max_length
            }
        )
        st.success("Settings saved successfully!")

def process_chat_input(user_input: str):
    """Process chat input and display response"""
    start_time = time.time()
    
    try:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user", avatar="🧑"):
            st.markdown(user_input)
        
        # Get response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking..."):
                try:
                    # Get response with context
                    response = st.session_state.agent.process(
                        user_input,
                        context=st.session_state.messages[-5:]  # Last 5 messages for context
                    )
                    
                    # Clean and display response
                    response_text = response.get('response', '')
                    if response_text:
                        st.markdown(response_text)
                        
                        # Add to message history
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response_text
                        })
                        
                        # Track analytics
                        processing_time = time.time() - start_time
                        st.session_state.analytics.track_conversation(
                            user_input,
                            {
                                'response': response_text,
                                'processing_time': processing_time,
                                'sentiment': 'neutral',
                                'tool_used': 'chat'
                            }
                        )
                    else:
                        raise ValueError("Empty response")
                        
                except Exception as e:
                    print(f"Chat processing error: {str(e)}")
                    error_message = "I'm here to help! Could you rephrase your question?"
                    st.warning(error_message)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_message
                    })
                    
    except Exception as e:
        print(f"Chat interface error: {str(e)}")
        st.error("Something went wrong. Let's start fresh!")

def show_help_modal():
    """Show help information"""
    st.info("""
    ### How to use the AI Assistant
    
    1. **Ask Questions**: Type any question in the chat box
    2. **Clear Chat**: Use the Clear button to start fresh
    3. **Quick Suggestions**: Click on suggestion chips for common queries
    
    ### Example Questions:
    - "What can you help me with?"
    - "Tell me a joke"
    - "Help me with Python coding"
    - "Explain how AI works"
    
    ### Tips:
    - Be specific in your questions
    - You can ask follow-up questions
    - Use the settings page to customize responses
    """)

def add_file_processing():
    uploaded_file = st.file_uploader("Upload a file for analysis", 
                                   type=['txt', 'pdf', 'py', 'json'])
    if uploaded_file:
        try:
            # Handle different file types
            file_type = uploaded_file.name.split('.')[-1].lower()
            
            if file_type == 'pdf':
                import PyPDF2
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                content = ' '.join([page.extract_text() for page in pdf_reader.pages])
            else:
                # For txt, py, json files
                content = uploaded_file.getvalue().decode('utf-8', errors='ignore')
            
            prompt = f"Analyze this {file_type} file content:\n{content}"
            process_chat_input(prompt)
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

def add_code_editor():
    if st.button("📝 Open Code Editor"):
        code = st_ace(
            placeholder="Write your code here...",
            language="python",
            theme="monokai",
            keybinding="vscode",
            show_gutter=True
        )
        if code:
            prompt = f"Review this code and suggest improvements:\n```python\n{code}\n```"
            process_chat_input(prompt)

def add_export_options():
    if st.button("💾 Export Chat"):
        chat_history = {
            "timestamp": datetime.now().isoformat(),
            "messages": st.session_state.messages
        }
        st.download_button(
            "Download Chat History",
            data=json.dumps(chat_history, indent=2),
            file_name="chat_history.json",
            mime="application/json"
        )

if __name__ == "__main__":
    main() 