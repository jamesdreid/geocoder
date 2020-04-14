#!/usr/bin/python
# coding: utf8

from __future__ import absolute_import

import logging
import requests
import ratelim
from geocoder.keys import ipstack_key

from geocoder.base import OneResult, MultipleResultsQuery




class IPStackResult(OneResult):

    @property
    def lat(self):
        return self.raw.get('latitude')

    @property
    def lng(self):
        return self.raw.get('longitude')

    @property
    def address(self):
        if self.city:
            return u'{0}, {1} {2}'.format(self.city, self.state, self.country)
        elif self.state:
            return u'{0}, {1}'.format(self.state, self.country)
        elif self.country:
            return u'{0}'.format(self.country)
        return u''

    @property
    def postal(self):
        zip_code = self.raw.get('zip_code')
        postal_code = self.raw.get('postal_code')
        zip = self.raw.get('zip')
        if zip_code:
            return zip_code
        if postal_code:
            return postal_code
        if zip:
            return zip

    @property
    def city(self):
        return self.raw.get('city')

    @property
    def type(self):
        return self.raw.get('type')

    @property
    def state(self):
        return self.raw.get('region_code')

    @property
    def state_name(self):
        return self.raw.get('region_name')

    @property
    def region_code(self):
        return self.raw.get('region_code')

    @property
    def region_name(self):
        return self.raw.get('region_name')

    @property
    def country(self):
        return self.raw.get('country_name')

    @property
    def country_code(self):
        return self.raw.get('country_code')

    @property
    def continent_code(self):
        return self.raw.get('continent_code')

    @property
    def continent_name(self):
        return self.raw.get('continent_name')

    @property
    def ip(self):
        return self.raw.get('ip')

    @property
    def location_data(self):
        return self.raw.get('location')

    @property
    def geoname_id(self):
        _location_data = self.raw.get('location')
        if _location_data:
            geoname_id = _location_data['geoname_id']
            return geoname_id

    @property
    def capital(self):
        _location_data = self.raw.get('location')
        if _location_data:
            capital = _location_data['capital']
            return capital





class IpStackQuery(MultipleResultsQuery):
    """
    IPStack.com
    =============
    ipstack.com provides a public HTTP API for software developers to
    search the geolocation of IP addresses. It uses a database of IP addresses
    that are associated to cities along with other relevant information like
    time zone, latitude and longitude.

    You're allowed up to 10,000 queries per month by default, but a free account
    must be created and an API key associated with that account must be used with
    every query.  Once this limit is reached, all of your requests will result
    in HTTP 403, forbidden, until your quota is cleared.

    API Reference
    -------------
    https://ipstack.com/documentation
    """
    provider = 'ipstack'
    method = 'geocode'

    _URL = 'http://api.ipstack.com/'
    _RESULT_CLASS = IPStackResult
    _KEY = ipstack_key

    def _before_initialize(self, location, **kwargs):
        self.url += location

    def _build_params(self, location, provider_key, **kwargs):
        return {
            'access_key': provider_key,
        }


    @staticmethod
    @ratelim.greedy(10000, 60 * 60)
    def rate_limited_get(*args, **kwargs):
        return requests.get(*args, **kwargs)

    def _adapt_results(self, json_response):
        return [json_response]

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    g = IpStackQuery('99.240.181.199')
    g.debug()
