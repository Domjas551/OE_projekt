import sys
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QApplication
from PyQt6.QtWidgets import QComboBox

from Genetic import Genetic, Genetic2


class GeneticUI(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Algorytm Genetyczny")
        self.setGeometry(100, 100, 500, 600)

        layout = QVBoxLayout()

        self.project_selector = QComboBox()
        self.project_selector.addItems(["Projekt 1", "Projekt 2"])

        self.project_selector.currentIndexChanged.connect(self.update_algorithm_labels)

        layout.addWidget(QLabel("Wybierz Projekt"))
        layout.addWidget(self.project_selector)

        # Pola do wpisania parametrów
        self.inputs = {}
        params = [
            ("Population Size", "20"),
            ("Chromosom Size", "20"),
            ("Min Range", "-5.12"),
            ("Max Range", "5.12"),
            ("Epochs", "2"),
            ("Selection Type (1-Best, 2-Roulette, 3-Tournament)", "3"),
            ("Crossover Type (1-Point, 2-Two Points, 3-Uniform, 4-Grainy)", "4"),
            ("Mutation Type (1-Edge, 2-One Point, 3-Two Points)", "3"),
            ("Crossover Chance", "70"),
            ("Mutation Chance", "20"),
            ("Inversion Chance", "10")
        ]

        for label_text, default_value in params:
            label = QLabel(label_text)
            line_edit = QLineEdit(default_value)
            self.inputs[label_text] = line_edit
            layout.addWidget(label)
            layout.addWidget(line_edit)

        # Przycisk do uruchomienia algorytmu
        self.run_button = QPushButton("Uruchom Algorytm")
        self.run_button.clicked.connect(self.run_algorithm)
        layout.addWidget(self.run_button)

        # Przycisk do zapisu wyników do pliku
        self.save_button = QPushButton("Zapisz do pliku")
        self.save_button.clicked.connect(self.save_results)
        self.save_button.setEnabled(False)  # Domyślnie wyłączony
        layout.addWidget(self.save_button)

        # Przycisk do wyświetlania wykresu
        self.plot_button = QPushButton("Wyświetl wykres")
        self.plot_button.clicked.connect(self.plot_results)
        self.plot_button.setEnabled(False)
        layout.addWidget(self.plot_button)

        # Pole na wyniki
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

        self.setLayout(layout)
        self.results = [] 

    def update_algorithm_labels(self):
        index = self.project_selector.currentIndex()

        mutation_field = self.inputs["Mutation Type (1-Edge, 2-One Point, 3-Two Points)"]
        crossover_field = self.inputs["Crossover Type (1-Point, 2-Two Points, 3-Uniform, 4-Grainy)"]
        
        mutation_label = None
        crossover_label = None

        for widget in self.findChildren(QLabel):
            if widget.text().startswith("Mutation Type"):
                mutation_label = widget
            elif widget.text().startswith("Crossover Type"):
                crossover_label = widget

        if index == 0:
            mutation_field.setText("3")
            crossover_field.setText("4")
            if mutation_label:
                mutation_label.setText("Mutation Type (1 - Edge, 2 - One Point, 3 - Two Points)")
            if crossover_label:
                crossover_label.setText("Crossover Type (1 - Single Point, 2 - Two Points, 3 - Uniform, 4 - Grainy)")
        else:
            # Project 2: Real-coded genetic algorithm
            mutation_field.setText("1")
            crossover_field.setText("1")
            if mutation_label:
                mutation_label.setText("Mutation Type (1 - Uniform, 2 - Gaussian)")
            if crossover_label:
                crossover_label.setText("Crossover Type (1 - Arithmetic, 2 - Alpha Blend, 3 - Alpha-Beta Blend, 4 - Averaging)")


    def run_algorithm(self):
        try:
            # Pobieranie danych z UI
            project = self.project_selector.currentIndex()
            population_size = int(self.inputs["Population Size"].text())
            chromosom_size = int(self.inputs["Chromosom Size"].text())
            min_range = float(self.inputs["Min Range"].text())
            max_range = float(self.inputs["Max Range"].text())
            epochs = int(self.inputs["Epochs"].text())
            type_s = int(self.inputs["Selection Type (1-Best, 2-Roulette, 3-Tournament)"].text())
            type_c = int(self.inputs["Crossover Type (1-Point, 2-Two Points, 3-Uniform, 4-Grainy)"].text())
            type_m = int(self.inputs["Mutation Type (1-Edge, 2-One Point, 3-Two Points)"].text())
            chance_c = int(self.inputs["Crossover Chance"].text())
            chance_m = int(self.inputs["Mutation Chance"].text())
            chance_in = int(self.inputs["Inversion Chance"].text())

            # Uruchomienie odpowiedniego algorytmu
            if project == 0:
                g = Genetic(population_size, chromosom_size, min_range, max_range, epochs)
            else:
                g = Genetic2(population_size, chromosom_size, min_range, max_range, epochs)

            g.adapt(type_s, type_c, type_m, chance_c, chance_m, chance_in)

            best_solution = min(g.population, key=g.fitness_function)

            self.results = [g.fitness_function(ind) for ind in g.population]
            
            if hasattr(best_solution, "chromosom_value"):
                chromo_value = best_solution.chromosom_value
            elif hasattr(best_solution, "chromosom_values"):
                    chromo_value = best_solution.chromosom_values
            else:
                    chromo_value = str(best_solution)

            result_text = (
                f"Wyniki fitness dla populacji: \n{self.results}\n\n"
                f"Najlepszy chromosom: {chromo_value}\n"
                f"Jego wartość fitness: {g.fitness_function(best_solution)}"
                )

            self.result_text.setText(result_text)

            self.save_button.setEnabled(True)
            self.plot_button.setEnabled(True)

        except Exception as e:
            # If any error occurs, show it in the QTextEdit instead of crashing
            self.result_text.setText(f"ERROR: {str(e)}")


    def save_results(self):
      """ Zapisuje wyniki do pliku, dodając je do istniejących danych """
      # Pobranie parametrów z UI
      population_size = int(self.inputs["Population Size"].text())
      chromosom_size = int(self.inputs["Chromosom Size"].text())
      min_range = float(self.inputs["Min Range"].text())
      max_range = float(self.inputs["Max Range"].text())
      epochs = int(self.inputs["Epochs"].text())
      type_s = int(self.inputs["Selection Type (1-Best, 2-Roulette, 3-Tournament)"].text())
      type_c = int(self.inputs["Crossover Type (1-Point, 2-Two Points, 3-Uniform, 4-Grainy)"].text())
      type_m = int(self.inputs["Mutation Type (1-Edge, 2-One Point, 3-Two Points)"].text())
      chance_c = int(self.inputs["Crossover Chance"].text())
      chance_m = int(self.inputs["Mutation Chance"].text())
      chance_in = int(self.inputs["Inversion Chance"].text())

      # Zapis do pliku
      with open("wyniki_genetyczne.txt", "a") as file:
          file.write("---- Wyniki dla parametrów ----\n")
          file.write(f"Rozmiar populacji: {population_size}\n")
          file.write(f"Rozmiar chromosomu: {chromosom_size}\n")
          file.write(f"Zakres: ({min_range}, {max_range})\n")
          file.write(f"Liczba epok: {epochs}\n")
          file.write(f"Typ selekcji: {type_s}\n")
          file.write(f"Typ krzyżowania: {type_c}\n")
          file.write(f"Typ mutacji: {type_m}\n")
          file.write(f"Szansa na krzyżowanie: {chance_c}%\n")
          file.write(f"Szansa na mutację: {chance_m}%\n")
          file.write(f"Szansa na inwersję: {chance_in}%\n\n")

          file.write("Wyniki fitness dla populacji:\n")
          file.write(", ".join(map(str, self.results)) + "\n\n")
          file.write("Najlepszy wynik fitness: " + str(min(self.results)) + "\n\n")

      self.result_text.append("\nWyniki zapisane do 'wyniki_genetyczne.txt' wraz z parametrami")

    def plot_results(self):
        """ Rysuje wykres wyników fitness """
        if not self.results:
            return

        plt.figure(figsize=(10, 5))
        plt.plot(self.results, marker="o", linestyle="-", color="b", label="Fitness")
        plt.xlabel("Indeks osobnika")
        plt.ylabel("Wartość funkcji przystosowania")
        plt.title("Wykres fitness dla populacji")
        plt.legend()
        plt.grid()
        plt.show()

"""
app = QApplication(sys.argv)
window = GeneticUI()
window.show()
sys.exit(app.exec())
"""

