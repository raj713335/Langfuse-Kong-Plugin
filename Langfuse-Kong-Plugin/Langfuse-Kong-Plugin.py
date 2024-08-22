#!/usr/bin/env python3
import os
import sys
import kong_pdk.pdk.kong as kong
from langfuse.decorators import observe
from langfuse.openai import openai


Schema = (
    {"OPENAI_API_KEY": {"type": "string"}},
    {"OPENAI_API_MODEL": {"type": "string"}},
    {"LANGFUSE_SECRET_KEY": {"type": "string"}},
    {"LANGFUSE_PUBLIC_KEY": {"type": "string"}},
    {"LANGFUSE_HOST": {"type": "string"}},
)

version = '0.1.0'
priority = 0


# This is an example plugin that uses Python Geocoding

class Plugin(object):
    def __init__(self, config):
        self.config = config

    def access(self, kongs: kong.kong):
        kongs.log.info("##########################  Inside Access Phase ######################################")
        os.environ["OPENAI_API_KEY"] = self.config['OPENAI_API_KEY']
        os.environ["OPENAI_API_MODEL"] = self.config['OPENAI_API_MODEL']
        os.environ["LANGFUSE_SECRET_KEY"] = self.config['LANGFUSE_SECRET_KEY']
        os.environ["LANGFUSE_PUBLIC_KEY"] = self.config['LANGFUSE_PUBLIC_KEY']
        os.environ["LANGFUSE_HOST"] = self.config['LANGFUSE_HOST']

        kongs.log.info("########################## prompt_helper ##########################")

        # define LLM

        body = kongs.request.get_raw_body().replace('\r', '')
        query = kongs.request.get_header("prompt")

        kongs.log.info(body)

        return kongs.response.exit(200, {"message": "OK"})


# add below section to allow this plugin optionally be running in a dedicated process
if __name__ == "__main__":
    from kong_pdk.cli import start_dedicated_server
    start_dedicated_server("Langfuse-Kong-Plugin", Plugin, version, priority, Schema)
