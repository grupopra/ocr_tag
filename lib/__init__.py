"""
🚚 Sistema Inteligente de Validação de Entregas - Biblioteca Principal
"""

from .tags_patterns import TagsPatterns, PatternMatch, CompanyType, tags_patterns
from .learning_engine import LearningEngine, LearningSession, learning_engine
from .validators import ValidationResult, EnhancedValidators, enhanced_validators

__version__ = "2.0.0"
__author__ = "OCR Learning System"

# Exportar instâncias globais para facilitar uso
__all__ = [
    "TagsPatterns", "PatternMatch", "CompanyType", "tags_patterns",
    "LearningEngine", "LearningSession", "learning_engine", 
    "ValidationResult", "EnhancedValidators", "enhanced_validators"
] 