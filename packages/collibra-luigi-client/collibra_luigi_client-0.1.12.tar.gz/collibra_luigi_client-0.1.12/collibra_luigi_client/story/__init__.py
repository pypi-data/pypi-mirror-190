import json
import logging

import luigi

from collibra_luigi_client.plot import Plot


class Story(luigi.Task):
    runner = luigi.Parameter()
    request = luigi.Parameter()

    def requires(self):
        logger = logging.getLogger(__name__)

        thePlot = self.runner.plot if self.runner.plot else Plot

        logger.debug(f"plot: {thePlot}")

        return thePlot(runner=self.runner, request=self.request)


    def output(self):
        return luigi.LocalTarget("stage/{}.story.json".format(json.loads(self.request)["Id"])) 


    def run(self):
        logger = logging.getLogger(__name__)

        with self.output().open("w") as outfile:  
            outfile.write("Once upon a time..") 

        logger.info(f"writing story output file: {outfile.name}")
        