import networkx as nx
from database.dao import DAO
from copy import copy

class Model:

    def __init__(self):
        self._lista_nodi=[]

        self._lista_playlist=[]
        self.G=nx.Graph() # creo un grafo

    def _getAllAlbums(self, durata):
        self._lista_album=DAO.read_all_album(durata)  # mi ritorna una lista di oggetti album
        for album in self._lista_album:
            self._lista_nodi.append(album.id)
        return self._lista_nodi

    def _build_graph(self, durata):
        # popolo la lista titoli
        # se aggiungo nodi come id, dovrò usare gli id anche per gli archi
        self._lista_nodi=self._getAllAlbums(durata)

        # costruisco i nodi
        self.G.add_nodes_from(self._lista_nodi)

        # costruisco gli archi
        self._lista_playlist=DAO.read_all_connessioni(durata)

        self.G.add_edges_from(self._lista_playlist)

        return self.G

    # calcolo la componente connessa
    def analisi_componente(self, album_id):

        componente=nx.node_connected_component(self.G, album_id) # mi ritorna una lista di id

        album_map={}
        for a in self._lista_album:
            album_map[a.id]=a # in questo modo dall'id arrivo direttamente all'oggetto per ottenere la durata

        # calcolo dimensione e durata totale
        dimensione=len(componente)

        durata=0

        for a_id in componente:  # mi prendo tutti gli id
            durata+=album_map[a_id].durata # prendo l'oggetto con quella durata

        return dimensione, durata


    # self.G.add_nodes_from()  --> costruisco i nodi
    # self.G.add_edges_from()--> costruisco i gli archi
    # self.G.get_number_of_nodes() --> restituisce  il numero dei nodi
    # self.G.get_numer_of_edges--> restituisce il numero degli archi

    # node_connected_components (analizza le componenti a partire da un grafo)

    # connected_components (analizza tutte le componenti connesse)

    # ricorsione
    def set_album(self, durata, album_id):

        self._best_album = [] # è una lista
        self._best_durata = 0


        componenti = nx.node_connected_component(self.G, album_id)

        album_map_filtrati = {}
        for a in self._lista_album:
            if a.id in componenti: # verifico che l'id si trova in componenti
                album_map_filtrati[a.id] =a

        lista_album = list(album_map_filtrati.values()) # mi creo una lista degli album filtrati

        a1 = album_map_filtrati[album_id]  # devo anche tenere traccia del primo album

        self.__ricorsione(lista_album, durata, [a1], a1.durata)  # lista album  e

    def __ricorsione(self,lista_album, dTot, parziale, durata_corrente):

        # condizione i terminazione

        if durata_corrente > dTot:
            return
        if len(parziale)> len(self._best_album):
            self._best_album=parziale.copy()
            self._best_durata=durata_corrente
            # esploro tutte le possibili opzioni

        for a in lista_album:
            if a not in parziale:
                parziale.append(a)
                self.__ricorsione(lista_album,dTot,parziale,durata_corrente + a.durata)
                parziale.pop()




    # per la ricorsione devo iterare su delle liste
    # analizzo tutte le componenti della lista



















