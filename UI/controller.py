import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDsRating(self):
        voti = self._model.getAllVoti()

        for y in voti:
            self._view._ddrating1.options.append(ft.dropdown.Option(y))
            self._view._ddrating2.options.append(ft.dropdown.Option(y))


        self._view.update_page()


    def handleCreaGrafo(self, e):
        if self._view._ddrating1.value is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare il primo voto"))
            self._view.update_page()
            return
        if self._view._ddrating2.value is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare il secondo voto"))
            self._view.update_page()
            return

        self._model.buildGraph(self._view._ddrating1.value, self._view._ddrating2.value)

        Nnodes, Nedges = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato: "))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {Nnodes}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {Nedges}"))


        top5 = self._model.getTop3Archi()
        self._view.txt_result.controls.append(ft.Text(f"Top 5 archi:"))
        for arco in top5:
            self._view.txt_result.controls.append(ft.Text(f"{arco[0]} -> {arco[1]} : {arco[2]["weight"]}"))


        numero, largest, dettagli = self._model.getComponentiConnesse()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene {numero} componenti connesse."))
        self._view.txt_result.controls.append(
            ft.Text(f"la componente connessa maggiore ha dimensione pari a {len(largest)}."))

        for l in largest:
            self._view.txt_result.controls.append(ft.Text(l))  # STAMPIANO TUTTI GLI ELEMENTI DI LARGEST SENZA ORDINARLI


        self._view.update_page()
    def handleCammino(self, e):
        pass