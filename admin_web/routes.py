# -*- coding: utf-8 -*-
"""
FastAPI routes for the admin web dashboard.
"""
import secrets
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from utils.gsheets import get_sheet_data, update_row
from config import get_env_var
# We need access to the bot instance to send notifications
from main import application

router = APIRouter()
security = HTTPBasic()
templates = Jinja2Templates(directory="admin_web/templates")

# Get admin credentials from environment variables
ADMIN_USER = get_env_var("ADMIN_USER", required=False, default="admin")
ADMIN_PASSWORD = get_env_var("ADMIN_PASSWORD", required=False, default="password")

def basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    """A simple HTTP Basic Auth dependency."""
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USER)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

class AnswerPayload(BaseModel):
    answer_text: str

@router.get("/dashboard")
def view_dashboard(request: Request, username: str = Depends(basic_auth)):
    """
    Displays the main admin dashboard with pending items.
    """
    # Fetch pending questions
    all_questions = get_sheet_data('questions')
    pending_questions = [q for q in all_questions[1:] if len(q) > 4 and q[4] == 'pending']

    # Fetch pending success stories
    all_stories = get_sheet_data('success_stories')
    pending_stories = [s for s in all_stories[1:] if len(s) > 5 and s[5] == 'pending']

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "pending_questions": pending_questions,
        "pending_stories": pending_stories,
    })

@router.post("/questions/{question_id}/answer")
async def api_answer_question(question_id: int, payload: AnswerPayload, username: str = Depends(basic_auth)):
    """
    API endpoint to answer a question.
    """
    questions_data = get_sheet_data('questions')
    row_index_to_update = -1
    question_row = None

    for i, row in enumerate(questions_data):
        if len(row) > 0 and str(row[0]) == str(question_id):
            row_index_to_update = i + 1
            question_row = row
            break

    if not question_row:
        raise HTTPException(status_code=404, detail="Question not found")

    # Update the row
    question_row[3] = payload.answer_text
    question_row[4] = "answered"
    update_row('questions', row_index_to_update, question_row)

    # Notify the user
    try:
        original_user_id = question_row[1]
        notification_text = f"Your question '{question_row[2]}' has been answered: {payload.answer_text}"
        await application.bot.send_message(chat_id=original_user_id, text=notification_text)
    except Exception as e:
        # Log this failure but don't fail the request
        print(f"Failed to send notification to user {original_user_id}: {e}")

    return {"status": "success", "message": f"Question {question_id} answered."}

@router.delete("/questions/{question_id}")
def api_delete_question(question_id: int, username: str = Depends(basic_auth)):
    """
    API endpoint to delete a question.
    (Note: Deleting rows from GSheets via API is complex, this is a placeholder)
    """
    # This is a placeholder. Deleting rows in GSheets requires more complex API calls
    # (batchUpdate with a DeleteDimensionRequest).
    # For now, we can clear the row or change its status to 'deleted'.
    return {"status": "wip", "message": "Delete functionality is not fully implemented yet."}

@router.post("/stories/{story_id}/approve")
def api_approve_story(story_id: int, username: str = Depends(basic_auth)):
    """
    API endpoint to approve a success story.
    """
    stories_data = get_sheet_data('success_stories')
    row_index_to_update = -1
    story_row = None

    for i, row in enumerate(stories_data):
        if len(row) > 0 and str(row[0]) == str(story_id):
            row_index_to_update = i + 1
            story_row = row
            break

    if not story_row:
        raise HTTPException(status_code=404, detail="Story not found")

    if story_row[5] == 'approved':
        raise HTTPException(status_code=400, detail="Story is already approved")

    story_row[5] = 'approved'
    update_row('success_stories', row_index_to_update, story_row)

    return {"status": "success", "message": f"Story {story_id} approved."}

@router.delete("/stories/{story_id}")
def api_delete_story(story_id: int, username: str = Depends(basic_auth)):
    """
    API endpoint to delete a story. (Placeholder)
    """
    return {"status": "wip", "message": "Delete functionality is not fully implemented yet."}
