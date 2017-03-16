from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.stores import PersistentStore


class LiquifactionHazardApp(TethysAppBase):
    """
    Tethys app class for Liquifaction Hazard App.
    """

    name = 'Liquefaction Hazard App'
    index = 'lfhazard:home'
    icon = 'lfhazard/images/icon.gif'
    package = 'lfhazard'
    root_url = 'lfhazard'
    color = '#64db6a'
    description = '"Liquifaction Hazard Lookup"'
    tags = '"Liquifaction", "Geotech"'
    enable_feedback = False
    feedback_emails = []

        
    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (UrlMap(name='home',
                           url='lfhazard',
                           controller='lfhazard.controllers.home'),
                    UrlMap(name='map',
                           url='lfhazard/map',
                           controller='lfhazard.controllers.map'),
                    UrlMap(name='documentation',
                           url='lfhazard/documentation',
                           controller='lfhazard.controllers.documentation')
        )

        return url_maps

    def persistent_stores(self):
        """
        Add one or more persistent stores
        """
        stores = (PersistentStore(name='stream_gage_db',
                                  initializer='lfhazard.init_stores.init_stream_gage_db',
                                  spatial=True
                                  ),
                  )

        return stores