import gymnasium as gym
import torch 
import torch_geometric as pyg 
import numpy as np 

import networkx as nx 
import random

from typing import Tuple

class ShortestPathEnv(gym.Env):
    def __init__(self, n_nodes, n_edges) -> None:
        super(ShortestPathEnv, self).__init__()
        
        self.HAS_NOTHING = np.array([1.0])
        self.HAS_MSG = np.array([2.0])
        self.IS_TARGET = np.array([3.0])
        self.inf_delay = np.array([-1.0])
        
        self.n_nodes = n_nodes
        self.n_edges = n_edges
        self.action_space = gym.spaces.MultiDiscrete([n_nodes, n_nodes])
        self.observation_space = gym.spaces.Box(low=-1., high=11., shape=(3, n_nodes, n_nodes))        

    def reset(self, seed=None, options={}) -> np.array:
        super().reset(seed=seed)
        random.seed(seed)
        np.random.seed(seed)
        
        while True:
            # G = global_G
            G = nx.gnm_random_graph(self.n_nodes, self.n_edges)
            if nx.is_connected(G):
                break
        
        bandwidth = np.random.randint(10,15, size=(self.n_nodes, self.n_nodes))
        delay = np.random.randint(2,5, size=(self.n_nodes, self.n_nodes))/1.0
        
        for u, v, d in G.edges(data=True):
            d['delay'] = delay[u, v]
            d['bandwidth'] = bandwidth[u, v]
        
        # asp = nx.floyd_warshall_numpy(G, delay='delay')
        adj = np.array(nx.adjacency_matrix(G, dtype=float, weight='delay').todense(), dtype=np.float32)
        adj[adj==0] = self.inf_delay
        np.fill_diagonal(adj, 1)
        
        bw = np.array(nx.adjacency_matrix(G, dtype=float, weight='bandwidth').todense(), dtype=np.float32)
        bw[bw==0] = self.inf_delay
        np.fill_diagonal(bw, 0)
        
        
        state = np.zeros_like(adj) + self.HAS_NOTHING
        state[0,:] = self.HAS_MSG
        state[-1,:] = self.IS_TARGET
        
        # self.x = np.stack([np.zeros_like(adj) + self.HAS_NOTHING, self.x], axis=1, dtype=np.float32)
        
        self.x = np.stack((state, adj, bw), axis=0, dtype=np.float32)
        
        self.shortest_path = nx.shortest_path_length(G, source=0, target=self.n_nodes-1, weight='delay')
        self.edge_index = pyg.utils.from_networkx(G).edge_index
        
        info = {'mask': self.get_mask(), 'opt': self.shortest_path, 'solution': []}
        
        return self.x, info
    
    def get_mask(self) -> np.array:

        valid_edges = np.logical_and(
            np.isclose(self.x[0, self.edge_index[0], 0],self.HAS_MSG),
            np.isclose(self.x[0, self.edge_index[1], 0],self.HAS_MSG) == False
            ) # shape: (2*n_edges,)
        
        mask = np.zeros((self.n_nodes,self.n_nodes), dtype=bool)
        mask[self.edge_index[0,valid_edges], self.edge_index[1,valid_edges]] = True
        
        return mask
    
    def step(self, action: Tuple[int, int]) -> Tuple[np.array, bool, dict]:
        
        u, v = action
        
        # assert action < 2 * self.n_edges
        # assert self.get_mask()[action] == True
        assert (u < self.n_nodes) and (v < self.n_nodes), f"Nodes {u, v} are out of bounds!"
        assert self.get_mask()[u, v] == True, f"Mask of {u, v} is False!"
        assert not np.isclose(self.x[1, u, v], self.inf_delay), f"Edge {u, v} is not in the graph!"

        assert np.isclose(self.x[0, u, 0], self.HAS_MSG), f"Node {u} does not have a message!"
        assert np.isclose(self.x[0, v, 0], self.HAS_MSG) == False, f"Node {v} already has a message!"
        
        
        done = False
        reward = -self.x[1, u, v]
        
        if np.isclose(self.x[0, v, 0], self.IS_TARGET):
            done = True
            # reward += 1
            
        self.x[0, v, :] = self.HAS_MSG
        
        info = {'opt': self.shortest_path, 'mask': self.get_mask()}
        
        return self.x, reward, done, False, info
        