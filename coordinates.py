import astropy.units as u
from astropy.coordinates import AltAz, EarthLocation, SkyCoord
from astropy.time import Time
from ugradio import nch
import datetime

c = SkyCoord(frame="galactic", l=120*u.deg, b=0*u.deg)
lab = EarthLocation(lat=nch.lat*u.deg, lon=nch.lon*u.deg, height=nch.alt*u.m)
obstime = Time(datetime.datetime.utcnow(), scale='utc', location=lab)
print(c.transform_to(AltAz(obstime=obstime, location=lab)))
