import os
import threading
import queue
import pkg_resources

import scrapeit
from ruamel import yaml

from horoscope_scraper.exceptions import SignNotFound


class GetReadings():
    """ This class returns text using websites from the config """
    def __init__(self, sign):
        """
        :param sign: String zodiac sign
        """
        self.sign = self.set_sign(sign)
        self.config = self.set_config()
        self.max_threads = 10
        self.q = queue.Queue()
        self.readings = {}
        self.threads = []

    @staticmethod
    def get_valid_signs():
        """
        List of valid zodiac signs
        :return: List
        """
        return [
            "aries",
            "taurus",
            "gemini",
            "cancer",
            "leo",
            "virgo",
            "libra",
            "scorpio",
            "sagittarius",
            "capricorn",
            "aquarius",
            "pisces"
        ]

    def set_sign(self, sign):
        """
        Validates sign and returns it
        :param sign: String zodiac sign
        :return: String sign if it real zodiac sign
        """
        available_sings = self.get_valid_signs()
        if sign.lower() in available_sings:
            return sign.lower()
        else:
            raise SignNotFound(SignNotFound.__doc__)

    @staticmethod
    def set_config():
        """
        This opens the configuration file and returns the
        parsed content
        :return: Dict config to drive web scraping
        """
        config_file = pkg_resources.resource_filename(
            __name__,
            'config/pages.yaml'
        )
        with open(config_file) as file:
            config = yaml.safe_load(file)
        return config

    def worker(self):
        """
        Thread worker function to retrieve text from web page
        :return: None
        """
        while True:
            item = self.q.get()
            if item is None:
                break
            domain = item
            self.get_text_from_scrapeit(domain)
            self.q.task_done()

    def get_text_from_scrapeit(self, domain):
        """
        Uses scrapeit to retrieve text from web page
        :param domain: String key for URL in config
        :return: None
        """
        self.readings[domain] = scrapeit.get_text(self.sign, **self.config[domain])

    def get_readings(self):
        """
        Use this method to retrieve text from the web
        pages specified in config/pages.yaml
        :return: String text from website
        """
        self.populate_queue()
        self.spawn_workers()
        self.q.join()
        self.cleanup_queue()
        self.cleanup_threads()
        return self.readings

    def cleanup_threads(self):
        """
        Blocks until threads are completed
        :return: None
        """
        for t in self.threads:
            t.join()

    def cleanup_queue(self):
        """
        Clears queue
        :return: None
        """
        for i in range(self.max_threads):
            self.q.put(None)

    def spawn_workers(self):
        """
        Spawns worker threads
        :return: None
        """
        for i in range(self.max_threads):
            t = threading.Thread(target=self.worker)
            t.start()
            self.threads.append(t)

    def populate_queue(self):
        """
        Adds domain key to the queue
        :return: None
        """
        for domain_key in self.config:
            self.q.put(domain_key)
