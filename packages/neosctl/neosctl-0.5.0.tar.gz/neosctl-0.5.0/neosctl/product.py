import json
import os
import pathlib
import typing

import httpx
import typer

from neosctl import constant, schema, util
from neosctl.auth import ensure_login
from neosctl.util import process_response

app = typer.Typer()


def product_url(ctx: typer.Context) -> str:
    return "{}/product".format(ctx.obj.get_gateway_api_url().rstrip("/"))


special_delimiters = {
    r"\t": "\t",
}


@app.command(name="template")
def template(
    ctx: typer.Context,
    name: str = typer.Argument(os.getenv("NEOSCTL_PRODUCT", ...), help="Data Product name"),
    filepath: str = typer.Option(..., "--filepath", "-f", help="Filepath of the csv template"),
    output_dir: str = typer.Option(..., "--output-dir", "-o", help="Output directory for the json template"),
    delimiter: str = typer.Option(",", "--delimiter", "-d", help="csv delimiter"),
    quotechar: typing.Optional[str] = typer.Option(None, "--quote-char", "-q", help="csv quote char"),
):
    """Generate a data product schema template from a csv.

    Given a csv with a header row, generate a template field schema.
    """

    @ensure_login
    def _request(ctx: typer.Context, f: typing.IO) -> httpx.Response:
        params = {k: v for k, v in [("delimiter", delimiter), ("quotechar", quotechar)] if v is not None}

        return util.post(
            ctx,
            f"{product_url(ctx)}/template",
            params=params,
            files={"csv_file": f},
        )

    fp = util.get_file_location(filepath)

    with fp.open("rb") as f:
        r = _request(ctx, f)

    if r.status_code >= constant.BAD_REQUEST_CODE:
        process_response(r)

    fp = pathlib.Path(output_dir) / f"{name}.json"
    with fp.open("w") as f:
        json.dump(r.json(), f, indent=4)


@app.command(name="create-stored")
def create_stored(
    ctx: typer.Context,
    name: str = typer.Argument(os.getenv("NEOSCTL_PRODUCT", ...), help="Data Product name"),
    filepath: str = typer.Option(..., "--filepath", "-f", help="Filepath of the table schema json payload"),
):
    """Create a stored data product."""

    @ensure_login
    def _request(ctx: typer.Context, dpc: schema.CreateStoredDataProduct) -> httpx.Response:
        return util.post(
            ctx,
            f"{product_url(ctx)}/{name}",
            json=dpc.dict(exclude_none=True),
        )

    fp = util.get_file_location(filepath)
    fields = util.load_json_file(fp, "schema")

    dpc = schema.CreateStoredDataProduct(type="stored", fields=fields)

    r = _request(ctx, dpc)
    process_response(r)


@app.command(name="create-streaming")
def create_streaming(
    ctx: typer.Context,
    name: str = typer.Argument(os.getenv("NEOSCTL_PRODUCT", ...), help="Data Product name"),
    flow_type: str = typer.Option(..., "--flow-type", "-t", help="Flow type"),
    filepath: str = typer.Option(..., "--filepath", "-f", help="Filepath of the table schema json payload"),
):
    """Create a streaming data product."""

    @ensure_login
    def _request(ctx: typer.Context, dpc: schema.CreateStreamingDataProduct) -> httpx.Response:
        return util.post(
            ctx,
            f"{product_url(ctx)}/{name}",
            json=dpc.dict(exclude_none=True),
        )

    fp = util.get_file_location(filepath)
    fields = util.load_json_file(fp, "schema")

    dpc = schema.CreateStreamingDataProduct(type="streaming", fields=fields, flow_type=flow_type)
    # TODO: support iceberg properties and orc bloom

    r = _request(ctx, dpc)
    process_response(r)


@app.command(name="create-subset")
def create_subset(
    ctx: typer.Context,
    name: str = typer.Argument(os.getenv("NEOSCTL_PRODUCT", ...), help="Data Product name"),
    parent: str = typer.Option(..., "--parent", "-p", help="Data product parent"),
    columns: typing.List[str] = typer.Option(..., "--column", "-c", help="Parent column(s) to include"),
):
    """Create a subset data product."""

    @ensure_login
    def _request(ctx: typer.Context, dpc: schema.CreateSubsetDataProduct) -> httpx.Response:
        return util.post(
            ctx,
            f"{product_url(ctx)}/{name}",
            json=dpc.dict(exclude_none=True),
        )

    dpc = schema.CreateSubsetDataProduct(type="subset", parent_product=parent, columns=columns)

    r = _request(ctx, dpc)
    process_response(r)


@app.command(name="list")
def list_products(ctx: typer.Context):
    """List data products."""

    @ensure_login
    def _request(ctx: typer.Context):
        return util.get(ctx, product_url(ctx))

    r = _request(ctx)
    process_response(r)


@app.command()
def delete_data(
    ctx: typer.Context,
    name: str = typer.Argument(os.getenv("NEOSCTL_PRODUCT", ...), help="Data Product name"),
):
    """Delete data from a data product."""

    @ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.delete(
            ctx,
            f"{product_url(ctx)}/{name}/data",
        )

    r = _request(ctx)
    process_response(r)


@app.command()
def delete(
    ctx: typer.Context,
    name: str = typer.Argument(os.getenv("NEOSCTL_PRODUCT", ...), help="Data Product name"),
    force: bool = typer.Option(
        False,
        "--force",
        help="Force remove even if attached spark application is still running.",
    ),
):
    """Delete a data product."""

    @ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.delete(
            ctx,
            f"{product_url(ctx)}/{name}",
            params={"force": force},
        )

    r = _request(ctx)
    process_response(r)


@app.command()
def publish(
    ctx: typer.Context,
    name: str = typer.Argument(os.getenv("NEOSCTL_PRODUCT", ...), help="Data Product name"),
):
    """Publish a data product."""

    @ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.post(
            ctx,
            f"{product_url(ctx)}/{name}/publish",
        )

    r = _request(ctx)
    process_response(r)


@app.command()
def unpublish(
    ctx: typer.Context,
    name: str = typer.Argument(os.getenv("NEOSCTL_PRODUCT", ...), help="Data Product name"),
):
    """Unpublish a product."""

    @ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.delete(
            ctx,
            f"{product_url(ctx)}/{name}/publish",
        )

    r = _request(ctx)
    process_response(r)


@app.command(name="get")
def get_product(
    ctx: typer.Context,
    product_name: str = typer.Argument(os.getenv("NEOSCTL_PRODUCT", ...), help="Data Product name"),
):
    """Get data product schema."""

    @ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.get(
            ctx,
            f"{product_url(ctx)}/{product_name}",
        )

    r = _request(ctx)
    process_response(r)


@app.command()
def preview(
    ctx: typer.Context,
    product_name: str = typer.Argument(os.getenv("NEOSCTL_PRODUCT", ...), help="Data Product name"),
):
    """Preview data product data.

    Get the first 25 rows of a data product's data.
    """

    @ensure_login
    def _request(ctx: typer.Context) -> httpx.Response:
        return util.get(
            ctx,
            "{product_url}/{name}/data".format(
                product_url=product_url(ctx),
                name=product_name,
            ),
        )

    r = _request(ctx)
    process_response(r)
