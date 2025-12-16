"""
Logging configuration for Career Counsellor backend.

Provides consistent logging across all modules.
"""
import logging
import sys
from datetime import datetime

# Create formatters
DETAILED_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s"
SIMPLE_FORMAT = "%(levelname)s | %(name)s | %(message)s"

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format=DETAILED_FORMAT,
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Create loggers for each module
def get_logger(name: str) -> logging.Logger:
    """Get a configured logger for the given module name."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    return logger

# Pre-configured loggers
main_logger = get_logger("main")
model_logger = get_logger("model_adapter")
counsellor_logger = get_logger("counsellor")
researcher_logger = get_logger("researcher")
a2a_logger = get_logger("a2a")


def log_request(logger: logging.Logger, endpoint: str, data: dict):
    """Log an incoming request."""
    logger.info(f"[REQUEST] {endpoint}")
    logger.debug(f"   Data: {data}")


def log_response(logger: logging.Logger, endpoint: str, data: dict, duration_ms: float = None):
    """Log an outgoing response."""
    duration_str = f" ({duration_ms:.0f}ms)" if duration_ms else ""
    logger.info(f"[RESPONSE] {endpoint}{duration_str}")
    logger.debug(f"   Data: {str(data)[:200]}...")


def log_tool_call(logger: logging.Logger, tool_name: str, args: dict):
    """Log a tool invocation."""
    logger.info(f"[TOOL CALL] {tool_name}")
    logger.debug(f"   Args: {args}")


def log_tool_result(logger: logging.Logger, tool_name: str, result: str):
    """Log a tool result."""
    logger.info(f"[TOOL RESULT] {tool_name}")
    logger.debug(f"   Result: {str(result)[:200]}...")


def log_a2a_call(logger: logging.Logger, agent_name: str, message: str):
    """Log an A2A agent call."""
    logger.info(f"[A2A CALL] {agent_name}")
    logger.debug(f"   Message: {message[:100]}...")


def log_a2a_response(logger: logging.Logger, agent_name: str, response: str):
    """Log an A2A agent response."""
    logger.info(f"[A2A RESPONSE] {agent_name}")
    logger.debug(f"   Response: {response[:200]}...")


def log_llm_call(logger: logging.Logger, model: str, messages: list):
    """Log an LLM API call."""
    logger.info(f"[LLM CALL] {model}")
    for msg in messages[-3:]:  # Log last 3 messages
        role = msg.get("role", "?")
        content = msg.get("content", "")[:100]
        logger.debug(f"   [{role}]: {content}...")


def log_llm_response(logger: logging.Logger, model: str, response: str, duration_ms: float = None):
    """Log an LLM response."""
    duration_str = f" ({duration_ms:.0f}ms)" if duration_ms else ""
    logger.info(f"[LLM RESPONSE] {model}{duration_str}")
    logger.debug(f"   Response: {response[:200]}...")
