import re
import enum

class Components(enum.Enum):
    username = r"(?P<username>.*)"
    password = r"(?P<password>.*)"
    host = r"(?P<host>.*)"
    port = r"(?P<port>.*)"
    at = "@"
    colon = ":"

class ProxyMaker:
    def read_lines(self, path):
        """
        Read lines from a file.

        Args:
            path (str): Path to the file.

        Returns:
            list: List of lines.
        
        Usage:
            >>> import os
            >>> from byproxy import ProxyMaker
            >>> basedir = os.path.abspath(os.path.dirname(__name__))
            >>> path = os.path.join(basedir, 'proxies.txt')
            >>> maker = ProxyMaker()
            >>> lines = maker.read_lines(path)
        """
        with open(path, "r") as f:
            return f.read().splitlines()


    def line_to_dict(
        self, 
        line, 
        pattern=[Components.host, Components.colon, Components.port, Components.colon, Components.username, Components.colon, Components.password]
        ):
        """
        Convert a list of lists to a list of dictionaries.

        Args:
            line (list): List of proxy information.
            pattern (list): List of Components in order. Defaults to [Components.host, Components.colon, Components.port, Components.colon, Components.username, Components.colon, Components.password].

        Returns:
            list: List of dictionaries.

        Usage:
            >>> import os
            >>> from byproxy import ProxyMaker
            >>> basedir = os.path.abspath(os.path.dirname(__name__))
            >>> path = os.path.join(basedir, 'proxies.txt')
            >>> maker = ProxyMaker()
            >>> lines = maker.read_lines(path)
            >>> dicts = maker.line_to_dict(lines[0])
        """
        pattern = [p.value if isinstance(p, Components) else p for p in pattern]
        return re.match("".join(pattern), line).groupdict()


    def dict_to_proxy(self, proxy_dict, schema="http", library="requests"):
        """
        Make proxies from a list of dictionaries.

        Args:
            proxy_dict (dict): A dict with keys "host", "port", "username", "password".
            schema (str): Schema of proxies, http, https, ftp etc.
            library (str): Library to use. Defaults to "requests". Options are "requests", "urllib3", "urllib", "aiohttp", "httpx".

        Returns:
            list: List of proxies.

        Usage:
            >>> import os
            >>> from byproxy import ProxyMaker
            >>> basedir = os.path.abspath(os.path.dirname(__name__))
            >>> path = os.path.join(basedir, 'proxies.txt')
            >>> maker = ProxyMaker()
            >>> lines = maker.read_lines(path)
            >>> dict_ = maker.line_to_dict(lines[0])
            >>> proxies = maker.dict_to_proxy(dicts_)
        """
        if (
            library == "requests"
            or library == "urllib3"
            or library == "urllib"
            or library == "aiohttp"
            or library == "selenium-wire"
        ):
            http_protocol = "http"
            https_protocol = "https"
        elif library == "httpx":
            http_protocol = "http://"
            https_protocol = "https://"
        else:
            raise Exception("Invalid library")
        if "username" in proxy_dict and "password" in proxy_dict:
            proxy = { 
                http_protocol: f"{schema}://{proxy_dict['username']}:{proxy_dict['password']}@{proxy_dict['host']}:{proxy_dict['port']}",
                https_protocol: f"{schema}://{proxy_dict['username']}:{proxy_dict['password']}@{proxy_dict['host']}:{proxy_dict['port']}",
            }
        else:
            proxy = { 
                http_protocol: f"{schema}://{proxy_dict['host']}:{proxy_dict['port']}",
                https_protocol: f"{schema}://{proxy_dict['host']}:{proxy_dict['port']}",
            }
        return proxy


    def lines_to_dicts(
        self, 
        lines, 
        pattern=[Components.host, Components.colon, Components.port, Components.colon, Components.username, Components.colon, Components.password]
        ):
        """
        Convert a list of lists to a list of dictionaries.

        Args:
            lines (list): List of lists.
            pattern (list): List of Components in order. Defaults to [Components.host, Components.colon, Components.port, Components.colon, Components.username, Components.colon, Components.password].
        
        Returns:
            list: List of dictionaries.

        Usage:
            >>> import os
            >>> from byproxy import ProxyMaker
            >>> basedir = os.path.abspath(os.path.dirname(__name__))
            >>> path = os.path.join(basedir, 'proxies.txt')
            >>> maker = ProxyMaker()
            >>> lines = maker.read_lines(path)
            >>> dicts = maker.lines_to_dicts(lines)
        """
        return [self.line_to_dict(line, pattern) for line in lines]


    def dicts_to_proxies(self, proxy_dicts, schema="http", library="requests"):
        """
        Make proxies from a list of dictionaries.

        Args:
            proxy_dicts (list): List of dictionaries with keys "host", "port", "username", "password".
            schema (str): Schema of proxy, http or https.

        Returns:
            list: List of proxies.

        Usage:
            >>> import os
            >>> from byproxy import ProxyMaker
            >>> basedir = os.path.abspath(os.path.dirname(__name__))
            >>> path = os.path.join(basedir, 'proxies.txt')
            >>> maker = ProxyMaker()
            >>> lines = maker.read_lines(path)
            >>> dicts = maker.lines_to_dicts(lines)
            >>> proxies = maker.dicts_to_proxies(dicts)
        """
        proxies = []
        for proxy_dict in proxy_dicts:
            proxies.append(self.dict_to_proxy(proxy_dict, schema, library=library))
        return proxies
