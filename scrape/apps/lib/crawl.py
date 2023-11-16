from scrapy.crawler import CrawlerRunner


def crawl(settings, spider_cls, *args, **kwargs):
    process = CrawlerRunner(settings=settings)
    from twisted.internet import reactor
    d = process.crawl(
        spider_cls,
        *args,
        **kwargs
    )

    d.addBoth(lambda _: reactor.stop())
    reactor.run()
