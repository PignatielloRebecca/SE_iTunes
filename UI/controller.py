import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        try:
            durata=float(self._view.txt_durata.value)
        except ValueError:
            self._view.show_alert('inserisci una durata minima')

        self._model.build_graph(durata)
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f" numero nodi: {self._model.G.number_of_nodes()}"))
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f" numero archi: {self._model.G.number_of_edges()}"))

        self._view.page.update()

        mappa=self._model.load_map_nodi(durata)

        # popolo la dropdown
        for (c,v) in mappa.items():
            self._view.dd_album.options.append(ft.dropdown.Option(key=c, text=v.title))

        self._view.page.update()


        """
        
        try:
            min_durata=float(self._view.txt_durata.value) # prendo la durata minima
        except ValueError:
            self._view.show_alert("inserire una data valida")
            return
        # costruisco il grafo
        self._model._build_graph(min_durata)
        # pulisco la dropdown
        self._view.dd_album.options.clear()

        # popolo la dropdown
        lista_album=self._model._lista_album # prendo gli oggetti album
        for album in lista_album:
            self._view.dd_album.options.append(ft.dropdown.Option(key=str(album.id), text=album.title))

        self._view.update()
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(
            f"Grafo creato {self._model.G.number_of_nodes()} album, numero archi {self._model.G.number_of_edges()}"))

        self._view.update()
        # TODO
    """


    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""

        if self._view.dd_album.value is None:
            self._view.show_alert('inserire un album selezionato')
            return
        self._album_selezionato=int(self._view.dd_album.value)

    """
            if self._view.dd_album.value is None:
            self._view.show_alert("scegliere un album")
            return
        self._album_selezionato=int(self._view.dd_album.value) # metto un intero perche mi trova un id
        # TODO
    """

    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""

        lunghezza, durata = self._model.analisi_componente_connessa(self._album_selezionato)
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"lunghezza: {lunghezza} durata: {durata:.2f}"))
        self._view.page.update()
    """
        
        if self._album_selezionato is None:
            self._view.show_alert("scegliere un album")
            return

        dimensione, durata= self._model.analisi_componente(self._album_selezionato)
        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"dimensione componente: {dimensione}"))
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"durata totale: {durata:.2f} minuti"))
        self._view.update()


        # TODO
    """

    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        # TODO
        # controllo sull'album
        if self._view.dd_album.value is None:
            self._view.show_alert("scegliere un album")
            return
        dTot= float(self._view.txt_durata_totale.value)

        album_id=int(self._view.dd_album.value)

        # richiamo la ricorsione
        cammino, durata=self._model.set_album(album_id, dTot)

        # visualizzazione
        self._view.lista_visualizzazione_3.controls.clear()

        if len(cammino) == 0:
            self._view.lista_visualizzazione_3.controls.append(
                ft.Text("Nessun set di album trovato")
            )
        else:
            self._view.lista_visualizzazione_3.controls.append(
                ft.Text(f"Numero album: {len(cammino)}")
            )
            self._view.lista_visualizzazione_3.controls.append(
                ft.Text(f"Durata totale: {durata} minuti")
            )

            for a in cammino: # mi ricordo che come a ho degli oggetti album
                self._view.lista_visualizzazione_3.controls.append(
                    ft.Text(f"- {a.title} ({a.durata:.2f} min)")
                )

        self._view.update()



    # self._view.dd_album.options.clear()
    #liasta_album= self._model.lista_album
    # for a i lista_album # importare iterare per la droptdown
    # self._view.dd_album.opions.append(ft.Dropdown.Option(key=album.id, test=album.title))

