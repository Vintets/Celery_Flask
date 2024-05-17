"""работа с файлами ini"""

import configparser
import time


class Ini():
    def __init__(self, filename) -> None:
        self.filename = filename
        self.rewrite = False
        self.parser = configparser.RawConfigParser()
        self.read_ini()
        time.sleep(0.06)

    def new_ini(self) -> None:
        with open(self.filename, 'w', encoding='utf-8') as f:
            text = ''
            # text = '[default]\n\n'
            f.write(text)
        time.sleep(0.06)

    def read_ini(self) -> None:
        if not self.filename.is_file():
            self.new_ini()
        """
        while (time.time() - self.filename.stat().st_atime) < 0.06:
            time.sleep(0.02)
            print('Файл {} занят! {:.17}'.format(self.filename, time.time() - self.filename.stat().st_atime))
        with open(self.filename, 'r', encoding='utf-8') as f:
            f.read()
        """
        self.parser.read(self.filename)
        self.rewrite = False

    def set_name_section(self, section: str) -> bool:
        if self.parser.has_section(section):
            self.sect = section
            return True
        return False

    def set_name_section_or_add(self, section: str) -> None:
        self.sect = section
        if not self.parser.has_section(section):
            self.add_section(section)

    def work_section(self) -> str:
        return self.sect

    def get_sections(self) -> list[str]:
        return self.parser.sections()

    def get_param(self, param: str) -> str | None:
        if param in self.parser.options(self.sect):
            return self.parser.get(self.sect, param)
        return None

    def get_boolean_param(self, param: str) -> bool | None:
        if param in self.parser.options(self.sect):
            return self.parser.getboolean(self.sect, param)
        return None

    def get_allparam(self) -> list[tuple[str, str]]:
        return self.parser.items(self.sect)

    def set_param(self, param: str, value: any) -> None:
        self.parser.set(self.sect, param, value)
        self.rewrite = True

    def set_param_dict(self, dict_: dict) -> None:
        for key in dict_.keys():
            dat = self.get_param(key)
            if dat and (dat == str(dict_[key])):
                continue
            self.rewrite = True
            self.parser.set(self.sect, key, dict_[key])

    def add_section(self, param: str) -> None:
        try:
            self.parser.add_section(param)
            self.rewrite = True
        except configparser.DuplicateSectionError:
            # print(f"Секция '{param}' уже есть")
            pass
        except Exception:
            print(f"Не смог записать секцию '{param}' в файл")  # noqa: T201

    def remove_option(self, param: str) -> None:
        self.parser.remove_option(self.sect, param)
        self.rewrite = True

    def remove_section(self, param: str) -> None:
        self.parser.remove_section(self.sect, param)
        self.rewrite = True

    def save(self) -> None:
        if self.rewrite:
            with open(self.filename, 'w', encoding='utf-8') as fp:
                self.parser.write(fp)
            self.rewrite = False

    def print_ini(self) -> None:
        for sec in self.get_sections():
            self.set_name_section(sec)
            print(sec)  # noqa: T201
            print(self.get_allparam())  # noqa: T201


# filter(lambda s: s != 'global_settings', self.parser.sections())

"""
try:
except configparser.NoOptionError:
except configparser.NoSectionError:
except configparser.DuplicateSectionError
"""

# .getfloat
# .getint
# .getboolean
