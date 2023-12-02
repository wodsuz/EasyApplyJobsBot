import utils, config


initialized = False


def init():
    try:
        if config.displayWarnings:
            print("Initializing repository wrapper...")
        initialized = import_backend_module()
    except Exception as e:
        if config.displayWarnings:
            print(f"Error initializing repository wrapper: {e}")


def import_backend_module():
    try:
        from ..backend import some_special_module
        return True
    except ImportError as e:
        if config.displayWarnings:
            print(f"Could not import backend module: {e}")
        return False
    

def get_answer_by_question(question):
    if initialized:
        try:
            if config.displayWarnings:
                print(f"Getting answer for question: {question}")
        except Exception as e:
            if config.displayWarnings:
                print(f"Error getting answer for question: {e}")


def post_question(question):
    if initialized:
        if config.displayWarnings:
            print(f"Posting question: {question} with answer:")