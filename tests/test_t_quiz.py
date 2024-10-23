"""This module has the tests for the t_quiz
file. It may need some modification as the quiz
is not fully operational yet.
"""
# test_quiz.py
import pytest
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        yield test_client

def test_t_quiz_page(client):
    """Test the quiz page loads successfully."""
    response = client.get('/ttest')
    assert response.status_code == 200
    assert b'Multiple Choice Quiz' in response.data

def test_quiz_submission_correct(client):
    """Test quiz submission with correct answers."""
    response = client.post('/quiz', data={
        'question_1': 'Paris',  # Assuming this is the correct answer
    })
    assert b'Your score is: 2/2' in response.data

def test_quiz_submission_incorrect(client):
    """Test quiz submission with one incorrect answer."""
    response = client.post('/quiz', data={
        'question_1': 'Berlin',  # Incorrect answer
    })
    assert b'Your score is: 0/1' in response.data
    assert b'Your answer: Berlin' in response.data
    assert b'Correct answer: Paris' in response.data

def test_quiz_submission_no_answers(client):
    """Test quiz submission with no answers selected."""
    response = client.post('/quiz', data={})
    assert response.status_code == 200
    assert b'Your score is: 0/1' in response.data  # Assuming 2 questions
