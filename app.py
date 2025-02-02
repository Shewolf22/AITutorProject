#!/usr/bin/env python3
"""
Python Tutor Application
-------------------------
A fun project to help kids learn basic Python coding with an AI-powered tutor.
Submitted by: Kritika
"""

import os
import openai
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'thanos' # not for productionenv

def get_api_key():
    return session.get('api_key', None)

def get_ai_response(prompt):
    api_key = get_api_key()
    if not api_key:
        return "Oh no! API key not found. Please set it up on the configuration page."

    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly Python tutor for kids."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response['choices'][0]['message']['content']
        return answer
    except Exception as e:
        # A human error message.
        return f"Oops! Something went wrong: {e}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/configure", methods=["GET", "POST"])
def configure():
    # not the most secure solution, but it gets the job done.
    if request.method == "POST":
        session['api_key'] = request.form["api_key"]
        return redirect(url_for("index"))
    return render_template("configure.html")

@app.route("/tutor", methods=["GET", "POST"])
def tutor():
    # kids can ask questions and get help.
    tutor_response = None
    user_question = ""
    if request.method == "POST":
        user_question = request.form["question"]
        tutor_character = request.form["tutor_character"]
        # tutor's style is based on the chosen character.
        modified_prompt = f"As {tutor_character}, please help me with this Python question: {user_question}"
        tutor_response = get_ai_response(modified_prompt)
    return render_template("tutor.html", response=tutor_response, question=user_question)

@app.route("/homework", methods=["GET", "POST"])
def homework():
    # a simple interactive assignment. the kids can test their Python skills and get feedback.
    assignment = "Write a Python function to reverse a string."
    feedback = None
    if request.method == "POST":
        student_answer = request.form["student_answer"]
        # we expect to see '[::-1]' somewhere.
        if "[::-1]" in student_answer or "slicing" in student_answer.lower():
            feedback = "Awesome job! It looks like you've got the hang of Python slicing."
        else:
            feedback = "Hmm, not quite right. Try using Python's slicing syntax to reverse a string!"
    return render_template("homework.html", assignment=assignment, feedback=feedback)

if __name__ == "__main__":
    app.run(debug=True)
