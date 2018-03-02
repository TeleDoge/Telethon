from abc import ABC, abstractmethod
import time
import platform


class Session(ABC):
    def __init__(self):
        self._sequence = 0
        self._last_msg_id = 0
        self._time_offset = 0

        system = platform.uname()
        self._device_model = system.system or 'Unknown'
        self._system_version = system.release or '1.0'
        self._app_version = '1.0'
        self._lang_code = 'en'
        self._system_lang_code = self.lang_code
        self._report_errors = True
        self._flood_sleep_threshold = 60

    def clone(self):
        cloned = self.__class__()
        cloned._device_model = self.device_model
        cloned._system_version = self.system_version
        cloned._app_version = self.app_version
        cloned._lang_code = self.lang_code
        cloned._system_lang_code = self.system_lang_code
        cloned._report_errors = self.report_errors
        cloned._flood_sleep_threshold = self.flood_sleep_threshold

    @abstractmethod
    def set_dc(self, dc_id, server_address, port):
        raise NotImplementedError

    @property
    @abstractmethod
    def server_address(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def port(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def auth_key(self):
        raise NotImplementedError

    @auth_key.setter
    @abstractmethod
    def auth_key(self, value):
        raise NotImplementedError

    @property
    def time_offset(self):
        return self._time_offset

    @time_offset.setter
    def time_offset(self, value):
        self._time_offset = value

    @property
    @abstractmethod
    def salt(self):
        raise NotImplementedError

    @salt.setter
    @abstractmethod
    def salt(self, value):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError

    @abstractmethod
    def save(self):
        raise NotImplementedError

    @abstractmethod
    def delete(self):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def list_sessions(cls):
        raise NotImplementedError

    @abstractmethod
    def process_entities(self, tlo):
        raise NotImplementedError

    @abstractmethod
    def get_input_entity(self, key):
        raise NotImplementedError

    @abstractmethod
    def cache_file(self, md5_digest, file_size, instance):
        raise NotImplementedError

    @abstractmethod
    def get_file(self, md5_digest, file_size, cls):
        raise NotImplementedError

    @property
    def device_model(self):
        return self._device_model

    @property
    def system_version(self):
        return self._system_version

    @property
    def app_version(self):
        return self._app_version

    @property
    def lang_code(self):
        return self._lang_code

    @property
    def system_lang_code(self):
        return self._system_lang_code

    @property
    def report_errors(self):
        return self._report_errors

    @property
    def flood_sleep_threshold(self):
        return self._flood_sleep_threshold

    @property
    def sequence(self):
        return self._sequence

    def get_new_msg_id(self):
        """Generates a new unique message ID based on the current
           time (in ms) since epoch"""
        now = time.time() + self._time_offset
        nanoseconds = int((now - int(now)) * 1e+9)
        new_msg_id = (int(now) << 32) | (nanoseconds << 2)

        if self._last_msg_id >= new_msg_id:
            new_msg_id = self._last_msg_id + 4

        self._last_msg_id = new_msg_id

        return new_msg_id

    def update_time_offset(self, correct_msg_id):
        now = int(time.time())
        correct = correct_msg_id >> 32
        self._time_offset = correct - now
        self._last_msg_id = 0

    def generate_sequence(self, content_related):
        if content_related:
            result = self._sequence * 2 + 1
            self._sequence += 1
            return result
        else:
            return self._sequence * 2
