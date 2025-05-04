
def sunmoonpos(gpst, de405):
    from skyfield.api import load
    from fast.com.gnssTime import gps2utc
    from astropy import units as u
    utct = gps2utc(gpst)
    ts = load.timescale()
    t = ts.utc(utct.year, utct.month, utct.day, utct.hour, utct.minute, utct.second + utct.microsecond / 1e6)    # 加载星体数据
    eph = load(de405)
    sun = eph['sun']
    # 获取太阳的位置
    au = sun.at(t).position.au
    ecef = (au * u.AU).to('m')
    return ecef


def orb2ecef(satPos, sunPosECEF):
    import numpy as np
    """
    Rotation matrix from satellite antenna frame to ECEF frame assuming
    standard yaw attitude law
    """
    rs = np.array(satPos)
    rsun = np.array(sunPosECEF)
    r = -np.array(satPos)
    ez = r/np.linalg.norm(r)
    r = rsun-rs
    es = r/np.linalg.norm(r)
    r = np.cross(ez, es)
    ey = r/np.linalg.norm(r)
    ex = np.cross(ey, ez)
    return np.array([ex, ey, ez])
