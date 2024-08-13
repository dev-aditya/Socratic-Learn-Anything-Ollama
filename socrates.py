import ollama


def get_initial_question(topic):
    """
    Generate the initial question to start the Socratic method teaching.

    Parameters:
    topic (str): The topic to be taught.

    Returns:
    str: The initial question.
    """
    return f"Let's begin with an intuition about {topic}. What do you already know about this topic?"


def get_next_question(topic, answers, complexity_level):
    """
    Generate the next question based on the previous answers and the complexity level.

    Parameters:
    topic (str): The topic to be taught.
    answers (str): The previous answers.
    client: The OpenAI client.
    complexity_level (str): The complexity level of the question.

    Returns:
    str: The next Socratic question.
    """
    prompt = f"The topic is {topic}. Based on the previous answers and at a {complexity_level} level, generate the next question to guide the user to learn more about the topic:\n{answers}"
    return call_llama3(prompt)


def call_llama3(prompt):
    """Parameters:
    prompt (str): The prompt describing the desired response.

    Returns:
    str: The generated response.
    """
    response = ollama.chat(
        model="llama3.1", ## Default model, you can change it to any model you want. 
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return response["message"]["content"].strip()


def generate_quiz(topic, answers, complexity_level):
    """
    Generate a quiz question to reinforce learning at the specified complexity level.

    Parameters:
    topic (str): The topic to be taught.
    answers (str): The previous answers.
    complexity_level (str): The complexity level of the quiz question.

    Returns:
    str: A quiz question.
    """
    prompt = f"The topic is {topic}. Based on the previous answers and at a {complexity_level} level, generate a quiz question to reinforce learning:\n{answers}"
    return call_llama3(prompt)


def construct_rich_prompt(topic):
    """
    Constructs a richer prompt based on the original topic.

    Parameters:
    topic (str): The topic to be taught.

    Returns:
    str: The constructed rich prompt.
    """
    prompt = f"Rephrase the following topic in a richer and more detailed way: {topic}"
    return call_llama3(prompt)


def determine_complexity_level(iteration, total_iterations, start_level, end_level):
    """
    Determine the complexity level based on the iteration, total iterations, start level, and end level.

    Parameters:
    iteration (int): The current iteration number.
    total_iterations (int): The total number of iterations.
    start_level (str): The starting complexity level.
    end_level (str): The ending complexity level.

    Returns:
    str: The complexity level.
    """
    if iteration < total_iterations * 0.3:
        return start_level
    elif iteration < total_iterations * 0.7:
        return "college"
    else:
        return end_level


def main():
    topic = input("Please enter the topic to teach: ")
    rich_prompt = construct_rich_prompt(topic)
    print(f"Generated Rich Prompt:\n{rich_prompt}\n")
    confirmation = input("Is this what you meant? (yes/no): ")
    if confirmation.lower() != "yes":
        print("Please restart the program and enter a more specific topic.")
        return

    iterations = int(
        input("How many teaching iterations would you like? (default is 50): ") or 50
    )
    start_level = (
        input("Enter the starting complexity level (default is 'high-school'): ")
        or "high-school"
    )
    end_level = (
        input("Enter the ending complexity level (default is 'graduate'): ")
        or "graduate"
    )

    answers = ""
    question = get_initial_question(topic)

    for i in range(iterations):
        print(f"\nIteration {i + 1}:")
        print("Question:", question)
        answer = input("Your answer: ")
        answers += f"Q: {question}\nA: {answer}\n"

        complexity_level = determine_complexity_level(
            i, iterations, start_level, end_level
        )
        question = get_next_question(topic, answers, complexity_level)

        if i % 10 == 0:
            quiz = generate_quiz(topic, answers, complexity_level)
            print("Quiz:", quiz)
            quiz_answer = input("Your quiz answer: ")
            answers += f"Q: {quiz}\nA: {quiz_answer}\n"

    print("\nTeaching session complete.")
    print("Summary of Q&A:")
    print(answers)


if __name__ == "__main__":
    main()
