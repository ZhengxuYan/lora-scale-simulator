from typing import Optional, List
from transformers import PreTrainedTokenizerBase, AutoTokenizer
from request import Request 

class TokenizerManager:
    def __init__(self):
        self.tokenizers = {}
    
    def add_tokenizer(self, adapter_idx: int, tokenizer: PreTrainedTokenizerBase):
        self.tokenizers[adapter_idx] = tokenizer
    
    def get_tokenizer(self, adapter_idx: int, default: Optional[PreTrainedTokenizerBase] = None) -> Optional[PreTrainedTokenizerBase]:
        return self.tokenizers.get(adapter_idx, default)
    
    def tokenize(self, adapter_idx: int, request: Request) -> List[int]:
        tokenizer = self.get_tokenizer(request.adapter_idx)
        if tokenizer is None:
            raise ValueError(f"Tokenizer for adapter {adapter_idx} not found")
        if isinstance(request.data, str):
            return tokenizer.encode(request.data, add_special_tokens=True)
        return None

if __name__ == "__main__":
    tokenizer_manager = TokenizerManager()
    
    bert_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    tokenizer_manager.add_tokenizer(0, bert_tokenizer)
    
    request = Request("bert-base-uncased", 0, "Hello, world!", 0)
    
    tokens = tokenizer_manager.tokenize(0, request)
    print(tokens)
