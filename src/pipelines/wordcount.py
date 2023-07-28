from typing import Any, Dict

import apache_beam as beam
from apache_beam.io import ReadFromPubSub
from apache_beam.options.pipeline_options import PipelineOptions

from src.common.io import *
from src.common.transform import *
from src.common.utils import *

def run(job_config, pipeline_config) -> None:
    """
    A simple Wordcount pipeline that reads from PubSub 
    and writes to either stdout or to an output location.
    """
    with beam.Pipeline(options=options) as pipeline:
        (
            pipeline
            | "Read from PubSub" >> ReadFromPubSub(subscription=job_config["input_subscription"]).with_output_types(bytes)
            | "Print" >> beam.Map(print)
        )
