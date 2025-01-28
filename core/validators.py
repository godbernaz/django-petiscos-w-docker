# core/validators.py
from django.core.exceptions import ValidationError
import re

COMMON_PASSWORDS = ['123456', 'password', '123456789', 'qwerty', 'abc123']

# Validador para garantir que a senha não seja uma senha comum
class PasswordNotCommonValidator:
    def validate(self, password, user=None):
        if password in COMMON_PASSWORDS:
            raise ValidationError("A palavra-passe não pode ser uma senha comum.")
    
    def get_help_text(self):
        return "A palavra-passe não pode ser uma senha comum."

# Validador para garantir que a palavra-passe tenha uma letra minúscula
class ComplexPasswordValidator:
    def validate(self, password, user=None):
        if not re.search(r'[a-z]', password):  # Verifica se tem pelo menos uma letra minúscula
            raise ValidationError("A palavra-passe deve conter pelo menos uma letra minúscula.")
    
    def get_help_text(self):
        return "A palavra-passe deve conter pelo menos uma letra minúscula."

# Validador para evitar palavras comuns no password
class PasswordNoCommonWordsValidator:
    def validate(self, password, user=None):
        forbidden_words = ['senha', 'password', 'qwerty']
        for word in forbidden_words:
            if word in password.lower():
                raise ValidationError(f"A palavra-passe não pode conter a palavra '{word}'.")
    
    def get_help_text(self):
        return "A palavra-passe não pode conter palavras comuns como 'senha', 'password', ou 'qwerty'."

# Validador para garantir que a palavra-passe não contenha caracteres especiais
class PasswordNoSpecialCharactersValidator:
    def validate(self, password, user=None):
        if re.search(r'[^a-zA-Z0-9]', password):  # Verifica se tem caracteres especiais
            raise ValidationError("A palavra-passe não pode conter caracteres especiais.")
    
    def get_help_text(self):
        return "A palavra-passe não pode conter caracteres especiais."

# Validador para garantir que a palavra-passe tenha uma letra maiúscula e um número
class CustomPasswordValidator:
    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password):  # Verifica se tem pelo menos uma letra maiúscula
            raise ValidationError("A palavra-passe deve conter pelo menos uma letra maiúscula.")
        if not re.search(r'[0-9]', password):  # Verifica se tem pelo menos um número
            raise ValidationError("A palavra-passe deve conter pelo menos um número.")
    
    def get_help_text(self):
        return "A palavra-passe deve conter pelo menos uma letra maiúscula e pelo menos um número."

# Validador para garantir que a palavra-passe não seja semelhante ao nome de utilizador
class PasswordNotSimilarToUserValidator:
    def validate(self, password, user):
        username = user.username  # Obtém o nome de utilizador
        if username.lower() in password.lower():  # Verifica se o nome de utilizador está na palavra-passe
            raise ValidationError("A palavra-passe não pode ser semelhante ao nome de utilizador ou email.")
    
    def get_help_text(self):
        return "A palavra-passe não pode ser semelhante ao nome de utilizador ou email."