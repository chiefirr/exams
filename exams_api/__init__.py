"""
API module for creating Exams service.
Provides possibilities:
- create Exam Sheets (collection of Task Sheets), edit and delete for its creator and view for another users
- create Task Sheets - question, accepted answer and score
- create Exam - for user who want to pass selected Exam Sheet
- create Task - user provides his answer for selected Task Sheet

Also optionally Exam Sheet creator can assign Marks Range - and this allows to show final grade for the user depending
on his answers.
"""
