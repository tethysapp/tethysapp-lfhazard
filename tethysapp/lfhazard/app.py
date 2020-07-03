from tethys_sdk.base import TethysAppBase, url_map_maker


class LiquefactionHazardApp(TethysAppBase):
    """
    Tethys app class for Liquefaction Hazard App.
    """

    name = 'Liquefaction Hazard App'
    index = 'lfhazard:home'
    icon = 'lfhazard/images/icon.gif'
    package = 'lfhazard'
    root_url = 'lfhazard'
    color = '#915F6D'
    description = '"Liquefaction Hazard Lookup"'
    tags = '"Liquifaction", "Geotech"'
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        urlmap = url_map_maker(self.root_url)

        return (
            urlmap(
                name='home',
                url='lfhazard/',
                controller='lfhazard.controllers.home'
            ),
            urlmap(
                name='getgeojson',
                url='lfhazard/getgeojson',
                controller='lfhazard.controllers.get_geojson'
            ),
            urlmap(
                name='query_csv',
                url='lfhazard/query-csv',
                controller='lfhazard.controllers.query_csv'
            ),
        )
