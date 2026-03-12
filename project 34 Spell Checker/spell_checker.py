import return
from collections import Counter

class SpellChecker:
    def __init__(self, dictionary_file=None):
        self.dictionary = set()
        self.word_freq = Counter()
        if dictionary_file:
            self.load_dictionary(dictionary_file)
        else:
            # Default dictionary with common words
            words = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 
                    'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
                    'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
                    'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their',
                    'python', 'programming', 'computer', 'system', 'code', 'function',
                    'class', 'variable', 'string', 'integer', 'list', 'dictionary',
                    'love', 'like', 'hello', 'world', 'example', 'test', 'data']
            self.dictionary = set(words)
            self.word_freq = Counter({w: 100 - i for i, w in enumerate(words)})
    
    def load_dictionary(self, file_path):
        with open(file_path, 'r') as f:
            for line in f:
                word = line.strip().lower()
                if word:
                    self.dictionary.add(word)
                    self.word_freq[word] += 1
    
    def preprocess(self, text):
        text = text.lower()
        words = re.findall(r'\b[a-z]+\b', text)
        return words
    
    def levenshtein_distance(self, s1, s2):
        if len(s1) < len(s2):
            return self.levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)
        
        prev = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            curr = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = prev[j + 1] + 1
                deletions = curr[j] + 1
                substitutions = prev[j] + (c1 != c2)
                curr.append(min(insertions, deletions, substitutions))
            prev = curr
        return prev[-1]
    
    def get_suggestions(self, word, max_distance=2, top_n=5):
        if word in self.dictionary:
            return []
        
        candidates = []
        for dict_word in self.dictionary:
            if abs(len(word) - len(dict_word)) > max_distance:
                continue
            distance = self.levenshtein_distance(word, dict_word)
            if distance <= max_distance:
                freq = self.word_freq.get(dict_word, 1)
                score = distance - (freq * 0.01)
                candidates.append((dict_word, distance, score))
        
        candidates.sort(key=lambda x: (x[2], x[1]))
        return [c[0] for c in candidates[:top_n]]
    
    def check_text(self, text):
        words = self.preprocess(text)
        results = {}
        
        for word in words:
            if word not in self.dictionary:
                suggestions = self.get_suggestions(word)
                if suggestions:
                    results[word] = suggestions
        
        return results
    
    def correct_text(self, text):
        words = self.preprocess(text)
        corrections = self.check_text(text)
        
        corrected = []
        for word in words:
            if word in corrections and corrections[word]:
                corrected.append(corrections[word][0])
            else:
                corrected.append(word)
        
        return ' '.join(corrected)


# Demo usage
if __name__ == "__main__":
    checker = SpellChecker()
    
    print("=" * 60)
    print("SPELL CHECKER - Python Application")
    print("=" * 60)
    
    # Test cases
    test_texts = [
        "I love progrmming in pyhton",
        "This is a tets of the speling checker",
        "Helo wrld from my computr systm"
    ]
    
    for text in test_texts:
        print(f"\nOriginal: {text}")
        results = checker.check_text(text)
        
        if results:
            print("Errors found:")
            for word, suggestions in results.items():
                print(f"  '{word}' -> {suggestions}")
            
            corrected = checker.correct_text(text)
            print(f"Corrected: {corrected}")
        else:
            print("No spelling errors found!")
    
    print("\n" + "=" * 60)
    print("Interactive Mode (type 'quit' to exit)")
    print("=" * 60)
    
    while True:
        user_input = input("\nEnter text to check: ").strip()
        if user_input.lower() == 'quit':
            break
        
        if not user_input:
            continue
        
        results = checker.check_text(user_input)
        if results:
            print("\nErrors found:")
            for word, suggestions in results.items():
                print(f"  '{word}' -> {suggestions}")
            print(f"\nAuto-corrected: {checker.correct_text(user_input)}")
        else:
            print("✓ No spelling errors found!")
