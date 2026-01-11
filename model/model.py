import networkx as nx
from database.dao import DAO

class Model:

    def __init__(self):
        self._lista_nodi=[]
        self._lista_playlist=[]
        self.G=nx.Graph()

    def _getAllAlbums(self, durata):
        self._lista_album=DAO.read_all_album(durata)
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

        for a_id in componente:
            durata+=album_map[a_id].durata

        return dimensione, durata
















