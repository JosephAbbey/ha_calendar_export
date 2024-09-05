"""The calendar_export component."""

from homeassistant.core import HomeAssistant
from .api import CalendarExportAPI, TodoListExportAPI, TodoListExportEventsAPI


DOMAIN = "calendar_export"


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the calendar_export component."""
    hass.http.register_view(CalendarExportAPI())
    hass.http.register_view(TodoListExportAPI())
    hass.http.register_view(TodoListExportEventsAPI())

    return True
