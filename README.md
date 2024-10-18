# Github action to find unsupported dependencies using [package-maintenance.dev](https://package-maintenance.dev)

This GitHub action is an easy-to-use client for the [package-maintenance.dev](https://package-maintenance.dev) API
to find unsupported dependencies in your project. It heavily relies on the also on GitHub dependency graph to find
the dependencies to check. So make sure to enable the dependency graph in your repository settings.
Please, find more information about Dependency Graph in the following GitHub documentation:

- [How to enable Dependency Graph](https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/configuring-the-dependency-graph)
- [Supported ecosystems](https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/dependency-graph-supported-package-ecosystems)

## Inputs

This action requires the following inputs:

#### `github-repository`

Repository full name in the format `owner/repo`. This value can be retrieved from the GitHub context
`${{ github.repository }}`.
Please, find more information about GitHub context in the following GitHub documentation:

- [Accessing contextual information about workflow runs](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/accessing-contextual-information-about-workflow-runs#github-context)

**Required** The repository full name in the format `owner/repo`. No default value.

#### `github-token`

GitHub token to access the GitHub API. This value can be retrieved from the GitHub secrets context
`${{ secrets.GITHUB_TOKEN }}`.
This token is required to access the GitHub API and the dependency graph for the repository. The value is optional and
required only if the action is used in a private repository.

Please, find more information about GitHub context in the following GitHub documentation:

- [Authenticating with the GITHUB_TOKEN](https://docs.github.com/en/actions/reference/authentication-in-a-workflow#about-the-github_token-secret)

**Optional** The GitHub token to access the GitHub API. No default value.

#### `sbom-ignore-packages`

List of packages to ignore. The action will not check the versions of the packages in this list. The value is optional
and the default value is an empty list, that means all packages will be checked.
The list should be in format of multiline string with each line in PURL format without version. For example:

```
pkg:npm/express
pkg:pypi/django
```

Version is not required in this case and will be ignored if provided. The action will check only the package id and
ecosystem.

**Optional** List of packages to ignore. The default value is an empty list.

#### `sbom-scores-thresholds`

[package-maintenance.dev](https://package-maintenance.dev) index as such does not provide a clear bar which packages to
be considered as unsupported. Instead, it supplies a data to make an informed decision.
This parameter allows to set a threshold for the score based on this data. Index includes score for various metrics.
Please, find more information about the index in the
following [documentation](https://package-maintenance.dev/docs/index).
This value format is a list of key-value pairs in the format of `metric:threshold`. For example:

```
sbom-scores-thresholds: "source.commit.frequency:B,binary.release.recency:A"
```

To set threshold for all metrics, use asterisk `*` as a key. For example:

```
sbom-scores-thresholds: "*:B"
```

To set no threshold set the value to an empty string. For example:

```
sbom-scores-thresholds: ""
```
In this case, the action will not check the score of the packages and just will output the complete audit information.

**Optional** The score threshold for the package. The default value is `*:B`.

## Outputs

This action does not provide any output, but it will fail if unsupported dependencies are found or output complete audit
information.

TODO: Show example output

## Example usage

The following example shows how to use the action in a workflow:

```yaml
uses: package-maintenance-dev/github-action@v0.0.1
with:
  github_repository: ${{ github.repository }}
  github_token: ${{ secrets.GITHUB_TOKEN }}
  sbom_ignore_packages: |
    pkg:npm/express
    pkg:pypi/django
  sbom_score_threshold: "source.commit.frequency:B,binary.release.recency:A"
```
