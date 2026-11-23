from typing import TypedDict, Optional, List

class AgentState(TypedDict):
    question: str
    csv_path: str
    csv_info: str
    code: str
    output: str
    error: Optional[str]
    charts: List[str]
    retries: int
    final_answer: str
