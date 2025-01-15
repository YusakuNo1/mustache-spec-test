import chevron
import json
import importlib

def readFile(filePath, type):
    if type == "text":
        with open(filePath, "r") as file:
            return file.read()
    elif type == "json":
        with open(filePath, "r") as file:
            return json.load(file)
    elif type == "lambdas-py":
        data_module = importlib.import_module(filePath.replace("/", "."))
        return data_module.data
    else:
        raise Exception("Unknown type")
    
def exec(folderName, inputTypes, inputSubTemplateKey):
    types = inputTypes if inputTypes else ["text", "json", "text"]
    template = readFile(f"{folderName}/template.mustache", types[0])
    data = readFile(f"{folderName}/data", types[1])
    subTemplate = readFile(f"{folderName}/sub_template.mustache", types[2]) if inputSubTemplateKey else None

    print("------------------------------------------------\n")
    print(f"[{folderName}]")
    if inputSubTemplateKey:
        partials_dict = { inputSubTemplateKey: subTemplate } if inputSubTemplateKey else {}
        result = chevron.render(template=template, data=data, partials_dict=partials_dict)
        print("Result:\n\n", result)
        return result
    else:
        result = chevron.render(template, data)
        print("Result:\n\n", result)
        return result

sampleInfoArray = [
    { "folderName": "synopsis" },
    { "folderName": "tags" },
    { "folderName": "implicitIterator", "types": ["text", "text"] },
    { "folderName": "lambdas", "types": ["text", "lambdas-py"] },
    { "folderName": "sectionsFalseValuesOrEmptyLists" },
    { "folderName": "sectionsNonEmptyLists" },
    { "folderName": "sectionsNonFalseValues" },
    { "folderName": "sectionsInvertedSections" },
    { "folderName": "sectionsComments" },
    { "folderName": "sectionsPartials", "subTemplateKey": "user" },
    # # { "folderName": "sectionDynamicNames", "subTemplateKey": "dynamic" }, # TODO: not working!
]

for sampleInfo in sampleInfoArray:
    exec(sampleInfo["folderName"], sampleInfo.get("types"), sampleInfo.get("subTemplateKey"))
