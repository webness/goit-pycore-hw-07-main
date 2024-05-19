from models import ContactError

def input_error(strerror: str = "Invalid input."):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except(ValueError, IndexError, ContactError) as e:
                if hasattr(e, "message"):
                    return f"{strerror}\nError: {e.message}"
                return strerror
        return wrapper
    return decorator
