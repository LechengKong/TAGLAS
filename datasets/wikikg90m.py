from typing import (
    Optional,
    Callable, Any,
)
import os
from TAGLAS.data import TAGData, TAGDataset
import os.path as osp
from TAGLAS.utils.io import download_url, extract_zip
import numpy as np
import pandas as pd
import torch
import shutil
from TAGLAS.data import BaseDict
from torch_geometric.data import InMemoryDataset
from TAGLAS.data.dataset import ROOT
from torch import Tensor




def get_rel_text(rel_raw_text, s2t=True):
    if s2t:
        prefix = "Relation from source entity to target entity. "
    else:
        prefix = "Relation from target entity to source entity. "
    text = (
        prefix
        + "Relation title: "
        + rel_raw_text["title"]
        + ". Relation description: "
        + rel_raw_text["desc"]
    )
    rel_text_lst = text.values
    return rel_text_lst


def get_node_text(node_raw_text):
    text = ("Entity in the knowledge graph. Entity name: "
            + node_raw_text["title"]
            + ". Entity description: "
            + node_raw_text["desc"])
    node_text_lst = text.values
    return node_text_lst.tolist()


class WikiKG90M(TAGDataset):
    data_url = 'https://dgl-data.s3-accelerate.amazonaws.com/dataset/OGB-LSC/wikikg90m-v2.zip'
    mapping_url = "http://snap.stanford.edu/ogb/data/lsc/mapping/wikikg90mv2_mapping.zip"

    def __init__(
            self,
            name: str = "wikikg90m",
            root: Optional[str] = None,
            transform: Optional[Callable] = None,
            pre_transform: Optional[Callable] = None,
            pre_filter: Optional[Callable] = None,
            to_undirected: bool = True,
            **kwargs,

    ) -> None:
        self.name = name
        root = (root if root is not None else ROOT)
        root = osp.join(root, self.name)
        super(InMemoryDataset, self).__init__(root, transform, pre_transform, pre_filter)
        self.to_undirected = to_undirected
        results = self.load_data()
        key_name_list = ["x", "edge_index", "edge_attr", "node_map", "edge_map",  "label", "label_map", "side_data"]
        update_dict = {}
        for key, value in zip(key_name_list, results):
            update_dict[key] = value

        data = TAGData(**update_dict)
        self.data, self.slices = self.collate([data])


    @property
    def processed_dir(self) -> str:
        return osp.join(self.raw_dir, 'processed')

    @property
    def processed_file_names(self) -> list:
        return ["train_hrt.npy", "val_hr.npy", "val_t.npy",
                osp.join("wikikg90mv2_mapping", "relation.csv"),
                osp.join("wikikg90mv2_mapping", "entity.csv"),
                ]
    @property
    def raw_file_names(self) -> list:
        return ["meta.pt", osp.join("processed", "train_hrt.npy"),
                osp.join("processed", "val_hr.npy"),
                osp.join("processed", "val_t.npy"),
                osp.join("processed", "wikikg90mv2_mapping", "relation.csv"),
                osp.join("processed", "wikikg90mv2_mapping", "entity.csv"),
                ]

    def download(self):
        data_path = download_url(self.data_url, self.root)
        extract_zip(osp.join(self.root, "wikikg90m-v2.zip"), self.root)
        os.remove(data_path)
        shutil.rmtree(self.raw_dir)
        os.rename(osp.join(self.root, "wikikg90m-v2"), self.raw_dir)
        mapping_path = download_url(self.mapping_url, self.root)
        extract_zip(osp.join(self.root, "wikikg90mv2_mapping.zip"), self.processed_dir)
        os.remove(mapping_path)

    def load_data(self):
        train_hrt = np.load(self.raw_paths[1])
        valid_dict = {}
        valid_dict['hr'] = np.load(self.raw_paths[2])
        valid_dict['t'] = np.load(self.raw_paths[3])
        valid_hrt = np.concatenate(
            [valid_dict["hr"], valid_dict["t"].reshape(-1, 1)], axis=1
        )
        edge_index = []
        edge_map = []
        for triplet in train_hrt:
            edge_index.append(
                [
                    triplet[0],
                    triplet[2],
                ]
            )
            edge_map.append(triplet[1])
        num_train = len(edge_index)
        for triplet in valid_hrt:
            edge_index.append(
                [
                    triplet[0],
                    triplet[2],
                ]
            )
            edge_map.append(triplet[1])
        num_val = len(edge_index) - num_train

        edge_index = torch.tensor(edge_index).transpose(0, 1)
        edge_map = torch.tensor(edge_map)
        rel_raw_text = pd.read_csv(self.raw_paths[4], index_col=0)
        edge_attr = get_rel_text(rel_raw_text)
        label = edge_attr
        label_map = edge_map
        node_raw_text = pd.read_csv(self.raw_paths[5], index_col=0)
        x = get_node_text(node_raw_text)
        node_map = torch.arange(len(x))

        keep_edges = torch.arange(num_train)
        if self.to_undirected:
            num_edges = edge_index.size(-1)
            edge_index = torch.cat([edge_index, torch.stack([edge_index[1], edge_index[0]])], dim=-1)
            edge_attr = edge_attr + get_rel_text(rel_raw_text, False)
            num_edge_type = len(edge_attr)
            edge_map = torch.cat([edge_map, edge_map + num_edge_type], dim=-1)
            keep_edges = torch.cat([keep_edges, keep_edges + num_edges], dim=-1)

        train_idx = torch.arange(num_train)
        val_idx = torch.arange(num_train, num_val + num_train,)

        split_dict = BaseDict(train=train_idx, val=val_idx)
        side_data = BaseDict(link_split=split_dict, keep_edges=keep_edges)

        return x, edge_index, edge_attr, node_map, edge_map, label, label_map, side_data

    def process(self) -> None:
        return None

    def gen_data(self) -> tuple[list[TAGData], Any]:
        return [], None

    def get_LP_indexs_labels(self, split: str = "train") -> tuple[Tensor, Tensor, list]:
        r"""Return sample labels and their corresponding index for the link-level tasks and the given split.
        Args:
            split (str, optional): Split to use. Defaults to "train".
        """
        idxs = self.side_data.link_split[split]
        edge_index = self.edge_index
        labels = self.label_map[idxs]
        label_map = labels
        idxs = edge_index[:, idxs].transpose(0, 1)
        return idxs, labels, label_map.tolist()

    def get_LQA_list(self, label_map, **kwargs) -> tuple[list[list], np.ndarray, np.ndarray]:
        r"""Return question and answer list for link question answering tasks.
        Args:
            label_map (list): Mapping to the label for all samples. Will use it to generate answer and question.
            **kwargs: Other arguments.
        """
        q_list = ["What is the relationship between two target entities?"]
        answer_list = []
        label_features = self.label
        for l in label_map:
            answer_list.append(label_features[l] + ".")
        a_list, a_idxs = np.unique(np.array(answer_list, dtype=object), return_inverse=True)
        a_list = a_list.tolist()
        label_map = [[0, l_idx, a_idx] for l_idx, a_idx in zip(label_map, a_idxs)]

        return label_map, q_list, a_list
