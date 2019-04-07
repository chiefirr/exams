def check_final_grade(mark_range, score):
    """
    Function to assign grade dependint of users score
    :param mark_range: mark range object from database
    :param score: user's score for exam
    :return: string with grade
    """
    if score <= mark_range.very_bad:
        return 'Non-Certification'
    elif mark_range.very_bad < score <= mark_range.bad:
        return 'Very bad'
    elif mark_range.bad < score <= mark_range.moderate:
        return 'Bad'
    elif mark_range.moderate < score <= mark_range.good:
        return 'Moderate'
    elif mark_range.good < score <= mark_range.very_good:
        return 'Good'
    else:
        return 'Very good'
