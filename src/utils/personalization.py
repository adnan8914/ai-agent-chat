from typing import Dict, Any, List
import numpy as np
from sklearn.cluster import KMeans
from datetime import datetime
from collections import Counter

class PersonalizationEngine:
    def __init__(self):
        self.user_interactions = {}
        self.user_preferences = {}
        self.interaction_clusters = None
        
    def track_interaction(
        self,
        user_id: str,
        interaction_type: str,
        content: Dict[str, Any]
    ):
        """Track user interaction"""
        if user_id not in self.user_interactions:
            self.user_interactions[user_id] = []
            
        interaction = {
            'type': interaction_type,
            'content': content,
            'timestamp': datetime.now()
        }
        self.user_interactions[user_id].append(interaction)
        self._update_user_preferences(user_id)
    
    def get_personalized_response(
        self,
        user_id: str,
        response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Personalize response based on user preferences"""
        preferences = self.user_preferences.get(user_id, {})
        
        # Adjust response based on preferences
        if preferences.get('communication_style'):
            response['tone'] = preferences['communication_style']
        
        if preferences.get('detail_level'):
            response['detail_level'] = preferences['detail_level']
            
        return response
    
    def _update_user_preferences(self, user_id: str):
        """Update user preferences based on interactions"""
        interactions = self.user_interactions[user_id]
        
        # Analyze recent interactions
        recent_interactions = sorted(
            interactions,
            key=lambda x: x['timestamp'],
            reverse=True
        )[:50]
        
        preferences = {
            'communication_style': self._analyze_communication_style(recent_interactions),
            'detail_level': self._analyze_detail_preference(recent_interactions),
            'favorite_tools': self._get_favorite_tools(recent_interactions),
            'last_updated': datetime.now()
        }
        
        self.user_preferences[user_id] = preferences
    
    def _analyze_communication_style(self, interactions: List[Dict[str, Any]]) -> str:
        """Analyze preferred communication style"""
        # Implement communication style analysis
        styles = [i['content'].get('style') for i in interactions if 'style' in i['content']]
        if styles:
            return max(set(styles), key=styles.count)
        return 'neutral'
    
    def _analyze_detail_preference(self, interactions: List[Dict[str, Any]]) -> str:
        """Analyze preferred level of detail"""
        # Implement detail preference analysis
        return 'medium'  # Default value
    
    def _get_favorite_tools(self, interactions: List[Dict[str, Any]]) -> List[str]:
        """Get user's favorite tools"""
        tools = [i['content'].get('tool') for i in interactions if 'tool' in i['content']]
        if tools:
            return [tool for tool, count in 
                   Counter(tools).most_common(3)]
        return [] 

    def update_preferences(self, user_id: str, preferences: Dict[str, Any]) -> None:
        """Update user preferences"""
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {}
        
        # Update preferences
        self.user_preferences[user_id].update({
            **preferences,
            'last_updated': datetime.now()
        })
        
        # Track preference update as an interaction
        self.track_interaction(
            user_id=user_id,
            interaction_type="preference_update",
            content=preferences
        ) 