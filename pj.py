from unicodedata import category
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from colorama import Fore, Style, init

init(autoreset=True)

default_suboptions = ["Ver estadísticas", "Generar reporte", "Ver gráfica"]
default_rows = 120
exit_color = Fore.RED
separation_line_w = 100

# load all tnme data
def load_data(rows): 
    return pd.read_csv('crime_data.csv', nrows=rows)

def change_loaded_rows():    
    input_text = "Cantidad de valores: "

    rows = input(input_text)
    while not(rows.isdigit()) or int(rows) > int(default_rows):
        print(Fore.RED + f"La cantidad de valores es incorrecta o no es un numero, maximo de valores: {default_rows}")
        rows = input(input_text)

    return load_data(int(rows))

def check_category_definition(category, data):
    print(category)
    if not(category in data.columns):
        raise Exception("The category wasnt found on the data")

# Functions for each function 
def view_statistics(label, category):
    data = change_loaded_rows()
    check_category_definition(category, data)
    
    print(Fore.GREEN + "Mostrando estadísticas...")

    line(separation_line_w)

    # Check if the category can be treated as numeric
    try:
        # Attempt to convert to numeric to see if it works
        data[category] = data[category].replace(',', '', regex=True).astype(float)
        is_numeric = True
    except ValueError:
        # If conversion fails, it is categorical
        is_numeric = False

    if is_numeric:
        # Calculate statistics for numeric data
        count = data[category].count()
        mean = data[category].mean()
        median = data[category].median()
        min_value = data[category].min()
        max_value = data[category].max()

        # Display results for numeric data
        print(Fore.CYAN + f"\nEstadísticas para {label}:")
        print(Fore.YELLOW + f"Cantidad: {count}")
        print(Fore.YELLOW + f"Promedio: {mean:.2f}")
        print(Fore.YELLOW + f"Mediana: {median:.2f}")
        print(Fore.YELLOW + f"Valor mínimo: {min_value:.2f}")
        print(Fore.YELLOW + f"Valor máximo: {max_value:.2f}")
    else:
        frequency = data[category].value_counts()

        print(Fore.CYAN + f"\nFrecuencia de {label}:")
        print(Fore.YELLOW + frequency.to_string())

    line(separation_line_w)

def line(len):
    print("\n")
    print("─" * len)

def generate_report(label, category): 
    data = change_loaded_rows() 
    check_category_definition(category, data)
    print(Fore.GREEN + "Generando reporte...")


    line(separation_line_w)

    if data[category].dtype == 'object':
        try:
            data[category] = data[category].replace(',', '', regex=True).astype(float)
        except ValueError:
            # If conversion fails, keep the original data
            pass


    if data[category].dtype in ['int64', 'float64']:
        summary = data.groupby('area_geografica', as_index=False)[category].sum()
    else:
        summary = data.groupby('area_geografica', as_index=False)[category].first()

    print(f"Reporte de {label} por Área Geográfica")
    line(separation_line_w)
    print(summary.to_string(index=False))

    line(separation_line_w)


def view_graph(label, category):
    data = change_loaded_rows() 
    check_category_definition(category, data)

    charts = ["Line", "line", "Pie", "pie", "All", "all"]
    chooseChartPrompt = "Escoge el tipo de grafico [Line, Pie, All]: "

    if data[category].dtype == 'object':
        try:
            data[category] = data[category].replace(',', '', regex=True).astype(float)
        except ValueError:
            # If conversion fails, keep the original data
            pass


    if data[category].dtype in ['int64', 'float64']:
        summary = data.groupby('area_geografica', as_index=False)[category].sum()
    else:
        summary = data.groupby('area_geografica', as_index=False)[category].first()


    def lineChart():
        y_min = summary[category].min()
        y_max = summary[category].max()


        plt.figure(figsize=(12, 6))
        bars = plt.bar(summary['area_geografica'], summary[category], 
               color='royalblue', edgecolor='black', alpha=0.85)

        # Title and Labels
        plt.title(f"Data por Área Geográfica de {label}", fontsize=20, fontweight='bold', color='darkblue', pad=20)
        plt.xlabel("Área Geográfica", fontsize=14, fontweight='bold', color='dimgray')
        plt.ylabel(f"{label}", fontsize=14, fontweight='bold', color='dimgray')
        plt.xticks(rotation=45, ha='right') 
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, yval + 100, str(yval), 
                ha='center', va='bottom', fontsize=10, color='black')

        plt.gca().set_facecolor('whitesmoke')
        plt.tight_layout()
        plt.show()

    def pieChart():
        counts = data[category].value_counts()
        plt.figure(figsize=(8, 8))
        plt.pie(counts, autopct='%1.1f%%', startangle=140)
        plt.title(f"{label}", fontsize=16, fontweight='bold')
        plt.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.
        plt.show()

    typeChart = input(chooseChartPrompt).replace(" ", "")
    while not(typeChart in charts):
        print(exit_color + "Tipo de grafico no valido, intentalo de nuevo")
        typeChart = input(chooseChartPrompt).replace(" ", "")

    print(Fore.GREEN + "Mostrando gráfica...")
    lowerCaseTypeChart = typeChart.lower()

    if lowerCaseTypeChart == "line":
        # Line chart
        lineChart()
    
    if lowerCaseTypeChart == "pie":
        # Pie chart
        pieChart()

    if lowerCaseTypeChart == "all":
        lineChart()
        pieChart()
    

def print_box(title, content):
    title = f" {title} "
    border = "─" * (len(title) + 4)
    print(Fore.CYAN + border)
    print(Fore.CYAN + "│" + title + "│")
    print(Fore.CYAN + border)
    for line in content:
        print(Fore.YELLOW + "│ " + line.ljust(len(border) - 3) + " │")
    print(Fore.CYAN + border)

def print_generic_menu_options(options, label):
    print("\n")
    print_box(label, [f"{i}. {option}" for i, option in enumerate(options, start=1)])
    print("\n")

# Generic menu function
def generic_menu(data, options, functions, label, nested):
    """
    Displays a menu based on the given title and options.
    Executes the corresponding function when an option is selected.
    Allows the user to return to the main menu.
    """

    while True:
        print_generic_menu_options(options, label) 

        if nested:
            print(Fore.CYAN + "Subopciones:")
            for i, option in enumerate(data["suboptions"], start=len(options) + 1):
                print(Fore.YELLOW + f"{i}. {option[0]}")
            
            print(exit_color + f"{len(options) + len(data["suboptions"]) + 1}. Regresar al menú anterior") 

        else:
            print(exit_color + f"{len(options) + 1}. Regresar al menú anterior")

        
        print("\n")
        selection = input("Selecciona una opción: ")
        
        # Check if the selection is valid
        if selection.isdigit():
            selection = int(selection)
            if 1 <= selection <= len(options):
                functions[selection - 1]()
            elif nested and len(options) + 1 <= selection <= len(options) + len(data["suboptions"]):
                currentSuboptionData = data["suboptions"][selection - (len(options) + 1)]
                currentSuboptionCategory = currentSuboptionData[1]
                currentSuboptionLabel = currentSuboptionData[0]

                sub_functions = [
                    lambda: view_statistics(currentSuboptionLabel, currentSuboptionCategory),
                    lambda: generate_report(currentSuboptionLabel, currentSuboptionCategory),
                    lambda: view_graph(currentSuboptionLabel, currentSuboptionCategory)
                ]
                generic_menu(data, default_suboptions, sub_functions, currentSuboptionData[0], False)
            elif selection == len(options) + len(data["suboptions"]) + 1:
                break
            else:
                break
        else:
            print("Opción no válida, intentalo de nuevo")
# Main menu function
def main_menu():
    """
    Displays the main menu and allows the user to select different categories
    related to crime classification. Each selection opens a specific submenu
    for further actions.
    """
    options = [
    {
        "label": "Clasificación por Naturaleza del Crimen",
        "category": "tasa",
        "suboptions": [["Crimenes contra las personas", "crimenes_contra_las_personas"], ["Crimenes contra la propiedad", "crimenes_contra_la_propiedad"], ["Crimenes sexuales", "crimenes_sexuales"], ["Crimenes economicos", "crimenes_economicos"]],
        "rows": default_rows,
    },
    {
        "label": "Clasificación por Gravedad del Crimen",
        "suboptions": [["Crimenes graves", "crimenes_graves"], ["Crimenes menores", "crimenes_menores"]],
        "category": "gravedad",
        "rows": default_rows,
    },
    {
        "label": "Clasificación por Modalidad del Crimen",
        "suboptions": [["Crimenes violentos", "crimenes_violentos"], ["Crimenes no violentos", "crimenes_no_violentos"]],
        "category": "modalidad",
        "rows": default_rows,
    },
    {
        "label": "Clasificación por Motivacion del Crimen",
        "suboptions": [["Crimenes por Motivacion Economica", "crimenes_motivacion_economica"], ["Crimenes por odio", "crimenes_odio"], ["Crimenes por Pasion o Venganza", "crimenes_pasion_venganza"]],
        "category": "motivacion",
        "rows": default_rows,
    },
    {
        "label": "Clasificación por Area Geografica",
        "suboptions": [["Crimenes urbanos", "crimenes_urbanos"], ["Crimenes rurales", "crimenes_rurales"]],
        "category": "area_geografica",
        "rows": default_rows,
    },
    {
        "label": "Clasificación por Temporalidad",
        "suboptions": [["Crimenes por Periodo del Año", "crimenes_periodo_anual"], ["Crimenes por Hora del Dia", "crimenes_hora_dia"]],
        "category": "Technological_Involvement",
        "rows": default_rows,
    },
    {
        "label": "Clasificación por Involucramiento tecnologico",
        "suboptions": [["Cybercrimenes", "cybercrimenes"], ["Crimenes Tradicionales", "crimenes_tradicionales"]],
        "category": "Case_Status",
        "rows": default_rows,
    },  
    {
        "label": "Clasificación por Estado del Caso",
        "suboptions": [["Casos resueltos", "casos_resueltos"], ["Casos no resueltos", "casos_no_resueltos"]],
        "category": "Case_Status",
        "rows": default_rows,
    },  
    ]
    
    data = load_data(default_rows)  # Load data once for the session
    while True:
        print(Fore.CYAN + "\n--- Menú Principal ---")
        for i, option in enumerate(options, start=1):
            print(Fore.WHITE + f"{i}. {option['label']}")
        print(Fore.WHITE + f"{len(options) + 1}. Salir")
        selection = input("Selecciona una opción: ")
        
        # Check if the selection is valid
        if selection.isdigit() and 1 <= int(selection) <= len(options):

            # Define sub-options for each submenua
            selected_option = options[int(selection) - 1]
            currentCategory = selected_option["category"]
            currentLabel = selected_option["label"]

            sub_functions = [
                lambda: view_statistics(currentLabel, currentCategory),
                lambda: generate_report(currentLabel, currentCategory),
                lambda: view_graph(currentLabel, currentCategory)
            ]

            generic_menu(options[int(selection) - 1], default_suboptions, sub_functions, options[int(selection) - 1]["label"], True)
        elif selection == str(len(options) + 1):
            print(Fore.GREEN + "Saliendo del programa...")
            break
        else:
            print(Fore.RED + "Opción no válida.")

# Start the program
main_menu()
