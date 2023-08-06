import typing

import click
import typer

from neosctl import schema, util
from neosctl.util import (
    check_profile_exists,
    constant,
    get_user_profile,
    is_success_response,
    process_response,
    read_config_dotfile,
    send_output,
    upsert_config,
)

app = typer.Typer()


def auth_url(iam_api_url: str) -> str:
    return "{}".format(iam_api_url.rstrip("/"))


def _check_refresh_token_exists(ctx: typer.Context):
    if ctx.obj.profile.refresh_token == "":  # nosec: B105
        send_output(
            msg=f"You need to login. Run neosctl -p {ctx.obj.profile_name} auth login",
            exit_code=1,
        )

    return True


def ensure_login(method):
    def check_access_token(*args, **kwargs):
        ctx = args[0]
        if not isinstance(ctx, click.core.Context):
            # Developer reminder
            msg = "First argument should be typer.Context instance"
            raise TypeError(msg)

        r = method(*args, **kwargs)

        check_profile_exists(ctx)

        # Try to refresh token
        # Confirm it is a token invalid 401, registry not configured mistriggers this flow.
        if r.status_code == constant.UNAUTHORISED_CODE:
            data = r.json()
            if "code" in data and data["code"].startswith("A0"):
                refresh_token(ctx)

                # Refresh the context
                c = read_config_dotfile()
                ctx.obj.config = c
                ctx.obj.profile = get_user_profile(c, ctx.obj.profile_name)

                r = method(*args, **kwargs)

        return r  # noqa: RET504

    return check_access_token


def _update_profile(
    ctx: typer.Context,
    auth: schema.Auth = schema.Auth(),
):
    return schema.Profile(
        gateway_api_url=ctx.obj.gateway_api_url,
        registry_api_url=ctx.obj.registry_api_url,
        iam_api_url=ctx.obj.iam_api_url,
        storage_api_url=ctx.obj.storage_api_url,
        user=ctx.obj.profile.user,
        access_token=auth.access_token,
        refresh_token=auth.refresh_token,
        ignore_tls=ctx.obj.profile.ignore_tls,
    )


@app.command()
def login(
    ctx: typer.Context,
    password: typing.Optional[str] = typer.Option(None, "--password", "-p"),
):
    """Login to neos."""
    check_profile_exists(ctx)

    if password is None:
        password = typer.prompt(
            "[{profile}] Enter password for user ({user})".format(
                profile=ctx.obj.profile_name,
                user=ctx.obj.profile.user,
            ),
            hide_input=True,
        )

    r = util.post(
        ctx,
        f"{auth_url(ctx.obj.get_iam_api_url())}/login",
        json={"user": ctx.obj.profile.user, "password": password},
    )

    if not is_success_response(r):
        process_response(r)

    upsert_config(ctx, _update_profile(ctx, schema.Auth(**r.json())))

    send_output(
        msg="Login success",
        exit_code=0,
    )


@app.command()
def logout(ctx: typer.Context):
    """Logout from neos."""
    check_profile_exists(ctx)

    _check_refresh_token_exists(ctx)

    r = util.post(
        ctx,
        f"{auth_url(ctx.obj.get_iam_api_url())}/logout",
        json={"refresh_token": ctx.obj.profile.refresh_token},
    )

    if not is_success_response(r):
        process_response(r)

    upsert_config(ctx, _update_profile(ctx, schema.Auth()))

    send_output(
        msg="Logout success",
        exit_code=0,
    )


def refresh_token(ctx: typer.Context):
    check_profile_exists(ctx)
    _check_refresh_token_exists(ctx)

    r = util.post(
        ctx,
        f"{auth_url(ctx.obj.get_iam_api_url())}/refresh",
        json={"refresh_token": ctx.obj.profile.refresh_token},
    )

    if not is_success_response(r):
        process_response(r)

    upsert_config(ctx, _update_profile(ctx, schema.Auth(**r.json())))

    return r
