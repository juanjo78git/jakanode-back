"""
Audit Logs Model
"""


def format_audit_log_data(audit_log_data):
    """
    Formats audit log data.

    Args:
        audit_log_data (tuple): Tuple with audit log data from the database.

    Returns:
        dict: Formatted audit log data or None if no data is provided.
    """
    if audit_log_data:
        return {
            "id": audit_log_data[0],
            "user_id": audit_log_data[1],
            "action": audit_log_data[2],
            "details": audit_log_data[3],
            "created_at": audit_log_data[4],
        }
    return None
