from tokens import TokenType  # Token tiplerini içe aktarır
from typing import Dict, List, Optional  # Tip ipuçları için
from tokens import Token  # Token sınıfını içe aktarır

# Simple parser for demonstration
class SimpleParser:
    """Simplified parser for demonstration"""
    
    def __init__(self, tokens: List[Token]):
        # WHITESPACE ve NEWLINE tokenlarını filtreleyerek sadece anlamlı tokenları saklar
        self.tokens = [t for t in tokens if t.type not in [TokenType.WHITESPACE, TokenType.NEWLINE]]
        self.position = 0  # Şu anki token pozisyonu (şu an kullanılmıyor)
        self.errors = []   # Bulunan sözdizimi hatalarını saklar
    
    def parse(self):
        """Parse the tokens (simplified)"""
        self.errors = []  # Önceki hataları temizle
        # Basit sözdizimi kontrolleri
        self._check_parentheses_balance()  # Parantez dengesi kontrolü
        self._check_string_completeness()  # Stringlerin doğru kapanıp kapanmadığı kontrolü
        return None  # Tam bir uygulamada burada AST dönerdi
    
    def _check_parentheses_balance(self):
        """Check if parentheses are balanced"""
        stack = []  # Açılan parantezleri saklamak için yığın
        pairs = {'(': ')', '[': ']', '{': '}'}  # Açılış-kapanış eşleşmeleri
        
        for token in self.tokens:
            if token.value in pairs:
                # Açılış parantezi ise yığına ekle
                stack.append((token.value, token.line, token.column))
            elif token.value in pairs.values():
                # Kapanış parantezi ise
                if not stack:
                    # Yığında hiç açılış yoksa hata ekle
                    self.errors.append(f"Unmatched closing '{token.value}' at line {token.line}, column {token.column}")
                else:
                    opening, line, col = stack.pop()  # Son açılanı çıkar
                    expected = pairs[opening]  # Beklenen kapanış karakteri
                    if token.value != expected:
                        # Eşleşmiyorsa hata ekle
                        self.errors.append(f"Mismatched parentheses: expected '{expected}' but found '{token.value}' at line {token.line}, column {token.column}")
        
        for opening, line, col in stack:
            # Yığında kalan açılışlar varsa kapanmamış demektir
            self.errors.append(f"Unclosed '{opening}' at line {line}, column {col}")
    
    def _check_string_completeness(self):
        """Check if strings are properly closed"""
        for token in self.tokens:
            if token.type == TokenType.STRING:
                # Stringin başı ve sonu aynı karakter mi ve en az iki karakter mi?
                if len(token.value) < 2 or token.value[0] != token.value[-1]:
                    self.errors.append(f"Unclosed string at line {token.line}, column {token.column}")