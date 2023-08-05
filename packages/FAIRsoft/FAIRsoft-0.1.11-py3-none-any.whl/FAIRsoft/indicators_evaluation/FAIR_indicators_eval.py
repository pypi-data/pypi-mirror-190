import sys
import configparser
from munch import munchify
from pymongo import MongoClient

from FAIRsoft.utils import instance


def  connect_to_db(config_file_path):
    # connecting to DB
    config = configparser.ConfigParser()
    config.read(config_file_path)
    DBHOST = config['MONGO_DETAILS']['DBHOST']
    DBPORT = config['MONGO_DETAILS']['DBPORT']
    DATABASE = config['MONGO_DETAILS']['DATABASE']
    TOOLS = config['MONGO_DETAILS']['TOOLS']
    FAIR = config['MONGO_DETAILS']['FAIR']

    connection = MongoClient(DBHOST, int(DBPORT))

    tools = connection[DATABASE][TOOLS]
    fair = connection[DATABASE][FAIR]
    return(tools, fair)


def prepFAIRcomp(instances):
    stdFormats= getFormats(instances)
    return(stdFormats)
    

def getFormats(instances):
    inputs = [a.input for a in instances]
    inputs_ = [a for a in inputs]
    inputsNames = []

    nonSFormats = ['txt', 'text', 'csv', 'tsv', 'tabular', 'xml', 'json', 'nucleotide', 'pdf', 'interval' ]
    for List in inputs_:
        for eachD in List:
            if 'format' in eachD.keys():
                if ' format' not in eachD['format']['term'] and eachD['format']['term'].lstrip() not in nonSFormats:
                    if '(text)' not in eachD['format']['term']:
                        if eachD['format']['term'].lstrip() not in inputsNames:
                            inputsNames.append(eachD['format']['term'].lstrip())
    return(inputsNames)


def convert_dict2instance(tool):
    NewInst = instance(tool['name'], tool['type'], tool['version'])
    NewInst.__dict__ = munchify(tool)
    NewInst.set_super_type()

    return(NewInst)

def computeFAIR(instances, stdFormats):
    for ins in instances:
        ins.generateFAIRMetrics(stdFormats)
        ins.FAIRscores()


def build_indicators_scores(instances):
    print('Saving indicators and scores')
    out_inst_metrics_scr = []
    for ins in instances:
        dic = { **ins.metrics.__dict__, **ins.scores.__dict__ }
        # name, version, type are needed to identify the instance
        dic['name'] = ins.name
        dic['type'] = ins.type
        dic['version'] = ins.version
        out_inst_metrics_scr.append(dic)

    print("Metrics and scores saved")
    return(out_inst_metrics_scr)   

def push_to_db(indicators_scores, fair):
    print('Pushing to DB')
    fair.insert_many(indicators_scores)
    print('Pushed to DB')


def computeScores(tools):
    instances = []

    for tool in tools.find():
        Inst = convert_dict2instance(tool)
        instances.append(Inst)

    global stdFormats
    stdFormats = prepFAIRcomp(instances)

    print('All dicts converted to instances')
    prepFAIRcomp(instances)

    print('Computing indicators and scores ...')
    computeFAIR(instances, stdFormats)

    print("Building objects of instances' indicators and scores (with instance ID) ...")
    indicators_scores = build_indicators_scores(instances)

    return(indicators_scores)

def computeScores_from_list(tools):
    instances = []

    for tool in tools:
        Inst = convert_dict2instance(tool)
        instances.append(Inst)

    global stdFormats
    stdFormats = prepFAIRcomp(instances)

    print('All dicts converted to instances')
    prepFAIRcomp(instances)

    print('Computing indicators and scores ...')
    computeFAIR(instances, stdFormats)

    print("Building objects of instances' indicators and scores (with instance ID) ...")
    indicators_scores = build_indicators_scores(instances)

    return(indicators_scores)


if __name__=='__main__':
    #get config from cmd parameters
    configfile = sys.argv[1]

    tools, fair = connect_to_db(configfile)
    indicators_scores = computeScores(tools)

    push_to_db(indicators_scores, fair)

