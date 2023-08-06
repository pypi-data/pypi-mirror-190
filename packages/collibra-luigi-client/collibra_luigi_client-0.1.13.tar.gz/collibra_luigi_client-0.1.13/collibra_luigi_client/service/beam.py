
import json
import logging
import os
import time

import apache_beam as beam
from apache_beam.coders import Coder
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions

from collibra_luigi_client.service.collibra import CollibraClient


class JsonCoder(Coder):
  def encode(self, x):
    return json.dumps(x).encode("utf-8")

  def decode(self, x):
    return json.loads(x)


class ShapeShifter(beam.DoFn):    
  def process(self, element):
    element_reshaped = {f"{element[0]}" : element[1]}
    
    yield element_reshaped


class BeamClient(beam.DoFn):
    def __init__(self, runner):
        logger = logging.getLogger(__name__)

        self.__config = runner.config

        try:
            self.__workers = runner.config['collibra']['metadata']['jobs']

            self.__seconds_to_wait = runner.config['collibra']['metadata']['seconds_to_wait']

        except Exception as e:
            logger.error(f"invalid collibra configuration [{e.args[0]}]")
            raise (e)

        self.__options = ['--runner', 'DirectRunner', '--direct_running_mode', 'multi_threading', '--direct_num_workers', str(self.__workers)]


    @property
    def config(self):
        return self.__config

    @property
    def options(self):
        return self.__options

    @property
    def workers(self):
        return self.__workers

    @property
    def seconds_to_wait(self):
        return self.__seconds_to_wait


    def run(self):
        logger = logging.getLogger(__name__)

        try:
            with open('stage/finale.json', "r") as infile:
                data = json.loads(infile.read())

        except IOError as e:
            logger.error(f"no such file or directory [{e.filename}]")
            raise (e)

        except json.JSONDecodeError as e:
            logger.error(f"failed to deserialize json document: {infile.name}")
            raise (e)

        except Exception as e:
            logger.error("something went wrong")
            raise (e)

        [self.__run_step_pipeline(self.options, infile.name, data, step) for step in data["steps"]] 

        results = {
            "runId": data["runId"],
            "steps": {}
        }

        if os.path.exists(f'{infile.name}.results'):
            os.remove(f'{infile.name}.results')

        [self.__get_step_results(self.options, infile.name, results, step) for step in data["steps"]] 

        with open(f'{infile.name}.results', "a+") as f:
            f.write(json.dumps(results))


    def __run_step_pipeline(self, options=None, filename=None, data=None, step=None):  
        logger = logging.getLogger(__name__)

        options = PipelineOptions(options)

        options.view_as(SetupOptions).save_main_session = True

        with beam.Pipeline(options=options) as pipeline:
            steps = (
            pipeline
                | "get step" >> beam.Create(data["steps"][step])
                | "run import" >> beam.ParDo(self, self.seconds_to_wait)
                | "group by step" >> beam.GroupBy(lambda s: s["stepNumber"])
                | "shape element" >> beam.ParDo(ShapeShifter())
                | "write json" >> WriteToText(f"{filename}.step.{step}", shard_name_template="", coder=JsonCoder())
            )


    def __get_step_results(self, options=None, filename=None, data=None, step=None):
        logger = logging.getLogger(__name__)

        with open(f"{filename}.step.{step}", "r") as f:
            try:
                o = json.load(f)
                data["steps"].update(o)
                
            except Exception as e:
                pass
            
        os.remove(f"{filename}.step.{step}")

        return data


    def process(self, element, seconds_to_wait):
        logger = logging.getLogger(__name__)

        try:
            filename = f"{element['resourceLocation']}/{'.'.join(element['fileName'].split('.')[:-1])}.{element['stepNumber']}.{element['partNumber']}.json"

            logger.info(f"importing file {filename}")

            try:
                collibraClient = CollibraClient(self)

                response = collibraClient.import_json_in_job(filename=filename)

            except Exception as e:
                print(e)

            state = response['state']
            
            while state != "COMPLETED" and state != "CANCELED" and state != "ERROR":
                time.sleep(int(seconds_to_wait))

                response = collibraClient.get_job(uuid = response['id'])

                state = response['state']
            
            element["job"] = {"id": response['id'], "result": response['result']}
            
        except Exception as e:
            logger.error("invalid collibra configuration")
            element["job"] = None
            
        yield element
        