from pydantic import BaseModel
from typing import Optional, Literal

class WordSearchRequest(BaseModel):
    input_word: str
    match_length: int
    word_length: Optional[int] = None
    operator: Optional[Literal["=", ">", "<", ">=", "<="]] = "="
    match_position: Optional[Literal["start", "end"]] = "end"  # New parameter

class WordSearchResponse(BaseModel):
    message: str
    input_word: str
    match_length: int
    word_length: Optional[int]
    operator: Optional[str]
    match_position: str  # New field
    total_matches: int
    output_file: str

class SynonymRequest(BaseModel):
    word: str
    max_results: Optional[int] = 50

class SynonymResponse(BaseModel):
    message: str
    input_word: str
    total_matches: int
    output_file: str