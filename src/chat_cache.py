class ChatCache:

    def __init__(self, keep_k: int = 3):
        self.keep_k = keep_k
        self.items = []

    def insert(self, item: tuple[str, str]):

        if len(self.items) < self.keep_k:
            self.items.append(item)
        else:
            for i in range(1, self.keep_k):
                self.items[i-1] = self.items[i]
            self.items[-1] = item

    def get_cache(self):
        if len(self.items) > 0:
            chat_text_cache = f"These are our {len(self.items)} previous chat:"
            for item in self.items:
                chat_text_cache += "user: {} \nyou: {}\n".format(item[0], item[1])
            return chat_text_cache
        else:
            return ""

