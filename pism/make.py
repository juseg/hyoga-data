#!/usr/bin/env python
# Copyright (c) 2021, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""Subset PISM data. This only works on Julien's computer."""

import os.path
import xarray as xr


def main():
    """Main program called during execution."""

    # encoding keyword arguments
    encoding = dict(zlib=True, shuffle=True, complevel=9)

    # copy 1km boot file without bathy
    with xr.open_dataset(
            '~/pism/input/boot/alps.srtm.hus12.nobathy.1km.nc',
            decode_cf=False) as ds:
        ds = ds.drop('topg')
        ds.to_netcdf(
            'pism.alps.in.boot.nc',
            encoding={var: encoding for var in ds})

    # concat 1d output in one file
    run = '~/pism/output/e9d2d1f/alpcyc4.1km.epica.1220.pp'
    run = os.path.expanduser(run)  # needed until xarray 0.17
    with xr.open_mfdataset(run+'/ts.???????.nc', decode_cf=False) as ds:
        ds = ds.isel(time=slice(9, None, 10))
        ds.to_netcdf(
            'pism.alps.out.1d.nc', encoding={var: encoding for var in ds})

    # select lgm slice of 2d output
    with xr.open_dataset(run+'/ex.0095500.nc', decode_cf=False) as ds:
        ds = ds.sel(time=-24.57*1000*365*24*60*60)
        ds = ds[[
            'mapping', 'pism_config', 'run_stats', 'time_bounds', 'topg',
            'thk', 'uvelbase', 'vvelbase', 'uvelsurf', 'vvelsurf']]
        ds.to_netcdf(
            'pism.alps.out.2d.nc', encoding={var: encoding for var in ds})


if __name__ == '__main__':
    main()
