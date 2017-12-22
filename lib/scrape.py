"""Module that scrapes the wallpapers."""
def get_image_links_list(websites = [], **options):
    """Return the links for images."""
    from lib import plugins
    image_links = []
    for plugin in dir(plugins):
        scraper = getattr(plugins, plugin)
        if(callable(scraper) and any(
                plugin.startswith(website) 
                for website in websites)):
            image_links.extend(scraper(**options))
    return image_links

            
    # image_links=[]
    # if 'unsplash' in websites:  # For Unsplash
    #     image_links.extend(get_unsplash_image_links(**options))
    # elif 'reddit' in websites:  # For Reddit
    #     image_links.extend(get_reddit_image_links(**options))
    # elif 'desktoppr' in websites:  # For Desktoppr
    #     image_links.extend(get_desktoppr_image_links(**options))
    # return image_links