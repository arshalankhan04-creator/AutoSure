"""
Helper Functions
Common utility functions used throughout the application
"""

from datetime import datetime, date
from typing import Any, Dict, List
import config


def format_currency(amount: float, include_symbol: bool = True) -> str:
    """Format a number as currency"""
    if amount is None:
        amount = 0.0
    
    formatted = f"{amount:,.2f}"
    
    if include_symbol:
        return f"{config.app_config.CURRENCY_SYMBOL}{formatted}"
    return formatted


def format_date(date_value: Any, format_str: str = "%Y-%m-%d") -> str:
    """Format a date value"""
    if date_value is None:
        return ""
    
    if isinstance(date_value, str):
        try:
            date_value = datetime.strptime(date_value, "%Y-%m-%d").date()
        except ValueError:
            return date_value
    
    if isinstance(date_value, datetime):
        return date_value.strftime(format_str)
    
    if isinstance(date_value, date):
        return date_value.strftime(format_str)
    
    return str(date_value)


def format_datetime(datetime_value: Any, format_str: str = "%Y-%m-%d %H:%M") -> str:
    """Format a datetime value"""
    if datetime_value is None:
        return ""
    
    if isinstance(datetime_value, datetime):
        return datetime_value.strftime(format_str)
    
    return str(datetime_value)


def format_phone(phone: str) -> str:
    """Format a phone number for display"""
    if not phone:
        return ""
    
    # Remove non-numeric characters
    digits = ''.join(filter(str.isdigit, phone))
    
    # Format based on length
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    
    return phone


def calculate_percentage(part: float, total: float) -> float:
    """Calculate percentage"""
    if total == 0:
        return 0.0
    return (part / total) * 100


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """Truncate text to a maximum length"""
    if not text or len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers"""
    if denominator == 0:
        return default
    return numerator / denominator


def get_status_color(status: str) -> str:
    """Get color for status display"""
    colors = {
        # Service order statuses
        'pending': '#FFA500',      # Orange
        'in_progress': '#007BFF',  # Blue
        'waiting_parts': '#DC3545', # Red
        'completed': '#28A745',    # Green
        'invoiced': '#17A2B8',     # Cyan
        'cancelled': '#6C757D',    # Gray
        
        # Invoice statuses
        'unpaid': '#DC3545',       # Red
        'partial': '#FFC107',      # Yellow
        'paid': '#28A745',         # Green
        
        # General
        'active': '#28A745',       # Green
        'inactive': '#6C757D',     # Gray
    }
    return colors.get(status.lower(), '#6C757D')


def get_status_icon(status: str) -> str:
    """Get icon for status display"""
    icons = {
        'pending': '⏳',
        'in_progress': '🔧',
        'waiting_parts': '📦',
        'completed': '✅',
        'invoiced': '📄',
        'cancelled': '❌',
        'unpaid': '💰',
        'partial': '💵',
        'paid': '✅',
        'active': '✓',
        'inactive': '✗',
    }
    return icons.get(status.lower(), '○')


def generate_report(title: str, data: List[Dict], 
                    columns: List[str] = None) -> str:
    """Generate a simple text report"""
    lines = []
    lines.append("=" * 60)
    lines.append(f"  {title}")
    lines.append(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 60)
    lines.append("")
    
    if not data:
        lines.append("No data to display.")
        return "\n".join(lines)
    
    if columns is None:
        columns = list(data[0].keys())
    
    # Calculate column widths
    widths = {col: len(col) for col in columns}
    for row in data:
        for col in columns:
            value = str(row.get(col, ''))
            widths[col] = max(widths[col], len(value))
    
    # Header
    header = " | ".join(col.ljust(widths[col]) for col in columns)
    lines.append(header)
    lines.append("-" * len(header))
    
    # Rows
    for row in data:
        line = " | ".join(str(row.get(col, '')).ljust(widths[col]) for col in columns)
        lines.append(line)
    
    lines.append("")
    lines.append(f"Total records: {len(data)}")
    
    return "\n".join(lines)


def create_paginated_list(items: List[Any], page: int = 1, 
                          items_per_page: int = 20) -> Dict:
    """Create paginated list result"""
    total_items = len(items)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    
    return {
        'items': items[start_idx:end_idx],
        'page': page,
        'items_per_page': items_per_page,
        'total_items': total_items,
        'total_pages': total_pages,
        'has_previous': page > 1,
        'has_next': page < total_pages
    }
