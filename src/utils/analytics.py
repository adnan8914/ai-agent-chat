from typing import Dict, List, Any
from datetime import datetime
import pandas as pd
from collections import defaultdict
import time

class ConversationAnalytics:
    def __init__(self):
        self.conversations = pd.DataFrame({
            'timestamp': [],
            'user_input': [],
            'response': [],
            'processing_time': [],
            'sentiment': [],
            'tool_used': []
        })
        
    def add_conversation(self, 
                        user_input: str, 
                        response: str, 
                        processing_time: float,
                        sentiment: str = "neutral",
                        tool_used: str = "chat"):
        """Add a conversation to the analytics"""
        new_row = pd.DataFrame({
            'timestamp': [time.time()],
            'user_input': [user_input],
            'response': [response],
            'processing_time': [processing_time],
            'sentiment': [sentiment],
            'tool_used': [tool_used]
        })
        self.conversations = pd.concat([self.conversations, new_row], ignore_index=True)
        
    def get_analytics_report(self) -> Dict[str, Any]:
        """Generate analytics report"""
        if len(self.conversations) == 0:
            return {
                'metrics': {
                    'total_conversations': 0,
                    'avg_processing_time': 0.0
                },
                'tool_usage': {'chat': 1},
                'sentiment_distribution': {'neutral': 1}
            }
            
        return {
            'metrics': {
                'total_conversations': len(self.conversations),
                'avg_processing_time': self.conversations['processing_time'].mean()
            },
            'tool_usage': self.conversations['tool_used'].value_counts().to_dict(),
            'sentiment_distribution': self.conversations['sentiment'].value_counts().to_dict()
        } 