# Token types and classes (simplified for standalone operation)
from enum import Enum  # Enum sınıfı, sabit değer kümeleri tanımlamak için kullanılır

class TokenType(Enum):
    """Token types for Python syntax highlighting"""
    KEYWORD = "KEYWORD"         # Anahtar kelimeler (def, if, else, vb.)
    STRING = "STRING"           # String sabitleri ("merhaba", 'dünya', vb.)
    NUMBER = "NUMBER"           # Sayısal sabitler (123, 3.14, vb.)
    COMMENT = "COMMENT"         # Yorum satırları (# ile başlayan)
    OPERATOR = "OPERATOR"       # Operatörler (+, -, *, /, =, vb.)
    DELIMITER = "DELIMITER"     # Ayraçlar (parantez, iki nokta, nokta, vb.)
    IDENTIFIER = "IDENTIFIER"   # Tanımlayıcılar (değişken/fonksiyon isimleri)
    UNKNOWN = "UNKNOWN"         # Tanımlanamayan karakterler
    WHITESPACE = "WHITESPACE"   # Boşluk karakterleri (analiz için)
    NEWLINE = "NEWLINE"         # Satır sonu karakteri

class Token:
    """Represents a token in the source code"""
    def __init__(self, type_: TokenType, value: str, position: int = 0, line: int = 1, column: int = 1):
        self.type = type_           # Token türü (TokenType enumundan)
        self.value = value          # Token'ın kaynak koddaki değeri
        self.position = position    # Kaynak kodda karakter bazında başlangıç pozisyonu
        self.line = line            # Token'ın bulunduğu satır numarası
        self.column = column        # Token'ın bulunduğu sütun numarası
    
    def __repr__(self):
        # Token nesnesinin okunabilir bir temsilini döndürür
        return f"Token({self.type.value}, {repr(self.value)}, {self.line}:{self.column})"