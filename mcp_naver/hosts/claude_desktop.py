import sys
from typing import Optional
from fastmcp.cli import claude

import json
from pathlib import Path
from typing import Dict


def update_claude_config(
    server_name: str,
    *,
    with_editable: Optional[Path] = None,
    with_packages: Optional[list[str]] = None,
    env_vars: Optional[Dict[str, str]] = None,
) -> bool:
    """Add or update a FastMCP server in Claude's configuration.

    Args:
        file_spec: Path to the server file, optionally with :object suffix
        server_name: Name for the server in Claude's config
        with_editable: Optional directory to install in editable mode
        with_packages: Optional list of additional packages to install
        env_vars: Optional dictionary of environment variables. These are merged with
            any existing variables, with new values taking precedence.

    Raises:
        RuntimeError: If Claude Desktop's config directory is not found, indicating
            Claude Desktop may not be installed or properly set up.
    """
    config_dir = claude.get_claude_config_path()
    if not config_dir:
        raise RuntimeError(
            "Claude Desktop config directory not found. Please ensure Claude Desktop "
            "is installed and has been run at least once to initialize its configuration."
        )

    config_file = config_dir / "claude_desktop_config.json"
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


def install_to_claude_desktop(
    env_vars: list[str] = None,
):
    """
    Install the MCP to Claude Desktop.
    """
    if not claude.get_claude_config_path():
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

    if update_claude_config(
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
        description="Install the MCP to Claude Desktop.",
    )
    parser.add_argument(
        "--env",
        "-e",
        action="append",
        help="Environment variables to set for the server.",
    )

    args = parser.parse_args()

    install_to_claude_desktop(
        env_vars=args.env,
    )
