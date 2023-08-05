from typing import Any

import pytest
from pgtoolkit import ctl
from psycopg.conninfo import conninfo_to_dict

from pglift import exceptions
from pglift.ctx import Context
from pglift.models import system
from pglift.models.system import Instance
from pglift.settings import PostgreSQLVersion, Settings


def test_default_postgresql_version(
    request: Any, pg_version: str, ctx: Context, monkeypatch: pytest.MonkeyPatch
) -> None:
    if request.config.option.pg_version is not None:
        pytest.skip("--pg-version manually set for tests")
    major_version = pg_version[:2]
    assert system.default_postgresql_version(ctx) == major_version

    new_settings = ctx.settings.copy(
        update={
            "postgresql": ctx.settings.postgresql.copy(update={"default_version": "42"})
        }
    )
    with monkeypatch.context() as m:
        m.setattr(ctx, "settings", new_settings)
        assert system.default_postgresql_version(ctx) == "42"


def test_baseinstance(instance: Instance) -> None:
    assert isinstance(instance.version, PostgreSQLVersion)


def test_baseinstance_str(pg_version: str, instance: Instance) -> None:
    assert str(instance) == f"{pg_version}/test"


def test_baseinstance_qualname(pg_version: str, instance: Instance) -> None:
    assert instance.qualname == f"{pg_version}-test"


@pytest.mark.parametrize(
    ["attrname", "expected_suffix"],
    [
        ("datadir", "srv/pgsql/{version}/test/data"),
        ("waldir", "srv/pgsql/{version}/test/wal"),
    ],
)
def test_baseinstance_paths(
    pg_version: str, instance: Instance, attrname: str, expected_suffix: str
) -> None:
    path = getattr(instance, attrname)
    assert path.match(expected_suffix.format(version=pg_version))


def test_baseinstance_get(request: Any, ctx: Context) -> None:
    if request.config.option.pg_version is not None:
        pytest.skip("--pg-version manually set for tests")
    i = system.BaseInstance.get("test", None, ctx=ctx)
    major_version = str(ctl.PGCtl(None).version)[:2]
    assert i.version == major_version


def test_baseinstance_get_invalid_version(ctx: Context) -> None:
    if any(
        v.bindir.exists() for v in ctx.settings.postgresql.versions if v.version == "12"
    ):
        pytest.skip("PostgreSQL 12 installed")
    with pytest.raises(
        exceptions.InvalidVersion, match="PostgreSQL executable directory"
    ):
        system.BaseInstance.get("onze", "12", ctx=ctx)


def test_postgresqlinstance_system_lookup(ctx: Context, instance: Instance) -> None:
    i = system.PostgreSQLInstance.system_lookup(ctx, instance)
    expected = system.PostgreSQLInstance(instance.name, instance.version, ctx.settings)
    assert i == expected

    i = system.PostgreSQLInstance.system_lookup(ctx, (instance.name, instance.version))
    assert i == expected

    with pytest.raises(TypeError, match="expecting either a BaseInstance or"):
        system.PostgreSQLInstance.system_lookup(ctx, ("nameonly",))  # type: ignore[arg-type]


def test_instance_validate(settings: Settings, pg_version: str) -> None:
    class Service:
        pass

    with pytest.raises(
        ValueError, match="values for 'services' field must be of distinct types"
    ):
        system.Instance(
            name="invalid",
            version=pg_version,
            settings=settings,
            services=[Service(), Service()],
        )

    class Service2:
        pass

    i = system.Instance(
        name="valid",
        version=pg_version,
        settings=settings,
        services=[Service(), Service2()],
    )
    assert i.services


def test_instance_system_lookup(ctx: Context, instance: Instance) -> None:
    i = system.Instance.system_lookup(ctx, instance)
    assert i == instance

    i = system.Instance.system_lookup(ctx, (instance.name, instance.version))
    assert i == instance


def test_instance_system_lookup_misconfigured(ctx: Context, instance: Instance) -> None:
    (instance.datadir / "postgresql.conf").unlink()
    with pytest.raises(exceptions.InstanceNotFound, match=str(instance)):
        system.Instance.system_lookup(ctx, instance)


def test_postgresqlinstance_exists(pg_version: str, settings: Settings) -> None:
    instance = system.PostgreSQLInstance(
        name="exists", version=pg_version, settings=settings
    )
    with pytest.raises(exceptions.InstanceNotFound):
        instance.exists()
    instance.datadir.mkdir(parents=True)
    (instance.datadir / "PG_VERSION").write_text(pg_version)
    with pytest.raises(exceptions.InstanceNotFound):
        instance.exists()
    (instance.datadir / "postgresql.conf").touch()
    assert instance.exists()


def test_postgresqlinstance_port(instance: Instance) -> None:
    assert instance.port == 999


def test_postgresqlinstance_config(instance: Instance) -> None:
    assert instance.config().as_dict() == {
        "port": 999,
        "unix_socket_directories": "/socks",
    }


def test_postgresqlinstance_standby_for(
    ctx: Context, instance: Instance, standby_instance: Instance
) -> None:
    assert not instance.standby
    assert standby_instance.standby
    assert conninfo_to_dict(standby_instance.standby.primary_conninfo) == {
        "host": "/tmp",
        "port": "4242",
        "user": "pg",
    }
    assert standby_instance.standby.slot == "aslot"
