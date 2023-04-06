from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="ZTPVIS",  # export envvars with `export DYNACONF_FOO=bar`.
    settings_files=["settings.yaml"],  # Load files in the given order.
)
