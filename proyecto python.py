import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import os

class IAAnalisisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis: Hábitos de IA y Pensamiento Crítico")
        self.root.geometry("1200x800")
        
        self.df = None
        self.df_limpio = None
        
        # Crear notebook (pestañas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear las pestañas
        self.crear_pestana_importar()
        self.crear_pestana_limpiar()
        self.crear_pestana_dashboard()
        self.crear_pestana_reporte()
        
    def crear_pestana_importar(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Importar")
        
        # Botón para cargar CSV
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Cargar CSV", 
                   command=self.cargar_csv).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Ver Info del Dataset", 
                   command=self.mostrar_info).pack(side='left', padx=5)
        
        # Frame para vista previa
        ttk.Label(frame, text="Vista Previa de Datos:", 
                  font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Crear Treeview para mostrar datos
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        self.tree_importar = ttk.Treeview(tree_frame, 
                                          yscrollcommand=vsb.set,
                                          xscrollcommand=hsb.set)
        vsb.config(command=self.tree_importar.yview)
        hsb.config(command=self.tree_importar.xview)
        
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        self.tree_importar.pack(fill='both', expand=True)
        
        # Label para información
        self.lbl_info_importar = ttk.Label(frame, text="", 
                                           font=('Arial', 10))
        self.lbl_info_importar.pack(pady=5)
        
    def crear_pestana_limpiar(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Limpiar")
        
        # Botones de limpieza
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Limpiar Datos", 
                   command=self.limpiar_datos).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Ver Datos Limpios", 
                   command=self.mostrar_datos_limpios).pack(side='left', padx=5)
        
        # Área de texto para mostrar proceso de limpieza
        ttk.Label(frame, text="Proceso de Limpieza:", 
                  font=('Arial', 12, 'bold')).pack(pady=10)
        
        text_frame = ttk.Frame(frame)
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.txt_limpieza = tk.Text(text_frame, height=15, 
                                    yscrollcommand=scrollbar.set)
        self.txt_limpieza.pack(fill='both', expand=True)
        scrollbar.config(command=self.txt_limpieza.yview)
        
        # Vista previa de datos limpios
        ttk.Label(frame, text="Vista Previa de Datos Limpios:", 
                  font=('Arial', 12, 'bold')).pack(pady=10)
        
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        self.tree_limpiar = ttk.Treeview(tree_frame, 
                                         yscrollcommand=vsb.set,
                                         xscrollcommand=hsb.set)
        vsb.config(command=self.tree_limpiar.yview)
        hsb.config(command=self.tree_limpiar.xview)
        
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        self.tree_limpiar.pack(fill='both', expand=True)
        
    def crear_pestana_dashboard(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Dashboard")
        
        # Frame de controles
        control_frame = ttk.Frame(frame)
        control_frame.pack(pady=10)
        
        ttk.Button(control_frame, text="Generar Gráficos", 
                   command=self.generar_graficos).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Guardar Gráficos", 
                   command=self.guardar_graficos).pack(side='left', padx=5)
        
        # Frame para los gráficos (2x2)
        self.graficos_frame = ttk.Frame(frame)
        self.graficos_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
    def crear_pestana_reporte(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Reporte")
        
        # Botones de exportación
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Exportar CSV Limpio", 
                   command=self.exportar_csv).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Exportar Gráficos PNG", 
                   command=self.exportar_graficos).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Generar Reporte Completo", 
                   command=self.generar_reporte_completo).pack(side='left', padx=5)
        
        # Área de texto para mostrar estadísticas
        ttk.Label(frame, text="Estadísticas Descriptivas:", 
                  font=('Arial', 12, 'bold')).pack(pady=10)
        
        text_frame = ttk.Frame(frame)
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.txt_reporte = tk.Text(text_frame, height=20, 
                                   yscrollcommand=scrollbar.set)
        self.txt_reporte.pack(fill='both', expand=True)
        scrollbar.config(command=self.txt_reporte.yview)
        
    def cargar_csv(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if archivo:
            try:
                self.df = pd.read_csv(archivo)
                self.mostrar_vista_previa(self.tree_importar, self.df)
                self.lbl_info_importar.config(
                    text=f"Dataset cargado: {len(self.df)} filas, {len(self.df.columns)} columnas"
                )
                messagebox.showinfo("Éxito", "CSV cargado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar CSV:\n{str(e)}")
                
    def mostrar_vista_previa(self, tree, df, max_rows=100):
        # Limpiar tree
        tree.delete(*tree.get_children())
        
        if df is None:
            return
            
        # Configurar columnas
        tree['columns'] = list(df.columns)
        tree['show'] = 'headings'
        
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        # Insertar datos
        for idx, row in df.head(max_rows).iterrows():
            tree.insert('', 'end', values=list(row))
            
    def mostrar_info(self):
        if self.df is None:
            messagebox.showwarning("Advertencia", "Primero carga un dataset")
            return
            
        info_text = f"Información del Dataset:\n\n"
        info_text += f"Filas: {len(self.df)}\n"
        info_text += f"Columnas: {len(self.df.columns)}\n\n"
        info_text += "Columnas disponibles:\n"
        for col in self.df.columns:
            info_text += f"  - {col} ({self.df[col].dtype})\n"
        
        messagebox.showinfo("Información del Dataset", info_text)
        
    def limpiar_datos(self):
        if self.df is None:
            messagebox.showwarning("Advertencia", "Primero carga un dataset")
            return
            
        self.txt_limpieza.delete(1.0, tk.END)
        self.txt_limpieza.insert(tk.END, "Iniciando limpieza de datos...\n\n")
        
        try:
            self.df_limpio = self.df.copy()
            
            # Detectar y limpiar columnas numéricas
            self.txt_limpieza.insert(tk.END, "1. Procesando columnas numéricas...\n")
            for col in self.df_limpio.columns:
                if 'promedio' in col.lower() or 'horas' in col.lower() or 'edad' in col.lower():
                    self.df_limpio[col] = pd.to_numeric(self.df_limpio[col], errors='coerce')
                    nulos_antes = self.df_limpio[col].isna().sum()
                    if nulos_antes > 0:
                        mediana = self.df_limpio[col].median()
                        self.df_limpio[col].fillna(mediana, inplace=True)
                        self.txt_limpieza.insert(tk.END, 
                            f"   - {col}: {nulos_antes} nulos rellenados con mediana ({mediana:.2f})\n")
            
            # Limpiar columnas categóricas
            self.txt_limpieza.insert(tk.END, "\n2. Procesando columnas categóricas...\n")
            for col in self.df_limpio.columns:
                if self.df_limpio[col].dtype == 'object':
                    nulos_antes = self.df_limpio[col].isna().sum()
                    if nulos_antes > 0:
                        self.df_limpio[col].fillna('DESCONOCIDO', inplace=True)
                        self.txt_limpieza.insert(tk.END, 
                            f"   - {col}: {nulos_antes} nulos rellenados con 'DESCONOCIDO'\n")
                    # Convertir a mayúsculas para estandarizar
                    self.df_limpio[col] = self.df_limpio[col].astype(str).str.upper().str.strip()
            
            # Calcular pc_total si existen columnas de pensamiento crítico
            self.txt_limpieza.insert(tk.END, "\n3. Calculando métricas derivadas...\n")
            pc_cols = [col for col in self.df_limpio.columns if col.startswith('pc_') and col != 'pc_total']
            if pc_cols:
                self.df_limpio['pc_total'] = self.df_limpio[pc_cols].mean(axis=1)
                self.txt_limpieza.insert(tk.END, 
                    f"   - pc_total calculado como promedio de {len(pc_cols)} columnas\n")
            
            self.txt_limpieza.insert(tk.END, "\n✓ Limpieza completada exitosamente!\n")
            self.mostrar_vista_previa(self.tree_limpiar, self.df_limpio)
            
            messagebox.showinfo("Éxito", "Datos limpiados correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en la limpieza:\n{str(e)}")
            
    def mostrar_datos_limpios(self):
        if self.df_limpio is None:
            messagebox.showwarning("Advertencia", "Primero limpia los datos")
            return
        
        self.mostrar_vista_previa(self.tree_limpiar, self.df_limpio)
        
    def generar_graficos(self):
        if self.df_limpio is None:
            messagebox.showwarning("Advertencia", "Primero limpia los datos")
            return
            
        try:
            # Limpiar frame de gráficos
            for widget in self.graficos_frame.winfo_children():
                widget.destroy()
            
            # Crear figura con 4 subplots
            fig = Figure(figsize=(12, 10))
            
            # Gráfico 1: Barras - Horas de estudio vs Promedio académico
            ax1 = fig.add_subplot(2, 2, 1)
            if 'horas_estudio_dia' in self.df_limpio.columns and 'promedio_academico' in self.df_limpio.columns:
                bins = [0, 2, 5, float('inf')]
                labels = ['0-2h', '3-5h', '6+h']
                self.df_limpio['horas_bin'] = pd.cut(self.df_limpio['horas_estudio_dia'], 
                                                      bins=bins, labels=labels)
                datos_grupo = self.df_limpio.groupby('horas_bin', observed=True)['promedio_academico'].mean()
                datos_grupo.plot(kind='bar', ax=ax1, color='steelblue')
                ax1.set_title('Promedio Académico vs Horas de Estudio', fontweight='bold')
                ax1.set_xlabel('Horas de Estudio por Día')
                ax1.set_ylabel('Promedio Académico')
                ax1.tick_params(axis='x', rotation=0)
            else:
                ax1.text(0.5, 0.5, 'Columnas no encontradas', ha='center', va='center')
            
            # Gráfico 2: Pastel - Distribución de métodos de estudio
            ax2 = fig.add_subplot(2, 2, 2)
            if 'metodo_estudio' in self.df_limpio.columns:
                metodos = self.df_limpio['metodo_estudio'].value_counts()
                ax2.pie(metodos.values, labels=metodos.index, autopct='%1.1f%%', startangle=90)
                ax2.set_title('Distribución de Métodos de Estudio', fontweight='bold')
            else:
                ax2.text(0.5, 0.5, 'Columna no encontrada', ha='center', va='center')
            
            # Gráfico 3: Líneas - Evolución del promedio según horas
            ax3 = fig.add_subplot(2, 2, 3)
            if 'horas_estudio_dia' in self.df_limpio.columns and 'promedio_academico' in self.df_limpio.columns:
                bins = [0, 2, 5, float('inf')]
                labels = ['0-2h', '3-5h', '6+h']
                self.df_limpio['horas_bin'] = pd.cut(self.df_limpio['horas_estudio_dia'], 
                                                      bins=bins, labels=labels)
                datos_grupo = self.df_limpio.groupby('horas_bin', observed=True)['promedio_academico'].mean()
                ax3.plot(range(len(datos_grupo)), datos_grupo.values, marker='o', 
                        linewidth=2, markersize=8, color='green')
                ax3.set_xticks(range(len(datos_grupo)))
                ax3.set_xticklabels(datos_grupo.index)
                ax3.set_title('Evolución del Promedio por Horas de Estudio', fontweight='bold')
                ax3.set_xlabel('Grupos de Horas')
                ax3.set_ylabel('Promedio Académico')
                ax3.grid(True, alpha=0.3)
            else:
                ax3.text(0.5, 0.5, 'Columnas no encontradas', ha='center', va='center')
            
            # Gráfico 4: Boxplot - Rendimiento por método de estudio
            ax4 = fig.add_subplot(2, 2, 4)
            if 'metodo_estudio' in self.df_limpio.columns and 'promedio_academico' in self.df_limpio.columns:
                datos_box = [self.df_limpio[self.df_limpio['metodo_estudio'] == metodo]['promedio_academico'].dropna()
                            for metodo in self.df_limpio['metodo_estudio'].unique()]
                ax4.boxplot(datos_box, labels=self.df_limpio['metodo_estudio'].unique())
                ax4.set_title('Distribución del Rendimiento por Método', fontweight='bold')
                ax4.set_xlabel('Método de Estudio')
                ax4.set_ylabel('Promedio Académico')
                ax4.tick_params(axis='x', rotation=45)
            else:
                ax4.text(0.5, 0.5, 'Columnas no encontradas', ha='center', va='center')
            
            fig.tight_layout()
            
            # Mostrar en el canvas
            canvas = FigureCanvasTkAgg(fig, master=self.graficos_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
            self.fig = fig  # Guardar referencia para exportar
            
            messagebox.showinfo("Éxito", "Gráficos generados correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar gráficos:\n{str(e)}")
            
    def guardar_graficos(self):
        if not hasattr(self, 'fig'):
            messagebox.showwarning("Advertencia", "Primero genera los gráficos")
            return
            
        archivo = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if archivo:
            try:
                self.fig.savefig(archivo, dpi=300, bbox_inches='tight')
                messagebox.showinfo("Éxito", f"Gráficos guardados en:\n{archivo}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar:\n{str(e)}")
                
    def exportar_csv(self):
        if self.df_limpio is None:
            messagebox.showwarning("Advertencia", "Primero limpia los datos")
            return
            
        archivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if archivo:
            try:
                self.df_limpio.to_csv(archivo, index=False)
                messagebox.showinfo("Éxito", f"CSV guardado en:\n{archivo}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar:\n{str(e)}")
                
    def exportar_graficos(self):
        self.guardar_graficos()
        
    def generar_reporte_completo(self):
        if self.df_limpio is None:
            messagebox.showwarning("Advertencia", "Primero limpia los datos")
            return
            
        try:
            self.txt_reporte.delete(1.0, tk.END)
            
            reporte = "="*70 + "\n"
            reporte += "REPORTE DE ANÁLISIS: HÁBITOS DE IA Y PENSAMIENTO CRÍTICO\n"
            reporte += "="*70 + "\n\n"
            
            reporte += f"Total de estudiantes: {len(self.df_limpio)}\n\n"
            
            # Estadísticas generales
            reporte += "ESTADÍSTICAS DESCRIPTIVAS\n"
            reporte += "-"*70 + "\n\n"
            
            if 'promedio_academico' in self.df_limpio.columns:
                reporte += f"Promedio Académico:\n"
                reporte += f"  Media: {self.df_limpio['promedio_academico'].mean():.2f}\n"
                reporte += f"  Mediana: {self.df_limpio['promedio_academico'].median():.2f}\n"
                reporte += f"  Desv. Est.: {self.df_limpio['promedio_academico'].std():.2f}\n\n"
            
            if 'horas_estudio_dia' in self.df_limpio.columns:
                reporte += f"Horas de Estudio Diarias:\n"
                reporte += f"  Media: {self.df_limpio['horas_estudio_dia'].mean():.2f}\n"
                reporte += f"  Mediana: {self.df_limpio['horas_estudio_dia'].median():.2f}\n"
                reporte += f"  Mínimo: {self.df_limpio['horas_estudio_dia'].min():.2f}\n"
                reporte += f"  Máximo: {self.df_limpio['horas_estudio_dia'].max():.2f}\n\n"
            
            if 'pc_total' in self.df_limpio.columns:
                reporte += f"Pensamiento Crítico Total:\n"
                reporte += f"  Media: {self.df_limpio['pc_total'].mean():.2f}\n"
                reporte += f"  Mediana: {self.df_limpio['pc_total'].median():.2f}\n\n"
            
            # Distribuciones
            reporte += "\nDISTRIBUCIÓN POR CATEGORÍAS\n"
            reporte += "-"*70 + "\n\n"
            
            if 'metodo_estudio' in self.df_limpio.columns:
                reporte += "Métodos de Estudio:\n"
                for metodo, count in self.df_limpio['metodo_estudio'].value_counts().items():
                    pct = (count / len(self.df_limpio)) * 100
                    reporte += f"  {metodo}: {count} ({pct:.1f}%)\n"
                reporte += "\n"
            
            if 'ia_frecuencia' in self.df_limpio.columns:
                reporte += "Frecuencia de Uso de IA:\n"
                for freq, count in self.df_limpio['ia_frecuencia'].value_counts().items():
                    pct = (count / len(self.df_limpio)) * 100
                    reporte += f"  {freq}: {count} ({pct:.1f}%)\n"
                reporte += "\n"
            
            # Correlaciones
            reporte += "\nANÁLISIS DE RELACIONES\n"
            reporte += "-"*70 + "\n\n"
            
            if all(col in self.df_limpio.columns for col in ['horas_estudio_dia', 'promedio_academico']):
                corr = self.df_limpio['horas_estudio_dia'].corr(self.df_limpio['promedio_academico'])
                reporte += f"Correlación Horas de Estudio - Promedio: {corr:.3f}\n"
            
            if all(col in self.df_limpio.columns for col in ['pc_total', 'promedio_academico']):
                corr = self.df_limpio['pc_total'].corr(self.df_limpio['promedio_academico'])
                reporte += f"Correlación Pensamiento Crítico - Promedio: {corr:.3f}\n"
            
            reporte += "\n" + "="*70 + "\n"
            reporte += "Fin del reporte\n"
            
            self.txt_reporte.insert(tk.END, reporte)
            
            messagebox.showinfo("Éxito", "Reporte generado correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte:\n{str(e)}")

# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = IAAnalisisApp(root)
    root.mainloop()