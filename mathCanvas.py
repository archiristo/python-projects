import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy.parsing.sympy_parser import parse_expr
from sympy import lambdify, symbols

class FunctionPlotterApp(tk.Tk):
    """
    Kullanıcıdan aldığı matematiksel denklemleri 2D veya 3D olarak çizen
    arayüze sahip bir uygulama.
    """
    def __init__(self):
        super().__init__()
        self.title("MathCanvas")
        self.geometry("900x700")

        # Arayüz elemanlarını oluştur
        self._create_widgets()

    def _create_widgets(self):
        # Ana çerçeveleri oluştur
        control_frame = ttk.Frame(self, padding="10")
        control_frame.pack(side=tk.TOP, fill=tk.X)

        plot_frame = ttk.Frame(self)
        plot_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # ---- Kontrol Paneli Elemanları ----

        # Fonksiyon Girişi
        ttk.Label(control_frame, text="Function f(x) or f(x, y):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.function_entry = ttk.Entry(control_frame, width=40)
        self.function_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky="ew")
        self.function_entry.insert(0, "sin(x) * x")

        # Çizim Tipi Seçimi
        self.plot_type = tk.StringVar(value="2D")
        ttk.Label(control_frame, text="Type:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(control_frame, text="2D", variable=self.plot_type, value="2D", command=self._toggle_controls).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        ttk.Radiobutton(control_frame, text="3D", variable=self.plot_type, value="3D", command=self._toggle_controls).grid(row=1, column=2, padx=5, pady=5, sticky="w")

        # Eksen Aralığı Girişleri
        # X Ekseni
        ttk.Label(control_frame, text="X:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.x_min_entry = ttk.Entry(control_frame, width=10)
        self.x_min_entry.grid(row=2, column=1, padx=5, pady=5)
        self.x_min_entry.insert(0, "-10")
        ttk.Label(control_frame, text="-").grid(row=2, column=2)
        self.x_max_entry = ttk.Entry(control_frame, width=10)
        self.x_max_entry.grid(row=2, column=3, padx=5, pady=5)
        self.x_max_entry.insert(0, "10")

        # Y Ekseni (3D için)
        self.y_label = ttk.Label(control_frame, text="Y:")
        self.y_min_entry = ttk.Entry(control_frame, width=10)
        self.y_max_entry = ttk.Entry(control_frame, width=10)
        self.y_separator = ttk.Label(control_frame, text="-")
        
        self.y_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.y_min_entry.grid(row=3, column=1, padx=5, pady=5)
        self.y_min_entry.insert(0, "-10")
        self.y_separator.grid(row=3, column=2)
        self.y_max_entry.grid(row=3, column=3, padx=5, pady=5)
        self.y_max_entry.insert(0, "10")

        # Çizim Butonu
        plot_button = ttk.Button(control_frame, text="Draw!", command=self.plot_function)
        plot_button.grid(row=0, column=4, rowspan=4, padx=20, pady=5, sticky="ns")
        
        # Grid konfigürasyonu
        control_frame.columnconfigure(1, weight=1)
        control_frame.columnconfigure(3, weight=1)

        # ---- Çizim Alanı ----
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Başlangıçta 2D kontrollerini ayarla
        self._toggle_controls()
        # Başlangıçta örnek bir çizim yap
        self.plot_function()

    def _toggle_controls(self):
        """2D ve 3D seçimine göre Y ekseni giriş alanlarını gizler/gösterir."""
        if self.plot_type.get() == "2D":
            self.y_label.grid_remove()
            self.y_min_entry.grid_remove()
            self.y_separator.grid_remove()
            self.y_max_entry.grid_remove()
        else: # 3D
            self.y_label.grid()
            self.y_min_entry.grid()
            self.y_separator.grid()
            self.y_max_entry.grid()

    def plot_function(self):
        """
        Giriş alanlarındaki bilgilere göre fonksiyonun grafiğini çizer.
        """
        function_str = self.function_entry.get()
        plot_type = self.plot_type.get()

        if not function_str:
            messagebox.showerror("Error", "Please enter a function")
            return

        try:
            # Aralıkları al ve float'a çevir
            x_min = float(self.x_min_entry.get())
            x_max = float(self.x_max_entry.get())
            if plot_type == '3D':
                y_min = float(self.y_min_entry.get())
                y_max = float(self.y_max_entry.get())

        except ValueError:
            messagebox.showerror("Error", "Invalid numbers.")
            return

        self.fig.clear() # Önceki çizimi temizle

        try:
            x, y = symbols('x y')
            
            # SymPy ile string ifadeyi matematiksel ifadeye çevir
            # 'all' transformasyonu x^2 gibi ifadeleri x**2 olarak anlar
            expr = parse_expr(function_str, transformations='all')

            if plot_type == '2D':
                # 2D Çizim
                ax = self.fig.add_subplot(111)
                
                # İfadeyi hızlı bir numpy fonksiyonuna dönüştür
                f = lambdify(x, expr, 'numpy')
                
                x_vals = np.linspace(x_min, x_max, 400)
                y_vals = f(x_vals)
                
                ax.plot(x_vals, y_vals)
                ax.set_title(f"$f(x) = {str(expr)}$")
                ax.set_xlabel("x ekseni")
                ax.set_ylabel("y ekseni")
                ax.grid(True)

            else: # 3D Çizim
                ax = self.fig.add_subplot(111, projection='3d')

                # İfadeyi hızlı bir numpy fonksiyonuna dönüştür
                f = lambdify((x, y), expr, 'numpy')
                
                x_vals = np.linspace(x_min, x_max, 50)
                y_vals = np.linspace(y_min, y_max, 50)
                X, Y = np.meshgrid(x_vals, y_vals)
                Z = f(X, Y)
                
                ax.plot_surface(X, Y, Z, cmap='viridis')
                ax.set_title(f"$f(x, y) = {str(expr)}$")
                ax.set_xlabel("x")
                ax.set_ylabel("y")
                ax.set_zlabel("z")

        except Exception as e:
            messagebox.showerror("Error", f"Couldn't draw the function:\n{e}")
            return

        self.canvas.draw()


if __name__ == "__main__":
    app = FunctionPlotterApp()
    app.mainloop()