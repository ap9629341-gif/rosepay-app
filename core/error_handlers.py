"""
Error handling middleware.

WHAT THIS FILE DOES:
- Catches errors globally
- Returns user-friendly error messages
- Logs errors for debugging
- Prevents sensitive information leaks

LEARN:
- Error handling = catching and managing errors gracefully
- Middleware = code that runs before/after requests
- Prevents app crashes from showing ugly errors
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation errors (invalid input).
    
    WHAT IT DOES:
    1. Catches validation errors (wrong data format)
    2. Returns friendly error message
    3. Shows what fields are wrong
    """
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        errors.append(f"{field}: {message}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": errors,
            "message": "Please check your input and try again."
        }
    )


async def integrity_error_handler(request: Request, exc: IntegrityError):
    """
    Handle database integrity errors (duplicate entries, etc.).
    
    WHAT IT DOES:
    1. Catches database errors (duplicate email, etc.)
    2. Returns friendly error message
    3. Doesn't expose database details
    """
    error_message = str(exc.orig) if hasattr(exc, 'orig') else str(exc)
    
    # Check for common errors
    if "UNIQUE constraint" in error_message or "duplicate" in error_message.lower():
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": "Duplicate entry",
                "message": "This record already exists. Please use a different value."
            }
        )
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": "Database error",
            "message": "Unable to process request. Please try again."
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle all other errors.
    
    WHAT IT DOES:
    1. Catches unexpected errors
    2. Logs error for debugging
    3. Returns friendly message to user
    4. Prevents sensitive info leaks
    """
    # Log error (in production, use proper logging)
    print(f"❌ Error: {type(exc).__name__}: {str(exc)}")
    print(f"   Path: {request.url.path}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "message": "Something went wrong. Please try again later."
        }
    )
