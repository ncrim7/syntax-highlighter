from tokens import Token, TokenType  # Token ve TokenType sınıflarını içe aktarır
from typing import Dict, List, Optional  # Tip ipuçları için

# Simple lexical analyzer for demonstration
class SimpleLexicalAnalyzer:
    """Simplified lexical analyzer for Python syntax"""
    
    KEYWORDS = {  # Python anahtar kelimeleri kümesi
        'def', 'class', 'if', 'elif', 'else', 'for', 'while', 'try', 'except', 
        'finally', 'with', 'as', 'import', 'from', 'return', 'yield', 'break', 
        'continue', 'pass', 'lambda', 'and', 'or', 'not', 'in', 'is', 'True', 
        'False', 'None', 'global', 'nonlocal', 'assert', 'del', 'raise'
    }
    
    OPERATORS = {  # Python operatörleri kümesi
        '+', '-', '*', '/', '//', '%', '**', '=', '==', '!=', '<', '>', 
        '<=', '>=', '+=', '-=', '*=', '/=', '&', '|', '^', '~', '<<', '>>'
    }
    
    DELIMITERS = {  # Python ayraç karakterleri kümesi
        '(', ')', '[', ']', '{', '}', ',', ':', ';', '.', '@'
    }
    
    def __init__(self, code: str):
        self.code = code  # Analiz edilecek kaynak kod
        self.position = 0  # Kodda mevcut karakter pozisyonu
        self.line = 1      # Satır numarası
        self.column = 1    # Sütun numarası
        self.tokens = []   # Bulunan tokenlar listesi
        self.statistics = {  # Tokenizasyon istatistikleri
            'total_tokens': 0,
            'total_lines': 0,
            'token_counts': {},
            'error_count': 0,
            'warning_count': 0
        }
    
    def tokenize(self) -> List[Token]:
        """Tokenize the input code"""
        self.tokens = []  # Token listesini temizle
        self.position = 0
        self.line = 1
        self.column = 1
        
        while self.position < len(self.code):  # Kodun sonuna kadar döngü
            self._skip_whitespace()  # Boşlukları atla
            
            if self.position >= len(self.code):
                break  # Kodun sonuna gelindiyse çık
                
            current_char = self.code[self.position]  # Şu anki karakter
            
            if current_char == '\n':  # Satır sonu karakteri
                self._add_token(TokenType.NEWLINE, current_char)
                self.line += 1
                self.column = 1
                self.position += 1
            elif current_char == '#':  # Yorum satırı
                self._tokenize_comment()
            elif current_char in ['"', "'"]:  # String başlangıcı
                self._tokenize_string(current_char)
            elif current_char.isdigit():  # Sayı başlangıcı
                self._tokenize_number()
            elif current_char.isalpha() or current_char == '_':  # Tanımlayıcı veya anahtar kelime
                self._tokenize_identifier()
            elif current_char in self.OPERATORS:  # Operatör
                self._tokenize_operator()
            elif current_char in self.DELIMITERS:  # Ayraç
                self._add_token(TokenType.DELIMITER, current_char)
                self.position += 1
                self.column += 1
            else:  # Tanımlanamayan karakter
                self._add_token(TokenType.UNKNOWN, current_char)
                self.position += 1
                self.column += 1
        
        self._update_statistics()  # İstatistikleri güncelle
        return self.tokens  # Token listesini döndür
    
    def _skip_whitespace(self):
        """Skip whitespace characters except newlines"""
        while (self.position < len(self.code) and 
               self.code[self.position] in ' \t\r' and 
               self.code[self.position] != '\n'):
            if self.code[self.position] == '\t':
                self.column += 4  # Tab karakteri 4 boşluk sayılır
            else:
                self.column += 1
            self.position += 1  # Boşluk karakterini atla
    
    def _tokenize_comment(self):
        """Tokenize a comment"""
        start_pos = self.position  # Yorumun başladığı pozisyon
        while self.position < len(self.code) and self.code[self.position] != '\n':
            self.position += 1
            self.column += 1
        
        comment_text = self.code[start_pos:self.position]  # Yorum metni
        self._add_token(TokenType.COMMENT, comment_text)
    
    def _tokenize_string(self, quote_char):
        """Tokenize a string literal"""
        start_pos = self.position  # Stringin başladığı pozisyon
        self.position += 1  # Açılış tırnağını atla
        self.column += 1
        
        while self.position < len(self.code):
            current_char = self.code[self.position]
            if current_char == quote_char:
                self.position += 1  # Kapanış tırnağını da dahil et
                self.column += 1
                break
            elif current_char == '\\' and self.position + 1 < len(self.code):
                self.position += 2  # Kaçış karakterini atla
                self.column += 2
            else:
                self.position += 1
                self.column += 1
        
        string_text = self.code[start_pos:self.position]  # String metni
        self._add_token(TokenType.STRING, string_text)
    
    def _tokenize_number(self):
        """Tokenize a number"""
        start_pos = self.position  # Sayının başladığı pozisyon
        
        while (self.position < len(self.code) and 
               (self.code[self.position].isdigit() or self.code[self.position] == '.')):
            self.position += 1
            self.column += 1
        
        number_text = self.code[start_pos:self.position]  # Sayı metni
        self._add_token(TokenType.NUMBER, number_text)
    
    def _tokenize_identifier(self):
        """Tokenize an identifier or keyword"""
        start_pos = self.position  # Tanımlayıcının başladığı pozisyon
        
        while (self.position < len(self.code) and 
               (self.code[self.position].isalnum() or self.code[self.position] == '_')):
            self.position += 1
            self.column += 1
        
        identifier_text = self.code[start_pos:self.position]  # Tanımlayıcı metni
        
        if identifier_text in self.KEYWORDS:
            self._add_token(TokenType.KEYWORD, identifier_text)  # Anahtar kelime ise
        else:
            self._add_token(TokenType.IDENTIFIER, identifier_text)  # Değilse tanımlayıcı
    
    def _tokenize_operator(self):
        """Tokenize an operator"""
        start_pos = self.position
        
        # Handle multi-character operators
        if self.position + 1 < len(self.code):
            two_char = self.code[self.position:self.position + 2]
            if two_char in self.OPERATORS:
                self.position += 2
                self.column += 2
                self._add_token(TokenType.OPERATOR, two_char)
                return
        
        # Single character operator
        self._add_token(TokenType.OPERATOR, self.code[self.position])
        self.position += 1
        self.column += 1
    
    def _add_token(self, token_type: TokenType, value: str):
        """Add a token to the list"""
        token = Token(token_type, value, self.position, self.line, self.column - len(value))  # Token oluştur
        self.tokens.append(token)  # Token'ı listeye ekle
    
    def _update_statistics(self):
        """Update tokenization statistics"""
        self.statistics['total_tokens'] = len(self.tokens)  # Toplam token sayısı
        self.statistics['total_lines'] = self.line  # Toplam satır sayısı
        
        # Count token types
        token_counts = {}
        for token in self.tokens:
            if token.type not in token_counts:
                token_counts[token.type] = 0
            token_counts[token.type] += 1
        
        self.statistics['token_counts'] = token_counts  # Her token türünden kaç tane var
    
    def get_statistics(self) -> dict:
        """Get tokenization statistics"""
        return self.statistics.copy()  # İstatistiklerin kopyasını döndür