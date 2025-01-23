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
                    'total_users': 0,
                    'active_sessions': 0,
                    'avg_response_time': 0.0,
                    'total_conversations': 0,
                    'avg_processing_time': 0.0
                },
                'tool_usage': {'chat': 1},
                'sentiment_distribution': {'neutral': 1},
                'activity_data': {
                    'timestamp': [],
                    'count': []
                }
            }
            
        # Convert sentiment values to strings for proper counting
        sentiment_counts = self.conversations['sentiment'].astype(str).value_counts()
        tool_counts = self.conversations['tool_used'].astype(str).value_counts()
        
        return {
            'metrics': {
                'total_users': len(set(self.conversations['user_input'])),
                'active_sessions': len(self.conversations),
                'avg_response_time': float(self.conversations['processing_time'].mean()),
                'total_conversations': len(self.conversations),
                'avg_processing_time': float(self.conversations['processing_time'].mean())
            },
            'tool_usage': dict(tool_counts),
            'sentiment_distribution': dict(sentiment_counts),
            'activity_data': {
                'timestamp': self.conversations['timestamp'].tolist(),
                'count': list(range(len(self.conversations)))
            }
        }

    def track_conversation(self, user_input: str, response: Dict[str, Any]):
        """Track a conversation interaction"""
        self.add_conversation(
            user_input=user_input,
            response=response['response'],
            processing_time=response.get('processing_time', 0.0),
            sentiment=response.get('sentiment', 'neutral'),
            tool_used=response.get('tool_used', 'chat')
        ) 