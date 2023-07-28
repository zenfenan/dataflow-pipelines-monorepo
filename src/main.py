import argparse
import importlib

import tomli


def _parse_args():
    """
    Parse the arguments for the pipeline entry point
    :return: Parsed args as Namespace
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--pipeline_module_name",
        type=str,
        required=True,
        help="Full module path of the pipeline to be run",
    )

    parser.add_argument(
        "--job_name",
        type=str,
        required=True,
        help="Job name to be used when submitting the Dataflow job",
    )

    parser.add_argument(
        "--region",
        type=str,
        default="europe-west1",
        help="Google Cloud region to submit the Dataflow job",
    )

    parser.add_argument(
        "--restart",
        default=False,
        action="store_true",
        help="If provided, an existing Dataflow job with the same --job-name "
        "will be stopped and a new job with the updated code will be "
        "submitted. If no job with the provided job-name is found, it "
        "will error out.",
    )

    parser.add_argument(
        "--config_file",
        type=str,
        help="Config file path",
        default="config.toml",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()

    if "/" in args.pipeline_module_name:
        raise ValueError(
            'pipeline_module_name should be "." separated, not "/". '
            "Ex: src.pipelines.wordcount"
        )

    pipeline_module = importlib.import_module(args.pipeline_module_name)

    if not hasattr(pipeline_module, "run"):
        raise NotImplementedError(
            f"Pipeline [{args.pipeline_module_name}] doesn't have run() method"
        )

    # Load the config
    with open(args.config_file, mode="rb") as fp:
        config = tomli.load(fp)

    job_name = args.job_name

    job_config = config.get(job_name).get("job_config")
    pipeline_config = config.get(job_name).get("pipeline_config")

    if "job_name" not in job_config:
        # Dataflow job name can only contain [-a-z0-9]
        pipeline_config["job_name"] = args.job_name.replace("_", "-")

    if args.restart:
        # Re-start already running Dataflow job with new code
        pipeline_config["update"] = True

    pipeline_config["region"] = args.region

    # Load defaults config
    defaults_config = config.get("defaults")

    # Merge the job specific Dataflow pipeline config with
    # the default pipeline configs
    pipeline_config = {**defaults_config, **pipeline_config}

    pipeline_run_fn = getattr(pipeline_module, "run")

    pipeline_run_fn(job_config=job_config, pipeline_config=pipeline_config)
