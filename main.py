from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from models.schemas import WordSearchRequest, WordSearchResponse, SynonymRequest, SynonymResponse
from services.word_service import WordService
import os

app = FastAPI(title="Malayalam Word Finder API")

# Configuration
WORDS_FILE_PATH = r"C:\Project\Malayalam_word_finder\unique_words.txt"
word_service = WordService(WORDS_FILE_PATH)

@app.get("/")
def read_root():
    return {
        "message": "Malayalam Word Finder API",
        "endpoints": {
            "POST /search": "Search for words with matching endings",
            "POST /synonyms": "Find words with similar meanings",
            "GET /download": "Download last search results",
            "GET /download-synonyms": "Download last synonym results"
        }
    }

@app.post("/search", response_model=WordSearchResponse)
def search_words(request: WordSearchRequest):
    """Search for words with matching endings"""
    try:
        matching_words = word_service.find_matching_words(
            input_word=request.input_word,
            match_length=request.match_length,
            word_length=request.word_length,
            operator=request.operator
        )
        
        # Save results to file
        output_file = "output.txt"
        save_results_to_file(request, matching_words, output_file)
        
        return WordSearchResponse(
            message="Search completed successfully. Download the file to view results.",
            input_word=request.input_word,
            match_length=request.match_length,
            word_length=request.word_length,
            operator=request.operator,
            total_matches=len(matching_words),
            output_file=output_file
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/synonyms", response_model=SynonymResponse)
def find_synonyms(request: SynonymRequest):
    """Find words with similar meanings"""
    try:
        synonyms = word_service.find_synonyms(
            word=request.word,
            max_results=request.max_results
        )
        
        # Save results to file
        output_file = "synonyms_output.txt"
        save_synonyms_to_file(request, synonyms, output_file)
        
        return SynonymResponse(
            message="Synonym search completed. Download the file to view results.",
            input_word=request.word,
            total_matches=len(synonyms),
            output_file=output_file
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download")
def download_results():
    """Download the ending match search results"""
    output_file = "output.txt"
    if os.path.exists(output_file):
        return FileResponse(
            output_file, 
            media_type="text/plain",
            filename="malayalam_words_results.txt"
        )
    else:
        raise HTTPException(status_code=404, detail="No results file found. Run a search first.")

@app.get("/download-synonyms")
def download_synonyms():
    """Download the synonym search results"""
    output_file = "synonyms_output.txt"
    if os.path.exists(output_file):
        return FileResponse(
            output_file, 
            media_type="text/plain",
            filename="malayalam_synonyms_results.txt"
        )
    else:
        raise HTTPException(status_code=404, detail="No synonym results found. Run a synonym search first.")

def save_results_to_file(request: WordSearchRequest, results: list[str], filename: str):
    """Save search results to output.txt"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Input word: {request.input_word}\n")
        f.write(f"Matching last {request.match_length} letters\n")
        if request.word_length:
            f.write(f"Word length: {request.operator} {request.word_length} characters\n")
        f.write(f"Total matches: {len(results)}\n\n")
        for word in results:
            f.write(word + '\n')

def save_synonyms_to_file(request: SynonymRequest, results: list[str], filename: str):
    """Save synonym results to file"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Input word: {request.word}\n")
        f.write(f"Maximum results: {request.max_results}\n")
        f.write(f"Total synonyms found: {len(results)}\n\n")
        for word in results:
            f.write(word + '\n')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)