from deepomatic.oef.configs.utils import dict_inject
from deepomatic.oef.configs.config_utils import ModelConfig

from ..utils import fixed_shape_resizer
from ..backbones import Backbones as bb

backbones_classification = [
    # Nadam Optimizer Architecture
    (
        bb.INCEPTION_V1,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 4e-5,
                "optimizer": {"nadam_optimizer": {}},
                "learning_rate_policy": {"one_cycle_learning_rate": {}},
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 0.8,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 4e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.INCEPTION_V2,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 1e-5,
                "optimizer": {"nadam_optimizer": {}},
                "learning_rate_policy": {"one_cycle_learning_rate": {}},
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 0.8,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 1e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.0025,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.0025,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.INCEPTION_V3,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 3e-5,
                "optimizer": {"nadam_optimizer": {}},
                "learning_rate_policy": {"one_cycle_learning_rate": {}},
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(299, 299)},
                "dropout_keep_prob": 0.8,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 3e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.005,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.005,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.INCEPTION_V4,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 4e-5,
                "optimizer": {"nadam_optimizer": {}},
                "learning_rate_policy": {"one_cycle_learning_rate": {}},
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(299, 299)},
                "dropout_keep_prob": 0.8,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 4e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.005,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.005,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.INCEPTION_RESNET_V2,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 4e-5,
                "optimizer": {"nadam_optimizer": {}},
                "learning_rate_policy": {"one_cycle_learning_rate": {}},
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(299, 299)},
                "dropout_keep_prob": 0.8,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 4e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.005,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.005,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.RESNET_50_V1,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 9e-6,
                "optimizer": {"nadam_optimizer": {}},
                "learning_rate_policy": {"one_cycle_learning_rate": {}},
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 1.0,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 9e-6,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    # TODO: try with dropout ?
    (
        bb.RESNET_101_V1,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 5e-6,
                "optimizer": {"nadam_optimizer": {}},
                "learning_rate_policy": {"one_cycle_learning_rate": {}},
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 1.0,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 5e-6,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.RESNET_152_V1,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 3e-6,
                "optimizer": {"nadam_optimizer": {}},
                "learning_rate_policy": {"one_cycle_learning_rate": {}},
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 1.0,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 3e-6,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.RESNET_50_V2,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 2e-5,
                "optimizer": {"nadam_optimizer": {}},
                "learning_rate_policy": {"one_cycle_learning_rate": {}},
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 1.0,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 2e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.025,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.025,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.RESNET_101_V2,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 2e-5,
                "optimizer": {"nadam_optimizer": {}},
                "learning_rate_policy": {"one_cycle_learning_rate": {}},
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 1.0,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 2e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.RESNET_152_V2,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 6e-6,
                "optimizer": {"nadam_optimizer": {}},
                "learning_rate_policy": {"one_cycle_learning_rate": {}},
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 1.0,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 6e-6,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.0025,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.0025,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.EFFICIENTNET_B0,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 2e-5,
                "optimizer": {"nadam_optimizer": {}},
                "learning_rate_policy": {"one_cycle_learning_rate": {}},
            },
            "@model": {
                "backbone": {
                    "input.image_resizer": {
                        "fixed_shape_resizer": {
                            "height": 224,
                            "width": 224,
                            "resize_method": "BICUBIC",
                        }
                    }
                },
                "dropout_keep_prob": 0.8,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 2e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.032,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.032,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.EFFICIENTNET_B1,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 2e-5,
                "optimizer": {"nadam_optimizer": {}},
                "learning_rate_policy": {"one_cycle_learning_rate": {}},
            },
            "@model": {
                "backbone": {
                    "input.image_resizer": {
                        "fixed_shape_resizer": {
                            "height": 240,
                            "width": 240,
                            "resize_method": "BICUBIC",
                        }
                    }
                },
                "dropout_keep_prob": 0.8,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 2e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.032,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.032,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.EFFICIENTNET_B2,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 2e-5,
                "optimizer": {"nadam_optimizer": {}},
                "learning_rate_policy": {"one_cycle_learning_rate": {}},
            },
            "@model": {
                "backbone": {
                    "input.image_resizer": {
                        "fixed_shape_resizer": {
                            "height": 260,
                            "width": 260,
                            "resize_method": "BICUBIC",
                        }
                    }
                },
                "dropout_keep_prob": 0.7,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 2e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.032,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.032,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.EFFICIENTNET_B3,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 2e-5,
                "optimizer": {"nadam_optimizer": {}},
                "learning_rate_policy": {"one_cycle_learning_rate": {}},
            },
            "@model": {
                "backbone": {
                    "input.image_resizer": {
                        "fixed_shape_resizer": {
                            "height": 300,
                            "width": 300,
                            "resize_method": "BICUBIC",
                        }
                    }
                },
                "dropout_keep_prob": 0.7,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 2e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.032,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.032,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.EFFICIENTNET_B4,
        {
            "trainer": {
                "batch_size": 16,
                "initial_learning_rate": 2e-5,
                "optimizer": {"nadam_optimizer": {}},
                "learning_rate_policy": {"one_cycle_learning_rate": {}},
            },
            "@model": {
                "backbone": {
                    "input.image_resizer": {
                        "fixed_shape_resizer": {
                            "height": 380,
                            "width": 380,
                            "resize_method": "BICUBIC",
                        }
                    }
                },
                "dropout_keep_prob": 0.6,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 2e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.016,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.016,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.EFFICIENTNET_B5,
        {
            "trainer": {
                "batch_size": 8,
                "initial_learning_rate": 2e-5,
                "optimizer": {"nadam_optimizer": {}},
                "learning_rate_policy": {"one_cycle_learning_rate": {}},
            },
            "@model": {
                "backbone": {
                    "input.image_resizer": {
                        "fixed_shape_resizer": {
                            "height": 456,
                            "width": 456,
                            "resize_method": "BICUBIC",
                        }
                    }
                },
                "dropout_keep_prob": 0.6,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 2e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.008,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.008,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.EFFICIENTNET_B6,
        {
            "trainer": {
                "batch_size": 4,
                "initial_learning_rate": 2e-5,
                "optimizer": {"nadam_optimizer": {}},
                "learning_rate_policy": {"one_cycle_learning_rate": {}},
            },
            "@model": {
                "backbone": {
                    "input.image_resizer": {
                        "fixed_shape_resizer": {
                            "height": 528,
                            "width": 528,
                            "resize_method": "BICUBIC",
                        }
                    }
                },
                "dropout_keep_prob": 0.5,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 2e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.004,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.004,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    # Momentum SGD - RMS Prop
    (
        bb.VGG_11,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.01,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 0.5,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.VGG_16,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.005,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 0.5,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.005,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.005,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.VGG_19,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.0025,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 0.5,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.0025,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.0025,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    # (bb.RESNET_200_V1, {'trainer': {'batch_size': 32, 'initial_learning_rate': 0.01}, '@model': {'backbone': {'input.image_resizer': fixed_shape_resizer(224, 224)}, 'dropout_keep_prob': 1.}},
    # [
    #     {
    #         'field': 'optimizer',
    #         'triggering_value': 'nadam_optimizer',
    #         'target_value': {'trainer': {
    #             'initial_learning_rate':2e-5,
    #             'learning_rate_policy': {'one_cycle_learning_rate': {}},  ]
    # ),
    #     {
    #         'field': 'optimizer',
    #         'triggering_value': 'momentum_optimizer',
    #         'target_value': {'trainer': {
    #             'initial_learning_rate': 0.032,
    #             'learning_rate_policy': {"manual_step_learning_rate": {"schedule": [{"learning_rate_factor": 0.1, "step_pct": 0.33}, {"learning_rate_factor": 0.01, "step_pct": 0.66}]}},
    #         }}
    #     },
    # ]
    # ),
    # (bb.RESNET_200_V2, {'trainer': {'batch_size': 32, 'initial_learning_rate': 0.01}, '@model': {'backbone': {'input.image_resizer': fixed_shape_resizer(224, 224)}, 'dropout_keep_prob': 1.}},
    # [
    #     {
    #         'field': 'optimizer',
    #         'triggering_value': 'nadam_optimizer',
    #         'target_value': {'trainer': {
    #             'initial_learning_rate':2e-5,
    #             'learning_rate_policy': {'one_cycle_learning_rate': {}},  ]
    # #
    #     {
    #         'field': 'optimizer',
    #         'triggering_value': 'momentum_optimizer',
    #         'target_value': {'trainer': {
    #             'initial_learning_rate': 0.032,
    #             'learning_rate_policy': {"manual_step_learning_rate": {"schedule": [{"learning_rate_factor": 0.1, "step_pct": 0.33}, {"learning_rate_factor": 0.01, "step_pct": 0.66}]}},
    #         }}
    #     },
    # ]
    # ),
    (
        bb.MOBILENET_V1,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 1e-5,
                "optimizer": {"nadam_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 0.999,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 1e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.MOBILENET_V1_075,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 1e-5,
                "optimizer": {"nadam_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 0.999,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 1e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.MOBILENET_V1_050,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 1e-5,
                "optimizer": {"nadam_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 0.999,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 1e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.MOBILENET_V1_025,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 1e-5,
                "optimizer": {"nadam_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 0.999,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 1e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.MOBILENET_V2,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 1.5e-5,
                "optimizer": {"nadam_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 1.0,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 1.5e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),  # TODO: try with dropout ?
    (
        bb.MOBILENET_V2_140,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 1.5e-5,
                "optimizer": {"nadam_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 1.0,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 1.5e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.NASNET_MOBILE,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.01,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 0.5,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.NASNET_LARGE,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.01,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(331, 331)},
                "dropout_keep_prob": 0.5,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.PNASNET_MOBILE,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.01,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 0.5,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.PNASNET_LARGE,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.01,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(331, 331)},
                "dropout_keep_prob": 0.5,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.EFFICIENTNET_B7,
        {
            "trainer": {
                "batch_size": 2,
                "initial_learning_rate": 0.002,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {
                    "input.image_resizer": {
                        "fixed_shape_resizer": {
                            "height": 600,
                            "width": 600,
                            "resize_method": "BICUBIC",
                        }
                    }
                },
                "dropout_keep_prob": 0.5,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.002,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.002,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.EFFICIENTNET_B8,
        {
            "trainer": {
                "batch_size": 1,
                "initial_learning_rate": 0.001,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {
                    "input.image_resizer": {
                        "fixed_shape_resizer": {
                            "height": 672,
                            "width": 672,
                            "resize_method": "BICUBIC",
                        }
                    }
                },
                "dropout_keep_prob": 0.5,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.001,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.001,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.EFFICIENTNET_L2,
        {
            "trainer": {
                "batch_size": 1,
                "initial_learning_rate": 0.001,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {
                    "input.image_resizer": {
                        "fixed_shape_resizer": {
                            "height": 800,
                            "width": 800,
                            "resize_method": "BICUBIC",
                        }
                    }
                },
                "dropout_keep_prob": 0.5,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.001,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.001,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
]

backbones_tagging = [
    (
        bb.VGG_11,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.01,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 0.5,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.VGG_16,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.005,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 0.5,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.005,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.005,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.VGG_19,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.0025,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },

            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 0.5,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.0025,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.0025,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.INCEPTION_V1,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.01,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 0.8,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 4e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.INCEPTION_V2,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.0025,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 0.8,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 1e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.0025,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.0025,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.INCEPTION_V3,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.005,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(299, 299)},
                "dropout_keep_prob": 0.8,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 3e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.005,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.005,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.INCEPTION_V4,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.005,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(299, 299)},
                "dropout_keep_prob": 0.8,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 4e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.005,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.005,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.INCEPTION_RESNET_V2,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.005,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },

            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(299, 299)},
                "dropout_keep_prob": 0.8,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 4e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.005,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.005,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.RESNET_50_V1,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.01,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 1.0,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 9e-6,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),  # TODO: try with dropout ?
    (
        bb.RESNET_101_V1,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.01,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 1.0,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 5e-6,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.RESNET_152_V1,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.01,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 1.0,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 3e-6,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.RESNET_50_V2,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.025,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 1.0,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 2e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.025,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.025,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.RESNET_101_V2,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.01,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 1.0,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 2e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.RESNET_152_V2,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.0025,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 1.0,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 6e-6,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.0025,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.0025,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.MOBILENET_V1,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.01,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 0.999,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 1e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.MOBILENET_V1_075,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.01,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 0.999,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 1e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.MOBILENET_V1_050,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.01,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 0.999,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 1e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.MOBILENET_V1_025,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.01,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 0.999,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 1e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.MOBILENET_V2,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.01,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 1.0,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 1.5e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),  # TODO: try with dropout ?
    (
        bb.MOBILENET_V2_140,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.01,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 1.0,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 1.5e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.NASNET_MOBILE,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.01,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 0.5,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.NASNET_LARGE,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.01,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(331, 331)},
                "dropout_keep_prob": 0.5,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.PNASNET_MOBILE,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.01,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(224, 224)},
                "dropout_keep_prob": 0.5,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.PNASNET_LARGE,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.01,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {"input.image_resizer": fixed_shape_resizer(331, 331)},
                "dropout_keep_prob": 0.5,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.EFFICIENTNET_B0,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.032,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {
                    "input.image_resizer": {
                        "fixed_shape_resizer": {
                            "height": 224,
                            "width": 224,
                            "resize_method": "BICUBIC",
                        }
                    }
                },
                "dropout_keep_prob": 0.8,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 2e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.032,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.032,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.EFFICIENTNET_B1,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.032,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {
                    "input.image_resizer": {
                        "fixed_shape_resizer": {
                            "height": 240,
                            "width": 240,
                            "resize_method": "BICUBIC",
                        }
                    }
                },
                "dropout_keep_prob": 0.8,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 2e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.032,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.032,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.EFFICIENTNET_B2,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.032,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {
                    "input.image_resizer": {
                        "fixed_shape_resizer": {
                            "height": 260,
                            "width": 260,
                            "resize_method": "BICUBIC",
                        }
                    }
                },
                "dropout_keep_prob": 0.7,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 2e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.032,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.032,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.EFFICIENTNET_B3,
        {
            "trainer": {
                "batch_size": 32,
                "initial_learning_rate": 0.032,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {
                    "input.image_resizer": {
                        "fixed_shape_resizer": {
                            "height": 300,
                            "width": 300,
                            "resize_method": "BICUBIC",
                        }
                    }
                },
                "dropout_keep_prob": 0.7,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 2e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.032,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.032,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.EFFICIENTNET_B4,
        {
            "trainer": {
                "batch_size": 16,
                "initial_learning_rate": 0.016,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {
                    "input.image_resizer": {
                        "fixed_shape_resizer": {
                            "height": 380,
                            "width": 380,
                            "resize_method": "BICUBIC",
                        }
                    }
                },
                "dropout_keep_prob": 0.6,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 2e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.016,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.016,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.EFFICIENTNET_B5,
        {
            "trainer": {
                "batch_size": 8,
                "initial_learning_rate": 0.008,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {
                    "input.image_resizer": {
                        "fixed_shape_resizer": {
                            "height": 456,
                            "width": 456,
                            "resize_method": "BICUBIC",
                        }
                    }
                },
                "dropout_keep_prob": 0.6,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.01,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.008,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.008,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.EFFICIENTNET_B6,
        {
            "trainer": {
                "batch_size": 4,
                "initial_learning_rate": 0.004,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {
                    "input.image_resizer": {
                        "fixed_shape_resizer": {
                            "height": 528,
                            "width": 528,
                            "resize_method": "BICUBIC",
                        }
                    }
                },
                "dropout_keep_prob": 0.5,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "nadam_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 2e-5,
                        "learning_rate_policy": {"one_cycle_learning_rate": {}},
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.004,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.004,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.EFFICIENTNET_B7,
        {
            "trainer": {
                "batch_size": 2,
                "initial_learning_rate": 0.002,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {
                    "input.image_resizer": {
                        "fixed_shape_resizer": {
                            "height": 600,
                            "width": 600,
                            "resize_method": "BICUBIC",
                        }
                    }
                },
                "dropout_keep_prob": 0.5,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.002,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.002,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.EFFICIENTNET_B8,
        {
            "trainer": {
                "batch_size": 1,
                "initial_learning_rate": 0.001,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {
                    "input.image_resizer": {
                        "fixed_shape_resizer": {
                            "height": 672,
                            "width": 672,
                            "resize_method": "BICUBIC",
                        }
                    }
                },
                "dropout_keep_prob": 0.5,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.001,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.001,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    (
        bb.EFFICIENTNET_L2,
        {
            "trainer": {
                "batch_size": 1,
                "initial_learning_rate": 0.001,
                "optimizer": {"momentum_optimizer": {}},
                "learning_rate_policy": {
                    "manual_step_learning_rate": {
                        "schedule": [
                            {"learning_rate_factor": 0.1, "step_pct": 0.33},
                            {"learning_rate_factor": 0.01, "step_pct": 0.66},
                        ]
                    }
                },
            },
            "@model": {
                "backbone": {
                    "input.image_resizer": {
                        "fixed_shape_resizer": {
                            "height": 800,
                            "width": 800,
                            "resize_method": "BICUBIC",
                        }
                    }
                },
                "dropout_keep_prob": 0.5,
            },
        },
        [
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "momentum_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.001,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
            {
                "field": "trainer.optimizer.optimizer",
                "triggering_value": "rms_prop_optimizer",
                "target_value": {
                    "trainer": {
                        "initial_learning_rate": 0.001,
                        "learning_rate_policy": {
                            "manual_step_learning_rate": {
                                "schedule": [
                                    {"learning_rate_factor": 0.1, "step_pct": 0.33},
                                    {"learning_rate_factor": 0.01, "step_pct": 0.66},
                                ]
                            }
                        },
                    }
                },
            },
        ],
    ),
    # (bb.RESNET_200_V1, {'trainer': {'batch_size': 32, 'initial_learning_rate': 0.01}, '@model': {'backbone': {'input.image_resizer': fixed_shape_resizer(224, 224)}, 'dropout_keep_prob': 1.}},
    # [
    #     {
    #         'field': 'optimizer',
    #         'triggering_value': 'nadam_optimizer',
    #         'target_value': {'trainer': {
    #             'initial_learning_rate':2e-5,
    #             'learning_rate_policy': {'one_cycle_learning_rate': {}},  ]
    # ),
    #     {
    #         'field': 'optimizer',
    #         'triggering_value': 'momentum_optimizer',
    #         'target_value': {'trainer': {
    #             'initial_learning_rate': 0.032,
    #             'learning_rate_policy': {"manual_step_learning_rate": {"schedule": [{"learning_rate_factor": 0.1, "step_pct": 0.33}, {"learning_rate_factor": 0.01, "step_pct": 0.66}]}},
    #         }}
    #     },
    # ]
    # ),
    # (bb.RESNET_200_V2, {'trainer': {'batch_size': 32, 'initial_learning_rate': 0.01}, '@model': {'backbone': {'input.image_resizer': fixed_shape_resizer(224, 224)}, 'dropout_keep_prob': 1.}},
    # [
    #     {
    #         'field': 'optimizer',
    #         'triggering_value': 'nadam_optimizer',
    #         'target_value': {'trainer': {
    #             'initial_learning_rate':2e-5,
    #             'learning_rate_policy': {'one_cycle_learning_rate': {}},  ]
    # #
    #     {
    #         'field': 'optimizer',
    #         'triggering_value': 'momentum_optimizer',
    #         'target_value': {'trainer': {
    #             'initial_learning_rate': 0.032,
    #             'learning_rate_policy': {"manual_step_learning_rate": {"schedule": [{"learning_rate_factor": 0.1, "step_pct": 0.33}, {"learning_rate_factor": 0.01, "step_pct": 0.66}]}},
    #         }}
    #     },
    # ]
    # ),
]

common_args = {
    "@model.backbone.input.data_augmentation_options": [
        {"random_horizontal_flip": {"keypoint_flip_permutation": []}}
    ],
}

softmax_classifier = ModelConfig(
    display_name="Softmax",
    args=dict_inject(
        common_args, {"@model.loss": {"weighted_softmax": {"logit_scale": 1.0}}}
    ),
    switch_args=[],
)
for backbone, args, switch_args in backbones_classification:
    softmax_classifier.add_backbone(backbone, args=args, switch_args=switch_args)

sigmoid_classifier = ModelConfig(
    display_name="Sigmoid",
    args=dict_inject(
        common_args,
        {"@model.loss": {"weighted_sigmoid": {}}},
    ),
)
for backbone, args, switch_args in backbones_tagging:
    sigmoid_classifier.add_backbone(backbone, args=args, switch_args=switch_args)

configs = [softmax_classifier, sigmoid_classifier]
