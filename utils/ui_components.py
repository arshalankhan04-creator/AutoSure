"""
Permission-Aware UI Components
Streamlit UI components that adapt based on user permissions and provide enhanced UX features.
"""

import streamlit as st
from typing import Callable, Optional, Any, Dict
from utils.access_control import _get_user_permissions
from utils.terminology import TerminologyMapper


# Initialize global terminology mapper
_terminology_mapper = TerminologyMapper()


def render_field_with_tooltip(
    label: str,
    tooltip: str,
    field_type: str = 'text_input',
    **kwargs
) -> Any:
    """
    Render a form field with tooltip.
    
    Args:
        label: Field label
        tooltip: Tooltip text
        field_type: Type of Streamlit input ('text_input', 'number_input', 'selectbox', etc.)
        **kwargs: Additional arguments for the Streamlit input function
    
    Returns:
        Value from the input field
    
    Example:
        value = render_field_with_tooltip(
            "Vehicle ID",
            "Unique 17-character identifier for the vehicle",
            field_type='text_input',
            max_chars=17
        )
    """
    # Get the Streamlit input function
    input_func = getattr(st, field_type, None)
    
    if input_func is None:
        st.error(f"Invalid field type: {field_type}")
        return None
    
    # Display label with help icon
    col1, col2 = st.columns([0.95, 0.05])
    
    with col1:
        # Render the input field with help parameter
        value = input_func(label, help=tooltip, **kwargs)
    
    return value


def render_auto_generate_field(
    label: str,
    tooltip: str,
    generator_func: Callable,
    **kwargs
) -> tuple:
    """
    Render a field with auto-generate option and comprehensive error handling.
    
    Args:
        label: Field label
        tooltip: Tooltip text
        generator_func: Function to call for auto-generation (should return generated value)
        **kwargs: Additional arguments for the input field
    
    Returns:
        Tuple of (value, was_auto_generated, error_occurred)
    
    Example:
        vin, auto_gen, error = render_auto_generate_field(
            "Vehicle ID",
            "Unique 17-character identifier for the vehicle",
            lambda: generator.ensure_unique_vin(),
            max_chars=17
        )
    """
    # Create columns for checkbox and input
    col1, col2 = st.columns([0.3, 0.7])
    
    with col1:
        auto_generate = st.checkbox(
            f"Auto-generate {label}",
            help=f"Automatically generate a unique {label}"
        )
    
    value = None
    was_auto_generated = False
    error_occurred = False
    
    with col2:
        if auto_generate:
            # Generate value automatically
            try:
                value = generator_func()
                was_auto_generated = True
                
                # Display the generated value as read-only
                st.text_input(
                    label,
                    value=value,
                    disabled=True,
                    help=tooltip
                )
                
                # Show success indicator
                st.success(f"✓ {label} generated successfully")
                
            except ValueError as e:
                # Handle uniqueness constraint errors
                error_occurred = True
                error_msg = str(e)
                
                if "Unable to generate unique" in error_msg:
                    st.error(f"⚠️ Unable to generate {label} automatically after multiple attempts.")
                    st.info("💡 Please uncheck 'Auto-generate' and enter a value manually below.")
                else:
                    st.error(f"⚠️ {error_msg}")
                    st.info("💡 Please uncheck 'Auto-generate' and enter a value manually.")
                
                # Provide manual entry fallback
                value = st.text_input(
                    label,
                    help=tooltip,
                    placeholder=f"Enter {label} manually",
                    **kwargs
                )
                was_auto_generated = False
                
            except Exception as e:
                # Handle unexpected errors
                error_occurred = True
                st.error(f"⚠️ Error generating {label}: {str(e)}")
                st.info("💡 Please uncheck 'Auto-generate' and enter a value manually.")
                
                # Provide manual entry fallback
                value = st.text_input(
                    label,
                    help=tooltip,
                    placeholder=f"Enter {label} manually",
                    **kwargs
                )
                was_auto_generated = False
        else:
            # Manual entry
            value = st.text_input(
                label,
                help=tooltip,
                **kwargs
            )
    
    return value, was_auto_generated, error_occurred


def render_permission_aware_button(
    label: str,
    permission: str,
    user: dict,
    **kwargs
) -> Optional[bool]:
    """
    Render button only if user has permission.
    
    Args:
        label: Button label
        permission: Required permission
        user: User dict from session state
        **kwargs: Additional button arguments
    
    Returns:
        True if button clicked, False otherwise, None if no permission
    
    Example:
        if render_permission_aware_button("Delete", "delete", st.session_state.user):
            # Handle delete action
            pass
    """
    if not user or 'role' not in user:
        return None
    
    # Get user permissions
    user_permissions = _get_user_permissions(user.get('role', ''))
    
    # Check if user has the required permission
    if 'all' in user_permissions or permission in user_permissions:
        # User has permission, render the button
        return st.button(label, **kwargs)
    
    # User doesn't have permission, don't render anything
    return None


def render_role_based_form(form_config: dict, user: dict) -> Dict[str, Any]:
    """
    Render form with fields visible/editable based on role.
    
    Args:
        form_config: Dict defining form structure and permissions
            Example:
            {
                'fields': [
                    {
                        'name': 'customer_name',
                        'label': 'Customer Name',
                        'type': 'text_input',
                        'required': True,
                        'view_permissions': ['all'],
                        'edit_permissions': ['all', 'customers']
                    },
                    {
                        'name': 'price',
                        'label': 'Price',
                        'type': 'number_input',
                        'required': True,
                        'view_permissions': ['all'],
                        'edit_permissions': ['all', 'orders']
                    }
                ]
            }
        user: User dict from session state
    
    Returns:
        Dict of form values
    
    Example:
        form_data = render_role_based_form(config, st.session_state.user)
        if st.button("Submit"):
            # Use form_data
            pass
    """
    if not user or 'role' not in user:
        st.error("User not authenticated")
        return {}
    
    # Get user permissions
    user_permissions = _get_user_permissions(user.get('role', ''))
    
    form_values = {}
    
    # Render each field based on permissions
    for field in form_config.get('fields', []):
        field_name = field.get('name')
        field_label = field.get('label', field_name)
        field_type = field.get('type', 'text_input')
        view_perms = field.get('view_permissions', ['all'])
        edit_perms = field.get('edit_permissions', ['all'])
        field_kwargs = field.get('kwargs', {})
        
        # Check if user can view this field
        can_view = 'all' in view_perms or any(p in user_permissions for p in view_perms)
        
        if not can_view:
            # Skip this field entirely
            continue
        
        # Check if user can edit this field
        can_edit = 'all' in edit_perms or any(p in user_permissions for p in edit_perms)
        
        # Get the Streamlit input function
        input_func = getattr(st, field_type, None)
        
        if input_func is None:
            st.warning(f"Invalid field type: {field_type}")
            continue
        
        # Render field (disabled if no edit permission)
        if not can_edit:
            field_kwargs['disabled'] = True
        
        # Add help text if provided
        if 'tooltip' in field:
            field_kwargs['help'] = field['tooltip']
        
        # Render the field
        value = input_func(field_label, **field_kwargs)
        form_values[field_name] = value
    
    return form_values


def show_quick_actions(user: dict):
    """
    Display quick action buttons based on user role.
    
    Args:
        user: User dict from session state
    
    Example:
        show_quick_actions(st.session_state.user)
    """
    if not user or 'role' not in user:
        return
    
    role = user.get('role', '')
    
    st.markdown("### Quick Actions")
    
    # Define quick actions for each role
    quick_actions = {
        'admin': [
            {'label': '➕ New Work Order', 'page': 'Service Orders', 'icon': '🔧'},
            {'label': '💰 Quick Sale', 'page': 'POS', 'icon': '💳'},
            {'label': '👤 Add Customer', 'page': 'Customers', 'icon': '👥'},
            {'label': '📦 View Inventory', 'page': 'Inventory', 'icon': '📊'},
            {'label': '📈 Reports', 'page': 'Reports', 'icon': '📊'},
        ],
        'manager': [
            {'label': '➕ New Work Order', 'page': 'Service Orders', 'icon': '🔧'},
            {'label': '💰 Quick Sale', 'page': 'POS', 'icon': '💳'},
            {'label': '👤 Add Customer', 'page': 'Customers', 'icon': '👥'},
            {'label': '📦 View Inventory', 'page': 'Inventory', 'icon': '📊'},
            {'label': '📈 Reports', 'page': 'Reports', 'icon': '📊'},
        ],
        'technician': [
            {'label': '🔧 My Work Orders', 'page': 'Service Orders', 'icon': '📋'},
            {'label': '📦 View Inventory', 'page': 'Inventory', 'icon': '📊'},
        ],
        'cashier': [
            {'label': '💰 Quick Sale', 'page': 'POS', 'icon': '💳'},
            {'label': '🧾 Invoices', 'page': 'Invoices', 'icon': '📄'},
            {'label': '🔍 Search Customer', 'page': 'Customers', 'icon': '👥'},
        ],
    }
    
    actions = quick_actions.get(role, [])
    
    if not actions:
        st.info("No quick actions available for your role.")
        return
    
    # Display actions in columns
    cols = st.columns(min(len(actions), 3))
    
    for idx, action in enumerate(actions):
        col_idx = idx % 3
        with cols[col_idx]:
            if st.button(
                action['label'],
                key=f"quick_action_{idx}",
                use_container_width=True
            ):
                # Store the target page in session state for navigation
                st.session_state['navigate_to'] = action['page']
                st.rerun()
