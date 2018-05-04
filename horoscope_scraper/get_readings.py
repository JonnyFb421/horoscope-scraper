import os
import threading
import queue
import pkg_resources

import scrapeit
from ruamel import yaml


class GetReadings():
    def __init__(self, sign):
        self.sign = sign
        self.q = queue.Queue()
        self.threads = []
        self.readings = {}
        self.config = self.set_config()

    def set_config(self):
        config_file = pkg_resources.resource_filename(
            __name__,
            'config/pages.yaml'
        )
        with open(config_file) as file:
            config = yaml.safe_load(file)
        return config

    def worker(self):
        while True:
            item = self.q.get()
            if item is None:
                break
            domain = item
            self.get_text_from_scrapeit(domain)
            self.q.task_done()

    def get_text_from_scrapeit(self, domain):
        self.readings[domain] = scrapeit.get_text(self.sign, **self.config[domain])

    def get_readings(self):
        for domain_key in self.config:
            self.q.put(domain_key)
        for i in range(10):
            t = threading.Thread(target=self.worker)
            t.start()
            self.threads.append(t)
        self.q.join()
        for i in range(10):
            self.q.put(None)
        for t in self.threads:
            t.join()
        return self.readings
