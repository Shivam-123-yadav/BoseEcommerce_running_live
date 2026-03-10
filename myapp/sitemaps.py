from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'base_index','registration', 'abouts-us', 'our-services', 'contact-us', 'shipping-policy',
            'privacy-policy', 'refund-returns-policy', 'cancellation-policy', 'appointment_form',
            'bose-service-center', 'bose-service-center-mumbai', 'bose-speaker-service-center',
            'bose-service-center-andheri', 'bose-service-center-thane', 'bose-service-center-in-india',
            'bose-service-center-andheri-east', 'bose-service-center-nagpur', 'bose-service-center-andheri-west',
            'bose-service-center-in-thane', 'bose-headphone-cushion-replacement', 'bose-speaker-repair',
            'repair-bose-speakers-mumbai', 'bose-portable-bluetooth-speaker', 'bose-soundbar',
            'bose-headphone-cushions',
            
            # location-based service centers
            'bose-service-center-in-worli',
            'bose-service-center-in-mulund',
            'bose-service-center-in-juhu',
            'bose-service-center-in-prabhadevi',
            'bose-service-center-in-bhandup',
            'bose-service-center-in-bandra',
            'bose-service-center-in-matunga',
            'bose-service-center-in-nahur',
            'bose-service-center-in-santacruz',
            'bose-service-center-in-mahim',
            'bose-service-center-in-kanjurmarg',
            'bose-service-center-in-khar',
            'bose-service-center-in-lower-parel',
            'bose-service-center-in-vikhroli',
            'bose-service-center-in-versova',
            'bose-service-center-in-sion',
            'bose-service-center-in-ghatkopar',
            'bose-service-center-in-lokhandwala',
            'bose-service-center-in-wadala',
            'bose-service-center-in-powai',
            'bose-service-center-in-goregaon',
            'bose-service-center-in-parel',
            'bose-service-center-in-chembur',
            'bose-service-center-in-malad',
            'bose-service-center-in-byculla',
            'bose-service-center-in-kurla',
            'bose-service-center-in-kandivali',
            'bose-service-center-in-marine-lines',
            'bose-service-center-in-vashi',
            'bose-service-center-in-jogeshwari',
            'bose-service-center-in-grant-road',
            'bose-service-center-in-airoli',
            'bose-service-center-in-dahisar',
            'bose-service-center-in-mumbai-central',
            'bose-service-center-in-kalyan-dombivli',
            'bose-service-center-in-borivali',
            'bose-service-center-in-cst',
            'bose-service-center-in-dombivli',
            'bose-service-center-in-marol',
            'bose-service-center-in-fort',
            'bose-service-center-in-ambernath',
            'bose-service-center-in-saki-naka',
            'bose-service-center-in-colaba',
            'bose-service-center-in-kalwa',
            'bose-service-center-in-chakala',
            'bose-service-center-in-charni-road',
            'bose-service-center-in-mumbra',
            'bose-service-center-in-dn-nagar',
            'bose-service-center-in-elphinstone',
            'bose-service-center-in-titwala',
            'bose-service-center-in-oshiwara',
            'bose-service-center-in-tardeo',
            'bose-service-center-in-badlapur',
            'bose-service-center-in-vile-parle',
            'bose-service-center-in-chinchpokli',
            'bose-service-center-in-sanpada',
            'bose-service-center-in-turbhe',
            'bose-service-center-in-ghansoli',
            'bose-service-center-in-andheri',
            'bose-service-center-in-thane',
            'bose-service-center-in-dadar',

            # accessories
            ('products-category', 'filter=remote'),
            ('products-category', 'filter=cushion'),
            ('products-category', 'filter=powersupply'),
            ('products-category', 'filter=cable'),
            ('products-category', 'filter=carrycase'),
            ('products-category', 'filter=adapter'),
            ('products-category', 'filter=stayhear'),
            ('products-category', 'filter=others'),
            # headphones
            ('products-category', 'filter=wireless'),
            ('products-category', 'filter=noisecancelling'),
            ('products-category', 'filter=earbuds'),
            # speakers
            ('products-category', 'filter=portablebluetooth'),
            ('products-category', 'filter=homeaudio'),
            ('products-category', 'filter=homecinema'),
            ('products-category', 'filter=soundbars'),
            ('products-category', 'filter=stereo'),
            ('products-category', 'filter=computerspeaker'),
            ('products-category', 'filter=portablepa'),
        ]

    def location(self, item):
        if isinstance(item, tuple):
            name, query = item
            url = reverse(name)
            return f"{url}?{query}"
        else:
            return reverse(item)
