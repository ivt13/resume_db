import io
import os
import json

class ConfigParser:

    def parse_file(filePath:str) -> dict:

        with open(filePath,'r') as fh:

            config = json.load(fh)

            fh.close()

            return config