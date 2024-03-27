import dataclasses
from typing import Any, Dict, Optional

@dataclasses.dataclass
class Request:
    """A single request."""
    model_name: str
    adapter_idx: int
    data: Any
    idx: int
    metadata: Optional[Dict[str, Any]] = None