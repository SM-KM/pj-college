from logging import setLoggerClass
import matplotlib.pyplot as plt
from numpy import broadcast_arrays
import pandas as pd
from pandas.core.api import isnull


default_suboptions = ["Ver estadísticas", "Generar reporte", "Ver gráfica"]

# load all tnme data
def load_data(rows): 
    return pd.read_csv('crime_data.csv', nrows=rows)

def change_loaded_rows():    
    input_text = "Cantidad de valores: "

    rows = input(input_text)
    while not(rows.isdigit()):
        print("La cantidad de columnas debe ser un numero, ej: 1,20,65")
        rows = input(input_text)

    return load_data(int(rows))

def check_category_definition(category, data):
    if not(category in data.columns):
        raise Exception("The category wasnt found on the data")

# Functions for each function 
def view_statistics(label, category):
    data = change_loaded_rows()
    check_category_definition(category, data)
    
    print("Mostrando estadísticas...")

def generate_report(label, category): 
    data = change_loaded_rows() 
    check_category_definition(category, data)

    print("Generando reporte...")


def view_graph(label, category):
    data = change_loaded_rows() 
    check_category_definition(category, data)

    print("Mostrando gráfica...")

    counts = data[category].value_counts()
    counts.plot(kind='bar', color='blue')
    plt.title(f"Número de Crímenes por {label}")
    plt.xlabel(label)
    plt.ylabel("Número de Casos")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def print_generic_menu_options(options, label):
    print(f"\n--- {label} ---")
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")

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
            for i, option in enumerate(data["suboptions"], start=len(options) + 1):
                print(f"{i}. {option[0]}")
            
            print(f"{len(options) + len(data["suboptions"]) + 1}. Regresar al menú anterior") 

        else:
            print(f"{len(options) + 1}. Regresar al menú anterior") 
        selection = input("Selecciona una opción: ")
        
        # Check if the selection is valid
        if selection.isdigit() and 1 <= int(selection) <= len(options):
            # Execute the corresponding function for the selected option
            functions[int(selection) - 1]()
        elif int(selection) == int(len(options) + len(data["suboptions"]) + 1) or int(selection) == int(len(options) + 1):
            break
        else:
            if int(len(options) + 1) <= int(selection) <= len(options) + len(data["suboptions"]):
                currentSuboptionData = data["suboptions"][int(selection) - (len(options)+ 1)]
                currentSuboptionCategory = currentSuboptionData[1]
                currentSuboptionLabel = currentSuboptionData[0]

                sub_functions = [
                    lambda: view_statistics(currentSuboptionLabel, currentSuboptionCategory),
                    lambda: generate_report(currentSuboptionLabel, currentSuboptionCategory),
                    lambda: view_graph(currentSuboptionLabel, currentSuboptionCategory)
                ]
                generic_menu(data, default_suboptions, sub_functions, currentSuboptionData[0], False)
            else:
                print("Opción no válida.")

# Main menu function
def main_menu():
    """
    Displays the main menu and allows the user to select different categories
    related to crime classification. Each selection opens a specific submenu
    for further actions.
    """
    default_rows = 120
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
        "category": "Modality",
        "rows": default_rows,
    },
    {
        "label": "Clasificación por Modalidad del Crimen",
        "suboptions": [["Crimenes violentos", "crimenes_violentos"], ["Crimenes no violentos", "crimenes_no_violentos"]],
        "category": "Motivation",
        "rows": default_rows,
    },
    {
        "label": "Clasificación por Motivacion del Crimen",
        "suboptions": [["Crimenes por Motivacion Economica", "crimenes_motivacion_economica"], ["Crimenes por odio", "crimenes_odio"], ["Crimenes por Pasion o Venganza", "crimenes_pasion_venganza"]],
        "category": "Area",
        "rows": default_rows,
    },
    {
        "label": "Clasificación por Area Geografica",
        "suboptions": [["Crimenes urbanos", "crimenes_urbanos"], ["Crimenes rurales", "crimenes_rurales"]],
        "category": "Temporality",
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
    
    defaultRowsLimit = 1000;
    data = load_data(defaultRowsLimit)  # Load data once for the session
    while True:
        print("\n--- Menú Principal ---")
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option["label"]}")
        print(f"{len(options) + 1}. Salir")
        
        selection = input("Selecciona una opción: ")
        
        # Check if the selection is valid
        if selection.isdigit() and 1 <= int(selection) <= len(options):
            # Define sub-options for each submenua
            selected_option = options[int(selection) - 1]
            sub_functions = [
                lambda: view_statistics(selected_option, data),
                lambda: generate_report(selected_option, data),
                lambda: view_graph(selected_option, data)
            ]

            generic_menu(options[int(selection) - 1], default_suboptions, sub_functions, options[int(selection) - 1]["label"], True)
        elif selection == str(len(options) + 1):
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida.")

# Start the program
main_menu()
