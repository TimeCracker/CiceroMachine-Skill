# CiceroMachine Skill

**一个独立的、跨平台的证据驱动辩论 Skill。** A 正方、B 反方分别检索与反驳，C 主持人逐轮审计，最后给出带来源、成立条件和反转条件的报告。

复用 [TimeCracker/CiceroMachine](https://github.com/TimeCracker/CiceroMachine) 已发布的 Skill，扩展为 Codex、Claude Code、DeepSeek Harness (DSH) 通用版本。仓库只包含 Skill、安装/校验工具和文档，不含原项目的 TypeScript Web 应用。

## 兼容范围

| 宿主 | Skill 安装 | 真实多 agent 运行 | 搜索依赖 |
| --- | --- | --- | --- |
| Codex CLI / IDE | `.agents/skills/cicero-machine/` | 宿主提供独立子代理和续接工具 | 可用的 web search/open |
| Claude Code | `.claude/skills/cicero-machine/` | Agent 创建角色，按实际版本续接 | WebSearch / WebFetch 可用且获准 |
| DeepSeek Harness | `.dsh/skills/cicero-machine/` | 本地 spawn 子代理 + send_message | 已配置可用的 web_search / web_fetch provider |

上表路径相对用户主目录或目标项目。DSH 也能发现 `.agents/skills`，但专用 `.dsh/skills` 优先。**Skill 可被加载，不代表当前会话已具备子代理和联网能力。** 开始时会检查；缺少能力时说明缺口，不伪造搜索或多 agent 结果。

默认继承宿主配置的模型，不绑定 GPT 型号。DeepSeek Harness 是独立宿主；“Claude Code 接入 DeepSeek API”仍按 Claude Code 安装，搜索可用性需另行确认。

## 安装

需要 Git 和 Python 3.9+。私有仓库先在本机配置 GitHub 访问权限，不把 token 写入命令或仓库。以下命令用于本仓库安装器；平台路径已于 **2026-10-29** 对照官方文档核查，以各平台当前官方文档和实际配置为准。

```bash
git clone https://github.com/TimeCracker/CiceroMachine-Skill.git
cd CiceroMachine-Skill

# 任选一个；默认安装到用户目录
python3 scripts/install.py --target codex
python3 scripts/install.py --target claude
python3 scripts/install.py --target deepseek

# 或一次安装到三个宿主
python3 scripts/install.py --target all
```

Windows 使用 `py -3` 代替 `python3`。安装器只复制 Skill 文件，不安装宿主、不修改模型/权限/搜索配置，也不处理凭据。

安装到指定项目：

```bash
python3 scripts/install.py --target all --scope project --project /absolute/path/to/project
```

`--project` 必须是已存在的项目根目录；若项目使用 Git，指向包含 `.git` 的根目录，避免 DSH 的发现范围不同。DSH 用户目录默认 `~/.dsh`，安装器尊重 `DSH_HOME`。若你自定义了 DSH provider 的 `dshHome` 配置，也须让 `DSH_HOME` 指向同一路径。Codex 与 Claude 使用各自标准目录。

预览与更新：

```bash
python3 scripts/install.py --target all --dry-run
git pull --ff-only
python3 scripts/install.py --target all --replace
```

已有相同文件时不重复写入；已有不同版本默认拒绝覆盖。`--replace` 先把旧目录完整备份到相应宿主配置目录下的 `cicero-machine-backups/`，然后替换。备份路径会打印出来；本安装器不自动删除备份。所有目标先预检，冲突时不会先更新一部分宿主。

手动安装也可以：把整个 `skills/cicero-machine/` 复制到上表对应目录，保留 `references/`、`agents/`、`assets/` 和 `LICENSE`。

## 使用

Codex：

```text
$cicero-machine 辩论：长用户行为序列是否应全部交给 Transformer？做三轮。
```

Claude Code：

```text
/cicero-machine 辩论：长用户行为序列是否应全部交给 Transformer？做三轮。
```

DeepSeek Harness：

```text
使用 cicero-machine skill 辩论：长用户行为序列是否应全部交给 Transformer？做三轮。
```

安装后先让宿主列出并读取 `cicero-machine`，确认加载路径是本次安装目录。若发现旧的同名 Skill，检查优先级与目录；不要仅凭文件复制成功就认定加载成功。

默认 3 轮，公开发言按 A → B → C 串行。支持指定语言、轮数、范围、查询预算、暂停、追加因素与继续。每方都必须寻找反证；C 可以支持一方或判定证据不足，不机械折中。

仅用已有材料时，请明确说“只使用这些材料，接受离线分析”。宿主没有真实子代理时不会自动切成角色模拟。

## 内容与验证

- [SKILL.md](skills/cicero-machine/SKILL.md)：流程、证据登记、暂停与收束。
- [角色协议](skills/cicero-machine/references/roles.md)、[报告模板](skills/cicero-machine/references/report-template.md)。
- [宿主适配与官方依据](skills/cicero-machine/references/runtime-adapters.md)：三平台工具差异与能力边界。
- [上游来源与差异](skills/cicero-machine/references/upstream.md)、[验证记录](docs/VALIDATION.md)。

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

安装目录、文件引用和安装器可以本地验证。Claude Code / DSH 的模型调用与实际联网结果仍须在配置完毕的相应宿主中验收；不把文档适配称为三平台均已完成端到端测试。

## License

[MIT](LICENSE)，保留 TimeCracker 原项目署名。
