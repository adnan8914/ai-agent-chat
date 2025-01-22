from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json

class PersonalAssistant:
    def __init__(self):
        self.task_categories = [
            "scheduling", "reminder", "task_management",
            "note_taking", "recommendation"
        ]
        self.tasks = []
        self.reminders = []
        
    def process_request(
        self,
        request: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process personal assistant request
        """
        try:
            # Analyze request type
            request_type = self._analyze_request_type(request)
            
            # Handle request based on type
            if request_type == "scheduling":
                response = self._handle_scheduling(request, context)
            elif request_type == "reminder":
                response = self._handle_reminder(request, context)
            elif request_type == "task_management":
                response = self._handle_task(request, context)
            elif request_type == "note_taking":
                response = self._handle_note(request, context)
            else:
                response = self._handle_general_request(request, context)
                
            return {
                "response": response,
                "request_type": request_type,
                "metadata": self._get_metadata(request_type)
            }
            
        except Exception as e:
            raise Exception(f"Error processing assistant request: {str(e)}")
    
    def _analyze_request_type(self, request: str) -> str:
        """
        Determine type of assistant request
        """
        keywords = {
            "scheduling": ["schedule", "appointment", "meeting", "book"],
            "reminder": ["remind", "remember", "alert", "notification"],
            "task_management": ["task", "todo", "deadline", "project"],
            "note_taking": ["note", "write down", "record", "save"]
        }
        
        for category, category_keywords in keywords.items():
            if any(keyword in request.lower() for keyword in category_keywords):
                return category
        return "general"
    
    def _handle_scheduling(
        self,
        request: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle scheduling-related requests
        """
        # Extract date/time information
        datetime_info = self._extract_datetime(request)
        
        # Create schedule entry
        schedule_entry = {
            "type": "schedule",
            "datetime": datetime_info,
            "description": request,
            "status": "pending"
        }
        
        return {
            "message": f"Scheduled for {datetime_info}",
            "schedule_entry": schedule_entry
        }
    
    def _handle_reminder(
        self,
        request: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle reminder-related requests
        """
        reminder = {
            "text": request,
            "created_at": datetime.now(),
            "reminder_time": self._extract_datetime(request)
        }
        self.reminders.append(reminder)
        
        return {
            "message": "Reminder set successfully",
            "reminder": reminder
        }
    
    def _handle_task(
        self,
        request: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle task-related requests
        """
        task = {
            "description": request,
            "created_at": datetime.now(),
            "status": "pending",
            "priority": self._determine_task_priority(request)
        }
        self.tasks.append(task)
        
        return {
            "message": "Task created successfully",
            "task": task
        }
    
    def _handle_note(
        self,
        request: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle note-taking requests
        """
        note = {
            "content": request,
            "created_at": datetime.now(),
            "category": "general"
        }
        
        return {
            "message": "Note saved successfully",
            "note": note
        }
    
    def _handle_general_request(
        self,
        request: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle general assistance requests
        """
        return {
            "message": "I'll help you with that request",
            "action": "general_assistance"
        }
    
    def _extract_datetime(self, text: str) -> Optional[datetime]:
        """
        Extract datetime information from text
        In production, use a proper datetime parsing library
        """
        # Simple datetime extraction
        # In production, use more sophisticated parsing
        return datetime.now() + timedelta(hours=1)
    
    def _determine_task_priority(self, text: str) -> str:
        """
        Determine task priority based on text
        """
        urgent_keywords = ["urgent", "asap", "important", "critical"]
        if any(keyword in text.lower() for keyword in urgent_keywords):
            return "high"
        return "normal"
    
    def _get_metadata(self, request_type: str) -> Dict[str, Any]:
        """
        Generate metadata for assistant request
        """
        return {
            "timestamp": datetime.now().timestamp(),
            "type": "personal_assistant",
            "request_type": request_type,
            "version": "1.0"
        } 