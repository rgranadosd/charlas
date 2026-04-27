"""Domain plugins for the Rafa agent."""

from .shopify import PriceMemory, ShopifyPlugin
from .weather import WeatherPlugin

__all__ = ["PriceMemory", "ShopifyPlugin", "WeatherPlugin"]
