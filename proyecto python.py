import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class IAAnalisisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hábitos de IA y Pensamiento Crítico - Análisis Universitario")
        self.root.geometry("1400x900")
        
        self.df = None
        self.df_limpio = None
        
        # Variables obligatorias de pensamiento crítico
        self.pc_cols = ['pc_analisis', 'pc_inferencia', 'pc_evaluacion', 
                        'pc_autorregulacion', 'pc_apertura_mental']
        
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
        self.notebook.add(frame, text="📥 Importar")
        
        # Botón para cargar CSV
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Cargar CSV", 
                   command=self.cargar_csv, width=20).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Ver Info del Dataset", 
                   command=self.mostrar_info, width=20).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Validar Columnas", 
                   command=self.validar_columnas, width=20).pack(side='left', padx=5)
        
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
        self.notebook.add(frame, text="🧹 Limpiar")
        
        # Botones de limpieza
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Limpiar y Estandarizar Datos", 
                   command=self.limpiar_datos, width=25).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Ver Datos Limpios", 
                   command=self.mostrar_datos_limpios, width=20).pack(side='left', padx=5)
        
        # Área de texto para mostrar proceso de limpieza
        ttk.Label(frame, text="Proceso de Limpieza y Estandarización:", 
                  font=('Arial', 12, 'bold')).pack(pady=10)
        
        text_frame = ttk.Frame(frame)
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.txt_limpieza = tk.Text(text_frame, height=12, 
                                    yscrollcommand=scrollbar.set, font=('Consolas', 9))
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
        self.notebook.add(frame, text="📊 Dashboard")
        
        # Frame de controles
        control_frame = ttk.Frame(frame)
        control_frame.pack(pady=10)
        
        ttk.Button(control_frame, text="🔄 Generar Gráficos", 
                   command=self.generar_graficos, width=20).pack(side='left', padx=5)
        ttk.Button(control_frame, text="💾 Guardar Gráficos PNG", 
                   command=self.guardar_graficos, width=20).pack(side='left', padx=5)
        
        # Frame para los gráficos (2x2)
        self.graficos_frame = ttk.Frame(frame)
        self.graficos_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
    def crear_pestana_reporte(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📄 Reporte")
        
        # Botones de exportación
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="📊 Exportar CSV Limpio", 
                   command=self.exportar_csv, width=20).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🖼️ Exportar Gráficos PNG", 
                   command=self.exportar_graficos, width=20).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="📝 Generar Reporte Completo", 
                   command=self.generar_reporte_completo, width=25).pack(side='left', padx=5)
        
        # Área de texto para mostrar estadísticas
        ttk.Label(frame, text="Reporte de Análisis Completo:", 
                  font=('Arial', 12, 'bold')).pack(pady=10)
        
        text_frame = ttk.Frame(frame)
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.txt_reporte = tk.Text(text_frame, height=25, 
                                   yscrollcommand=scrollbar.set, font=('Consolas', 9))
        self.txt_reporte.pack(fill='both', expand=True)
        scrollbar.config(command=self.txt_reporte.yview)
        
    def cargar_csv(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo CSV de encuesta",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if archivo:
            try:
                self.df = pd.read_csv(archivo)
                self.mostrar_vista_previa(self.tree_importar, self.df)
                self.lbl_info_importar.config(
                    text=f"✓ Dataset cargado: {len(self.df)} estudiantes, {len(self.df.columns)} variables"
                )
                messagebox.showinfo("Éxito", "CSV cargado correctamente.\n\nAhora valida las columnas obligatorias.")
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
            tree.column(col, width=120)
        
        # Insertar datos
        for idx, row in df.head(max_rows).iterrows():
            tree.insert('', 'end', values=list(row))
            
    def mostrar_info(self):
        if self.df is None:
            messagebox.showwarning("Advertencia", "Primero carga un dataset")
            return
            
        info_text = f"INFORMACIÓN DEL DATASET\n{'='*60}\n\n"
        info_text += f"Dimensiones: {len(self.df)} filas × {len(self.df.columns)} columnas\n\n"
        info_text += "COLUMNAS DISPONIBLES:\n" + "-"*60 + "\n"
        for col in self.df.columns:
            dtype = str(self.df[col].dtype)
            nulls = self.df[col].isna().sum()
            info_text += f"  • {col}\n    Tipo: {dtype} | Nulos: {nulls}\n"
        
        messagebox.showinfo("Información del Dataset", info_text)
    
    def validar_columnas(self):
        if self.df is None:
            messagebox.showwarning("Advertencia", "Primero carga un dataset")
            return
        
        # Validar columnas obligatorias
        cols_requeridas = self.pc_cols + ['pc_total', 'promedio_academico', 
                                          'horas_estudio_dia', 'metodo_estudio']
        
        faltantes = [col for col in cols_requeridas if col not in self.df.columns]
        
        if faltantes:
            msg = "⚠️ COLUMNAS FALTANTES:\n\n"
            msg += "\n".join([f"  • {col}" for col in faltantes])
            msg += "\n\nEl análisis completo requiere estas columnas."
            messagebox.showwarning("Validación", msg)
        else:
            msg = "✓ VALIDACIÓN EXITOSA\n\n"
            msg += "Todas las columnas obligatorias están presentes:\n\n"
            msg += "Pensamiento Crítico:\n"
            for col in self.pc_cols:
                msg += f"  ✓ {col}\n"
            msg += f"  ✓ pc_total\n\n"
            msg += "Variables de análisis:\n"
            msg += "  ✓ promedio_academico\n"
            msg += "  ✓ horas_estudio_dia\n"
            msg += "  ✓ metodo_estudio\n\n"
            msg += "Puedes proceder a limpiar los datos."
            messagebox.showinfo("Validación", msg)
        
    def limpiar_datos(self):
        if self.df is None:
            messagebox.showwarning("Advertencia", "Primero carga un dataset")
            return
            
        self.txt_limpieza.delete(1.0, tk.END)
        self.txt_limpieza.insert(tk.END, "="*70 + "\n")
        self.txt_limpieza.insert(tk.END, "PROCESO DE LIMPIEZA Y ESTANDARIZACIÓN\n")
        self.txt_limpieza.insert(tk.END, "="*70 + "\n\n")
        
        try:
            self.df_limpio = self.df.copy()
            
            # 1. VALIDAR Y LIMPIAR PROMEDIO ACADÉMICO
            self.txt_limpieza.insert(tk.END, "1️⃣  VALIDANDO PROMEDIO ACADÉMICO [1-3]...\n")
            if 'promedio_academico' in self.df_limpio.columns:
                self.df_limpio['promedio_academico'] = pd.to_numeric(
                    self.df_limpio['promedio_academico'], errors='coerce')
                
                fuera_rango = ((self.df_limpio['promedio_academico'] < 1) | 
                              (self.df_limpio['promedio_academico'] > 3)).sum()
                
                # Limitar al rango válido
                self.df_limpio['promedio_academico'] = self.df_limpio['promedio_academico'].clip(1, 3)
                
                nulos = self.df_limpio['promedio_academico'].isna().sum()
                if nulos > 0:
                    mediana = self.df_limpio['promedio_academico'].median()
                    self.df_limpio['promedio_academico'].fillna(mediana, inplace=True)
                    self.txt_limpieza.insert(tk.END, 
                        f"   ✓ {nulos} valores nulos rellenados con mediana: {mediana:.2f}\n")
                if fuera_rango > 0:
                    self.txt_limpieza.insert(tk.END, 
                        f"   ✓ {fuera_rango} valores ajustados al rango [1-3]\n")
                self.txt_limpieza.insert(tk.END, 
                    f"   ✓ Media actual: {self.df_limpio['promedio_academico'].mean():.2f}\n\n")
            
            # 2. VALIDAR Y LIMPIAR HORAS DE ESTUDIO
            self.txt_limpieza.insert(tk.END, "2️⃣  VALIDANDO HORAS DE ESTUDIO [≥0]...\n")
            if 'horas_estudio_dia' in self.df_limpio.columns:
                self.df_limpio['horas_estudio_dia'] = pd.to_numeric(
                    self.df_limpio['horas_estudio_dia'], errors='coerce')
                
                # Asegurar valores no negativos
                self.df_limpio['horas_estudio_dia'] = self.df_limpio['horas_estudio_dia'].clip(lower=0)
                
                nulos = self.df_limpio['horas_estudio_dia'].isna().sum()
                if nulos > 0:
                    mediana = self.df_limpio['horas_estudio_dia'].median()
                    self.df_limpio['horas_estudio_dia'].fillna(mediana, inplace=True)
                    self.txt_limpieza.insert(tk.END, 
                        f"   ✓ {nulos} valores nulos rellenados con mediana: {mediana:.2f}h\n")
                
                # Crear bins para análisis
                self.df_limpio['horas_bin'] = pd.cut(
                    self.df_limpio['horas_estudio_dia'],
                    bins=[-0.001, 2, 5, 10],
                    labels=['0-2h', '3-5h', '6+h']
                )
                self.txt_limpieza.insert(tk.END, 
                    f"   ✓ Variable 'horas_bin' creada: 0-2h, 3-5h, 6+h\n\n")
            
            # 3. LIMPIAR Y NORMALIZAR MÉTODO DE ESTUDIO
            self.txt_limpieza.insert(tk.END, "3️⃣  NORMALIZANDO MÉTODO DE ESTUDIO...\n")
            if 'metodo_estudio' in self.df_limpio.columns:
                nulos_antes = self.df_limpio['metodo_estudio'].isna().sum()
                self.df_limpio['metodo_estudio'] = (self.df_limpio['metodo_estudio']
                    .astype(str).str.upper().str.strip())
                self.df_limpio['metodo_estudio'].replace('NAN', 'DESCONOCIDO', inplace=True)
                
                if nulos_antes > 0:
                    self.txt_limpieza.insert(tk.END, 
                        f"   ✓ {nulos_antes} valores nulos → 'DESCONOCIDO'\n")
                
                metodos = self.df_limpio['metodo_estudio'].value_counts()
                self.txt_limpieza.insert(tk.END, "   ✓ Distribución:\n")
                for met, count in metodos.items():
                    self.txt_limpieza.insert(tk.END, f"      • {met}: {count}\n")
                self.txt_limpieza.insert(tk.END, "\n")
            
            # 4. NORMALIZAR FRECUENCIA DE IA
            self.txt_limpieza.insert(tk.END, "4️⃣  NORMALIZANDO FRECUENCIA DE USO DE IA...\n")
            if 'ia_frecuencia' in self.df_limpio.columns:
                nulos_antes = self.df_limpio['ia_frecuencia'].isna().sum()
                self.df_limpio['ia_frecuencia'] = (self.df_limpio['ia_frecuencia']
                    .astype(str).str.upper().str.strip())
                self.df_limpio['ia_frecuencia'].replace('NAN', 'DESCONOCIDO', inplace=True)
                
                if nulos_antes > 0:
                    self.txt_limpieza.insert(tk.END, 
                        f"   ✓ {nulos_antes} valores nulos → 'DESCONOCIDO'\n")
                
                freq = self.df_limpio['ia_frecuencia'].value_counts()
                self.txt_limpieza.insert(tk.END, "   ✓ Distribución:\n")
                for f, count in freq.items():
                    self.txt_limpieza.insert(tk.END, f"      • {f}: {count}\n")
                self.txt_limpieza.insert(tk.END, "\n")
            
            # 5. VALIDAR Y CALCULAR PENSAMIENTO CRÍTICO
            self.txt_limpieza.insert(tk.END, "5️⃣  PROCESANDO PENSAMIENTO CRÍTICO [Likert 1-5]...\n")
            
            pc_disponibles = [col for col in self.pc_cols if col in self.df_limpio.columns]
            
            if pc_disponibles:
                for col in pc_disponibles:
                    self.df_limpio[col] = pd.to_numeric(self.df_limpio[col], errors='coerce')
                    self.df_limpio[col] = self.df_limpio[col].clip(1, 5).round(2)
                    nulos = self.df_limpio[col].isna().sum()
                    if nulos > 0:
                        mediana = self.df_limpio[col].median()
                        self.df_limpio[col].fillna(mediana, inplace=True)
                        self.txt_limpieza.insert(tk.END, 
                            f"   ✓ {col}: {nulos} nulos → mediana {mediana:.2f}\n")
                
                # Calcular o recalcular pc_total
                self.df_limpio['pc_total'] = self.df_limpio[pc_disponibles].mean(axis=1).round(2)
                self.txt_limpieza.insert(tk.END, 
                    f"\n   ✓ pc_total calculado (promedio de {len(pc_disponibles)} dimensiones)\n")
                self.txt_limpieza.insert(tk.END, 
                    f"   ✓ Media pc_total: {self.df_limpio['pc_total'].mean():.2f}\n\n")
            
            # 6. LIMPIAR OTRAS COLUMNAS CATEGÓRICAS
            self.txt_limpieza.insert(tk.END, "6️⃣  ESTANDARIZANDO OTRAS VARIABLES CATEGÓRICAS...\n")
            for col in ['facultad', 'sexo']:
                if col in self.df_limpio.columns:
                    nulos = self.df_limpio[col].isna().sum()
                    self.df_limpio[col] = (self.df_limpio[col]
                        .astype(str).str.upper().str.strip())
                    self.df_limpio[col].replace('NAN', 'DESCONOCIDO', inplace=True)
                    if nulos > 0:
                        self.txt_limpieza.insert(tk.END, 
                            f"   ✓ {col}: {nulos} nulos → 'DESCONOCIDO'\n")
            
            # 7. LIMPIAR VARIABLES NUMÉRICAS RESTANTES
            self.txt_limpieza.insert(tk.END, "\n7️⃣  PROCESANDO VARIABLES NUMÉRICAS ADICIONALES...\n")
            for col in ['edad', 'semestre']:
                if col in self.df_limpio.columns:
                    self.df_limpio[col] = pd.to_numeric(self.df_limpio[col], errors='coerce')
                    nulos = self.df_limpio[col].isna().sum()
                    if nulos > 0:
                        mediana = self.df_limpio[col].median()
                        self.df_limpio[col].fillna(mediana, inplace=True)
                        self.txt_limpieza.insert(tk.END, 
                            f"   ✓ {col}: {nulos} nulos → mediana {mediana:.0f}\n")
            
            self.txt_limpieza.insert(tk.END, "\n" + "="*70 + "\n")
            self.txt_limpieza.insert(tk.END, "✅ LIMPIEZA COMPLETADA EXITOSAMENTE\n")
            self.txt_limpieza.insert(tk.END, "="*70 + "\n")
            
            self.mostrar_vista_previa(self.tree_limpiar, self.df_limpio)
            
            messagebox.showinfo("Éxito", 
                "Datos limpiados y estandarizados correctamente.\n\n" +
                "Ya puedes generar visualizaciones en el Dashboard.")
            
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
            fig = Figure(figsize=(14, 11))
            fig.suptitle('Dashboard: Hábitos de IA y Pensamiento Crítico', 
                        fontsize=16, fontweight='bold', y=0.995)
            
            # GRÁFICO 1: Barras - Horas vs Promedio + PC
            ax1 = fig.add_subplot(2, 2, 1)
            if 'horas_bin' in self.df_limpio.columns and 'promedio_academico' in self.df_limpio.columns:
                # Agrupar datos
                grouped = self.df_limpio.groupby('horas_bin', observed=True).agg({
                    'promedio_academico': 'mean',
                    'pc_total': 'mean'
                }).reset_index()
                
                x = np.arange(len(grouped))
                width = 0.35
                
                bars1 = ax1.bar(x - width/2, grouped['promedio_academico'], width, 
                               label='Promedio Académico', color='steelblue', alpha=0.8)
                bars2 = ax1.bar(x + width/2, grouped['pc_total'], width, 
                               label='Pensamiento Crítico', color='coral', alpha=0.8)
                
                ax1.set_xlabel('Horas de Estudio por Día', fontweight='bold')
                ax1.set_ylabel('Puntaje', fontweight='bold')
                ax1.set_title('Rendimiento y PC según Horas de Estudio', fontweight='bold', pad=10)
                ax1.set_xticks(x)
                ax1.set_xticklabels(grouped['horas_bin'])
                ax1.legend()
                ax1.grid(axis='y', alpha=0.3)
                
                # Añadir valores sobre las barras
                for bars in [bars1, bars2]:
                    for bar in bars:
                        height = bar.get_height()
                        ax1.text(bar.get_x() + bar.get_width()/2., height,
                                f'{height:.2f}',
                                ha='center', va='bottom', fontsize=8)
            else:
                ax1.text(0.5, 0.5, 'Datos no disponibles\n(horas_bin o promedio_academico)', 
                        ha='center', va='center', transform=ax1.transAxes)
            
            # GRÁFICO 2: Pastel - Métodos de Estudio
            ax2 = fig.add_subplot(2, 2, 2)
            if 'metodo_estudio' in self.df_limpio.columns:
                metodos = self.df_limpio['metodo_estudio'].value_counts()
                colors = plt.cm.Set3(np.linspace(0, 1, len(metodos)))
                wedges, texts, autotexts = ax2.pie(metodos.values, labels=metodos.index, 
                                                    autopct='%1.1f%%', startangle=90,
                                                    colors=colors)
                ax2.set_title('Distribución de Métodos de Estudio', fontweight='bold', pad=10)
                
                # Mejorar legibilidad
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
            else:
                ax2.text(0.5, 0.5, 'Datos no disponibles\n(metodo_estudio)', 
                        ha='center', va='center', transform=ax2.transAxes)
            
            # GRÁFICO 3: Líneas - Tendencia Promedio y PC por Horas
            ax3 = fig.add_subplot(2, 2, 3)
            if 'horas_bin' in self.df_limpio.columns and 'promedio_academico' in self.df_limpio.columns:
                grouped = self.df_limpio.groupby('horas_bin', observed=True).agg({
                    'promedio_academico': 'mean',
                    'pc_total': 'mean'
                }).reset_index()
                
                x = range(len(grouped))
                
                line1 = ax3.plot(x, grouped['promedio_academico'], marker='o', 
                               linewidth=2.5, markersize=10, label='Promedio Académico',
                               color='steelblue')
                line2 = ax3.plot(x, grouped['pc_total'], marker='s', 
                               linewidth=2.5, markersize=10, label='Pensamiento Crítico',
                               color='coral')
                
                ax3.set_xticks(x)
                ax3.set_xticklabels(grouped['horas_bin'])
                ax3.set_xlabel('Grupos de Horas de Estudio', fontweight='bold')
                ax3.set_ylabel('Puntaje Promedio', fontweight='bold')
                ax3.set_title('Tendencia: Rendimiento y PC vs Horas', fontweight='bold', pad=10)
                ax3.legend(loc='best')
                ax3.grid(True, alpha=0.3)
                
                # Añadir valores en los puntos
                for i, (prom, pc) in enumerate(zip(grouped['promedio_academico'], grouped['pc_total'])):
                    ax3.text(i, prom, f'{prom:.2f}', ha='center', va='bottom', fontsize=8)
                    ax3.text(i, pc, f'{pc:.2f}', ha='center', va='top', fontsize=8)
            else:
                ax3.text(0.5, 0.5, 'Datos no disponibles\n(horas_bin o promedio_academico)', 
                        ha='center', va='center', transform=ax3.transAxes)
            
            # GRÁFICO 4: Boxplot - Dispersión del Promedio por Método
            ax4 = fig.add_subplot(2, 2, 4)
            if 'metodo_estudio' in self.df_limpio.columns and 'promedio_academico' in self.df_limpio.columns:
                metodos_unicos = sorted(self.df_limpio['metodo_estudio'].unique())
                datos_box = [self.df_limpio[self.df_limpio['metodo_estudio'] == metodo]['promedio_academico'].dropna()
                            for metodo in metodos_unicos]
                
                bp = ax4.boxplot(datos_box, labels=metodos_unicos, patch_artist=True,
                               medianprops=dict(color='red', linewidth=2),
                               boxprops=dict(facecolor='lightblue', alpha=0.7))
                
                ax4.set_xlabel('Método de Estudio', fontweight='bold')
                ax4.set_ylabel('Promedio Académico', fontweight='bold')
                ax4.set_title('Dispersión del Rendimiento por Método', fontweight='bold', pad=10)
                ax4.tick_params(axis='x', rotation=15)
                ax4.grid(axis='y', alpha=0.3)
                
                # Añadir línea con promedio de PC por método
                if 'pc_total' in self.df_limpio.columns:
                    pc_medias = [self.df_limpio[self.df_limpio['metodo_estudio'] == metodo]['pc_total'].mean()
                                for metodo in metodos_unicos]
                    ax4_twin = ax4.twinx()
                    ax4_twin.plot(range(1, len(metodos_unicos)+1), pc_medias, 
                                 marker='D', color='coral', linewidth=2, markersize=8,
                                 label='PC Promedio')
                    ax4_twin.set_ylabel('Pensamiento Crítico Promedio', fontweight='bold', color='coral')
                    ax4_twin.tick_params(axis='y', labelcolor='coral')
                    ax4_twin.legend(loc='upper right')
            else:
                ax4.text(0.5, 0.5, 'Datos no disponibles\n(metodo_estudio o promedio_academico)', 
                        ha='center', va='center', transform=ax4.transAxes)
            
            fig.tight_layout()
            
            # Mostrar en el canvas
            canvas = FigureCanvasTkAgg(fig, master=self.graficos_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
            self.fig = fig  # Guardar referencia para exportar
            
            messagebox.showinfo("Éxito", "✓ Gráficos generados correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar gráficos:\n{str(e)}")
            
    def guardar_graficos(self):
        if not hasattr(self, 'fig'):
            messagebox.showwarning("Advertencia", "Primero genera los gráficos")
            return
            
        archivo = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            initialfile="dashboard_ia_pensamiento_critico.png"
        )
        
        if archivo:
            try:
                self.fig.savefig(archivo, dpi=300, bbox_inches='tight')
                messagebox.showinfo("Éxito", f"✓ Gráficos guardados en:\n{archivo}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar:\n{str(e)}")
                
    def exportar_csv(self):
        if self.df_limpio is None:
            messagebox.showwarning("Advertencia", "Primero limpia los datos")
            return
            
        archivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="datos_limpios_ia_pc.csv"
        )
        
        if archivo:
            try:
                self.df_limpio.to_csv(archivo, index=False, encoding='utf-8-sig')
                messagebox.showinfo("Éxito", f"✓ CSV limpio guardado en:\n{archivo}")
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
            
            reporte = "="*80 + "\n"
            reporte += "      REPORTE DE ANÁLISIS: HÁBITOS DE IA Y PENSAMIENTO CRÍTICO\n"
            reporte += "                    EN ESTUDIANTES UNIVERSITARIOS\n"
            reporte += "="*80 + "\n\n"
            
            reporte += f"📊 Total de estudiantes analizados: {len(self.df_limpio)}\n"
            reporte += f"📅 Fecha de generación: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            
            # SECCIÓN 1: ESTADÍSTICAS GENERALES
            reporte += "━"*80 + "\n"
            reporte += "1. ESTADÍSTICAS DESCRIPTIVAS GENERALES\n"
            reporte += "━"*80 + "\n\n"
            
            if 'promedio_academico' in self.df_limpio.columns:
                reporte += "📚 PROMEDIO ACADÉMICO [escala 1-3]:\n"
                reporte += f"   • Media:          {self.df_limpio['promedio_academico'].mean():.3f}\n"
                reporte += f"   • Mediana:        {self.df_limpio['promedio_academico'].median():.3f}\n"
                reporte += f"   • Desv. Est.:     {self.df_limpio['promedio_academico'].std():.3f}\n"
                reporte += f"   • Mínimo:         {self.df_limpio['promedio_academico'].min():.3f}\n"
                reporte += f"   • Máximo:         {self.df_limpio['promedio_academico'].max():.3f}\n\n"
            
            if 'horas_estudio_dia' in self.df_limpio.columns:
                reporte += "⏰ HORAS DE ESTUDIO DIARIAS:\n"
                reporte += f"   • Media:          {self.df_limpio['horas_estudio_dia'].mean():.2f} horas\n"
                reporte += f"   • Mediana:        {self.df_limpio['horas_estudio_dia'].median():.2f} horas\n"
                reporte += f"   • Desv. Est.:     {self.df_limpio['horas_estudio_dia'].std():.2f} horas\n"
                reporte += f"   • Mínimo:         {self.df_limpio['horas_estudio_dia'].min():.2f} horas\n"
                reporte += f"   • Máximo:         {self.df_limpio['horas_estudio_dia'].max():.2f} horas\n\n"
            
            # SECCIÓN 2: PENSAMIENTO CRÍTICO
            reporte += "━"*80 + "\n"
            reporte += "2. ANÁLISIS DE PENSAMIENTO CRÍTICO [Likert 1-5]\n"
            reporte += "━"*80 + "\n\n"
            
            pc_cols_disponibles = [col for col in self.pc_cols if col in self.df_limpio.columns]
            
            if pc_cols_disponibles:
                reporte += "🧠 DIMENSIONES DEL PENSAMIENTO CRÍTICO:\n\n"
                for col in pc_cols_disponibles:
                    nombre = col.replace('pc_', '').replace('_', ' ').title()
                    media = self.df_limpio[col].mean()
                    reporte += f"   • {nombre:20s}: {media:.3f}\n"
                
                if 'pc_total' in self.df_limpio.columns:
                    reporte += f"\n   ► PC TOTAL (Índice Global): {self.df_limpio['pc_total'].mean():.3f}\n"
                    reporte += f"     Desv. Est.: {self.df_limpio['pc_total'].std():.3f}\n\n"
            
            # SECCIÓN 3: DISTRIBUCIONES
            reporte += "━"*80 + "\n"
            reporte += "3. DISTRIBUCIÓN POR CATEGORÍAS\n"
            reporte += "━"*80 + "\n\n"
            
            if 'metodo_estudio' in self.df_limpio.columns:
                reporte += "📖 MÉTODOS DE ESTUDIO:\n"
                for metodo, count in self.df_limpio['metodo_estudio'].value_counts().items():
                    pct = (count / len(self.df_limpio)) * 100
                    reporte += f"   • {metodo:15s}: {count:4d} estudiantes ({pct:5.1f}%)\n"
                reporte += "\n"
            
            if 'ia_frecuencia' in self.df_limpio.columns:
                reporte += "🤖 FRECUENCIA DE USO DE IA:\n"
                for freq, count in self.df_limpio['ia_frecuencia'].value_counts().items():
                    pct = (count / len(self.df_limpio)) * 100
                    reporte += f"   • {freq:15s}: {count:4d} estudiantes ({pct:5.1f}%)\n"
                reporte += "\n"
            
            if 'horas_bin' in self.df_limpio.columns:
                reporte += "⏱️  DISTRIBUCIÓN POR HORAS DE ESTUDIO:\n"
                for grupo, count in self.df_limpio['horas_bin'].value_counts().sort_index().items():
                    pct = (count / len(self.df_limpio)) * 100
                    reporte += f"   • {grupo:10s}: {count:4d} estudiantes ({pct:5.1f}%)\n"
                reporte += "\n"
            
            # SECCIÓN 4: RELACIONES CLAVE
            reporte += "━"*80 + "\n"
            reporte += "4. ANÁLISIS DE RELACIONES: IA ↔ PENSAMIENTO CRÍTICO ↔ RENDIMIENTO\n"
            reporte += "━"*80 + "\n\n"
            
            # Tabla: Promedio académico y PC por frecuencia de IA
            if 'ia_frecuencia' in self.df_limpio.columns and 'promedio_academico' in self.df_limpio.columns:
                reporte += "📊 RENDIMIENTO Y PC SEGÚN FRECUENCIA DE USO DE IA:\n\n"
                reporte += f"   {'Frecuencia IA':<15} {'N':<6} {'Prom.Acad.':<12} {'PC Total':<10}\n"
                reporte += f"   {'-'*15} {'-'*6} {'-'*12} {'-'*10}\n"
                
                grouped_ia = self.df_limpio.groupby('ia_frecuencia').agg({
                    'promedio_academico': 'mean',
                    'pc_total': 'mean',
                    'id_est': 'count' if 'id_est' in self.df_limpio.columns else lambda x: len(x)
                }).reset_index()
                
                for _, row in grouped_ia.iterrows():
                    freq = row['ia_frecuencia'][:15]
                    n = int(row.get('id_est', 0)) if 'id_est' in row else len(self.df_limpio[self.df_limpio['ia_frecuencia']==row['ia_frecuencia']])
                    prom = row['promedio_academico']
                    pc = row['pc_total']
                    reporte += f"   {freq:<15} {n:<6d} {prom:<12.3f} {pc:<10.3f}\n"
                reporte += "\n"
            
            # Tabla: Promedio académico y PC por método de estudio
            if 'metodo_estudio' in self.df_limpio.columns and 'promedio_academico' in self.df_limpio.columns:
                reporte += "📚 RENDIMIENTO Y PC SEGÚN MÉTODO DE ESTUDIO:\n\n"
                reporte += f"   {'Método':<15} {'N':<6} {'Prom.Acad.':<12} {'PC Total':<10}\n"
                reporte += f"   {'-'*15} {'-'*6} {'-'*12} {'-'*10}\n"
                
                grouped_met = self.df_limpio.groupby('metodo_estudio').agg({
                    'promedio_academico': 'mean',
                    'pc_total': 'mean',
                    'id_est': 'count' if 'id_est' in self.df_limpio.columns else lambda x: len(x)
                }).reset_index()
                
                for _, row in grouped_met.iterrows():
                    met = row['metodo_estudio'][:15]
                    n = int(row.get('id_est', 0)) if 'id_est' in row else len(self.df_limpio[self.df_limpio['metodo_estudio']==row['metodo_estudio']])
                    prom = row['promedio_academico']
                    pc = row['pc_total']
                    reporte += f"   {met:<15} {n:<6d} {prom:<12.3f} {pc:<10.3f}\n"
                reporte += "\n"
            
            # Tabla: Promedio académico y PC por grupos de horas
            if 'horas_bin' in self.df_limpio.columns and 'promedio_academico' in self.df_limpio.columns:
                reporte += "⏰ RENDIMIENTO Y PC SEGÚN HORAS DE ESTUDIO:\n\n"
                reporte += f"   {'Horas/día':<15} {'N':<6} {'Prom.Acad.':<12} {'PC Total':<10}\n"
                reporte += f"   {'-'*15} {'-'*6} {'-'*12} {'-'*10}\n"
                
                grouped_horas = self.df_limpio.groupby('horas_bin', observed=True).agg({
                    'promedio_academico': 'mean',
                    'pc_total': 'mean',
                    'id_est': 'count' if 'id_est' in self.df_limpio.columns else lambda x: len(x)
                }).reset_index()
                
                for _, row in grouped_horas.iterrows():
                    horas = str(row['horas_bin'])[:15]
                    n = int(row.get('id_est', 0)) if 'id_est' in row else len(self.df_limpio[self.df_limpio['horas_bin']==row['horas_bin']])
                    prom = row['promedio_academico']
                    pc = row['pc_total']
                    reporte += f"   {horas:<15} {n:<6d} {prom:<12.3f} {pc:<10.3f}\n"
                reporte += "\n"
            
            # SECCIÓN 5: CORRELACIONES
            reporte += "━"*80 + "\n"
            reporte += "5. ANÁLISIS DE CORRELACIONES\n"
            reporte += "━"*80 + "\n\n"
            
            reporte += "🔗 CORRELACIONES DE PEARSON:\n\n"
            
            if all(col in self.df_limpio.columns for col in ['horas_estudio_dia', 'promedio_academico']):
                corr = self.df_limpio['horas_estudio_dia'].corr(self.df_limpio['promedio_academico'])
                reporte += f"   • Horas de Estudio ↔ Promedio Académico:     {corr:>7.3f}\n"
            
            if all(col in self.df_limpio.columns for col in ['pc_total', 'promedio_academico']):
                corr = self.df_limpio['pc_total'].corr(self.df_limpio['promedio_academico'])
                reporte += f"   • Pensamiento Crítico ↔ Promedio Académico:  {corr:>7.3f}\n"
            
            if all(col in self.df_limpio.columns for col in ['pc_total', 'horas_estudio_dia']):
                corr = self.df_limpio['pc_total'].corr(self.df_limpio['horas_estudio_dia'])
                reporte += f"   • Pensamiento Crítico ↔ Horas de Estudio:    {corr:>7.3f}\n"
            
            reporte += "\n"
            
            # SECCIÓN 6: INSIGHTS Y RECOMENDACIONES
            reporte += "━"*80 + "\n"
            reporte += "6. INSIGHTS Y RECOMENDACIONES\n"
            reporte += "━"*80 + "\n\n"
            
            reporte += "💡 HALLAZGOS CLAVE:\n\n"
            
            # Analizar relación horas-rendimiento
            if 'horas_bin' in self.df_limpio.columns and 'promedio_academico' in self.df_limpio.columns:
                grouped = self.df_limpio.groupby('horas_bin', observed=True)['promedio_academico'].mean()
                if len(grouped) >= 2:
                    if grouped.iloc[-1] > grouped.iloc[0]:
                        reporte += "   ✓ Tendencia positiva: Más horas de estudio se asocian con mejor\n"
                        reporte += "     rendimiento académico.\n\n"
                    else:
                        reporte += "   ⚠ Considerar: No se observa relación directa entre más horas y\n"
                        reporte += "     mejor rendimiento. La calidad del estudio puede ser más importante.\n\n"
            
            # Analizar PC y rendimiento
            if all(col in self.df_limpio.columns for col in ['pc_total', 'promedio_academico']):
                corr = self.df_limpio['pc_total'].corr(self.df_limpio['promedio_academico'])
                if corr > 0.3:
                    reporte += "   ✓ Correlación positiva entre pensamiento crítico y rendimiento:\n"
                    reporte += "     Fomentar PC puede mejorar el desempeño académico.\n\n"
                elif corr < -0.1:
                    reporte += "   ⚠ Correlación negativa detectada: Requiere investigación adicional.\n\n"
            
            # Analizar uso de IA
            if 'ia_frecuencia' in self.df_limpio.columns:
                usuarios_ia = self.df_limpio[self.df_limpio['ia_frecuencia'].isin(['DIARIO', 'SEMANAL'])].shape[0]
                pct_usuarios = (usuarios_ia / len(self.df_limpio)) * 100
                reporte += f"   📈 {pct_usuarios:.1f}% de estudiantes usan IA semanal o diariamente.\n"
                if pct_usuarios > 50:
                    reporte += "     Recomendación: Implementar guías de uso responsable de IA.\n\n"
            
            reporte += "\n📋 RECOMENDACIONES PEDAGÓGICAS:\n\n"
            reporte += "   1. Promover el uso crítico de IA como herramienta de apoyo, no sustitución.\n"
            reporte += "   2. Integrar ejercicios que desarrollen las dimensiones del pensamiento crítico.\n"
            reporte += "   3. Fomentar la verificación y contraste de información generada por IA.\n"
            reporte += "   4. Diseñar actividades que equilibren autonomía y uso tecnológico.\n"
            reporte += "   5. Monitorear continuamente la relación IA-PC-Rendimiento.\n\n"
            
            reporte += "="*80 + "\n"
            reporte += "                              FIN DEL REPORTE\n"
            reporte += "="*80 + "\n"
            
            self.txt_reporte.insert(tk.END, reporte)
            
            messagebox.showinfo("Éxito", 
                "✓ Reporte completo generado exitosamente.\n\n" +
                "Incluye estadísticas, tablas relacionales y recomendaciones.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte:\n{str(e)}")

# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = IAAnalisisApp(root)
    root.mainloop()
