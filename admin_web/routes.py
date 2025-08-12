# -*- coding: utf-8 -*-
"""
FastAPI routes for the admin web dashboard.
"""
import secrets
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates

from utils.gsheets import get_sheet_data
from config import get_env_var

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
