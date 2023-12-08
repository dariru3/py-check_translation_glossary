import pandas as pd
import re

# Function to read a text file
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Load the Japanese and English text files
japanese_text_path = 'japanese.txt'  # Replace with the path to your Japanese text file
english_translation_path = 'english.txt'  # Replace with the path to your English text file

japanese_text = read_text_file(japanese_text_path)
english_translation = read_text_file(english_translation_path)

# Load the glossary
glossary_path = 'glossary.csv'  # Replace with the path to your glossary file
glossary_df = pd.read_csv(glossary_path)

# Function to check if the translations are consistent with the glossary
def check_translation_consistency(japanese_text, english_translation, glossary_df):
    inconsistencies = []
    glossary_terms = glossary_df.to_dict(orient='records')
    terms_used = set()
    correct_translations = 0

    for term in glossary_terms:
        japanese_term = term['日本語'].strip()
        english_term = term['English'].strip().strip('"')

        # Check if the Japanese term is in the text and hasn't been counted yet
        if re.search(japanese_term, japanese_text) and japanese_term not in terms_used:
            terms_used.add(japanese_term)
            # Check if the English translation is in the English text
            if re.search(english_term, english_translation, re.IGNORECASE):
                correct_translations += 1
            else:
                inconsistencies.append((japanese_term, english_term))

    total_terms_used = len(terms_used)
    print(f'Terms found:{terms_used}')
    return inconsistencies, total_terms_used, correct_translations

# Running the function with the provided texts and the actual glossary
inconsistencies_found, total_terms_used, correct_translations = check_translation_consistency(japanese_text, english_translation, glossary_df)

# Output the inconsistencies
print("\nInconsistencies Found:")
for inconsistency in inconsistencies_found:
    print(f"Japanese Term: {inconsistency[0]}, Expected English Translation: {inconsistency[1]}")

# Calculate and print the percentage of correct translations
if total_terms_used > 0:
    percentage_correct = (correct_translations / total_terms_used) * 100
    print(f"\nPercentage of Glossary Terms Correctly Translated: {percentage_correct:.2f}%")
else:
    print("No glossary terms found in the Japanese text.")
