#-*- coding:utf-8 -*-

import os

import collections

ME_LOC=os.path.dirname(os.path.abspath(__file__))


class _ParseError(Exception):
    def __init__(self, message, lineno, line):
        self.msg = message
        self.line = line
        self.lineno = lineno

    def __str__(self):
        return 'at line %d, %s: %r' % (self.lineno, self.msg, self.line)


class BaseParser(object):
    lineno = 0
    parse_exc = _ParseError

    def _assignment(self, key, value):
        self.assignment(key, value)
        return None, []

    def _get_section(self, line):
        if line[-1] != ']':
            return self.error_no_section_end_bracket(line)
        if len(line) <= 2:
            return self.error_no_section_name(line)

        return line[1:-1]

    def _split_key_value(self, line):
        colon = line.find(':')
        equal = line.find('=')
        if colon < 0 and equal < 0:
            return self.error_invalid_assignment(line)

        if colon < 0 or (equal >= 0 and equal < colon):
            key, value = line[:equal], line[equal + 1:]
        else:
            key, value = line[:colon], line[colon + 1:]

        return key.strip(), [value.strip()]

    def parse(self, lineiter):
        key = None
        value = []

        for line in lineiter:
            self.lineno += 1

            line = line.rstrip()
            if not line:
                # Blank line, ends multi-line values
                if key:
                    key, value = self._assignment(key, value)
                continue
            elif line[0] in (' ', '\t'):
                # Continuation of previous assignment
                if key is None:
                    self.error_unexpected_continuation(line)
                else:
                    value.append(line.lstrip())
                continue

            if key:
                # Flush previous assignment, if any
                key, value = self._assignment(key, value)

            if line[0] == '[':
                # Section start
                section = self._get_section(line)
                if section:
                    self.new_section(section)
            elif line[0] in '#;':
                self.comment(line[1:].lstrip())
            else:
                key, value = self._split_key_value(line)
                if not key:
                    return self.error_empty_key(line)

        if key:
            # Flush previous assignment, if any
            self._assignment(key, value)

    def assignment(self, key, value):
        """Called when a full assignment is parsed"""
        raise NotImplementedError()

    def new_section(self, section):
        """Called when a new section is started"""
        raise NotImplementedError()

    def comment(self, comment):
        """Called when a comment is parsed"""
        pass

    def error_invalid_assignment(self, line):
        raise self.parse_exc("No ':' or '=' found in assignment",
                             self.lineno, line)

    def error_empty_key(self, line):
        raise self.parse_exc('Key cannot be empty', self.lineno, line)

    def error_unexpected_continuation(self, line):
        raise self.parse_exc('Unexpected continuation line',
                             self.lineno, line)

    def error_no_section_end_bracket(self, line):
        raise self.parse_exc('Invalid section (must end with ])',
                             self.lineno, line)

    def error_no_section_name(self, line):
        raise self.parse_exc('Empty section name', self.lineno, line)


class ParseError(_ParseError):
    def __init__(self, msg, lineno, line, filename):
        super(ParseError, self).__init__(msg, lineno, line)
        self.filename = filename

    def __str__(self):
        return 'at %s:%d, %s: %r' % (self.filename, self.lineno,
                                     self.msg, self.line)


class ConfigParser(BaseParser):
    def __init__(self, filename, sections):
        super(ConfigParser, self).__init__()
        self.filename = filename
        self.sections = sections
        self.section = None

    def parse(self):
        with open(self.filename) as f:
            return super(ConfigParser, self).parse(f)

    def new_section(self, section):
        self.section = section
        self.sections.setdefault(self.section, {})

    def assignment(self, key, value):
        if not self.section:
            raise self.error_no_section()

        self.sections[self.section][key]= '\n'.join(value)

    def parse_exc(self, msg, lineno, line=None):
        return ParseError(msg, lineno, line, self.filename)

    def error_no_section(self):
        return self.parse_exc('Section must be started before assignment',
                              self.lineno)


class MultiConfigParser(object):
    def __init__(self):
        self.sections = {}

    def read(self, config_files):
        read_ok = []

        for filename in config_files:
            parser = ConfigParser(filename, self.sections)

            try:
                parser.parse()
            except IOError:
                continue

            read_ok.append(filename)

        return read_ok

    def get(self, section, name):
        return self.sections[section][name]

class Config(collections.Mapping):

    def __init__(self, files):

        self._parser = MultiConfigParser()
        self._parser.read(files)

    def __getattr__(self, key):

        for _, sect in self._parser.sections.iteritems():
            if key in sect:
                return sect[key]

    def __getitem__(self, key):

        return self.__getattr__(key)

    def __len__(self):

        size = 0
        for _, sect in self._parser.sections.iteritems():
            size +=len(sect)
        return size

    def __iter__(self):
        
        keys = []
        for _, sect in self._parser.sections.iteritems():
            for key in sect:
                keys.append(key)
        for key in sorted(keys):
            yield key

    def get(self, key, section):

        if section in self._parser.sections:
            return self._parser.sections[section][key]


CONF_MAPPING={
        'dev':('default.ini', 'dev.ini'),
        'live':('default.ini', 'live.ini'),
        }


def find_files(files):

    def find_file(file):
        if os.path.exists(file):
            return file
        elif os.path.exists(os.path.join('conf', file)):
            return os.path.join('conf', file)
        elif os.path.exists(os.path.join(ME_LOC, file)):
            return os.path.join(ME_LOC, file)
        else :
            return None

    return filter(lambda x:x is not None , [find_file(f) for f in files])       

def get_cfg(mode=None, conf_mapping=CONF_MAPPING, default='live'):

    conf_files = None
    env_mode = os.environ.get('MODE', None)
    real_mode = mode if mode else env_mode if env_mode else default
    conf_files = conf_mapping[real_mode]
    config = Config(find_files(conf_files))
    return config

CFG=get_cfg()

