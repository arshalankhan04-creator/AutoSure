"""
Configuration Manager Module
Manages application configuration for UX customization including terminology mappings
and auto-generation patterns.
"""

import json
import os
import copy
from typing import Dict, Any, Optional
from pathlib import Path


# Default configuration structure
DEFAULT_CONFIG = {
    "terminology": {
        "sku": "Product Code",
        "vin": "Vehicle ID",
        "pos": "Quick Sale",
        "service_order": "Work Order",
        "customer_types": {
            "wholesale": "Business",
            "vip": "Premium",
            "regular": "Standard"
        }
    },
    "tooltips": {
        "sku": "Unique code to identify this part in inventory",
        "vin": "Unique 17-character identifier for the vehicle",
        "product_code": "Unique code to identify this part in inventory",
        "vehicle_id": "Unique 17-character identifier for the vehicle",
        "reorder_level": "Stock quantity that triggers a reorder alert",
        "customer_type": "Business: wholesale pricing, Premium: VIP benefits, Standard: regular pricing",
        "work_order": "Service request for vehicle maintenance or repair",
        "quick_sale": "Fast checkout for parts and services"
    },
    "auto_generation": {
        "vin_pattern": "1HGBH41JXMN{random:6}",
        "sku_pattern": "PART-{date:YYYYMMDD}-{seq:4}",
        "order_pattern": "WO-{date:YYYYMMDD}-{seq:4}",
        "invoice_pattern": "INV-{date:YYYYMMDD}-{seq:4}"
    },
    "defaults": {
        "reorder_level": 10,
        "tax_rate": 0.0,
        "order_status": "pending"
    }
}


class ConfigManager:
    """Manages application configuration for UX customization."""
    
    def __init__(self, config_file: str = 'config/ux_config.json'):
        """
        Initialize configuration manager.
        
        Args:
            config_file: Path to configuration JSON file
        """
        self.config_file = config_file
        self.config = copy.deepcopy(DEFAULT_CONFIG)
        
        # Load configuration from file if it exists
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file, create with defaults if not exists."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge loaded config with defaults (loaded config takes precedence)
                    self._merge_config(loaded_config)
            else:
                # Create config directory if it doesn't exist
                config_dir = os.path.dirname(self.config_file)
                if config_dir and not os.path.exists(config_dir):
                    os.makedirs(config_dir, exist_ok=True)
                
                # Save default configuration
                self._save_config()
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load configuration from {self.config_file}: {e}")
            print("Using default configuration.")
    
    def _merge_config(self, loaded_config: Dict[str, Any]):
        """
        Merge loaded configuration with defaults.
        
        Args:
            loaded_config: Configuration loaded from file
        """
        for key in DEFAULT_CONFIG:
            if key in loaded_config:
                if isinstance(DEFAULT_CONFIG[key], dict) and isinstance(loaded_config[key], dict):
                    # Deep merge for nested dictionaries
                    self.config[key] = {**DEFAULT_CONFIG[key], **loaded_config[key]}
                else:
                    self.config[key] = loaded_config[key]
    
    def _save_config(self):
        """Save current configuration to file."""
        try:
            # Ensure directory exists
            config_dir = os.path.dirname(self.config_file)
            if config_dir and not os.path.exists(config_dir):
                os.makedirs(config_dir, exist_ok=True)
            
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except IOError as e:
            print(f"Error: Could not save configuration to {self.config_file}: {e}")
    
    def get_terminology_config(self) -> Dict[str, Any]:
        """
        Get terminology mappings configuration.
        
        Returns:
            Dictionary containing terminology mappings and customer types
        """
        return self.config.get('terminology', {})
    
    def get_auto_gen_config(self) -> Dict[str, str]:
        """
        Get auto-generation patterns configuration.
        
        Returns:
            Dictionary containing auto-generation patterns for various identifiers
        """
        return self.config.get('auto_generation', {})
    
    def get_tooltips_config(self) -> Dict[str, str]:
        """
        Get tooltips configuration.
        
        Returns:
            Dictionary containing tooltip text for various fields
        """
        return self.config.get('tooltips', {})
    
    def get_defaults_config(self) -> Dict[str, Any]:
        """
        Get default values configuration.
        
        Returns:
            Dictionary containing default values for form fields
        """
        return self.config.get('defaults', {})
    
    def update_terminology(self, mappings: Dict[str, Any]):
        """
        Update terminology mappings.
        
        Args:
            mappings: Dictionary of terminology mappings to update
        """
        if 'terminology' not in self.config:
            self.config['terminology'] = {}
        
        # Update terminology mappings
        self.config['terminology'].update(mappings)
        
        # Save updated configuration
        self._save_config()
    
    def update_auto_gen_patterns(self, patterns: Dict[str, str]):
        """
        Update auto-generation patterns.
        
        Args:
            patterns: Dictionary of auto-generation patterns to update
        """
        if 'auto_generation' not in self.config:
            self.config['auto_generation'] = {}
        
        # Update auto-generation patterns
        self.config['auto_generation'].update(patterns)
        
        # Save updated configuration
        self._save_config()
    
    def update_tooltips(self, tooltips: Dict[str, str]):
        """
        Update tooltip text.
        
        Args:
            tooltips: Dictionary of tooltip text to update
        """
        if 'tooltips' not in self.config:
            self.config['tooltips'] = {}
        
        # Update tooltips
        self.config['tooltips'].update(tooltips)
        
        # Save updated configuration
        self._save_config()
    
    def update_defaults(self, defaults: Dict[str, Any]):
        """
        Update default values.
        
        Args:
            defaults: Dictionary of default values to update
        """
        if 'defaults' not in self.config:
            self.config['defaults'] = {}
        
        # Update defaults
        self.config['defaults'].update(defaults)
        
        # Save updated configuration
        self._save_config()
    
    def reset_to_defaults(self):
        """Reset configuration to defaults."""
        self.config = copy.deepcopy(DEFAULT_CONFIG)
        self._save_config()
    
    def get_full_config(self) -> Dict[str, Any]:
        """
        Get complete configuration.
        
        Returns:
            Dictionary containing all configuration settings
        """
        return copy.deepcopy(self.config)
