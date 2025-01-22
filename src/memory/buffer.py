class WindowBuffer:
    def __init__(self, max_size: int = 10):
        self.buffer = []
        self.max_size = max_size
        
    def add(self, user_input: str, response: str):
        self.buffer.append({"input": user_input, "response": response})
        if len(self.buffer) > self.max_size:
            self.buffer.pop(0)
            
    def get_context(self):
        return self.buffer 