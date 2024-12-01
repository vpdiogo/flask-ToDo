import json
from typing import Any, Dict

from flask import Response


def json_response(data: Dict[str, Any], status: int = 200) -> Response:
    """
    Formats the JSON response consistently.

    Args:
        data (dict): The data to be returned in the response.
        status (int): The HTTP status code. Default is 200.

    Returns:
        Response: The formatted JSON response.
    """
    return Response(
        json.dumps(data, ensure_ascii=False, indent=4),
        status=status,
        mimetype='application/json',
    )
