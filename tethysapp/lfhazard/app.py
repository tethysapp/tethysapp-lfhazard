from tethys_sdk.base import TethysAppBase, url_map_maker


class LiquifactionHazardApp(TethysAppBase):
    """
    Tethys app class for Liquifaction Hazard App.
    """

    name = 'Liquefaction Hazard App'
    index = 'lfhazard:home'
    icon = 'lfhazard/images/icon.gif'
    package = 'lfhazard'
    root_url = 'lfhazard'
    color = '#915F6D'
    description = '"Liquifaction Hazard Lookup"'
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
                url='lfhazard/map',
                controller='lfhazard.controllers.home'
            ),
            urlmap(
                name='query_csv',
                url='lfhazard/query-csv',
                controller='lfhazard.controllers.query_csv'
            ),
        )
