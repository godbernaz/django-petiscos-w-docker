# core/validators.py
from django.core.exceptions import ValidationError
import re

COMMON_PASSWORDS = ['87654321A', 'Password', 'Qwerty123', 'Abc12345678']

# Validator to ensure that the password is not an ordinary password
class PasswordNotCommonValidator:
    def validate(self, password, user=None):
        if password in COMMON_PASSWORDS:
            raise ValidationError("A palavra-passe não pode ser uma senha comum.")
    
    def get_help_text(self):
        return "A palavra-passe não pode ser uma senha comum."

# Validator to ensure that the password has a lowercase letter
class ComplexPasswordValidator:
    def validate(self, password, user=None):
        if not re.search(r'[a-z]', password):  # Check that it has at least one lower-case letter
            raise ValidationError("A palavra-passe deve conter pelo menos uma letra minúscula.")
    
    def get_help_text(self):
        return "A palavra-passe deve conter pelo menos uma letra minúscula."

# Validator to avoid common password words
class PasswordNoCommonWordsValidator:
    def validate(self, password, user=None):
        forbidden_words = ['senha', 'password', 'qwerty']
        for word in forbidden_words:
            if word in password.lower():
                raise ValidationError(f"A palavra-passe não pode conter a palavra '{word}'.")
    
    def get_help_text(self):
        return "A palavra-passe não pode conter palavras comuns como 'senha', 'password', ou 'qwerty'."

# Validator to ensure that the password does not contain special characters
class PasswordNoSpecialCharactersValidator:
    def validate(self, password, user=None):
        if re.search(r'[^a-zA-Z0-9]', password):  # Check for special characters
            raise ValidationError("A palavra-passe não pode conter caracteres especiais.")
    
    def get_help_text(self):
        return "A palavra-passe não pode conter caracteres especiais."

# Validator to ensure that the password has a capital letter and a number
class CustomPasswordValidator:
    def validate(self, password, user=None):
        if not re.search(r'[A-Z]', password):  # Check that it has at least one capital letter
            raise ValidationError("A palavra-passe deve conter pelo menos uma letra maiúscula.")
        if not re.search(r'[0-9]', password):  # Check that you have at least one number
            raise ValidationError("A palavra-passe deve conter pelo menos um número.")
    
    def get_help_text(self):
        return "A palavra-passe deve conter pelo menos uma letra maiúscula e pelo menos um número."

# Validator to ensure that the password is not similar to the username
class PasswordNotSimilarToUserValidator:
    def validate(self, password, user=None):
        if user and hasattr(user, "username") and user.username: 
            username = user.username
            if username.lower() in password.lower():
                raise ValidationError("A palavra-passe não pode ser semelhante ao nome de utilizador ou email.")
    
    def get_help_text(self):
        return "A palavra-passe não pode ser semelhante ao nome de utilizador ou email."