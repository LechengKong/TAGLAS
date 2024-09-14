from functools import partial
from typing import (
    Optional,
    Union,
    Callable,
)

from torchmetrics import Metric

from TAGLAS.data import *
from TAGLAS.datasets import *
from TAGLAS.evaluation import *
from TAGLAS.tasks import *

DATASET_TO_CLASS_DICT = {
    "cora": Cora,
    "pubmed": Pubmed,
    "wikics": WikiCS,
    "arxiv": Arxiv,
    "fb15k237": FB15K237,
    "wn18rr": WN18RR,
    "hiv": partial(Chembl, name="hiv"),
    "pcba": partial(Chembl, name="pcba"),
    "bbbp": partial(Chembl, name="bbbp"),
    "bace": partial(Chembl, name="bace"),
    "toxcast": partial(Chembl, name="toxcast"),
    "esol": partial(Chembl, name="esol"),
    "freesolv": partial(Chembl, name="freesolv"),
    "lipo": partial(Chembl, name="lipo"),
    "cyp450": partial(Chembl, name="cyp450"),
    "tox21": partial(Chembl, name="tox21"),
    "muv": partial(Chembl, name="muv"),
    "chemblpre": partial(Chembl, name="chemblpre"),
    "molproperties": partial(Chembl, name="molproperties"),
    "products": Products,
    "ml1m": ML1M,
    "ml1m_cls": ML1M_CLS,
    "expla_graph": ExplaGraph,
    "scene_graph": SceneGraph,
    "wiki_graph": WikiGraph,
    "mag240m": MAG240M,
    "ultrachat200k": UltraChat200k,
    "wikikg90m": WikiKG90M,
}

DATASET_INFOR_DICT = {
    "cora": {"dataset": "cora"},
    "pubmed": {"dataset": "pubmed"},
    "cora_node": {"dataset": "cora",
                  "task": {"default": DefaultNPTask,
                           "subgraph": SubgraphNPTask,
                           "default_text": DefaultTextNPTask,
                           "subgraph_text": SubgraphTextNPTask,
                           "QA": NQATask},
                  "evaluation": {"default": ("accuracy", {"metric_name": "accuracy", "num_classes": 7}),
                                 "QA": ("text_accuracy",  {"metric_name": "text_accuracy"})},
                  },
    "cora_link": {"dataset": "cora",
                  "task": {"default": DefaultLPTask,
                           "subgraph": SubgraphLPTask,
                           "default_text": DefaultTextLPTask,
                           "subgraph_text": SubgraphTextLPTask,
                           "QA": LQATask},
                  "evaluation": {"default": ("accuracy", {"metric_name": "accuracy", "num_classes": 2}),
                                 "QA": ("text_accuracy", {"metric_name": "text_accuracy", "mode": "re",
                                                          "regular_patterns": r"\b(Yes|yes|No|no)\b"})},
                  },
    "pubmed_node": {"dataset": "pubmed",
                    "task": {"default": DefaultNPTask,
                             "subgraph": SubgraphNPTask,
                             "default_text": DefaultTextNPTask,
                             "subgraph_text": SubgraphTextNPTask,
                             "QA": NQATask},
                    "evaluation": {"default": ("accuracy", {"metric_name": "accuracy", "num_classes": 3}),
                                   "QA": ("text_accuracy", {"metric_name": "text_accuracy"})},
                    },
    "pubmed_link": {"dataset": "pubmed",
                    "task": {"default": DefaultLPTask,
                             "subgraph": SubgraphLPTask,
                             "default_text": DefaultTextLPTask,
                             "subgraph_text": SubgraphTextLPTask,
                             "QA": LQATask},
                    "evaluation": {"default": ("accuracy", {"metric_name": "accuracy", "num_classes": 2}),
                                   "QA": ("text_accuracy", {"metric_name": "text_accuracy", "mode": "re",
                                                          "regular_patterns": r"\b(Yes|yes|No|no)\b"})},
                    },
    "wikics": {"dataset": "wikics",
               "task": {"default": DefaultNPTask,
                        "subgraph": SubgraphNPTask,
                        "default_text": DefaultTextNPTask,
                        "subgraph_text": SubgraphTextNPTask,
                        "QA": NQATask},
               "evaluation": {"default": ("accuracy", {"metric_name": "accuracy", "num_classes": 10}),
                              "QA": ("text_accuracy", {"metric_name": "text_accuracy"})},
               },
    "arxiv": {"dataset": "arxiv",
              "task": {"default": DefaultNPTask,
                       "subgraph": SubgraphNPTask,
                       "default_text": DefaultTextNPTask,
                       "subgraph_text": SubgraphTextNPTask,
                       "QA": NQATask},
              "evaluation": {"default": ("accuracy", {"metric_name": "accuracy", "num_classes": 40}),
                             "QA": ("text_accuracy", {"metric_name": "text_accuracy"})},
              },
    "arxiv_link": {"dataset": "arxiv",
                    "task": {"default": DefaultLPTask,
                             "subgraph": SubgraphLPTask,
                             "default_text": DefaultTextLPTask,
                             "subgraph_text": SubgraphTextLPTask,
                             "QA": LQATask},
                    "evaluation": {"default": ("accuracy", {"metric_name": "accuracy", "num_classes": 2}),
                                   "QA": ("text_accuracy", {"metric_name": "text_accuracy", "mode": "re",
                                                          "regular_patterns": r"\b(Yes|yes|No|no)\b"})},
                    },
    "fb15k237": {"dataset": "fb15k237",
                 "task": {"default": DefaultLPTask,
                          "subgraph": SubgraphLPTask,
                          "default_text": DefaultTextLPTask,
                          "subgraph_text": SubgraphTextLPTask,
                          "QA": LQATask},
                 "evaluation": {"default": ("accuracy", {"metric_name": "accuracy", "num_classes": 237}),
                                "QA": ("text_accuracy", {"metric_name": "text_accuracy"})},
                 },
    "wn18rr": {"dataset": "wn18rr",
               "task": {"default": DefaultLPTask,
                        "subgraph": SubgraphLPTask,
                        "default_text": DefaultTextLPTask,
                        "subgraph_text": SubgraphTextLPTask,
                        "QA": LQATask},
               "evaluation": {"default": ("accuracy", {"metric_name": "accuracy", "num_classes": 11}),
                              "QA": ("text_accuracy", {"metric_name": "text_accuracy"})},
               },
    "hiv": {"dataset": "hiv",
            "task": {"default": DefaultGPTask,
                     "default_text": DefaultTextGPTask,
                     "QA": GQATask},
            "evaluation": {"default": ("auc", {"metric_name": "auc"}),
                           "QA": ("text_accuracy", {"metric_name": "text_accuracy", "mode": "re",
                                                          "regular_patterns": r"\b(Yes|yes|No|no)\b"})},
            },
    "pcba": {"dataset": "pcba",
             "task": {"default": DefaultGPTask,
                      "default_text": DefaultTextGPTask,
                      "QA": GQATask},
             "evaluation": {"default": ("apr", {"metric_name": "apr", "num_labels": 128}),
                            "QA": ("text_accuracy", {"metric_name": "text_accuracy", "mode": "re",
                                                          "regular_patterns": r"\b(Yes|yes|No|no)\b"})},
             },
    "bbbp": {"dataset": "bbbp",
             "task": {"default": DefaultGPTask,
                      "default_text": DefaultTextGPTask,
                      "QA": GQATask},
             "evaluation": {"default": ("auc", {"metric_name": "auc"}),
                            "QA": ("text_accuracy", {"metric_name": "text_accuracy", "mode": "re",
                                                          "regular_patterns": r"\b(Yes|yes|No|no)\b"})},
             },
    "bace": {"dataset": "bace",
             "task": {"default": DefaultGPTask,
                      "default_text": DefaultTextGPTask,
                      "QA": GQATask},
             "evaluation": {"default": ("auc", {"metric_name": "auc"}),
                            "QA": ("text_accuracy", {"metric_name": "text_accuracy", "mode": "re",
                                                          "regular_patterns": r"\b(Yes|yes|No|no)\b"})},
             },
    "toxcast": {"dataset": "toxcast",
                "task": {"default": DefaultGPTask,
                         "default_text": DefaultTextGPTask,
                         "QA": GQATask},
                "evaluation": {"default": ("multiauc", {"metric_name": "multiauc", "num_labels": 588}),
                               "QA": ("text_accuracy",  {"metric_name": "text_accuracy", "mode": "re",
                                                          "regular_patterns": r"\b(Yes|yes|No|no)\b"})},
                },
    "esol": {"dataset": "esol",
             "task": {"default": DefaultGPTask,
                      "default_text": DefaultTextGPTask,
                      "QA": GQATask},
             "evaluation": {"default": ("rmse", {"metric_name": "rmse"}),
                            "QA": ("text_rmse", {"metric_name": "text_rmse"})},
             },
    "freesolv": {"dataset": "freesolv",
                 "task": {"default": DefaultGPTask,
                          "default_text": DefaultTextGPTask,
                          "QA": GQATask},
                 "evaluation": {"default": ("rmse", {"metric_name": "rmse"}),
                                "QA": ("text_rmse", {"metric_name": "text_rmse"})},
                 },
    "lipo": {"dataset": "lipo",
             "task": {"default": DefaultGPTask,
                      "default_text": DefaultTextGPTask,
                      "QA": GQATask},
             "evaluation": {"default": ("rmse", {"metric_name": "rmse"}),
                            "QA": ("text_rmse", {"metric_name": "text_rmse"})},
             },
    "cyp450": {"dataset": "cyp450",
               "task": {"default": DefaultGPTask,
                        "default_text": DefaultTextGPTask,
                        "QA": GQATask},
               "evaluation": {"default": ("multiauc", {"metric_name": "multiauc", "num_labels": 5}),
                              "QA": ("text_accuracy", {"metric_name": "text_accuracy", "mode": "re",
                                                       "regular_patterns": r"\b(Yes|yes|No|no)\b"})},
               },
    "tox21": {"dataset": "tox21",
              "task": {"default": DefaultGPTask,
                       "default_text": DefaultTextGPTask,
                       "QA": GQATask},
              "evaluation": {"default": ("multiauc", {"metric_name": "multiauc", "num_labels": 12}),
                             "QA": ("text_accuracy", {"metric_name": "text_accuracy", "mode": "re",
                                                      "regular_patterns": r"\b(Yes|yes|No|no)\b"})},
              },
    "muv": {"dataset": "muv",
            "task": {"default": DefaultGPTask,
                     "default_text": DefaultTextGPTask,
                     "QA": GQATask},
            "evaluation": {"default": ("multiauc", {"metric_name": "multiauc", "num_labels": 17}),
                           "QA": ("text_accuracy", {"metric_name": "text_accuracy", "mode": "re",
                                                    "regular_patterns": r"\b(Yes|yes|No|no)\b"})},
            },
    "chemblpre": {"dataset": "chemblpre",
                  "task": {"default": DefaultGPTask,
                           "default_text": DefaultTextGPTask,
                           "QA": GQATask},
                  "evaluation": {"default": ("multiauc", {"metric_name": "multiauc", "num_labels": 1048}),
                                 "QA": ("text_accuracy", {"metric_name": "text_accuracy", "mode": "re",
                                                          "regular_patterns": r"\b(Yes|yes|No|no)\b"})},
                  },
    "molproperties": {"dataset": "molproperties",
                      "task": {"QA": GQATask},
                      "evaluation": {"QA": ("text_accuracy", {"metric_name": "text_accuracy"})},
                      },
    "products": {"dataset": "products",
                 "task": {"default": DefaultNPTask,
                          "subgraph": SubgraphNPTask,
                          "default_text": DefaultTextNPTask,
                          "subgraph_text": SubgraphTextNPTask,
                          "QA": NQATask},
                 "evaluation": {"default": ("accuracy", {"metric_name": "accuracy", "num_classes": 44}),
                                "QA": ("text_accuracy", {"metric_name": "text_accuracy"})},
                 },
    "ml1m": {"dataset": "ml1m",
             "task": {"default": DefaultLPTask,
                      "subgraph": SubgraphLPTask,
                      "default_text": DefaultTextLPTask,
                      "subgraph_text": SubgraphTextLPTask,
                      "QA": LQATask},
             "evaluation": {"default": ("rmse", {"metric_name": "rmse"}),
                            "QA": ("text_rmse", {"metric_name": "text_rmse"})},
             },
    "ml1m_cls": {"dataset": "ml1m_cls",
                 "task": {"default": DefaultLPTask,
                          "subgraph": SubgraphLPTask,
                          "default_text": DefaultTextLPTask,
                          "subgraph_text": SubgraphTextLPTask,
                          "QA": LQATask},
                 "evaluation": {"default": ("accuracy", {"metric_name": "accuracy", "num_classes": 2}),
                                "QA": ("text_accuracy", {"metric_name": "text_accuracy", "mode": "re",
                                                         "regular_patterns": r"\b(Yes|yes|No|no)\b"})},
                 },
    "mag240m": {"dataset": "mag240m",
                "task": {"default": DefaultNPTask,
                         "subgraph": SubgraphNPTask,
                         "default_text": DefaultTextNPTask,
                         "subgraph_text": SubgraphTextNPTask,
                         "QA": NQATask},
                "evaluation": {"default": ("accuracy", {"metric_name": "accuracy", "num_classes": 153}),
                               "QA": ("text_accuracy", {"metric_name": "text_accuracy"})},
                },
    "expla_graph": {"dataset": "expla_graph",
            "task": {"default_text": DefaultTextGPTask,
                     "QA": GQATask},
            "evaluation": {"default": ("accuracy", {"metric_name": "accuracy", "num_classes": 2}),
                            "QA": ("text_accuracy", {"metric_name": "text_accuracy"})},
            },
    "scene_graph": {"dataset": "scene_graph",
                    "task": {"QA": GQATask},
                    "evaluation": {"QA": ("text_accuracy", {"metric_name": "text_accuracy", "mode": "search"})},
                    },
    "wiki_graph": {"dataset": "wiki_graph",
                    "task": {"QA": GQATask},
                    "evaluation": {"QA": ("text_accuracy", {"metric_name": "text_accuracy"})},
                    },
    "ultrachat200k": {"dataset": "ultrachat200k",
                    "task": {"QA": GQATask},
                    "evaluation": {"QA": ("text_accuracy", {"metric_name": "text_accuracy"})},
                    },
    "wikikg90m": {"dataset": "wikikg90m",
                 "task": {"default": DefaultLPTask,
                          "subgraph": SubgraphLPTask,
                          "default_text": DefaultTextLPTask,
                          "subgraph_text": SubgraphTextLPTask,
                          "QA": LQATask},
                 "evaluation": {"default": ("accuracy", {"metric_name": "accuracy", "num_classes": 1387}),
                                "QA": ("text_accuracy", {"metric_name": "text_accuracy"})},
                 },
}


def get_dataset(
        name: str,
        root: Optional[str] = None,
        transform: Optional[Callable] = None,
        pre_transform: Optional[Callable] = None,
        pre_filter: Optional[Callable] = None,
        **kwargs) -> TAGDataset:
    return DATASET_TO_CLASS_DICT[DATASET_INFOR_DICT[name]["dataset"]](root=root, transform=transform,
                                                                      pre_transform=pre_transform,
                                                                      pre_filter=pre_filter, **kwargs)


def get_datasets(names: Union[str, list[str]],
                 root: Optional[str] = None,
                 transform: Optional[Callable] = None,
                 pre_transform: Optional[Callable] = None,
                 pre_filter: Optional[Callable] = None,
                 **kwargs) -> list[TAGDataset]:
    if isinstance(names, str):
        return [get_dataset(names, root, transform, pre_transform, pre_filter, **kwargs)]
    else:
        return [get_dataset(name, root, transform, pre_transform, pre_filter, **kwargs) for name in names]


def get_task(
        name: str,
        task_type: str = "default",
        split: str = "train",
        root: Optional[str] = None,
        transform: Optional[Callable] = None,
        pre_transform: Optional[Callable] = None,
        pre_filter: Optional[Callable] = None,
        **kwargs) -> BaseTask:
    dataset = get_dataset(name, root, transform, pre_transform, pre_filter, **kwargs)
    if task_type not in DATASET_INFOR_DICT[name]["task"].keys():
        avaliable_tasks = ', '.join(list(DATASET_INFOR_DICT[name]["task"].keys()))
        raise ValueError(f"The task type {task_type} is not supported for dataset {name}. "
                         f"The supported task types are {avaliable_tasks}")
    return DATASET_INFOR_DICT[name]["task"][task_type](dataset, split, **kwargs)


def get_tasks(names: Union[str, list[str]],
              task_types: Union[str, list[str]] = "default",
              root: Optional[str] = None,
              transform: Optional[Callable] = None,
              pre_transform: Optional[Callable] = None,
              pre_filter: Optional[Callable] = None,
              **kwargs):
    if isinstance(names, str):
        names = [names]
    if isinstance(task_types, str):
        task_types = [task_types] * len(names)
    assert len(names) == len(task_types)
    return [get_task(name, task_type, root, transform, pre_transform, pre_filter, **kwargs) for name, task_type in
            zip(names, task_types)]


def get_evaluator(name: str,
                  task_type: str = "default") -> tuple[str, Metric]:
    task_type = "QA" if task_type == "QA" else "default"
    if task_type not in DATASET_INFOR_DICT[name]["evaluation"].keys():
        avaliable_evaluation = ', '.join(list(DATASET_INFOR_DICT[name]["evaluation"].keys()))
        raise ValueError(f"The evaluation of task type {task_type} is not supported for dataset {name}. "
                         f"The supported task types are {avaliable_evaluation}")
    metric_name, evaluator_args = DATASET_INFOR_DICT[name]["evaluation"][task_type]
    return metric_name, Evaluator(**evaluator_args)


def get_evaluators(names: Union[str, list[str]], task_types: Union[str, list[str]] = "default") \
        -> tuple[list[str], list[Metric]]:
    if isinstance(names, str):
        names = [names]
    if isinstance(task_types, str):
        task_types = [task_types] * len(names)

    metric_names = []
    evaluator_list = []
    for name, task_type in zip(names, task_types):
        metric_name, evaluator_func = get_evaluator(name, task_type)
        metric_names.append(metric_name)
        evaluator_list.append(evaluator_func)

    return metric_names, evaluator_list
