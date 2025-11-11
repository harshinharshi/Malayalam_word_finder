"""
1. Create folder structure:
   word_finder/
   ├── main.py
   ├── services/
   │   ├── __init__.py (empty file)
   │   └── word_service.py
   ├── models/
   │   ├── __init__.py (empty file)
   │   └── schemas.py
   └── requirements.txt

2. Install dependencies:
   pip install fastapi uvicorn

3. Run the server:
   python main.py

4. API will be available at:
   http://localhost:8000
   
5. Access interactive docs at:
   http://localhost:8000/docs

6. Example API requests:

   A. Ending match search:
   POST http://localhost:8000/search
   {
       "input_word": "അടിച്ച്",
       "match_length": 3,
       "word_length": 10,
       "operator": ">"
   }

   B. Synonym search:
   POST http://localhost:8000/synonyms
   {
       "word": "സന്തോഷം",
       "max_results": 50
   }

7. Response examples:

   A. Search response:
   {
       "message": "Search completed successfully. Download the file to view results.",
       "input_word": "അടിച്ച്",
       "match_length": 3,
       "word_length": 10,
       "operator": ">",
       "total_matches": 1523,
       "output_file": "output.txt"
   }

   B. Synonym response:
   {
       "message": "Synonym search completed. Download the file to view results.",
       "input_word": "സന്തോഷം",
       "total_matches": 25,
       "output_file": "synonyms_output.txt"
   }

8. Download results:
   GET http://localhost:8000/download (for ending matches)
   GET http://localhost:8000/download-synonyms (for synonyms)

NOTE: The synonym feature uses two methods:
1. Pattern matching - finds words with similar root structure (fast)
2. Translation comparison - uses Google Translate API via deep-translator (slower but more accurate)

The algorithm combines both methods for better results.
"""