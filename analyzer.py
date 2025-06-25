import fitz  # PyMuPDF
import argparse
from collections import Counter
from rich.console import Console
from rich.table import Table

TARGET_SKILLS = [
    "Python", "SQL", "Machine Learning", "Deep Learning", "Data Science",
    "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "Keras", "NLP",
    "Data Analysis", "Excel", "Power BI", "Tableau", "Spark", "Git", "Docker"
]

console = Console()

def extract_text_from_pdf(file_path):
    try:
        with fitz.open(file_path) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            return text
    except Exception as e:
        console.print(f"[red]Error reading PDF: {e}[/red]")
        return ""

def analyze_skills(text):
    words = text.lower().split()
    found = Counter()

    for skill in TARGET_SKILLS:
        count = sum(skill.lower() in word for word in words)
        if count:
            found[skill] = count

    return found

def suggest_improvements(found_skills):
    missing = [skill for skill in TARGET_SKILLS if skill not in found_skills]
    return missing

def display_results(found_skills, missing_skills):
    console.print("[bold green]\nSkill Match Report:[/bold green]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Skill")
    table.add_column("Mentions")

    for skill, count in found_skills.items():
        table.add_row(skill, str(count))

    console.print(table)

    if missing_skills:
        console.print("\n[bold yellow]Suggestions:[/bold yellow]")
        console.print("Consider including these relevant skills (if applicable):")
        for skill in missing_skills:
            console.print(f"- {skill}")

def main():
    parser = argparse.ArgumentParser(description="Analyze a resume PDF for key skills.")
    parser.add_argument("pdf_path", help="Path to the resume PDF file")
    args = parser.parse_args()

    console.print(f"[cyan]Analyzing:[/cyan] {args.pdf_path}")
    text = extract_text_from_pdf(args.pdf_path)

    if not text:
        console.print("[red]No text extracted. Exiting.[/red]")
        return

    found_skills = analyze_skills(text)
    missing_skills = suggest_improvements(found_skills)
    display_results(found_skills, missing_skills)

if __name__ == "__main__":
    main()
