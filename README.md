# Github action to find unsupported dependencies using [package-maintenance.dev](https://package-maintenance.dev)

This GitHub action is an easy-to-use client for the [package-maintenance.dev](https://package-maintenance.dev) API
to find unsupported dependencies in your project. It heavily relies on the also on GitHub dependency graph to find
the dependencies to check. So make sure to enable the dependency graph in your repository settings.
Please, find more information about Dependency Graph in the following GitHub documentation:

- [How to enable Dependency Graph](https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/configuring-the-dependency-graph)
- [Supported ecosystems](https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/dependency-graph-supported-package-ecosystems)

## Inputs

This action requires the following inputs:

#### `github-token`

GitHub token to access the GitHub API. This value can be retrieved from the GitHub secrets context
`${{ secrets.GITHUB_TOKEN }}`.
This token is required to access the GitHub API and the dependency graph for the repository. The value is optional and
required only if the action is used in a private repository.

Please, find more information about GitHub context in the following GitHub documentation:

- [Authenticating with the GITHUB_TOKEN](https://docs.github.com/en/actions/reference/authentication-in-a-workflow#about-the-github_token-secret)

**Optional** The GitHub token to access the GitHub API. No default value.

#### `packages-ignore`

List of packages to ignore. The action will not check the versions of the packages in this list. The value is optional
and the default value is an empty list, that means all packages will be checked.
The list should be in format of multiline string with each line in [PURL](https://github.com/package-url/purl-spec) format without version. For example:

```
pkg:pypi/django
```

Version is not required in this case and will be ignored if provided. The action will check only the package id and
ecosystem.

**Optional** List of packages to ignore. The default value is an empty list.

#### `packages-scores-thresholds`

[package-maintenance.dev](https://package-maintenance.dev) index as such does not provide a clear bar which packages to
be considered as unsupported. Instead, it supplies a data to make an informed decision.
This parameter allows to set a threshold for the score based on this data. Index includes score for various metrics.
Please, find more information about the index in the
following [documentation](https://package-maintenance.dev/docs/index).
This value format is a list of key-value pairs in the format of `metric:threshold`. For example:

```
packages-scores-thresholds: "source_commit_frequency:B,binary_release_recency:A"
```

To set no threshold set the value to an empty string. For example:

```
packages-scores-thresholds: ""
```
In this case, the action will not check the score of the packages and just will output the complete audit information.

**Optional** The score threshold for the package. The default value is `binary_release_recency:B,source_commit_recency:B,source_commit_frequency:B`.

## Report

This action produces as a result a report about found packages maintenance data and mark those that are below the
configured threshold. The report is printed in the action output.
Example of the report:

---
### Package maintenance report
This report provides brief information about current repository dependencies maintenance status.

### Found packages

| Type | Id | Latest version | URLs | Release recency | Commits recency | Commits frequency | Issues lifetime | Issues open percentage | Pull requests lifetime | Pull requests open percentage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <code style="color: red">maven</code> | <code style="color: red">org.ehcache:ehcache</code> | <code>3.10.8</code> | [binary](https://mvnrepository.com/artifact/org.ehcache/ehcache) / [source](https://github.com/ehcache/ehcache3) | <code style="color: red">⚠</code> 25 / <code style="color: orange">C</code> | <code style="color: red">⚠</code> 5 / <code style="color: orange">C</code> |  31 / <code style="color: green">A</code> |  25 / <code style="color: orange">C</code> | `*` |  1 / <code style="color: yellow">B</code> | `*` |
| <code>maven</code> | <code>org.springframework.boot:spring-boot-starter-web</code> | <code>3.4.1</code> | [binary](https://mvnrepository.com/artifact/org.springframework.boot/spring-boot-starter-web) / [source](https://github.com/spring-projects/spring-boot) |  0 / <code style="color: green">A</code> |  0 / <code style="color: green">A</code> |  1100 / <code style="color: green">A</code> |  6 / <code style="color: green">A</code> | `*` |  3 / <code style="color: orange">C</code> | `*` |

``*`` - Data is not available or is not enough to calculate a score;
<code style="color: red">⚠</code> - A package maintenance score is below the threshold;

### Missing data packages
The following packages are missing maintenance data in the package-maintenance.dev index

| Type | Namespace | Name            |
| --- |-----------|-----------------|
| maven | com.acme  | private-package |

This report was generated by the Package Maintenance Report Action.
For more information, visit [action documentation](https://github.com/package-maintenance-dev/github-action).

---

In the "Found packages" table you may see two found packages:
- `org.ehcache:ehcache` with a score below the threshold for the `Release recency` and `Commits recency` metrics. Because of that, the package is marked with a red color.
- `org.springframework.boot:spring-boot-starter-web` with a score above the threshold for all metrics, so the package shown as regular text.

In the "Missing data packages" table you may see a package `com.acme:private-package` that is not found in the index.


### Metrics
The following metrics you can find in the report:
- `Release recency` - how recent the latest release of the package is.
  Calculated as months since the latest release.
- `Commits recency` - how recent the last commit in the repository of the package is.
  Calculated as months since the last commit.
- `Commits frequency` - how often the commits are made in the repository of the package.
  Calculated as average number of commits per month for the last 100 commits
- `Issues lifetime` - how long in average the issues in the repository of the package are open.
  Calculated as average time span in days between and issue is open until its closed for last 100 issues.
- `Issues open percentage` - what percentage of the issues in the repository of the package are open.
  Calculated as percentage of open issues from the last 100 issues.
- `Pull requests lifetime` - how long in average the pull requests in the repository of the package are open.
  Calculated as average time span in days between and pull request is open until its closed for last 100 pull requests.
- `Pull requests open percentage` - what percentage of the pull requests in the repository of the package are open.
  Calculated as percentage of open pull requests from the last 100 pull requests.

Each score consist of value and grade:
- `A` - The value is in the top 10% of the index.
- `B` - The value is in the top 75% of the index.
- `C` - The value is in the bottom 75% of the index.
- `D` - A package is not maintained anymore.

For packages with archived source repositories the grade is `D` and the value is always `0`.

## Example usage

The following example shows how to use the action in a workflow:

```yaml
uses: package-maintenance-dev/github-action@v0.0.1
with:
  github-token: ${{ secrets.GITHUB_TOKEN }}
  packages-ignore: |
    pkg:pypi/django
  packages-scores-thresholds: "source.commit.frequency:B,binary.release.recency:A"
```
