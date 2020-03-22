import requests
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point


class Locate(models.Model):
    dong = models.CharField(max_length=20)
    gu = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    longitude = models.DecimalField(decimal_places=8, max_digits=12, null=True, blank=True)
    latitude = models.DecimalField(decimal_places=8, max_digits=12, null=True, blank=True)
    latlng = models.PointField(null=True, blank=True)

    def __str__(self):
        return f'{self.dong}'

    class Meta:
        verbose_name = '위치 정보 '
        verbose_name_plural = '%s 목록' % verbose_name

    def save(self, *args, **kwargs):
        if self.latitude is not None and self.longitude is not None:
            if self.latitude == 0 and self.longitude == 0:
                self.convert_latlng(self.address)
            else:
                self.latitude = float(self.latitude)
                self.longitude = float(self.longitude)
            self.latlng = Point(self.longitude, self.latitude)
        super(Locate, self).save(*args, **kwargs)

    def convert_latlng(self, addr):
        try:
            param = {
                'query': addr,
            }
            header = {
                'X-NCP-APIGW-API-KEY-ID': 'lbzlb3algi',
                'X-NCP-APIGW-API-KEY': 'UjwPAw2nA123bslejXIWZZng9qQ3NVIcaOaDNjar',
            }
            url = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?'

            response = requests.get(url, params=param, headers=header)
            json = response.json()
            address = json['addresses'][0]

            self.latitude = float(address['x'])
            self.longitude = float(address['y'])
            return True

        except ConnectionError:
            self.latitude = float(0)
            self.longitude = float(0)
            return True

        except IndexError:
            self.latitude = float(0)
            self.longitude = float(0)
            return True

