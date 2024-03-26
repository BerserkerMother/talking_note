class NoteSearchRequest:
    def __init__(self, userID: int, text: str):
        self.user_id = (userID,)
        self.text = text
