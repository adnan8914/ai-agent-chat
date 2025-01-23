from typing import Dict, Any, List
import random
from datetime import datetime
import uuid

class ABTestingSystem:
    def __init__(self):
        self.experiments = {}
        self.user_assignments = {}
        self.results = {}
        
    def create_experiment(
        self,
        name: str,
        variants: List[Dict[str, Any]],
        traffic_split: List[float] = None
    ) -> str:
        """Create new A/B test experiment"""
        experiment_id = str(uuid.uuid4())
        
        if traffic_split is None:
            traffic_split = [1.0 / len(variants)] * len(variants)
            
        experiment = {
            'id': experiment_id,
            'name': name,
            'variants': variants,
            'traffic_split': traffic_split,
            'start_time': datetime.now(),
            'status': 'active'
        }
        
        self.experiments[experiment_id] = experiment
        return experiment_id
    
    def get_variant(self, user_id: str, experiment_id: str) -> Dict[str, Any]:
        """Get variant for user"""
        if user_id not in self.user_assignments:
            self.user_assignments[user_id] = {}
            
        if experiment_id not in self.user_assignments[user_id]:
            variant = self._assign_variant(experiment_id)
            self.user_assignments[user_id][experiment_id] = variant
            
        return self.user_assignments[user_id][experiment_id]
    
    def track_result(
        self,
        user_id: str,
        experiment_id: str,
        metrics: Dict[str, float]
    ):
        """Track experiment results"""
        if experiment_id not in self.results:
            self.results[experiment_id] = []
            
        result = {
            'user_id': user_id,
            'variant': self.user_assignments[user_id][experiment_id],
            'metrics': metrics,
            'timestamp': datetime.now()
        }
        
        self.results[experiment_id].append(result)
    
    def get_experiment_results(self, experiment_id: str) -> Dict[str, Any]:
        """Get experiment results and analysis"""
        if experiment_id not in self.results:
            return {}
            
        results = self.results[experiment_id]
        analysis = self._analyze_results(results)
        
        return {
            'experiment': self.experiments[experiment_id],
            'total_participants': len(set(r['user_id'] for r in results)),
            'results_per_variant': analysis,
            'winning_variant': self._determine_winner(analysis)
        }
    
    def _assign_variant(self, experiment_id: str) -> Dict[str, Any]:
        """Assign user to experiment variant"""
        experiment = self.experiments[experiment_id]
        return random.choices(
            experiment['variants'],
            weights=experiment['traffic_split']
        )[0]
    
    def _analyze_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze experiment results"""
        analysis = {}
        for result in results:
            variant = result['variant']['name']
            if variant not in analysis:
                analysis[variant] = {
                    'metrics': {},
                    'count': 0
                }
            
            for metric, value in result['metrics'].items():
                if metric not in analysis[variant]['metrics']:
                    analysis[variant]['metrics'][metric] = []
                analysis[variant]['metrics'][metric].append(value)
            
            analysis[variant]['count'] += 1
            
        return analysis
    
    def _determine_winner(self, analysis: Dict[str, Any]) -> str:
        """Determine winning variant"""
        # Implement winning variant determination logic
        return max(analysis.keys(), key=lambda k: analysis[k]['count']) 