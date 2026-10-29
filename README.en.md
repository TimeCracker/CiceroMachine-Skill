![CiceroMachine Skill — evidence-driven multi-agent debate for Codex, Claude Code, and DeepSeek Harness](assets/readme-banner.webp)

# CiceroMachine Skill

[简体中文](README.md) | **English**

**A standalone, cross-platform skill for evidence-driven debate.** Agent A argues for the proposition, Agent B challenges it, and Agent C audits each round. The final report includes sources, conditions under which conclusions hold, and evidence that could reverse them.

Adapted from the published skill in [TimeCracker/CiceroMachine](https://github.com/TimeCracker/CiceroMachine) for Codex, Claude Code, and DeepSeek Harness (DSH). This repository contains the skill, installation/validation utilities, and documentation. It does not bundle the original TypeScript web application.

## Usage examples

Codex:

```text
$cicero-machine Debate: Is the 2000 dot-com bubble an appropriate comparison for today's AI investment? Run 5 rounds. Answer in English.
```

## Runtime requirements

**A complete online debate requires both real subagents and working search/source-reading tools in the host. Successful installation does not establish that these capabilities are available.** The host is the agent application that runs the skill, such as Codex, Claude Code, or DeepSeek Harness.

- **Real subagents:** the session must be able to create and run A/B/C in separate contexts and receive their results. One model acting out three roles in a single response does not meet this requirement.
- **Search and source reading:** the session needs usable, permitted search and webpage-reading tools, with any required provider configuration. If a subagent cannot search, a capable coordinating session can run its queries and return the results.
- **Continuation across rounds:** reuse each role's context where supported. If continuation is unavailable, roles can only be rebuilt from public checkpoints, with the loss of private context explicitly disclosed.

The skill does not supply these runtime capabilities or automatically configure models, API keys, search services, or permissions. A model API key alone, or copying the skill files, does not guarantee a complete run.

Without real subagents, the skill reports that independent-agent debate is unavailable; clearly labeled role simulation is offered only when you explicitly request it. Without search, it reports the limitation and proceeds offline only if you explicitly accept offline analysis or request use of supplied materials only. It never fabricates online results.

For a first check, ask: “Check cicero-machine's subagent, continuation, search, and source-reading capabilities. Report missing capabilities without changing configuration.” See [runtime adapters and capability boundaries](skills/cicero-machine/references/runtime-adapters.md) for details.

## Compatibility

| Host | Skill installation | Real multi-agent execution | Search dependency |
| --- | --- | --- | --- |
| Codex CLI / IDE | `.agents/skills/cicero-machine/` | Independent subagents and continuation tools exposed by the host | Available web search/open tools |
| Claude Code | `.claude/skills/cicero-machine/` | Agent creates roles; continuation follows the installed version | Available and permitted WebSearch / WebFetch |
| DeepSeek Harness | `.dsh/skills/cicero-machine/` | Local spawn subagents + send_message | A configured, working web_search / web_fetch provider |

Paths are relative to the user's home directory or the target project. DSH also discovers `.agents/skills`, but its dedicated `.dsh/skills` directory takes precedence. Each debate starts by checking the current session's capabilities, rather than just checking that installation files exist.

The skill inherits the host's configured model and does not require a particular GPT model. DeepSeek Harness is a separate host. Claude Code connected to the DeepSeek API still uses the Claude Code installation path; search availability must be checked separately.

## Installation

Requires Git and Python 3.9+. If the repository or mirror is private, configure GitHub access locally first; do not put tokens in commands or repository files. The commands below use this repository's installer. Platform paths were checked against official documentation on **2026-10-29**; current official documentation and your actual configuration take precedence.

```bash
git clone https://github.com/TimeCracker/CiceroMachine-Skill.git
cd CiceroMachine-Skill

# Choose one; installation is user-scoped by default
python3 scripts/install.py --target codex
python3 scripts/install.py --target claude
python3 scripts/install.py --target deepseek

# Or install for all three hosts
python3 scripts/install.py --target all
```

On Windows, use `py -3` instead of `python3`. The installer only copies skill files. It does not install the host, change model/permission/search settings, or handle credentials.

Install into a specific project:

```bash
python3 scripts/install.py --target all --scope project --project /absolute/path/to/project
```

`--project` must identify an existing project root. For a Git project, use the root containing `.git` to avoid differences in DSH discovery scope. The default DSH user directory is `~/.dsh`; the installer respects `DSH_HOME`. If you customize the DSH provider's `dshHome`, set `DSH_HOME` to the same path for installation. Codex and Claude use their standard directories.

Preview and update:

```bash
python3 scripts/install.py --target all --dry-run
git pull --ff-only
python3 scripts/install.py --target all --replace
```

Identical files are left unchanged. A different existing version is not overwritten by default. With `--replace`, the installer first backs up the complete old directory under `cicero-machine-backups/` in the relevant host configuration directory, then replaces it. The backup path is printed; backups are not automatically deleted. All destinations are checked before writing, so a conflict does not cause a partial installation across hosts.

For manual installation, copy the entire `skills/cicero-machine/` directory into the corresponding location above, keeping `references/`, `agents/`, `assets/`, and `LICENSE`.

## Usage

Codex:

```text
$cicero-machine Debate: Is the 2000 dot-com bubble an appropriate comparison for today's AI investment? Run 5 rounds. Answer in English.
```

Claude Code:

```text
/cicero-machine Debate: Is the 2000 dot-com bubble an appropriate comparison for today's AI investment? Run 5 rounds. Answer in English.
```

DeepSeek Harness:

```text
Use the cicero-machine skill to debate: Is the 2000 dot-com bubble an appropriate comparison for today's AI investment? Run 5 rounds. Answer in English.
```

After installation, ask the host to list and read `cicero-machine` and confirm that it loads the intended directory. If another skill with the same name exists, check discovery priority and paths. Copying files successfully does not prove that the host loaded them.

## Custom rounds and output

**Three rounds is the default, not a fixed limit. Request a positive integer such as 1, 2, 5, or 8 without editing or reinstalling the skill.** The examples above request five rounds; omitting the count defaults to three. You can also specify output language, scope, and query budget. Chinese is the default output language, so the English examples explicitly include “Answer in English” to override it.

| Requested rounds | Flow |
| --- | --- |
| 1 | A opens → B opens and responds → A briefly responds and closes → B briefly closes → C audits and reports; all within the same evidence/query budget, without multi-round follow-up |
| 2 | Round 1: opening; round 2: rebuttal and closure |
| 3 (default) | Opening → confrontation → closure |
| N (N > 3) | Round 1: opening; rounds 2 through N−1: confrontation; round N: closure |

Except for the special one-round sequence above, public turns follow A → B → C in every round. A round includes both sides' exchange and the moderator's audit, not just one message. Both sides must look for counterevidence. C can support one side or conclude that evidence is insufficient, without forcing a compromise.

Early agreement does not cancel the remaining rounds you requested. If you ask to stop or summarize early, or tool limitations prevent continuation, the report states how many rounds actually completed. More rounds generally require more time, tokens, and searches; execution remains subject to host quotas, context limits, and tool availability.

You can pause, add factors, and continue. Resuming in a new session depends on available public records. For supplied-materials-only analysis, explicitly say: “Use only these materials; offline analysis is acceptable.”

## Contents and validation

- [SKILL.md](skills/cicero-machine/SKILL.md): flow, evidence registry, pausing, and closure.
- [Role protocol](skills/cicero-machine/references/roles.md) and [report template](skills/cicero-machine/references/report-template.md).
- [Runtime adapters and official sources](skills/cicero-machine/references/runtime-adapters.md): tool differences and capability boundaries.
- [Upstream attribution and differences](skills/cicero-machine/references/upstream.md) and [validation record](docs/VALIDATION.md).

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

Installation paths, local references, and installer behavior can be validated locally. Model calls and online execution in Claude Code / DSH still require acceptance testing in configured hosts. Documentation adaptation is not a claim that all three platforms have passed end-to-end testing.

This README is available in Chinese and English. The skill instructions and detailed reference documents are currently written in Chinese; the requested report language is configurable.

## License

[MIT](LICENSE), retaining attribution to the original TimeCracker project.
