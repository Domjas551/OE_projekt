import sys
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QTextEdit
)
from Genetic import Genetic

class GeneticUI(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Algorytm Genetyczny")
        self.setGeometry(100, 100, 500, 600)

        layout = QVBoxLayout()

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
        self.results = []  # Lista przechowująca wyniki

    def run_algorithm(self):
        """ Pobranie danych z UI, uruchomienie algorytmu i wyświetlenie wyników """
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

        # Uruchomienie algorytmu genetycznego
        g = Genetic(population_size, chromosom_size, min_range, max_range, epochs)
        g.adapt(type_s, type_c, type_m, chance_c, chance_m, chance_in)

        # Znalezienie najlepszego rozwiązania
        best_solution = min(g.population, key=g.fitness_function)

        # Lista wyników
        self.results = [g.fitness_function(ind) for ind in g.population]
        result_text = (
            f"Wyniki fitness dla populacji: \n{self.results}\n\n"
            f"Najlepszy chromosom: {best_solution.chromosom_value}\n"
            f"Jego wartość fitness: {g.fitness_function(best_solution)}"
        )

        self.result_text.setText(result_text)

        # Aktywacja przycisków po wygenerowaniu wyników
        self.save_button.setEnabled(True)
        self.plot_button.setEnabled(True)

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


app = QApplication(sys.argv)
window = GeneticUI()
window.show()
sys.exit(app.exec())
