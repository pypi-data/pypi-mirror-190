import multiprocessing as mp
import os
import sys
from functools import partial
from typing import Tuple

import click
import pandas as pd
import xarray as xr
import yaml

from src.mhw_detect.detection.detect import prepare_data
from src.mhw_detect.detection.parser import (
    check_climato_period,
    check_file_exist,
    count_files,
    parse_data,
    parse_param,
)


def check_extension(ctx, param, value):
    if not value.endswith((".parquet", ".csv")):
        raise click.BadParameter("The extension must be .parquet or .csv")
    else:
        return value


@click.command(
    help="""
    Detect extreme events
    """
)
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    required=True,
    help="Specify configuration file",
)
@click.option(
    "--geographical-subset",
    "-g",
    type=(
        click.FloatRange(min=-90, max=90),
        click.FloatRange(min=-90, max=90),
        click.FloatRange(min=-180, max=180),
        click.FloatRange(min=-180, max=180),
    ),
    help="The geographical subset as "
    + "minimal latitude, maximal latitude, "
    + "minimal longitude and maximal longitude.\n\n"
    + "If set, the detection will be done on the subsetted global dataset given in \
            config file (not the cuts) and sequentially.",
)
@click.option(
    "--categ-map",
    type=str,
    help="Generate category map in a netcdf file.",
    show_default=True,
)
@click.option(
    "--output-df",
    type=click.UNPROCESSED,
    help="Give a name to the output dataframe.\
            Two extensions are available: csv and parquet (default).\
            Save in csv if you want to open the dataframe with excel.\
            Parquet is more efficient and takes less disk space.",
    default="data.parquet",
    show_default=True,
    callback=check_extension,
)
def extreme_events(
    config: str,
    geographical_subset: Tuple[float, float, float, float],
    categ_map: str,
    output_df: str,
):
    mask = bool(categ_map)

    conf = yaml.safe_load(open(config))

    output = conf["output_detection"]

    try:
        check_file_exist(conf)
    except Exception as error:
        click.echo(repr(error))
        sys.exit()

    param = parse_param(conf)

    def output_path(file_name):
        return os.path.join(output, file_name)

    def save_dataframe(dataframe):
        if output_df.endswith(".parquet"):
            dataframe.to_parquet(output_path(output_df))
        else:
            dataframe.to_csv(output_path(output_df), sep=";")

    if geographical_subset is not None:
        data = parse_data(conf, False)

        lat = geographical_subset[0:2]
        lon = geographical_subset[2:4]

        prepare_data(
            0, output, mask=mask, lat=lat, lon=lon, p=param["pctile"], **data, **param
        )

        click.echo("Creating csv")
        df = pd.read_csv(output_path("0.txt"), sep=";")
        save_dataframe(df)

        if categ_map:
            os.rename(output_path("0.txt.nc"), output_path(categ_map))

    else:
        data = parse_data(conf)
        nfile = count_files(conf)

        if "clim" not in data:
            check_climato_period(conf)

        pool = mp.Pool()
        pool.imap(
            partial(
                prepare_data,
                outdir=output,
                mask=mask,
                p=param["pctile"],
                **data,
                **param
            ),
            range(1, nfile),
        )
        pool.close()
        pool.join()

        click.echo("Computation done")

        click.echo("Saving dataframe")

        def f(i):
            return pd.read_csv(i, sep=";")

        filepaths = [output_path(str(i) + ".txt") for i in range(1, nfile)]
        df = pd.concat(map(f, filepaths))
        save_dataframe(df)

        if categ_map:
            click.echo("Creating mask")
            mask = xr.open_mfdataset(output_path("*.txt.nc"))
            comp = dict(zlib=True)
            encoding = {var: comp for var in mask.data_vars}
            mask.to_netcdf(output_path(categ_map), encoding=encoding)
            p = [output_path(str(g) + ".txt.nc") for g in range(1, nfile)]

            for path in p:
                try:
                    os.remove(path)
                except OSError:
                    click.echo("Error while deleting file: ", path)


if __name__ == "__main__":
    extreme_events()
