import typer
import json
import os

print("CLI Script: Starting execution")

app = typer.Typer(
    help="A command-line tool to manage the SmartStudentBot's content."
)

QNA_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "qna.json")

@app.command()
def add_qna(
    question: str = typer.Option(..., "--question", "-q", help="The question to add."),
    answer: str = typer.Option(..., "--answer", "-a", help="The answer to the question.")
):
    """
    Adds a new question and answer to the qna.json file.
    """
    try:
        with open(QNA_FILE_PATH, "r", encoding="utf-8") as f:
            qna_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        typer.echo("Warning: qna.json not found or invalid. Creating a new one.")
        qna_data = {"version": "1.0", "data": {}}

    qna_data["data"][question] = answer

    try:
        with open(QNA_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(qna_data, f, indent=2, ensure_ascii=False)
        typer.secho(f"Successfully added Q&A:", fg=typer.colors.GREEN)
        typer.echo(f"  Q: {question}")
        typer.echo(f"  A: {answer}")
    except IOError as e:
        typer.secho(f"Error writing to file: {e}", fg=typer.colors.RED)

if __name__ == "__main__":
    print("CLI Script: Running app")
    app()
