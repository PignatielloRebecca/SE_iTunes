import networkx as nx
from database.dao import DAO
from copy import copy

class Model:
    def __init__(self):
        self._lista_id=[]
        self._map_nodi={}

        self.G=nx.Graph()

    def load_map_nodi(self, durata):

        for a in DAO.read_all_album(durata):
            self._map_nodi[a.id]=a
        return self._map_nodi


    def build_graph(self, durata):

        # aggiungo gli archi
        self._mappa_nodi=self.load_map_nodi(durata)
        nodi=[id for id in self._mappa_nodi.keys()]
        self.G.add_nodes_from(nodi)

        #aggiungo i nodi
        album=DAO.read_all_connessioni(durata)
        for (a1,a2) in album:
            self.G.add_edge(a1,a2)

        return self.G

    def analisi_componente_connessa(self, id_album):

        # componente connessa
        nodi=nx.node_connected_component(self.G, id_album) # mi restituisce una lista di id

        lunghezza=len(nodi)

        durata=0
        id=list(n for n in nodi)

        for (c,v) in self._mappa_nodi.items():
            # se la chiave si trova in quella mappa
            if c in id:
                durata+=self._mappa_nodi[c].durata

        return lunghezza, durata


    def set_album(self, id_album, dTot):

        # prendo la componente connessa di a1
        nodo = nx.node_connected_component(self.G, id_album)

        lista_album=[]
        # mi costruisco un dizionario con fli ID della componente connessa, perchè ho gli id e devo risalire agli oggetti--> mi serve la durata
        for (c,v) in self._mappa_nodi.items():
            if c in nodo:
                lista_album.append(v)  # lista_album è una lista di oggetti
        a1=self._mappa_nodi[id_album]

        self._best_cammmino=[]
        self._best_durata=0

        self.__ricorsione(lista_album ,dTot, [a1], a1.durata)

        return self._best_cammmino, self._best_durata


    def __ricorsione(self,lista_album, dTot, lunghezza_parziale, durata_corrente):

        if durata_corrente > dTot:
            return

        if len(lunghezza_parziale) > len(self._best_cammmino): # mi ricordo che devo trovare una lista che contiene il maggior numero di cammini
            self._best_cammmino=lunghezza_parziale.copy()
            self._best_durata=durata_corrente

        for a in lista_album:
            if a not in lunghezza_parziale:  # devo verificare che il vicino non si trovi nell'album
                lunghezza_parziale.append(a)
                self.__ricorsione(lista_album, dTot, lunghezza_parziale, durata_corrente + a.durata)

                lunghezza_parziale.pop()

"""

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
"""


















