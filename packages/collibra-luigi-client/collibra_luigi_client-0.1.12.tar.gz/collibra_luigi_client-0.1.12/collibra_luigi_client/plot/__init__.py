import json
import logging

import luigi


class Plot(luigi.Task):
    runner = luigi.Parameter()
    request = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget("stage/{}.plot.json".format(json.loads(self.request)["Id"])) 


    def run(self):
        logger = logging.getLogger(__name__)
        
        with self.output().open("w") as outfile:
            outfile.write(self.request)
            
        logger.info(f"writing plot output file {outfile.name}")
        