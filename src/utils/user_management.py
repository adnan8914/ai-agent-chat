from typing import Dict, Any, Optional
import jwt
from datetime import datetime, timedelta
from passlib.hash import bcrypt
import uuid

class UserManager:
    def __init__(self):
        self.users_db = {}  # In production, use a proper database
        self.SECRET_KEY = "your-secret-key"  # Use environment variable in production
        
    def register_user(self, username: str, password: str, email: str) -> Dict[str, Any]:
        """Register a new user"""
        if username in self.users_db:
            raise ValueError("Username already exists")
            
        user_id = str(uuid.uuid4())
        user = {
            'id': user_id,
            'username': username,
            'password_hash': bcrypt.hash(password),
            'email': email,
            'preferences': {},
            'created_at': datetime.now(),
            'last_login': None
        }
        self.users_db[username] = user
        return self._create_user_response(user)
    
    def authenticate(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user and return token"""
        user = self.users_db.get(username)
        if user and bcrypt.verify(password, user['password_hash']):
            user['last_login'] = datetime.now()
            return {
                'token': self._create_token(user['id']),
                'user': self._create_user_response(user)
            }
        return None
    
    def _create_token(self, user_id: str) -> str:
        """Create JWT token"""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        return jwt.encode(payload, self.SECRET_KEY, algorithm='HS256')
    
    def _create_user_response(self, user: Dict[str, Any]) -> Dict[str, Any]:
        """Create safe user response (without sensitive data)"""
        return {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'created_at': user['created_at'],
            'last_login': user['last_login']
        } 