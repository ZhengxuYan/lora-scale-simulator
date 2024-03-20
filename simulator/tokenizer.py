import tiktoken
from typing import Optional

class TokenizerManager:
    def __init__(self):
        self.tokenizers = {}
    
    def add_tokenizer(self, adapter_idx: int, encoding_name: str) -> None:
        self.tokenizers[adapter_idx] = self.load_tokenizer(encoding_name)
    
    def get_tokenizer(self, adapter_idx: int) -> Optional[tiktoken.Encoding]:
        return self.tokenizers.get(adapter_idx, None)
    
    def load_tokenizer(self, encoding_name: str = None) -> tiktoken.Encoding:
        if encoding_name is None:
            encoding = tiktoken.get_encoding("cl100k_base")
        else:
            encoding = tiktoken.get_encoding(encoding_name)
        return encoding

    def count_tokens(self, string: str, encoding_name: str) -> int:
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens
    
