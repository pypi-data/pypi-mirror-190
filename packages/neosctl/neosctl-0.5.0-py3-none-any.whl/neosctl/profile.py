import re
import typing

import click
import typer

from neosctl import schema
from neosctl.util import get_user_profile_section, prettify_json, remove_config, send_output, upsert_config

app = typer.Typer()


r = re.compile(r"http[s]?:\/\/.*")


def validate_url(value):
    m = r.match(value)
    if m is None:
        msg = f"Invalid url, must match pattern: `{r}`."
        raise click.UsageError(msg)
    return value


@app.command()
def init(
    ctx: typer.Context,
    hostname: typing.Optional[str] = typer.Option(None, "--host", "-h"),
    gateway_api_url: typing.Optional[str] = typer.Option(None, "--gateway-api-url", "-g"),
    registry_api_url: typing.Optional[str] = typer.Option(None, "--registry-api-url", "-r"),
    iam_api_url: typing.Optional[str] = typer.Option(None, "--iam-api-url", "-i"),
    storage_api_url: typing.Optional[str] = typer.Option(None, "--storage-api-url", "-s"),
    username: typing.Optional[str] = typer.Option(None, "--username", "-u"),
    ignore_tls: bool = typer.Option(
        False,
        "--ignore-tls",
        help="Ignore TLS errors (useful in local/development environments",
    ),
    non_interactive: bool = typer.Option(
        False,
        "--non-interactive",
        help="Don't ask for input, generate api values based on hostname.",
    ),
):
    """Initialise a profile.

    Create a profile that can be reused in later commands to define which
    services to interact with, and which user to interact as.

    Call `init` on an existing profile will update the existing profile.
    """
    typer.echo(f"Initialising [{ctx.obj.profile_name}] profile.")
    default_host = f"{hostname}/api/{{}}" if hostname else ""

    if non_interactive and not (hostname and username):
        send_output(
            msg="\nError: --hostname/-h and --username/-u required for non-interactive mode.",
            exit_code=1,
        )

    if non_interactive:
        gateway_api_url = gateway_api_url or f"{hostname}/api/gateway"
        storage_api_url = storage_api_url or f"{hostname}/api/storage"
        iam_api_url = iam_api_url or f"{hostname}/api/iam"
        registry_api_url = registry_api_url or f"{hostname}/api/registry"

    urls = {
        "gateway_api_url": gateway_api_url,
        "registry_api_url": registry_api_url,
        "iam_api_url": iam_api_url,
        "storage_api_url": storage_api_url,
    }
    for key, default, prompt in [
        ("gateway", ctx.obj.get_gateway_api_url(), "Gateway API url"),
        ("registry", ctx.obj.get_registry_api_url(), "Registry API url"),
        ("iam", ctx.obj.get_iam_api_url(), "IAM API url"),
        ("storage", ctx.obj.get_storage_api_url(), "Storage API url"),
    ]:
        url_key = f"{key}_api_url"
        if urls[url_key] is None:
            urls[url_key] = typer.prompt(
                prompt,
                default=default or default_host.format(key),
                value_proc=validate_url,
            )
        else:
            validate_url(urls[url_key])

    if username is None:
        kwargs = {}
        if ctx.obj.profile:
            kwargs["default"] = ctx.obj.profile.user
        username = typer.prompt(
            "Username",
            **kwargs,
        )

    profile = schema.Profile(  # nosec: B106
        user=username,
        access_token="",
        refresh_token="",
        ignore_tls=ignore_tls,
        **urls,
    )

    upsert_config(ctx, profile)


@app.command()
def delete(
    ctx: typer.Context,
):
    """Delete a profile."""
    typer.confirm(f"Remove [{ctx.obj.profile_name}] profile", abort=True)
    remove_config(ctx)


@app.command()
def view(
    ctx: typer.Context,
):
    """View configuration for a profile."""
    send_output(
        msg=prettify_json({**get_user_profile_section(ctx.obj.config, ctx.obj.profile_name)}),
    )


@app.command(name="list")
def list_profiles(
    ctx: typer.Context,
):
    """List available profiles."""
    send_output(
        msg=prettify_json(sorted(ctx.obj.config.sections())),
    )
