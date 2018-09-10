import asyncio
import logging
import requests
import json
from datetime import timedelta

from homeassistant.const import CONF_ELEVATION
from homeassistant.core import callback
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import (async_track_time_interval)

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = []

DOMAIN = 'great_britain_carbon_intensity'
FORECAST = "forecast"

INTERVAL = timedelta(minutes=5)

@asyncio.coroutine
def async_setup(hass, config):
    carbon = GreatBritainCarbonIntensity(hass)
    return True

class GreatBritainCarbonIntensity(Entity):

    entity_id = DOMAIN + ".instance"

    def __init__(self, hass):
        self.hass = hass
        self._state = None
        async_track_time_interval(hass, self.timer_update, INTERVAL)

    @property
    def name(self):
        return 'Carbon intensity'

    @property
    def state(self):
        return str(self._state)

    @property
    def state_attributes(self):
        return {
            FORECAST: self._state
        }

    @property
    def unit_of_measurement(self):
        return "gCO2/kWh"

    def update(self):
        _LOGGER.warning("Updating")
        resp = requests.get("https://api.carbonintensity.org.uk/intensity")
        response_json = resp.json()
        forecast = int(response_json['data'][0]['intensity']['forecast'])
        self._state = forecast

    @callback
    def timer_update(self, time):
        _LOGGER.warning("timer_update")
        self.update()
        self.async_schedule_update_ha_state()
