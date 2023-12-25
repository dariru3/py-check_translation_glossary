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
    inconsistencies = {}
    glossary_terms = glossary_df.to_dict(orient='records')
    total_occurrences = 0
    correct_translations = 0

    for term in glossary_terms:
        japanese_term = term['日本語'].strip()
        english_term = term['English'].strip().strip('"')

        # Find all occurrences of the Japanese term in the Japanese text
        japanese_occurrences = re.findall(japanese_term, japanese_text)
        # Find all occurrences of the English term in the English text
        english_occurrences = re.findall(english_term, english_translation, re.IGNORECASE)

        occurrence_count = len(japanese_occurrences)
        total_occurrences += occurrence_count
        if japanese_occurrences and not english_occurrences:
            inconsistencies[japanese_term] = (english_term, occurrence_count)

        if japanese_occurrences:
            correct_translations += occurrence_count if english_occurrences else 0

    return inconsistencies, total_occurrences, correct_translations

# Running the function with the provided texts and the actual glossary
inconsistencies_found, total_occurrences, correct_translations = check_translation_consistency(japanese_text, english_translation, glossary_df)

# Output the inconsistencies
print("\nInconsistencies Found:")
for japanese_term, (english_term, count) in inconsistencies_found.items():
    print(f"Japanese Term: {japanese_term}, Expected English Translation: {english_term}, Count: {count}")

# Calculate and print the percentage of correct translations
if total_occurrences > 0:
    percentage_correct = (correct_translations / total_occurrences) * 100
    print(f"\nPercentage of Glossary Terms Correctly Translated: {percentage_correct:.2f}%")
else:
    print("No glossary terms found in the Japanese text.")
