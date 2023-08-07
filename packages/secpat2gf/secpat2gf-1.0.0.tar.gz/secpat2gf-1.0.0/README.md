# secpat2gf

convert secret pattern to gf compatible.

## Install

**from PyPi:**

```console
$ pip3 install secpat2gf
```

**from Source:**

```console
$ git clone https://github.com/dwisiswant0/secpat2gf
$ cd secpat2gf/
$ pip3 install -r requirements.txt
```

## Usage

```console
$ secpat2gf --help
usage: secpat2gf [-h] -r RULE_FILE [-f FLAGS] [-s]

options:
  -h, --help            show this help message and exit
  -r RULE_FILE, --rule-file RULE_FILE
                        path to rule file/URL
  -f FLAGS, --flags FLAGS
                        grep flags (default: -aHnPr)
  -s, --save            save to $HOME/.gf instead of stdout
```

### Example

Converting YAML-based rule URL to gf compatible

```console
$ secpat2gf -r https://github.com/mazen160/secrets-patterns-db/raw/master/datasets/generic.yml
[02/10/2023 08:56:55 AM] Slack Token pattern
{
  "flags": "-aHnPr",
  "pattern": "(xox[pborsa]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32})"
}
[02/10/2023 08:56:55 AM] test pattern
{
  "flags": "-aHnPr",
  "pattern": "test"
}
[02/10/2023 08:56:55 AM] generic password pattern
{
  "flags": "-aHnPr",
  "pattern": "password.+"
}
[02/10/2023 08:56:55 AM] Generic secret pattern
{
  "flags": "-aHnPr",
  "pattern": "secret.+"
}
...
```

Converting YAML-based rule file to gf & save the results

```console
$ secpat2gf --save -r generic.yaml
```

### More 

More example, see [workaround](https://github.com/dwisiswant0/gf-secrets#workaround-recycle) from [gf-secrets](https://github.com/dwisiswant0/gf-secrets).

## Resources

- [secrets-patterns-db](https://github.com/mazen160/secrets-patterns-db) - Secrets Patterns DB: The largest open-source Database for detecting secrets, API keys, passwords, tokens, and more.
- [gf](https://github.com/tomnomnom/gf) - A wrapper around grep, to help you grep for things.
- [gf-secrets](https://github.com/dwisiswant0/gf-secrets) - Secret and/or credential patterns used for gf.

## License

`secpat2gf` is distributed under MIT. See `LICENSE` file.