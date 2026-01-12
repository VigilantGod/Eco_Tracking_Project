import random

def generate_feedbackID():

    """
    Generates a ID for feedbacks
    returns:
        feedback_id
    """
    suffix = random.randint(100000,999999)

    return f"FD-{suffix}"

  