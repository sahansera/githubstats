from typing import Union

import click

from .github import GitHubClient


@click.command()
@click.argument("repo")
@click.option("--token", help="GitHub API token", envvar="GITHUB_TOKEN")
def main(repo: str, token: Union[str, None] = None):
    """Fetch statistics for a GitHub repository.

    REPO should be in the format 'owner/repo', e.g., 'python/cpython'
    """
    try:
        owner, repo_name = repo.split("/", 1)
    except ValueError:
        click.echo("Error: Repository should be in the format 'owner/repo'", err=True)
        raise SystemExit(1)

    client = GitHubClient(token)
    try:
        stats = client.get_repo_stats(owner, repo_name)
        click.echo()
        click.echo(f"{stats['name']} statistics")
        click.echo("-" * len(f"{stats['name']} statistics"))
        rows = (
            ("Stars", f"{stats['stars']:,}"),
            ("Forks", f"{stats['forks']:,}"),
            ("Open issues", f"{stats['open_issues']:,}"),
            ("Watchers", f"{stats['watchers']:,}"),
            ("Language", stats["language"] or "Unknown"),
            ("Created", stats["created_at"]),
            ("Updated", stats["updated_at"]),
        )
        for label, value in rows:
            click.echo(f"{label:<12}: {value}")
        click.echo()
    except Exception as e:
        click.echo(f"Error: Failed to fetch repository stats: {e}", err=True)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
