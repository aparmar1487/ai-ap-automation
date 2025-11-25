"""
Central configuration for AP Automation.
This file holds ALL settings in one place so we don't hardcode values everywhere.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load secrets from .env file (if it exists)
load_dotenv()
# ============================================================================
# PROJECT PATHS
# ============================================================================
# __file__ is a special variable = full path to current file
# Example: /Users/asap/Documents/GitHub/ai-ap-automation/config/config.py
PROJECT_ROOT = Path(__file__).parent.parent

# Build all other paths relative to project root
DATA_DIR = PROJECT_ROOT / "data"
BRONZE_DIR = DATA_DIR / "bronze"
SILVER_DIR = DATA_DIR / "silver"
GOLD_DIR = DATA_DIR / "gold"
POLICIES_DIR = DATA_DIR / "policies"
INVOICES_DIR = DATA_DIR / "invoices"


# ============================================================================
# STORAGE BACKEND SETTINGS
# ============================================================================
# Which database to use: 'duckdb' (local) or 'fabric' (cloud - later)
STORAGE_BACKEND = 'duckdb'

# DuckDB database file location
DUCKDB_PATH = DATA_DIR / "lakehouse.db"

# ============================================================================
# LLM MODEL REGISTRY (Multi-Provider Support)
# ============================================================================

# API Keys (from .env file)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')

# ============================================================================
# COST SAFETY CONTROLS (Your Budget Protection!)
# ============================================================================

# Daily spending limits (fail-safe to prevent accidents)
MAX_COST_PER_QUERY = 0.02      # Maximum 2 cents per query
DAILY_BUDGET_LIMIT = 2.00      # Stop at $2/day (safety net)
MONTHLY_BUDGET_LIMIT = 20.00   # Stop at $20/month (hard limit)

# Alert thresholds (warn before hitting limits)
WARN_AT_DAILY_PCT = 0.75       # Warning at 75% of daily budget ($1.50)
WARN_AT_MONTHLY_PCT = 0.80     # Warning at 80% of monthly budget ($16)

# Cost tracking file (persists spend across sessions)
COST_TRACKING_FILE = PROJECT_ROOT / "data" / "llm_cost_tracking.json"

# ============================================================================
# MODEL REGISTRY (Available Models & Their Specs)
# ============================================================================

LLM_MODELS = {
    # === OPENAI MODELS ===
    'gpt-4o': {
        'provider': 'openai',
        'model_name': 'gpt-4o',
        'cost_per_1k_input': 0.0025,   # $2.50 per 1M input tokens
        'cost_per_1k_output': 0.010,   # $10 per 1M output tokens
        'context_window': 128000,
        'strengths': ['vision', 'function_calling', 'structured_output'],
        'best_for': ['invoice_ocr', 'complex_reasoning'],
    },
    'gpt-4o-mini': {
        'provider': 'openai',
        'model_name': 'gpt-4o-mini',
        'cost_per_1k_input': 0.00015,  # $0.15 per 1M tokens
        'cost_per_1k_output': 0.0006,  # $0.60 per 1M tokens
        'context_window': 128000,
        'strengths': ['speed', 'cost', 'good_quality'],
        'best_for': ['simple_queries', 'classification', 'sql_generation'],
    },
    
    # === ANTHROPIC (CLAUDE) MODELS ===
    'claude-sonnet-4': {
        'provider': 'anthropic',
        'model_name': 'claude-sonnet-4-20250514',
        'cost_per_1k_input': 0.003,    # $3 per 1M tokens
        'cost_per_1k_output': 0.015,   # $15 per 1M tokens
        'context_window': 200000,
        'strengths': ['reasoning', 'analysis', 'long_context', 'instruction_following'],
        'best_for': ['policy_rag', 'explanations', 'complex_reasoning'],
    },
    'claude-haiku-4': {
        'provider': 'anthropic',
        'model_name': 'claude-haiku-4-20250514',
        'cost_per_1k_input': 0.0008,   # $0.80 per 1M tokens
        'cost_per_1k_output': 0.004,   # $4 per 1M tokens
        'context_window': 200000,
        'strengths': ['speed', 'cost', 'quality'],
        'best_for': ['high_volume', 'simple_tasks', 'validation'],
    },
    
    # === GOOGLE MODELS ===
    'gemini-2.0-flash': {
        'provider': 'google',
        'model_name': 'gemini-2.0-flash-exp',
        'cost_per_1k_input': 0.0,      # FREE during preview!
        'cost_per_1k_output': 0.0,
        'context_window': 1000000,     # 1M tokens!
        'strengths': ['free', 'speed', 'multimodal', 'long_context'],
        'best_for': ['experimentation', 'document_analysis', 'testing'],
    },
    'gemini-1.5-pro': {
        'provider': 'google',
        'model_name': 'gemini-1.5-pro',
        'cost_per_1k_input': 0.00125,  # $1.25 per 1M tokens
        'cost_per_1k_output': 0.005,   # $5 per 1M tokens
        'context_window': 2000000,     # 2M tokens!
        'strengths': ['very_long_context', 'reasoning', 'multimodal'],
        'best_for': ['multi_document', 'large_context'],
    },
    
    # === LOCAL MODELS (OLLAMA - FREE) ===
    'llama-3.2': {
        'provider': 'ollama',
        'model_name': 'llama3.2',
        'cost_per_1k_input': 0.0,      # FREE (local)
        'cost_per_1k_output': 0.0,
        'context_window': 8192,
        'strengths': ['free', 'privacy', 'offline', 'no_limits'],
        'best_for': ['development', 'simple_tasks', 'unlimited_testing'],
    },
    'mistral': {
        'provider': 'ollama',
        'model_name': 'mistral',
        'cost_per_1k_input': 0.0,      # FREE (local)
        'cost_per_1k_output': 0.0,
        'context_window': 32768,
        'strengths': ['free', 'speed', 'good_quality'],
        'best_for': ['sql_generation', 'classification', 'fast_tasks'],
    },
}

# ============================================================================
# TASK-SPECIFIC MODEL SELECTION (Simple Defaults)
# ============================================================================

# Phase 1-2: Start simple with good defaults
TASK_MODEL_MAPPING = {
    # Development/Testing (use free)
    'data_generation': 'llama-3.2',           # Free, good enough
    
    # Invoice Processing (accuracy matters)
    'invoice_ocr': 'gpt-4o-mini',             # Cheap but accurate (start here)
    'invoice_validation': 'llama-3.2',        # Free validation
    
    # SQL Tasks (start free, upgrade if needed)
    'sql_generation': 'llama-3.2',            # Try free first
    'sql_explanation': 'claude-haiku-4',      # Better explanations
    
    # RAG/Policy (reasoning important)
    'policy_search': 'claude-haiku-4',        # Good reasoning, affordable
    'policy_explanation': 'claude-sonnet-4',  # Best explanations (when needed)
    
    # 3-Way Match
    'match_logic': 'llama-3.2',               # Rule-based, free works
    'match_explanation': 'claude-haiku-4',    # When user asks why
    
    # General
    'chat': 'claude-haiku-4',                 # Fast, friendly
    'classification': 'llama-3.2',            # Free for simple stuff
    
    # Critical (only when needed)
    'compliance': 'claude-sonnet-4',          # Don't cheap out
    'fraud_detection': 'claude-sonnet-4',     # Accuracy critical
}

# ============================================================================
# MODEL SELECTION STRATEGY
# ============================================================================

# How should system choose models?
MODEL_SELECTION_STRATEGY = 'hybrid'  
# Options:
#   - 'static': Always use TASK_MODEL_MAPPING (simple)
#   - 'cost_optimized': Prefer cheaper models when possible
#   - 'quality_optimized': Prefer best models regardless of cost
#   - 'hybrid': Balance cost/quality + respect budget limits (RECOMMENDED)

# Hybrid strategy settings
PREFER_FREE_MODELS = True          # Try Ollama first when possible
FALLBACK_TO_PAID = True            # If free model fails, try paid
MAX_RETRIES_PER_MODEL = 2          # Retry failed calls twice

# Fallback chain (if primary model fails)
FALLBACK_ORDER = [
    'llama-3.2',        # Try free first
    'claude-haiku-4',   # Cheap paid option
    'gpt-4o-mini',      # Another cheap option
    'claude-sonnet-4',  # More expensive but reliable
    'gpt-4o',           # Last resort (most expensive)
]

# ============================================================================
# EVALUATION SETTINGS (Phase 3+)
# ============================================================================

# Enable model evaluation and comparison
ENABLE_MODEL_EVALUATION = False  # Set True in Phase 3
EVAL_COMPARISON_MODELS = [
    'llama-3.2',        # Baseline (free)
    'gpt-4o-mini',      # Cheap paid
    'claude-haiku-4',   # Cheap paid alternative
    'gemini-2.0-flash', # Free during preview
]

# Evaluation metrics to track
EVAL_METRICS = ['accuracy', 'cost', 'speed', 'quality']
EVAL_DATA_DIR = PROJECT_ROOT / "tests" / "eval_data"


# ============================================================================
# DATA GENERATION SETTINGS
# ============================================================================
# How many records to create for testing
NUM_VENDORS = 50              # 50 fake companies
NUM_PURCHASE_ORDERS = 200     # 200 POs (multiple POs per vendor)
NUM_INVOICES = 300            # 300 invoices (some POs have multiple invoices)

# Invoice scenario distribution (percentages must sum to 1.0)
SCENARIO_DISTRIBUTION = {
    'PERFECT_MATCH': 0.40,        # 40% - Invoice = PO = GR (everything matches)
    'PARTIAL_QTY': 0.20,          # 20% - Partial delivery (got 80 of 100 units)
    'PRICE_VARIANCE_MINOR': 0.15, # 15% - Price difference ±2% (acceptable)
    'PRICE_VARIANCE_MAJOR': 0.10, # 10% - Price difference >5% (needs review)
    'NO_PO': 0.07,                # 7%  - Invoice received but no PO in system
    'NO_GR': 0.05,                # 5%  - PO exists but goods not received yet
    'DUPLICATE_INVOICE': 0.03,    # 3%  - Same invoice submitted twice (fraud?)
}


# ============================================================================
# 3-WAY MATCH TOLERANCE SETTINGS
# ============================================================================
# How much variance is acceptable before flagging for review?

PRICE_TOLERANCE_PERCENT = 2.0      # Allow ±2% price difference
# Example: PO says $100, Invoice says $102 → PASS (within 2%)
#          PO says $100, Invoice says $110 → FAIL (10% difference)

QUANTITY_TOLERANCE_PERCENT = 5.0   # Allow ±5% quantity difference  
# Example: PO says 100 units, GR received 98 → PASS (within 5%)
#          PO says 100 units, GR received 80 → FAIL (20% short)

AMOUNT_TOLERANCE_ABSOLUTE = 10.0   # Allow ±$10 total difference
# Example: Total should be $1000, actual $1005 → PASS ($5 diff)
#          Total should be $1000, actual $1050 → FAIL ($50 diff)



# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def ensure_directories():
    """
    Create all data directories if they don't exist.
    Called automatically when config is imported.
    
    Why? So we don't get "FileNotFoundError" when trying to save data.
    """
    directories_to_create = [
        BRONZE_DIR, 
        SILVER_DIR, 
        GOLD_DIR, 
        POLICIES_DIR, 
        INVOICES_DIR,
        PROJECT_ROOT / "tests" / "eval_data"
    ]
    
    for directory in directories_to_create:
        # mkdir = make directory
        # parents=True = create parent folders too if needed
        # exist_ok=True = don't error if already exists
        directory.mkdir(parents=True, exist_ok=True)
    
    print("✅ All directories ready")


# ============================================================================
# AUTO-RUN ON IMPORT
# ============================================================================
# When anyone does "from config.config import ...", this runs automatically
ensure_directories()


