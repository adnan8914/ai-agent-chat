from typing import Dict, Any, List
from datetime import datetime
import json

class CustomerSupport:
    def __init__(self):
        self.knowledge_base = self._load_knowledge_base()
        self.issue_categories = [
            "technical", "billing", "account", 
            "product", "general", "service"
        ]
        
    def handle_inquiry(
        self,
        query: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle customer support inquiry
        """
        try:
            # Analyze query and categorize issue
            issue_category = self._categorize_issue(query)
            priority = self._determine_priority(query, context)
            
            # Generate response
            response = self._generate_response(query, issue_category, context)
            
            return {
                "response": response,
                "issue_category": issue_category,
                "priority": priority,
                "metadata": self._get_metadata(issue_category, priority)
            }
            
        except Exception as e:
            raise Exception(f"Error handling customer inquiry: {str(e)}")
    
    def _load_knowledge_base(self) -> Dict[str, Any]:
        """
        Load customer support knowledge base
        """
        # In production, this would load from a database or file
        return {
            "technical": {
                "common_issues": [
                    "login_problems",
                    "performance_issues",
                    "connectivity_problems"
                ],
                "solutions": {
                    "login_problems": "Please try clearing your cache and cookies...",
                    "performance_issues": "Check your internet connection and try...",
                    "connectivity_problems": "Ensure you're connected to a stable..."
                }
            },
            "billing": {
                "common_issues": [
                    "payment_failed",
                    "refund_request",
                    "subscription_issues"
                ],
                "solutions": {
                    "payment_failed": "Please verify your payment details...",
                    "refund_request": "Our refund policy allows...",
                    "subscription_issues": "To manage your subscription..."
                }
            }
        }
    
    def _categorize_issue(self, query: str) -> str:
        """
        Categorize customer issue based on query
        """
        # Simple keyword-based categorization
        # In production, use more sophisticated NLP
        keywords = {
            "technical": ["error", "bug", "not working", "failed"],
            "billing": ["payment", "charge", "refund", "subscription"],
            "account": ["login", "password", "access", "account"],
            "product": ["product", "feature", "how to", "usage"],
            "service": ["service", "support", "help", "assistance"]
        }
        
        for category, category_keywords in keywords.items():
            if any(keyword in query.lower() for keyword in category_keywords):
                return category
        return "general"
    
    def _determine_priority(self, query: str, context: Dict[str, Any]) -> str:
        """
        Determine inquiry priority
        """
        # Priority factors
        urgent_keywords = ["urgent", "emergency", "critical", "immediately"]
        customer_tier = context.get("customer_tier", "standard")
        issue_category = self._categorize_issue(query)
        
        if any(keyword in query.lower() for keyword in urgent_keywords):
            return "high"
        elif customer_tier == "premium" or issue_category in ["billing", "technical"]:
            return "medium"
        return "low"
    
    def _generate_response(
        self,
        query: str,
        category: str,
        context: Dict[str, Any]
    ) -> str:
        """
        Generate appropriate response based on query and context
        """
        # Get relevant solution from knowledge base
        solutions = self.knowledge_base.get(category, {}).get("solutions", {})
        
        # Find most relevant solution
        # In production, use better matching algorithm
        for issue, solution in solutions.items():
            if issue in query.lower():
                return solution
        
        # Default response if no specific solution found
        return (
            f"Thank you for contacting support regarding your {category} issue. "
            "A support representative will review your case and respond shortly."
        )
    
    def _get_metadata(self, category: str, priority: str) -> Dict[str, Any]:
        """
        Generate metadata for support inquiry
        """
        return {
            "timestamp": datetime.now().timestamp(),
            "category": category,
            "priority": priority,
            "status": "open",
            "type": "customer_support"
        } 