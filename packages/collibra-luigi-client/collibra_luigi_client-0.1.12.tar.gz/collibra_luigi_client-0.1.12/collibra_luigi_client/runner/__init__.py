import argparse
import logging
import logging.config

import luigi
import toml
from dotenv import dotenv_values, load_dotenv

from collibra_luigi_client.finale import Finale
from collibra_luigi_client.plot import Plot
from collibra_luigi_client.service.collibra import CollibraClient
from collibra_luigi_client.story import Story


class Runner:
    def __init__(self, argv: list = None, finale: Finale = None, story: Story = None, plot: Plot = None):
        self.__plot = plot

        self.__story = story

        self.__finale = finale

        self.__env = dotenv_values(".env")

        load_dotenv()

        parser = argparse.ArgumentParser()

        parser.add_argument(
            "--config",
            dest="config",
            required=True,
            help="path to the configuration file")

        parser.add_argument(
            "--workers",
            dest="workers",
            required=False,
            type=int,
            default=1,
            help="number of workers (default: 1)")

        parser.add_argument(
            "--local-scheduler",
            dest="local_scheduler",
            required=False,
            default=False,
            action='store_true',
            help="local scheduler")

        self.__args, self.__opts = parser.parse_known_args(argv)

        self.__config = toml.load(self.__args.config)

        fname = self.__config['runner']['config']['logging']['location']

        logging.config.fileConfig(fname=fname, disable_existing_loggers=True)

        self.__viewConfig = None
        try:
            self.__viewConfig = self.__config['runner']['config']['viewconfig']['location']
        except Exception as e:
            pass

        self.__collibraClient = CollibraClient(self)


    @property
    def args(self):
        return self.__args

    @property
    def collibraClient(self):
        return self.__collibraClient

    @property
    def config(self):
        return self.__config

    @property
    def env(self):
        return self.__env

    @property
    def finale(self):
        return self.__finale

    @property
    def opts(self):
        return self.__opts

    @property
    def plot(self):
        return self.__plot

    @property
    def story(self):
        return self.__story

    @property
    def viewConfig(self):
        return self.__viewConfig


    def run(self):
        logger = logging.getLogger(__name__)

        logger.info(f"config: {self.args.config}")

        logger.info(f"workers: {self.__args.workers}, local_scheduler: {self.__args.local_scheduler}")

        theFinale = self.__finale if self.__finale else Finale

        logger.debug(f"finale: {theFinale}")

        luigi.build([theFinale(runner=self)], workers=self.__args.workers, local_scheduler=self.__args.local_scheduler)

        logger.info("done")
