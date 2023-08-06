from dataclasses import dataclass


@dataclass
class Geo:
    lat: str
    lng: str


@dataclass
class Adress:
    street: str
    suite: str
    city: str
    zipcode: str
    geo: Geo


@dataclass
class Company:
    name: str
    catch_phrase: str
    bs: str
