"""API for calendar export."""

from datetime import UTC, datetime, timedelta
from hashlib import sha256
from http import HTTPStatus
from typing import Final

from aiohttp import web
from homeassistant.components import http
from homeassistant.components.calendar import DOMAIN as CALENDAR_DOMAIN
from homeassistant.components.calendar import CalendarEntity
from homeassistant.components.todo import (
    DOMAIN as TODO_DOMAIN,
)
from homeassistant.components.todo import (
    TodoListEntity,
)
from homeassistant.core import HomeAssistant
from homeassistant.util.dt import get_time_zone
from icalendar import Calendar, Event, Todo, vRecur


def rrule_str_to_dict(rrule_str: str) -> dict:
    """
    Parse an RFC 5545 RRULE value string (as found in HA's
    CalendarEvent.rrule, e.g. "FREQ=DAILY;INTERVAL=1;COUNT=10")
    into a dict suitable for icalendar's Event.add('rrule', ...).

    Strips an optional leading "RRULE:" prefix. Uses icalendar's own
    vRecur parser so COUNT/INTERVAL become ints, UNTIL becomes a real
    datetime/date, and multi-valued parts (BYDAY, BYMONTH, ...) become
    lists -- rather than reimplementing RFC 5545 parsing by hand.
    """
    if rrule_str.upper().startswith("RRULE:"):
        rrule_str = rrule_str.split(":", 1)[1]
    return dict(vRecur.from_ical(rrule_str))

def uid(*args: bytes | str) -> str:
    """Generate a stable hash from stable input data."""
    m = sha256()
    for arg in args:
        m.update(str(arg).encode())
    return m.hexdigest()


class CalendarExportAPI(http.HomeAssistantView):
    """View to export calendar in ICS format."""

    url = "/api/calendars/{entity_id}/export.ics"
    name = "api:calendars:ics"
    requires_auth = False

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize calender state."""
        self.tz: Final = get_time_zone(hass.config.time_zone)

    async def get(self, request: web.Request, entity_id: str):  # noqa: ANN201
        """Handle GET requests to export calendar in ICS format."""
        hass = request.app[http.KEY_HASS]

        if not (
            entity := hass.data[CALENDAR_DOMAIN].get_entity(entity_id)
        ) or not isinstance(entity, CalendarEntity):
            return web.Response(status=HTTPStatus.BAD_REQUEST)

        if not isinstance(entity, CalendarEntity):
            return web.Response(status=HTTPStatus.BAD_REQUEST)

        # Generate ICS data
        cal = Calendar()
        cal["VERSION"] = "2.0"  # RFC5545 3.7.4
        cal["X-WR-CALNAME"] = entity.name
        cal["PRODID"] = "-//Home Assistant//Calendar Export//EN"

        events = await entity.async_get_events(
            hass,
            datetime.now(tz=self.tz) - timedelta(days=365),
            datetime.now(tz=self.tz) + timedelta(days=365),
        )

        for event in events:
            e = Event()
            e.add("uid", uid(event.uid, event.start))
            e.add("summary", event.summary)
            # TODO: migrate to date of last edit once exposed by homeassistant
            e.add("dtstamp", datetime(1970, 1, 1, tzinfo=UTC))
            e.add("dtstart", event.start)
            e.add("dtend", event.end)
            if event.description:
                e.add("description", event.description)
            if event.location:
                e.add("location", event.location)
            # rrule logic added by Salvador Hernandez
            if event.rrule:
                e.add("rrule", rrule_str_to_dict(event.rrule))
            cal.add_component(e)

        ics = cal.to_ical().decode("utf-8")

        # Return ICS data as response
        return web.Response(
            status=HTTPStatus.OK,
            body=ics,
            headers={"Content-Type": "text/calendar"},
        )


class TodoListExportAPI(http.HomeAssistantView):
    """View to export todo list in ICS format."""

    url = "/api/todo/{entity_id}/export.ics"
    name = "api:todo:ics"
    requires_auth = False

    async def get(self, request: web.Request, entity_id: str):  # noqa: ANN201
        """Handle GET requests to export todo list in ICS format."""
        hass = request.app[http.KEY_HASS]

        if not (entity := hass.data[TODO_DOMAIN].get_entity(entity_id)):
            return web.Response(status=HTTPStatus.BAD_REQUEST)

        if not isinstance(entity, TodoListEntity):
            return web.Response(status=HTTPStatus.BAD_REQUEST)

        # Generate ICS data
        todo = Calendar()
        todo["X-WR-CALNAME"] = entity.name
        todo["PRODID"] = "-//Home Assistant//Todo List Export//EN"

        todos = entity.todo_items

        if todos:
            for todo_item in todos:
                t = Todo()
                t.add("uid", todo_item.uid)
                t.add("summary", todo_item.summary)
                if todo_item.due:
                    t.add("due", todo_item.due)
                if todo_item.description:
                    t.add("description", todo_item.description)
                if todo_item.status:
                    t.add("status", todo_item.status.value)
                todo.add_component(t)

        ics = todo.to_ical().decode("utf-8")

        # Return ICS data as response
        return web.Response(
            status=HTTPStatus.OK,
            body=ics,
            headers={"Content-Type": "text/calendar"},
        )


class TodoListExportEventsAPI(http.HomeAssistantView):
    """View to export todo list in ICS format (using vevent not vtodo)."""

    url = "/api/todo/{entity_id}/export_events.ics"
    name = "api:todo:events_ics"
    requires_auth = False

    async def get(self, request: web.Request, entity_id: str):  # noqa: ANN201
        """Handle GET requests to export todo list in ICS format."""
        hass = request.app[http.KEY_HASS]

        if not (entity := hass.data[TODO_DOMAIN].get_entity(entity_id)):
            return web.Response(status=HTTPStatus.BAD_REQUEST)

        if not isinstance(entity, TodoListEntity):
            return web.Response(status=HTTPStatus.BAD_REQUEST)

        # Generate ICS data
        todo = Calendar()
        todo["X-WR-CALNAME"] = entity.name
        todo["PRODID"] = "-//Home Assistant//Todo List Export Events//EN"

        todos = entity.todo_items

        if todos:
            for todo_item in todos:
                t = Event()
                t.add("uid", todo_item.uid)
                t.add("summary", todo_item.summary)
                if todo_item.due:
                    t.add("dtstart", todo_item.due)
                if todo_item.due:
                    t.add("dtend", todo_item.due)
                if todo_item.description:
                    t.add("description", todo_item.description)
                if todo_item.status:
                    t.add("status", todo_item.status.value)
                todo.add_component(t)

        ics = todo.to_ical().decode("utf-8")

        # Return ICS data as response
        return web.Response(
            status=HTTPStatus.OK,
            body=ics,
            headers={"Content-Type": "text/calendar"},
        )
