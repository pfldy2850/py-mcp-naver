import json
import sys
from pathlib import Path
from typing import Dict, Optional


def get_cursor_mcp_config_path() -> Path | None:
    """Get the Cursor MCP config directory based on platform."""
    path = Path(Path.home(), ".cursor")

    if path.exists():
        return path
    return None


def update_cursor_config(
    server_name: str,
    *,
    with_editable: Optional[Path] = None,
    with_packages: Optional[list[str]] = None,
    env_vars: Optional[Dict[str, str]] = None,
) -> bool:
    """
    Add or update a FastMCP server in Cursor's configuration.
    """
    config_dir = get_cursor_mcp_config_path()
    if not config_dir:
        raise RuntimeError(
            "Cursor config directory not found. Please ensure Cursor "
            "is installed and has been run at least once to initialize its configuration."
        )

    config_file = config_dir / "mcp.json"
    if not config_file.exists():
        config_file.write_text("{}")

    config = json.loads(config_file.read_text())
    if "mcpServers" not in config:
        config["mcpServers"] = {}

    # Always preserve existing env vars and merge with new ones
    if (
        server_name in config["mcpServers"]
        and "env" in config["mcpServers"][server_name]
    ):
        existing_env = config["mcpServers"][server_name]["env"]
        if env_vars:
            # New vars take precedence over existing ones
            env_vars = {**existing_env, **env_vars}
        else:
            env_vars = existing_env

    # Build uv run command
    args = ["run"]

    # Collect all packages in a set to deduplicate
    packages = {"fastmcp", "mcp-naver"}
    if with_packages:
        packages.update(pkg for pkg in with_packages if pkg)

    # Add all packages with --with
    for pkg in sorted(packages):
        args.extend(["--with", pkg])

    if with_editable:
        args.extend(["--with-editable", str(with_editable)])

    # Add fastmcp run command
    args.extend(["python", "-m", "mcp_naver.server"])

    server_config = {
        "command": "uv",
        "args": args,
    }

    # Add environment variables if specified
    if env_vars:
        server_config["env"] = env_vars

    assert "NAVER_CLIENT_ID" in env_vars, "Missing NAVER_CLIENT_ID in env_vars"
    assert "NAVER_CLIENT_SECRET" in env_vars, "Missing NAVER_CLIENT_SECRET in env_vars"

    config["mcpServers"][server_name] = server_config

    config_file.write_text(json.dumps(config, indent=2))


def install_to_cursor(
    env_vars: list[str] = None,
):
    """
    Install the MCP to Cursor.
    """
    if not get_cursor_mcp_config_path():
        sys.exit(1)

    from mcp_naver.server import mcp

    name = mcp.name
    server = mcp

    with_packages = getattr(server, "dependencies", []) if server else []

    env_dict: Optional[dict[str, str]] = None
    if env_vars:
        env_dict = {}
        for env_var in env_vars:
            key, value = env_var.split("=", 1)
            env_dict[key.strip()] = value.strip()

    if update_cursor_config(
        name,
        with_packages=with_packages,
        env_vars=env_dict,
    ):
        ...
    else:
        sys.exit(1)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(
        description="Install the MCP to Cursor.",
    )
    parser.add_argument(
        "--env",
        "-e",
        action="append",
        help="Environment variables to set for the server.",
    )

    args = parser.parse_args()

    install_to_cursor(
        env_vars=args.env,
    )
