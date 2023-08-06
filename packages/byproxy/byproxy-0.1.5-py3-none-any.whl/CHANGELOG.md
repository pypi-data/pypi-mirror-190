# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Version 0.1.5 - 2023-02-08

### Removed

* split_lines in ProxyMaker class.
* split_line in ProxyMaker class.

### Changed

* ProxyMaker class now uses line_to_dict method to split lines and make dicts. It's more efficient and flexible. It doesn't use keys parameter anymore, it uses the "pattern" parameter to split lines in a given pattern and make a dict from them. It has a default value of "host:port:username:password" and you can change it with Components enum.
* Improved documentation of ProxyMaker class and added some examples.
* Moved async_api.ProxyChecker to proxy_checker and renamed it to AsyncProxyChecker.
* Updated dependencies.

### Added

* Flake8, isort and, black to dev dependencies. Formatted code with black.
* .flake8 file to configure flake8.
* black and isort configuration in pyproject.toml.

## Version 0.1.4 - 2022-12-31

### Added

* async_api for ProxyChecker class.

### Changed

* ProxyChecker file structure is changed. Now it's more moduler.
* Improved documentation of ProxyMaker class and added some expected outputs.
* Improved ProxyMaker make_proxy method, now we can pick a library for making proxies in the format we want.

## Version 0.1.3.3 - 2022-12-26

### Internal

* Updated ProxyChecker class methods, they don't return dict anymore, they make the request and return the response object.

## Version 0.1.3.2 - 2022-12-26

### Fixed

* "make_proxies" method in "ProxyMaker" class was confused with the order of the keys in the dict. It's fixed now.

### Internal

* Removed all print statements.

## Version 0.1.3.1 - 2022-12-26

### Added

* Added new methods to ProxyMaker class:
  * split_line
  * line_to_dict

### Internal

* ProxyMaker class has few updates:
  * split_lines uses split_line method.
  * lines_to_dicts uses line_to_dict method.

## Version 0.1.3 - 2022-12-26

### Added

* Added another method to "ProxyMaker" class. It's called "make_proxy" and it requires a single dict with keys "host", "port", "username" and "password". It returns a single proxy dict.

### Fixed

* "make_proxies" method in "ProxyMaker" class. It had a problem, it requires a list of dict with keys "host", "port", "username" and "password" but used index instead of key.

### Internal

* "make_proxies" method now uses "make_proxy" method to make proxies.

## Version 0.1.2.1 - 2022-12-25

### Fixed

* Dependency conflicts.

## Version 0.1.2 - 2022-12-14

### Added

* CHANGELOG.md
* README.md
* Git Repository
