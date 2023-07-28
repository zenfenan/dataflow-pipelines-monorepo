# Dataflow Pipelines Monorepo
A template repository to structure Dataflow pipelines as a monorepo. This is intended to be used as a reference and to bootstrap new repo to develop and maintain Dataflow pipelines.
## Structure
```
├── src                      <- Instead of 'src', use a proper 'root' package name like your company
│   ├── common               <- Package for common re-usable code
│       ├── io.py            <- module for reusable IO related code, like custom source/sink operator
│       ├── transforms.py    <- module for reusable non-io transormation function code
│       ├── ...
│       ├── ...
│       ├── utils.py         <- module for any other util functions
│   ├── pipelines
│       ├── pipeline_1.py    <- Dataflow pipeline
│       ├── ...           
│       ├── ...
│       ├── pipeline_N.py    <- Dataflow pipeline
│   ├── main.py              <- Single entry point that runs/triggers the actual pipeline
├── config.toml          <- Config file containing Pipelines' config
├── setup.py                 <- setup.py to be used for packaging the pipelines (Refer --setup_file options)
├── devops                   <- Directory containing any devops scripts
│   ├── scripts
│       ├── deploy.sh           
│
├── docs                     <- Directory for any documentations
│   ├── ...                 
├── tests                    <- Project pytest unittest modules.
└── README.md                <- Top-level README for developers using this project.
```
