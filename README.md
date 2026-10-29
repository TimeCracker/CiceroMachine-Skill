![CiceroMachine Skill — evidence-driven multi-agent debate for Codex, Claude Code, and DeepSeek Harness](assets/readme-banner.webp)

# CiceroMachine Skill

**简体中文** | [English](README.en.md)

**一个独立的、跨平台的证据驱动辩论 Skill。** A 正方、B 反方分别检索与反驳，C 主持人逐轮审计，最后给出带来源、成立条件和反转条件的报告。

复用 [TimeCracker/CiceroMachine](https://github.com/TimeCracker/CiceroMachine) 已发布的 Skill，扩展为 Codex、Claude Code、DeepSeek Harness (DSH) 通用版本。仓库只包含 Skill、安装/校验工具和文档，不含原项目的 TypeScript Web 应用。

## 运行前提

**完整的联网辩论要求宿主同时具备真实子代理和搜索/原文读取能力；安装成功不代表这些能力已经可用。** “宿主”指运行本 Skill 的 Codex、Claude Code 或 DeepSeek Harness 等 agent 程序。

- **真实子代理**：能够创建、运行并接收 A/B/C 三个独立上下文的 agent 的结果。单个模型在一条回复里扮演三种角色不满足这一要求。
- **搜索与原文读取**：当前会话有可用、获准的搜索和网页读取工具，以及必要的 provider 配置。子代理不能搜索时，可由具备能力的主会话代查并回传结果。
- **跨轮续接**：优先复用同一角色的上下文。若宿主不支持续接，只能从公开检查点重建角色，并明确披露私有上下文丢失。

Skill 本身不提供这些运行能力，也不会自动配置模型、API Key、搜索服务或权限。只有模型 API Key，或仅复制 Skill 文件，不能保证完整运行。

缺少真实子代理时，会报告无法执行独立 agent 辩论；只有你明确要求，才提供标明降级的角色模拟。缺少搜索时，会说明限制；只有你明确接受离线分析或要求仅用给定材料，才基于这些材料继续，不伪造联网结果。

首次使用时可以先说：“检查 cicero-machine 的子代理、续接、搜索和原文读取能力，报告缺口，不修改配置。” 具体适配见 [宿主适配与能力边界](skills/cicero-machine/references/runtime-adapters.md)。

## 兼容范围

| 宿主 | Skill 安装 | 真实多 agent 运行 | 搜索依赖 |
| --- | --- | --- | --- |
| Codex CLI / IDE | `.agents/skills/cicero-machine/` | 宿主提供独立子代理和续接工具 | 可用的 web search/open |
| Claude Code | `.claude/skills/cicero-machine/` | Agent 创建角色，按实际版本续接 | WebSearch / WebFetch 可用且获准 |
| DeepSeek Harness | `.dsh/skills/cicero-machine/` | 本地 spawn 子代理 + send_message | 已配置可用的 web_search / web_fetch provider |

上表路径相对用户主目录或目标项目。DSH 也能发现 `.agents/skills`，但专用 `.dsh/skills` 优先。每次开始辩论时先核对当前会话的能力，不仅看安装目录是否存在。

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
$cicero-machine 辩论：长用户行为序列是否应全部交给 Transformer？做 5 轮，用中文输出。
```

Claude Code：

```text
/cicero-machine 辩论：长用户行为序列是否应全部交给 Transformer？做 5 轮，用中文输出。
```

DeepSeek Harness：

```text
使用 cicero-machine skill 辩论：长用户行为序列是否应全部交给 Transformer？做 5 轮，用中文输出。
```

安装后先让宿主列出并读取 `cicero-machine`，确认加载路径是本次安装目录。若发现旧的同名 Skill，检查优先级与目录；不要仅凭文件复制成功就认定加载成功。

## 自定义轮数与输出

**3 轮只是默认值，可以在请求中指定 1、2、5、8 等正整数轮数，无需修改或重新安装 Skill。** 上面的示例指定了 5 轮；省略轮数时默认 3 轮。也可指定输出语言、讨论范围和查询预算；默认输出中文，在英文请求中也应明确写出 “Answer in English” 来覆盖默认语言。

| 请求轮数 | 流程 |
| --- | --- |
| 1 轮 | A 开场 → B 开场与回应 → A 简短回应与收束 → B 简短收束 → C 审计与报告；共用本轮证据与查询预算，缺少多轮追问 |
| 2 轮 | 第 1 轮开场；第 2 轮反驳与收束 |
| 3 轮（默认） | 开场 → 对抗 → 收束 |
| N 轮（N > 3） | 第 1 轮开场；第 2 至 N−1 轮对抗；第 N 轮收束 |

除 1 轮的上述特殊顺序外，每轮公开发言均按 A → B → C 串行，一轮包含双方交锋和主持人审计，不等于一条发言。每方都必须寻找反证；C 可以支持一方或判定证据不足，不机械折中。

不会因为双方提前达成一致就省略你指定的剩余轮次。你要求停止、提前总结，或工具限制导致无法继续时，会如实说明实际完成轮数。更多轮通常增加耗时、token 与搜索消耗，实际执行仍受宿主配额、上下文和工具限制。

支持暂停、追加因素和继续；跨会话恢复取决于可用的公开记录。仅用已有材料时，请明确说“只使用这些材料，接受离线分析”。

## 使用示例

以下自然语言请求可以接在上面的平台入口后：Codex 用 `$cicero-machine`，Claude Code 用 `/cicero-machine`，DSH 用“使用 cicero-machine skill”。轮数和输出语言都直接写在请求中。

### 投资研究：存储周期，5 轮

```text
使用 cicero-machine skill 辩论：本轮存储周期是否会显著长于以往周期？
做 5 轮，用中文输出，以今天为信息截止日。
范围：服务器 DRAM、利基型 DRAM、HBM，以及模组厂。
先明确“更长”的衡量指标和历史比较区间。
区分需求结构、供给扩张、库存和价格；每方必须寻找反证。
优先使用公司公告、财报和官方资料，标明数据期间与来源。
最后给出成立条件、反转条件和仍待核实的关键事实。
```

### 技术选型：长用户序列，2 轮

```text
使用 cicero-machine skill 辩论：工业推荐排序中的长用户行为序列，
应优先使用全量 Transformer，还是检索/压缩后再建模？
做 2 轮，用中文输出。
评价维度：CTR/CVR 效果、线上延迟、显存、训练成本和信息损失。
只用可核查的论文或官方资料；未公开的线上指标列为未知。
```

### 离线材料分析：缓存方案，2 轮

此例不需要联网搜索，仍需要真实子代理。下面的数据是演示用虚构材料。

```text
使用 cicero-machine skill 辩论：现有证据是否足以把缓存方案推广到所有用户？
做 2 轮，只使用下面材料，接受离线分析，用中文输出。
材料 1：虚构实验中，实验组和对照组各有 10 万用户。
实验组平均延迟 80 ms，对照组 100 ms；没有方差、分位数或显著性结果。
材料 2：实验组每千次请求成本 0.9 元，对照组 1.0 元，不含新增固定成本。
材料 3：5% 的高频更新商品出现缓存过期，尚未评估对转化率的影响。
请区分已知结果与假设，引用材料编号；不要补造外部来源。
```

### 暂停、补充条件与继续

在正在执行的同一场辩论中，依次发送：

```text
暂停，保存当前公开进度，不再派发新任务。
```

```text
补充约束：线上延迟预算必须满足 p95 ≤ 100 ms。
按原计划的总轮数继续；若前提变化导致需要重做，先说明受影响的结论。
```

恢复依赖仍可用的会话或公开检查点；新会话不会自动拥有旧角色的私有上下文。

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

本 README 提供中英双语；Skill 指令和详细参考文件目前为中文，报告输出语言可在请求中指定。

## License

[MIT](LICENSE)，保留 TimeCracker 原项目署名。
