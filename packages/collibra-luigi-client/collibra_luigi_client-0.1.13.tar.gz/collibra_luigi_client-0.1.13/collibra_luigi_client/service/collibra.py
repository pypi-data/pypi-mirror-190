import base64
import json
import logging

from collibra_core import (ApiClient, ApplicationApi, AssetsApi, CommunitiesApi, Configuration, OutputModuleApi, JobsApi)
from collibra_importer import ImportApi
from cryptography.fernet import Fernet

from collibra_luigi_client.model.community import Community
from collibra_luigi_client.model.domain import Domain
from collibra_luigi_client.model.entry import Entry
from collibra_luigi_client.model.identifier import Identifier
from collibra_luigi_client.model.type import Type


class CollibraClient:
    def __init__(self, runner):
        logger = logging.getLogger(__name__)

        try:
            viewConfig = runner.viewConfig if runner.viewConfig else "viewConfig.json"

            with open(viewConfig, "r") as file:
                self.__viewConfig = json.loads(file.read())

        except IOError as e:
            logger.error(f"no such file or directory [{e.filename}]")
            raise (e)

        except json.JSONDecodeError as e:
            logger.error("viewConfig json decode error")
            raise (e)

        except Exception as e:
            pass

        configuration = Configuration()

        try:
            configuration.host = runner.config['collibra']['url']

            configuration.username = runner.config['collibra']['username']

            configuration.password = None

        except Exception as e:
            logger.error(f"invalid collibra configuration [{e.args[0]}]")
            raise (e)

        try:
            fernet = Fernet(base64.urlsafe_b64encode((f"{runner.config['runner']['config']['security']['key']}.plusanystringtomakeitmorecomplextoguess")[:32].encode()))

            configuration.password = fernet.decrypt(f"{runner.config['collibra']['password']}".encode()).decode()

        except KeyError as e:
            logger.error(f"invalid collibra configuration [{e.args[0]}]")
            raise (e)

        except Exception as e:
            logger.error("signature did not match digest [invalid token]")
            raise (e)

        self.__client = ApiClient(configuration)

        self.__client.user_agent = 'collibra-runner'

        self.info

    @property
    def client(self):
        return self.__client

    @property
    def info(self):
        logger = logging.getLogger(__name__)

        try:
            response = ApplicationApi(self.__client).get_info()

        except Exception as e:
            logger.error("failed to authenticate request [configuration]")
            raise (e)

        try:
            logger.debug(f"fullversion: {response.version.full_version}")

        except Exception as e:
            logger.error("failed to authenticate request [configuration]")
            raise (e)

        logger.debug(f"buildnumber: {response.build_number}")

        return response

    @property
    def view(self):
        logger = logging.getLogger(__name__)

        try:
            body = self.__viewConfig

            response = OutputModuleApi(self.__client).export_json(validation_enabled=False, body=body)

            response = json.loads(response.replace("'", '"'))

            return response["view"]["Assets"]

        except Exception as e:
            logger.error("viewconfig wrong or no view assets found")
            raise (e)

    @property
    def viewConfig(self):
        return self.__viewConfig


    def get_asset(self, uuid: str):
        logger = logging.getLogger(__name__)

        try:
            response = AssetsApi(self.__client).get_asset(asset_id=uuid)

            return response.to_dict()

        except Exception as e:
            logger.error("asset id wrong or no asset found")
            raise (e)


    def get_community(self, uuid: str):
        logger = logging.getLogger(__name__)

        try:
            response = CommunitiesApi(self.__client).get_community(community_id=uuid)

            return response.to_dict()

        except Exception as e:
            logger.error("community id wrong or no asset found")
            raise (e)
        

    def get_job(self, uuid: str):
        logger = logging.getLogger(__name__)

        try:
            response = JobsApi(self.__client).get_job(job_id=uuid)

            return response.to_dict()

        except Exception as e:
            logger.error("job id wrong or no job found")
            raise (e)


    def get_import_entry(self, entryName: str = None, entryType: str = None, resourceType: str = None, domainName: str = None, communityName: str = None, attributes: list = None, relations: list = None, tags: list = None, status: str = None):
        type = Type(name=entryType)

        identifier = self.get_import_entry_identifier(name=entryName, domainName=domainName, communityName=communityName)

        return Entry(resourceType=resourceType, identifier=identifier, type=type, displayName=entryName, attributes=attributes, relations=relations, tags=tags, status=status)


    def get_import_entry_identifier(self, name: str = None, domainName: str = None, communityName: str = None):
        community = Community(name=communityName)

        domain = Domain(name=domainName, community=community) if domainName else None

        return Identifier(name=name, domain=domain, community=None if domain else community)


    def import_json_in_job(self, filename:str = None):
        logger = logging.getLogger(__name__)

        try:
            response = ImportApi(self.__client).import_json_in_job(file=filename, file_name=filename)

            return response.to_dict()

        except Exception as e:
            logger.error("file wrong or no file found")
            raise (e)
