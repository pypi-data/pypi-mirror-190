import os
import json
import logging
import math

import luigi

from collibra_luigi_client.service.collibra import CollibraClient
from collibra_luigi_client.story import Story


class Finale(luigi.Task):    
    runner = luigi.Parameter()
    
    def requires(self):
        logger = logging.getLogger(__name__)

        requiredProperties = ['jobs', 'entries', 'least_files_strategy', 'location']

        try:
            [self.runner.config['collibra']['metadata'][property] for property in requiredProperties]

        except KeyError as e:
            logger.error(f"invalid collibra metadata configuration [{e.args[0]}]")
            raise (e)

        requests = CollibraClient(self.runner).view

        theStory = self.runner.story if self.runner.story else Story

        logger.debug(f"story: {theStory}")

        stories = [theStory(runner=self.runner, request=json.dumps(request)) for request in requests]  

        return stories


    def output(self):
        return luigi.LocalTarget('stage/finale.json')  # TODO: change


    def run(self):
        logger = logging.getLogger(__name__)
        
        parts = []
        for input in self.input():
            try:
                with input.open() as infile:
                    obj = json.loads(infile.read())

                logger.info(f"reading finale input file {infile.name}")
            except Exception as e:
                continue

            clusters={'Undefined': 0}
            try:
                [[clusters.update({typeName: i}) for typeName in cluster] for i, cluster in enumerate(obj['clusters'])]

                clusters.update({'Undefined': len(obj['clusters'])})
            
            except Exception as e:
                pass

            document = obj['document'] if 'document' in obj else []

            entriesClusters = [[] for i in range(len(obj['clusters'])+1)]

            [self.__get_entry_cluster(entry, clusters, entriesClusters) for entry in document]

            [logger.debug(f"preparing file {infile.name} cluster {cluster:02d} with {len(entries):02d} entries") for cluster, entries in enumerate(entriesClusters)]

            [self.__write_entries_cluster(infile, entriesCluster, entries, parts) for entriesCluster, entries in enumerate(entriesClusters)]


        with self.output().open("w") as outfile:  
            result = dict(runId=None, steps={})

            for part in parts: 
                try:
                    if str(part['stepNumber']) in result['steps']:
                        result['steps'][str(part['stepNumber'])].append(part)
                        
                    else: 
                        result['steps'].update({str(part['stepNumber']):[part]})
 
                except Exception as e:
                    print(e)

            if len(result['steps']):
                outfile.write(json.dumps(result)) 
            else:
                outfile.write("..lived happily ever after.") 

        logger.info(f"writing finale output file: {outfile.name}")


    def __get_entry_cluster(self, entry, clusters, entriesClusters):
        logger = logging.getLogger(__name__)

        logger.debug(f"getting document entry {entry['identifier']['name']} cluster")

        try:
            typeName = f"{entry['resourceType']}:{entry['type']['name']}"

            entryCluster = clusters[typeName] if typeName in clusters else clusters['Undefined']

            entriesClusters[entryCluster].append(entry.copy())

            relationsClusters = [[] for i in range(len(entriesClusters))]

            [self.__get_relation_cluster(relation, clusters, entryCluster, relationsClusters) for relation in entry['relations']]
            
            [self.__get_relations_cluster(entry, entryCluster, relations, relationsCluster, entriesClusters) for relationsCluster, relations in enumerate(relationsClusters)]

        except Exception as e:
            pass


    def __get_relation_cluster(self, relation, clusters, entryCluster, relationsClusters):
        typeName = f"relations:{relation}"

        relationCluster = clusters[typeName] if typeName in clusters else entryCluster

        if relationCluster != entryCluster: relationsClusters[relationCluster].append(relation)


    def __get_relations_cluster(self, entry, entryCluster, relations, relationsCluster,  entriesClusters):
        if not relations: return

        entriesClusters[relationsCluster].append(dict(resourceType=entry['resourceType'], identifier=entry['identifier'], type=entry['type'], relations={}))

        [entriesClusters[relationsCluster][-1]['relations'].update({relation: entry['relations'][relation]}) for relation in relations]

        for relation in relations: del entriesClusters[entryCluster][-1]['relations'][relation]


    def __write_entries_cluster(self, infile, entriesCluster, entries, parts):
        if not len(entries): return
        
        logger = logging.getLogger(__name__)

        metadataJobs = self.runner.config['collibra']['metadata']['jobs'] 

        metadataEntries = self.runner.config['collibra']['metadata']['entries'] 
        
        leastFilesStrategy = self.runner.config['collibra']['metadata']['least_files_strategy']

        locationOfFiles  = self.runner.config['collibra']['metadata']['location'] 

        if leastFilesStrategy:
            numberOfFiles = min(math.ceil(len(entries)/metadataEntries), metadataJobs)
        
        else:
            numberOfFiles = max(math.ceil(len(entries)/metadataEntries), metadataJobs)

        numberOfEntriesPerFile = math.ceil(len(entries)/numberOfFiles)
        
        logger.info(f"preparing file {infile.name} cluster {entriesCluster:02d} with {numberOfEntriesPerFile} entries per file and {numberOfFiles} files")

        for part in range(numberOfFiles):
            fname = f"{locationOfFiles}/{'.'.join(os.path.basename(infile.name).split('.')[:-1])}.{entriesCluster}.{part}.json"

            if entries[0:numberOfEntriesPerFile]:
                with open(fname, "w") as outfile:  
                    outfile.write(json.dumps(entries[0:numberOfEntriesPerFile])) 

                del entries[0:numberOfEntriesPerFile]

                parts.append(dict(stepNumber=entriesCluster, resourceLocation=os.path.dirname(os.path.abspath(outfile.name)), fileName=os.path.basename(infile.name), partNumber=part))
