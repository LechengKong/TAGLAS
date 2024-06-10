from typing import (
    Union,
    Optional,
    Callable,
)

import torch
from torch import Tensor, LongTensor

from TAGLAS.data import TAGData, TAGDataset
from ..base import DefaultTask, DefaultTextTask
from ..process import value_to_tensor, parallel_build_sample_process


def default_labels(dataset: TAGDataset, split: str) -> tuple[LongTensor, Tensor, list]:
    r"""Obtain graph prediction labels from dataset for the specified split. The dataset should implement get_GP_indexs_labels function.
    Args:
        dataset (TAGDataset): Dataset which implement the get_GP_indexs_labels function.
        split (str): Dataset split.
    """
    sample_indexs, sample_labels, sample_label_maps = dataset.get_GP_indexs_labels(split)
    return sample_indexs, sample_labels, sample_label_maps,


class DefaultGPTask(DefaultTask):
    r"""Graph prediction task with original node/edge features.
    """

    def __init__(
            self,
            dataset: TAGDataset,
            split: Optional[str] = "train",
            save_data: Optional[bool] = False,
            from_saved: Optional[bool] = False,
            save_name: Optional[str] = None,
            post_funcs: Optional[Union[Callable, list[Callable]]] = None,
            filter_func: Optional[Callable] = None,
            sample_size: Optional[Union[float, int, list]] = 1.0,
            sample_mode: Optional[str] = "random",
            num_workers: Optional[int] = 0,
            **kwargs) -> None:
        self.num_workers = num_workers
        super().__init__(dataset, split, save_data, from_saved, save_name, post_funcs, filter_func, sample_size, sample_mode,
                         **kwargs)

    def __process_split_and_label__(self):
        sample_indexs, sample_labels, sample_label_maps, = default_labels(self.dataset, self.split)
        return sample_indexs, sample_labels, sample_label_maps,

    def __build_sample__(
            self,
            index: Union[int, Tensor, list],
            y: Union[int, float, Tensor,],
            label_map: Union[int, LongTensor, tuple],
            edge_index: LongTensor,
            node_map: LongTensor,
            edge_map: LongTensor,
    ):
        edge_index, node_map, edge_map = self.__process_graph__(index, edge_index, node_map, edge_map)
        # for graph tasks, target index will be all nodes in the graph.
        new_index = torch.arange(len(node_map))
        label_map = value_to_tensor(label_map)
        y = value_to_tensor(y, to_long=False)

        return TAGData(edge_index=edge_index, node_map=node_map, y=y, label_map=label_map, target_index=new_index,
                       edge_map=edge_map)

    def __before_build_dataset__(self, sample_index: int):
        edge_index = self.dataset[sample_index].edge_index
        node_map = self.dataset[sample_index].node_map
        edge_map = self.dataset[sample_index].edge_map
        return edge_index, node_map, edge_map

    def __build_task__(self):
        data_list = parallel_build_sample_process(self, True)
        return data_list


class DefaultTextGPTask(DefaultTextTask):
    r"""Graph prediction task with text node/edge features.
    """

    def __init__(
            self,
            dataset: TAGDataset,
            split: Optional[str] = "train",
            save_data: Optional[bool] = False,
            from_saved: Optional[bool] = False,
            save_name: Optional[str] = None,
            post_funcs: Optional[Union[Callable, list[Callable]]] = None,
            filter_func: Optional[Callable] = None,
            sample_size: Optional[Union[float, int, list]] = 1.0,
            sample_mode: Optional[str] = "random",
            num_workers: Optional[int] = 0,
            **kwargs) -> None:
        self.num_workers = num_workers
        super().__init__(dataset, split, save_data, from_saved, save_name, post_funcs, filter_func, sample_size, sample_mode,
                         **kwargs)

    def __process_split_and_label__(self):
        sample_indexs, sample_labels, sample_label_maps, = default_labels(self.dataset, self.split)
        return sample_indexs, sample_labels, sample_label_maps,

    def __build_sample__(
            self,
            index: Union[int, Tensor, list],
            y: Union[int, float, Tensor,],
            label_map: Union[int, LongTensor, tuple],
            edge_index: LongTensor,
            node_map: LongTensor,
            edge_map: LongTensor,
    ):
        edge_index, node_map, edge_map = self.__process_graph__(index, edge_index, node_map, edge_map)
        # for graph tasks, target index will be all nodes in the graph.
        new_index = torch.arange(len(node_map))

        label_map = value_to_tensor(label_map)
        y = value_to_tensor(y, to_long=False)
        return TAGData(edge_index=edge_index, node_map=node_map, y=y, label_map=label_map, target_index=new_index,
                       edge_map=edge_map)

    def __before_build_dataset__(self, sample_index: int):
        edge_index = self.dataset[sample_index].edge_index
        node_map = self.dataset[sample_index].node_map
        edge_map = self.dataset[sample_index].edge_map
        return edge_index, node_map, edge_map

    def __build_task__(self):
        data_list = parallel_build_sample_process(self, True)
        return data_list