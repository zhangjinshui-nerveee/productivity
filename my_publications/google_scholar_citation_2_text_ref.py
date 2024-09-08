import pandas as pd
import re

excluded_words = {"and", "or", "of", "in", "for", "on", "with", "a", "an", "the", "to", "at", "by"}

# Define a function to convert a title to title case, excluding certain words
def format_title(title): 
    words = title.split() 
    print(title, words)
    formatted_words = [words[0].capitalize()]  # Capitalize the first word 
    for word in words[1:]: 
        if word.lower() in excluded_words: 
            formatted_words.append(word.lower()) 
        else: 
            formatted_words.append(word.capitalize()) 
    return ' '.join(formatted_words)


def format_authors(authors): 
    formatted_authors = [] 
    # Split the authors by semicolons and format each author 
    for author in authors.split(';'): 
        author = author.strip() 
        if ',' in author: 
            # Split into Last Name and First Name(s) 
            last_name, first_names = [part.strip() for part in author.split(',', 1)] 
            # Take the first letter of the first name and format as "F. Lastname" 
            initials = f"{first_names[0].upper()}." 
            formatted_name = f"{initials} {last_name}" 
        else: 
            # If the name isn't formatted correctly, just skip formatting 
            formatted_name = author 
        # Check for Zhang, Jinshui or Zhang, J and bold them 
        if re.match(r"Zhang,\s*(Jinshui|J)", author, flags=re.IGNORECASE): 
            formatted_name = f"\\textbf{{{formatted_name}}}" 
        formatted_authors.append(formatted_name) 
    # Join the formatted authors with commas 
    return ', '.join(formatted_authors)


# Define a function to format each row according to the LaTeX format with bold highlighting and numbering
def format_publication_latex(row, index): 
    authors = format_authors(row['Authors'])  # Format the authors' names
    title = format_title(row['Title'])
    publication = row['Publication'] 
    year = row['Year'] 
    # Optional fields with conditional formatting 
    volume = f"Vol. {row['Volume']}" if not pd.isna(row['Volume']) else "" 
    number = f"No. {row['Number']}" if not pd.isna(row['Number']) else "" 
    pages = f"pp. {row['Pages']}" if not pd.isna(row['Pages']) else "" 
    publisher = row['Publisher'] if not pd.isna(row['Publisher']) else ""
    # Format the output string in LaTeX format with auto-numbering 
    return f"[{index}] {authors[:-2]} ({year}). {title}. {publication} {volume} {number} {pages} {publisher}."


references = pd.read_csv('citations.csv')
references = references.sort_values(by='Year', ascending=False)
references = references.reset_index(drop=True)
# Apply the formatting function to each row in the DataFrame with auto-numbering 
formatted_publications_latex = [format_publication_latex(row, index+1) for index, row in references.iterrows()] 
# Convert the formatted publications to a single LaTeX text block 
latex_output = "\n\n".join(formatted_publications_latex) 
# Save the LaTeX-formatted text to a file 
with open('formatted_publications_latex.tex', 'w') as file: 
    file.write(latex_output) 
    print("Data exported to formatted_publications_latex.tex with numbering successfully.")
