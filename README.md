# Calendar Export

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Project Maintenance][maintenance-shield]

[![Community Forum][forum-shield]][forum]

The integration provides the `https://<your-domain>/api/calendars/{entity_id}/export.ics` endpoint to export the calendar events in the iCalendar format.

## Installation

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=JosephAbbey&repository=ha_calendar_export&category=Integration)

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `calendar_export`.
1. Download _all_ the files from the `custom_components/calendar_export/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Integration blueprint"

## Configuration is done in the YAML file

Just add this at top level:

```yaml
calendar_export:
```

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[ha_calendar_export]: https://github.com/josephabbey/ha_calendar_export
[commits-shield]: https://img.shields.io/github/commit-activity/y/josephabbey/ha_calendar_export.svg?style=for-the-badge
[commits]: https://github.com/josephabbey/ha_calendar_export/commits/main
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/josephabbey/ha_calendar_export.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Joakim%20Sørensen%20%40ludeeus-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/josephabbey/ha_calendar_export.svg?style=for-the-badge
[releases]: https://github.com/josephabbey/ha_calendar_export/releases
