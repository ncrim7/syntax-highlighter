from typing import List, Optional
from tokens import Token, TokenType
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext, ttk
from lexer import SimpleLexicalAnalyzer
from parser import SimpleParser

class ColorScheme:
    """Color scheme for syntax highlighting"""
    
    COLORS = {
        TokenType.KEYWORD: "#0066CC",      # Anahtar kelimeler için mavi
        TokenType.STRING: "#009900",       # Stringler için yeşil
        TokenType.NUMBER: "#FF6600",       # Sayılar için turuncu
        TokenType.COMMENT: "#808080",      # Yorumlar için gri
        TokenType.OPERATOR: "#CC0000",     # Operatörler için kırmızı
        TokenType.DELIMITER: "#663399",    # Ayraçlar için mor
        TokenType.IDENTIFIER: "#000000",   # Tanımlayıcılar için siyah
        TokenType.UNKNOWN: "#FF0000"       # Hatalı/unknown için parlak kırmızı
    }
    
    @classmethod
    def get_color(cls, token_type: TokenType) -> str:
        """Belirli bir token türü için renk döndürür"""
        return cls.COLORS.get(token_type, "#000000")
    
class StatusManager:
    """Durum çubuğu güncellemelerini yönetir"""
    
    def __init__(self, status_var: tk.StringVar):
        self.status_var = status_var
        
    def set_status(self, message: str):
        """Durum mesajını ayarla"""
        self.status_var.set(message)
        
    def set_analyzing(self):
        """Analiz ediliyor mesajı"""
        self.set_status("Analyzing...")
        
    def set_complete(self, token_count: int, error_count: int = 0):
        """Analiz tamamlandı mesajı"""
        if error_count > 0:
            self.set_status(f"Analysis complete - {token_count} tokens, {error_count} parse errors")
        else:
            self.set_status(f"Analysis complete - {token_count} tokens")
            
    def set_error(self, error_msg: str):
        """Hata mesajı"""
        self.set_status(f"Error: {error_msg}")

class HighlightedTextView:
    """Sözdizimi vurgulu metin gösterimini yönetir"""
    
    def __init__(self, parent_frame):
        self.text_widget = scrolledtext.ScrolledText(
            parent_frame,
            wrap=tk.NONE, 
            font=("Consolas", 12),
            state=tk.DISABLED,
            width=50,
            height=30
        )
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        self._setup_tags()
    
    def _setup_tags(self):
        """Vurgulama için tag'leri ayarla"""
        for token_type in TokenType:
            tag_name = token_type.value.lower()
            color = ColorScheme.get_color(token_type)
            self.text_widget.tag_configure(tag_name, foreground=color)
            
            # Anahtar kelimeler kalın, yorumlar italik
            if token_type == TokenType.KEYWORD:
                self.text_widget.tag_configure(tag_name, font=("Consolas", 12, "bold"))
            elif token_type == TokenType.COMMENT:
                self.text_widget.tag_configure(tag_name, font=("Consolas", 12, "italic"))
    
    def update_highlighted_text(self, tokens: List[Token]):
        """Vurgulu metni güncelle"""
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete("1.0", tk.END)
        for token in tokens:
            tag_name = token.type.value.lower()
            self.text_widget.insert(tk.END, token.value, tag_name)
        self.text_widget.config(state=tk.DISABLED)

class TokenAnalysisView:
    """Token analiz ağacını yönetir"""
    
    def __init__(self, parent_frame):
        self.setup_treeview(parent_frame)
        
    def setup_treeview(self, parent_frame):
        """Token analiz ağacını oluşturur"""
        columns = ("Position", "Line", "Column", "Type", "Value")
        self.tree = ttk.Treeview(parent_frame, columns=columns, show="headings", height=20)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        scrollbar = ttk.Scrollbar(parent_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def update_tokens(self, tokens: List[Token]):
        """Token analiz ekranını günceller"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for token in tokens[:500]:  # Performans için 500 ile sınırla
            self.tree.insert("", tk.END, values=(
                token.position,
                token.line,
                token.column,
                token.type.value,
                repr(token.value)
            ))

class StatisticsView:
    """İstatistik ekranını yönetir"""
    
    def __init__(self, parent_frame):
        self.text_widget = scrolledtext.ScrolledText(
            parent_frame, 
            height=20, 
            width=80,
            state=tk.DISABLED
        )
        self.text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def update_statistics(self, lexer_stats: dict, parser_errors: List[str]):
        """İstatistik ekranını günceller"""
        stats_text = self._generate_statistics_text(lexer_stats, parser_errors)
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert("1.0", stats_text)
        self.text_widget.config(state=tk.DISABLED)
    
    def _generate_statistics_text(self, lexer_stats: dict, parser_errors: List[str]) -> str:
        """İstatistik metnini oluşturur"""
        if not lexer_stats:
            return "No analysis data available."
        stats_text = "=== LEXICAL ANALYSIS STATISTICS ===\n\n"
        stats_text += f"Total Tokens: {lexer_stats.get('total_tokens', 0)}\n"
        stats_text += f"Total Lines: {lexer_stats.get('total_lines', 0)}\n\n"
        stats_text += "Token Type Distribution:\n"
        stats_text += "-" * 30 + "\n"
        token_counts = lexer_stats.get('token_counts', {})
        total_tokens = lexer_stats.get('total_tokens', 1)
        for token_type, count in sorted(token_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_tokens) * 100
            stats_text += f"{token_type.value:<15}: {count:>6} ({percentage:>5.1f}%)\n"
        if parser_errors:
            stats_text += "\n=== PARSE ERRORS ===\n\n"
            for error in parser_errors:
                stats_text += f"• {error}\n"
        else:
            stats_text += "\nNo parse errors detected.\n"
        if lexer_stats.get('error_count', 0) > 0:
            stats_text += f"\nTotal Lexical Errors: {lexer_stats.get('error_count', 0)}\n"
        else:
            stats_text += "\nNo lexical errors detected.\n"
        if lexer_stats.get('warning_count', 0) > 0:
            stats_text += f"Total Warnings: {lexer_stats.get('warning_count', 0)}\n"
        else:
            stats_text += "No warnings detected.\n"
        return stats_text

class SyntaxHighlighter:
    """Ana sözdizimi vurgulayıcı uygulama sınıfı"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Python Syntax Highlighter - BLM0238 Project")
        self.root.geometry("1400x900")
        self.lexer = None  # Leksik analizci
        self.parser = None  # Parser
        self.tokens = []    # Token listesi
        self.ast = None     # (Kullanılmıyor)
        self.update_pending = False  # Gerçek zamanlı güncelleme için flag
        self.setup_gui()  # Arayüzü kur
        self.setup_event_bindings()  # Olay bağlamalarını kur
        self.root.after(100, self.update_highlighting)  # Başlangıçta analiz yap
    
    def setup_gui(self):
        """Arayüz bileşenlerini kurar"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        self._setup_editor_tab(notebook)
        self._setup_analysis_tab(notebook)
        self._setup_statistics_tab(notebook)
        self.status_var = tk.StringVar()
        self.status_manager = StatusManager(self.status_var)
        self.status_manager.set_status("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _setup_editor_tab(self, notebook):
        """Kod editörü sekmesini kurar"""
        editor_frame = ttk.Frame(notebook)
        notebook.add(editor_frame, text="Code Editor")
        paned = ttk.PanedWindow(editor_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        left_frame = ttk.LabelFrame(paned, text="Python Code Input", padding=5)
        paned.add(left_frame, weight=1)
        self.code_text = scrolledtext.ScrolledText(
            left_frame, 
            wrap=tk.NONE,
            font=("Consolas", 12),
            undo=True,
            width=50,
            height=30
        )
        self.code_text.pack(fill=tk.BOTH, expand=True)
        right_frame = ttk.LabelFrame(paned, text="Syntax Highlighted Output", padding=5)
        paned.add(right_frame, weight=1)
        self.highlighted_view = HighlightedTextView(right_frame)
        self._load_sample_code()
    
    def _setup_analysis_tab(self, notebook):
        """Token analiz sekmesini kurar"""
        analysis_frame = ttk.Frame(notebook)
        notebook.add(analysis_frame, text="Token Analysis")
        self.token_analysis_view = TokenAnalysisView(analysis_frame)
    
    def _setup_statistics_tab(self, notebook):
        """İstatistik sekmesini kurar"""
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="Statistics")
        self.statistics_view = StatisticsView(stats_frame)
    
    def setup_event_bindings(self):
        """Gerçek zamanlı vurgulama için olay bağlamalarını kurar"""
        self.code_text.bind("<KeyRelease>", self.on_text_change)
        self.code_text.bind("<Button-1>", self.on_text_change)
        self.code_text.bind("<ButtonRelease-1>", self.on_text_change)
    
    def _load_sample_code(self):
        """Örnek Python kodu yükler"""
        sample_code = '''# Python Syntax Highlighter Demo
def fibonacci(n):
    """Calculate fibonacci number recursively"""
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Test the function
def main():
    for i in range(10):
        result = fibonacci(i)
        print(f"fibonacci({i}) = {result}")

# Variables and operations
name = "Python Syntax Highlighter"
version = 1.0
is_working = True

if __name__ == "__main__":
    main()
'''
        self.code_text.insert("1.0", sample_code)
    
    def on_text_change(self, event=None):
        """Kullanıcı kodu değiştirdiğinde çağrılır (debounce ile)"""
        if not self.update_pending:
            self.update_pending = True
            self.root.after(300, self.update_highlighting)
    
    def update_highlighting(self):
        """Gerçek zamanlı sözdizimi vurgulamasını günceller"""
        self.update_pending = False
        try:
            code = self.code_text.get("1.0", tk.END)
            self.status_manager.set_analyzing()
            self.root.update_idletasks()
            self._perform_analysis(code)
            self._update_all_views()
        except Exception as e:
            self.status_manager.set_error(str(e))
            messagebox.showerror("Analysis Error", f"An error occurred during analysis:\n{str(e)}")
    
    def _perform_analysis(self, code: str):
        """Leksik ve sözdizimsel analiz yapar"""
        self.lexer = SimpleLexicalAnalyzer(code)
        self.tokens = self.lexer.tokenize()
        self.parser = SimpleParser(self.tokens)
        self.ast = self.parser.parse()
    
    def _update_all_views(self):
        """Tüm arayüzü analiz sonuçlarıyla günceller"""
        self.highlighted_view.update_highlighted_text(self.tokens)
        self.token_analysis_view.update_tokens(self.tokens)
        lexer_stats = self.lexer.get_statistics()
        parser_errors = self.parser.errors if self.parser else []
        self.statistics_view.update_statistics(lexer_stats, parser_errors)
        error_count = len(parser_errors)
        self.status_manager.set_complete(len(self.tokens), error_count)