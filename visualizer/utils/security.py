"""Security utilities for file validation and safe processing."""
import json
import logging
from typing import Any, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security constraints
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
MAX_JSON_DEPTH = 20
MAX_DATAFRAME_ROWS = 1_000_000
MAX_FLATTEN_ROWS = 100_000


def validate_file_size(uploaded_file) -> None:
    """
    Validate that uploaded file doesn't exceed size limit.

    Raises:
        ValueError: If file size exceeds limit
    """
    # Handle both Streamlit UploadedFile objects and regular file objects
    if hasattr(uploaded_file, 'size'):
        file_size = uploaded_file.size
        if file_size > MAX_FILE_SIZE:
            logger.warning(f"File upload rejected: size {file_size} exceeds limit {MAX_FILE_SIZE}")
            raise ValueError(f"File size exceeds maximum allowed size of {MAX_FILE_SIZE // (1024*1024)}MB")
    elif hasattr(uploaded_file, 'seek') and hasattr(uploaded_file, 'tell'):
        # For file-like objects without size attribute (like StringIO in tests)
        current_pos = uploaded_file.tell()
        uploaded_file.seek(0, 2)  # Seek to end
        file_size = uploaded_file.tell()
        uploaded_file.seek(current_pos)  # Restore position
        if file_size > MAX_FILE_SIZE:
            logger.warning(f"File upload rejected: size {file_size} exceeds limit {MAX_FILE_SIZE}")
            raise ValueError(f"File size exceeds maximum allowed size of {MAX_FILE_SIZE // (1024*1024)}MB")


def get_json_depth(obj: Any, current_depth: int = 0) -> int:
    """
    Calculate the depth of a JSON object.

    Args:
        obj: The JSON object to analyze
        current_depth: Current recursion depth

    Returns:
        Maximum depth of the object
    """
    if not isinstance(obj, (dict, list)):
        return current_depth

    if isinstance(obj, dict):
        if not obj:
            return current_depth + 1
        return max(get_json_depth(v, current_depth + 1) for v in obj.values())

    if isinstance(obj, list):
        if not obj:
            return current_depth + 1
        return max(get_json_depth(item, current_depth + 1) for item in obj)

    return current_depth


def validate_json_structure(data: Any) -> None:
    """
    Validate JSON structure for security constraints.

    Args:
        data: Parsed JSON data

    Raises:
        ValueError: If JSON structure violates security constraints
    """
    depth = get_json_depth(data)
    if depth > MAX_JSON_DEPTH:
        logger.warning(f"JSON rejected: depth {depth} exceeds limit {MAX_JSON_DEPTH}")
        raise ValueError(f"JSON structure too deeply nested (max depth: {MAX_JSON_DEPTH})")


def validate_json_content(uploaded_file) -> Dict[str, Any]:
    """
    Validate that file contains valid JSON content.

    Args:
        uploaded_file: Streamlit uploaded file object or file-like object

    Returns:
        Parsed JSON data

    Raises:
        ValueError: If content is not valid JSON or violates constraints
    """
    try:
        # Read and parse JSON
        if hasattr(uploaded_file, 'read'):
            current_pos = uploaded_file.tell() if hasattr(uploaded_file, 'tell') else 0
            uploaded_file.seek(0) if hasattr(uploaded_file, 'seek') else None
            content = uploaded_file.read()
            if hasattr(uploaded_file, 'seek'):
                uploaded_file.seek(current_pos)  # Reset file pointer
        else:
            raise ValueError("Invalid file object")

        # Parse JSON (handle both string and bytes)
        if isinstance(content, bytes):
            content = content.decode('utf-8')

        data = json.loads(content)

        # Validate structure
        validate_json_structure(data)

        return data
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON content: {e}")
        raise ValueError("File does not contain valid JSON")
    except Exception as e:
        logger.error(f"JSON validation error: {e}")
        raise


def validate_csv_content(uploaded_file) -> bytes:
    """
    Validate CSV file content (basic check for text format).

    Args:
        uploaded_file: Streamlit uploaded file object or file-like object

    Returns:
        Raw file content as bytes or string

    Raises:
        ValueError: If content appears invalid
    """
    try:
        # Handle Streamlit UploadedFile objects
        if hasattr(uploaded_file, 'getvalue'):
            content = uploaded_file.getvalue()
        # Handle file-like objects (like StringIO in tests)
        elif hasattr(uploaded_file, 'read'):
            current_pos = uploaded_file.tell()
            uploaded_file.seek(0)
            content = uploaded_file.read()
            uploaded_file.seek(current_pos)
        else:
            raise ValueError("Invalid file object")

        # Try to decode as UTF-8 to verify it's text
        if isinstance(content, bytes):
            try:
                content.decode('utf-8')
            except UnicodeDecodeError:
                # Try with error handling
                content.decode('utf-8', errors='replace')

        return content
    except Exception as e:
        logger.error(f"CSV validation error: {e}")
        raise ValueError("Invalid CSV file content")


def sanitize_column_name(col_name: str) -> str:
    """
    Sanitize column names to prevent injection attacks.

    Args:
        col_name: Raw column name

    Returns:
        Sanitized column name
    """
    # Remove potentially dangerous characters
    # Allow alphanumeric, spaces, underscores, hyphens, and dots
    import re
    sanitized = re.sub(r'[^\w\s\-\.]', '_', str(col_name))
    return sanitized[:200]  # Limit length


def check_dataframe_size(row_count: int, operation: str = "processing") -> None:
    """
    Check if DataFrame size is within safe limits.

    Args:
        row_count: Number of rows in DataFrame
        operation: Description of operation being performed

    Raises:
        ValueError: If DataFrame exceeds size limits
    """
    if row_count > MAX_DATAFRAME_ROWS:
        logger.warning(f"DataFrame {operation} rejected: {row_count} rows exceeds limit")
        raise ValueError(f"Dataset too large for {operation} (max: {MAX_DATAFRAME_ROWS:,} rows)")


def check_flatten_size(row_count: int) -> None:
    """
    Check if DataFrame is safe to flatten.

    Args:
        row_count: Number of rows in DataFrame

    Raises:
        ValueError: If DataFrame is too large to safely flatten
    """
    if row_count > MAX_FLATTEN_ROWS:
        logger.warning(f"Flatten operation rejected: {row_count} rows exceeds limit")
        raise ValueError(f"Dataset too large to flatten (max: {MAX_FLATTEN_ROWS:,} rows)")
