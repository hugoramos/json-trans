import json
from google.cloud import translate
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "trilogo-usa-478c47cc7c47.json"

file = 'pt-BRcopy.json'
line = 2803

# Current line of file
line = 0


def translate_text(text):

    project_id = "trilogo-usa"
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": "pt-BR",
            "target_language_code": "en-US",
        }
    )

    # return 'string'

    for translation in response.translations:
        return translation.translated_text


def json_loop(resource_string, data):
    global line

    count = 0
    resource_string += '{'

    for key in data:
        line = line + 1
        if (line % 50 == 0):
            print('Line:', line)

        count = count + 1

        if not (isinstance(data[key], dict)):
            resource_string += '"' + key + '":"' + \
                translate_text(text=data[key]) + '"'
            if (count < len(data)):
                resource_string += ','
        else:
            resource_string += '"' + key + '":'
            # print(data[key])
            resource_string = json_loop(resource_string, data[key])
            resource_string += '}'
            if (count < len(data)):
                resource_string += ','

    return resource_string


print('Reading file:', file)

f = open(file, encoding="utf-8")


data = json.load(f)

resource_string = json_loop('', data)

f.close()

resource_string += '}'

# print(resource_string)

with open("sample.json", "w") as outfile:
    outfile.write(resource_string)


# # convert string to  object
# dictionary = json.loads(resource_string)
# json_object = json.dumps(dictionary, indent=4, ensure_ascii=False)

# # print(json_object)
# # # Writing to sample.json
# with open("sample.json", "w") as outfile:
#     outfile.write(json_object)
