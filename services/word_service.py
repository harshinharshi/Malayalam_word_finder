from deep_translator import GoogleTranslator
import re

class WordService:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.translator = GoogleTranslator(source='ml', target='en')
        self._load_words()
    
    def _load_words(self):
        """Load all words into memory for faster searching"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.all_words = [line.strip() for line in file if line.strip()]
        except Exception as e:
            print(f"Error loading words: {e}")
            self.all_words = []
    
    def find_matching_words(
        self, 
        input_word: str, 
        match_length: int,
        word_length: int = None,
        operator: str = "=",
        match_position: str = "end"  # New parameter
    ) -> list[str]:
        """Find words matching the criteria from start or end
        
        Logic:
        - Extract substring based on match_position
        - If match_position="end": extract last N chars, find words ENDING with it
        - If match_position="start": extract first N chars, find words STARTING with it
        """
        
        # Validate match_length
        if match_length > len(input_word):
            match_length = len(input_word)
        
        # Extract pattern based on position
        if match_position == "start":
            # Extract first N characters
            pattern = input_word[:match_length]
        else:  # default to "end"
            # Extract last N characters
            pattern = input_word[-match_length:]
        
        matching_words = []
        
        for word in self.all_words:
            if word == input_word:
                continue
            
            # Match based on position
            if match_position == "start":
                # Find words that START with the extracted pattern
                matches = word.startswith(pattern)
            else:
                # Find words that END with the extracted pattern
                matches = word.endswith(pattern)
            
            if matches:
                if self._check_length_condition(len(word), word_length, operator):
                    matching_words.append(word)
        
        return matching_words
    
    def find_synonyms(self, word: str, max_results: int = 50) -> list[str]:
        """Find similar meaning words using translation and pattern matching"""
        try:
            synonyms = []
            
            # Method 1: Find words with similar root/structure
            root_pattern = self._extract_root(word)
            
            for candidate_word in self.all_words:
                if candidate_word == word:
                    continue
                
                # Check if words share similar root
                if root_pattern and root_pattern in candidate_word:
                    synonyms.append(candidate_word)
                    if len(synonyms) >= max_results:
                        break
            
            # Method 2: Translation-based similarity (optional, slower)
            if len(synonyms) < max_results:
                try:
                    english_translation = self.translator.translate(word).lower()
                    
                    # Sample a subset of words for translation comparison
                    sample_size = min(500, len(self.all_words))
                    for i in range(0, sample_size, 10):  # Check every 10th word
                        if len(synonyms) >= max_results:
                            break
                        
                        candidate = self.all_words[i]
                        if candidate == word or candidate in synonyms:
                            continue
                        
                        try:
                            candidate_translation = self.translator.translate(candidate).lower()
                            
                            if self._is_similar(english_translation, candidate_translation):
                                synonyms.append(candidate)
                        except:
                            continue
                except:
                    pass
            
            return synonyms[:max_results]
        
        except Exception as e:
            raise Exception(f"Error finding synonyms: {str(e)}")
    
    def _extract_root(self, word: str) -> str:
        """Extract the root pattern from a Malayalam word"""
        # Simple approach: take first 3-5 characters as root
        if len(word) >= 5:
            return word[:5]
        elif len(word) >= 3:
            return word[:3]
        return word
    
    def _is_similar(self, word1: str, word2: str) -> bool:
        """Check if two English words are similar"""
        # Clean words
        word1 = re.sub(r'[^\w\s]', '', word1).strip()
        word2 = re.sub(r'[^\w\s]', '', word2).strip()
        
        # Exact match
        if word1 == word2:
            return True
        
        # Words share common words
        words1 = set(word1.split())
        words2 = set(word2.split())
        
        if words1.intersection(words2):
            return True
        
        # Check if one word is contained in another
        if word1 in word2 or word2 in word1:
            return True
        
        # Check edit distance for short words
        if len(word1) <= 5 and len(word2) <= 5:
            if self._levenshtein_distance(word1, word2) <= 1:
                return True
        
        return False
    
    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings"""
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def _check_length_condition(self, word_len: int, target_length: int, operator: str) -> bool:
        """Check if word length meets the condition"""
        if target_length is None:
            return True
        
        if operator == "=":
            return word_len == target_length
        elif operator == ">":
            return word_len > target_length
        elif operator == "<":
            return word_len < target_length
        elif operator == ">=":
            return word_len >= target_length
        elif operator == "<=":
            return word_len <= target_length
        return True