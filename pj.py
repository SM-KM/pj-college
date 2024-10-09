import matplotlib.pyplot as plt
import pandas as pd

# load all the data
def load_data(rows): 
    return pd.read_csv('crime_data.csv', nrows=rows)

# Functions for each function 
def view_statistics(option, data):
    print("Mostrando estadísticas...")

def generate_report(option, data): 
    print("Generando reporte...")

def view_graph(option, data):
    rows = int(input("Cantidad de valores: "))
    data = load_data(rows)

    print("Mostrando gráfica...")

    counts = data[option['category']].value_counts()
    counts.plot(kind='bar', color='blue')
    plt.title(f"Número de Crímenes por {option['label']}")
    plt.xlabel(option['label'])
    plt.ylabel("Número de Casos")
    plt.xticks(rotation=45)
    #plt.tight_layout()
    plt.show()

# Generic menu function
def generic_menu(title, options, functions):
    """
    Displays a menu based on the given title and options.
    Executes the corresponding function when an option is selected.
    Allows the user to return to the main menu.
    """
    while True:
        print(f"\n--- {title["label"]} ---")
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")
        print(f"{len(options) + 1}. Regresar al menú principal")
        
        selection = input("Selecciona una opción: ")
        
        # Check if the selection is valid
        if selection.isdigit() and 1 <= int(selection) <= len(options):
            # Execute the corresponding function for the selected option
            functions[int(selection) - 1]()
        elif selection == str(len(options) + 1):
            break  # Exit the submenu and return to the main menu
        else:
            print("Opción no válida.")

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
        "rows": 10,
    },
    {
        "label": "Clasificación por Modalidad del Crimen",
        "category": "Modality",
    },
    {
        "label": "Clasificación por Motivación del Crimen",
        "category": "Motivation",
    },
    {
        "label": "Clasificación por Área Geográfica",
        "category": "Area",
    },
    {
        "label": "Clasificación por Temporalidad",
        "category": "Temporality",
    },
    {
        "label": "Clasificación por Involucramiento Tecnológico",
        "category": "Technological_Involvement",
    },
    {
        "label": "Clasificación por Estado del caso",
        "category": "Case_Status",
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
            sub_options = ["Ver estadísticas", "Generar reporte", "Ver gráfica"]
            sub_functions = [
                lambda option=selected_option: view_statistics(selected_option, data),
                lambda option=selected_option: generate_report(selected_option, data),
                lambda option=selected_option: view_graph(selected_option, data)
            ]

            generic_menu(options[int(selection) - 1], sub_options, sub_functions)
        elif selection == str(len(options) + 1):
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida.")

# Start the program
main_menu()
