# 宿主适配

接口依据核对日期：2026-10-29。以下工具名用于识别能力；调用参数以当前工具 schema 为准，不因文档示例就假定工具存在。

## 公共协议

1. 发现真实的创建、续接、等待/结果、停止、搜索及原文读取能力。只检查存在性与配置；首次实际调用失败时按错误处理，不循环猜测参数。
2. 主会话建立三个隔离角色；A、B、C 均禁止继续委派。保持公开发言 A → B → C 串行，不能并行产生双方同轮结论。
3. 每个角色只收到自己角色说明、公共任务卡、允许的工具/模式、已发表发言和已登记来源。子代理不会自动继承 Skill 正文时显式提供必要内容或可读路径。
4. 保存真实 agent ID。复用同一角色实例；原生续接不可用时仅从公开记录重建，增加 context_generation，并在报告披露。不得借宿主全历史 fork 假装独立研究。
5. “已接受”或“已启动”不代表发言已完成。等待真实结果，再登记来源和推进下一角色。
6. 不自动设置 API Key、模型、网络 provider、权限或插件。缺少必要能力时报告具体缺口。只有用户已接受离线/模拟模式才执行相应降级。
7. 离线材料按文件标识和版本去重，段落作为定位字段；同一文件的不同段落复用 S 编号，保留各自主张和定位。公开来源规则与在线模式一致，不伪造搜索日志。

## Codex / ChatGPT Work

- 用当前提供的 spawn 工具创建新上下文；如工具暴露 `fork_turns`，选择 `none`。不要依赖固定命名空间或硬编码模型。
- 在本类 Work 环境中，`collaboration.followup_task` 可唤起空闲角色；`send_message` 本身不启动空闲角色。其他 Codex 版本按其实际续接 schema。
- 使用宿主提供的 web search/open 工具。ChatGPT 保持内置搜索策略；Codex 如未提供联网能力，说明限制。
- `agents/openai.yaml` 仅提供 UI 信息，不创建三个子代理、不配置权限，也不代表其他平台不能使用 Skill。

## Claude Code

- 用 `Agent` 创建三个命名的 `general-purpose` 或合适的自定义角色，给最小任务卡；不要使用复制完整对话的 fork 模式。
- 需要多轮复用时，不选只执行一次的 Explore/Plan。保存返回 ID，按宿主实际工具继续同一角色；当前文档描述 `SendMessage` 可唤起已完成子代理，旧版本可能提供其他 resume 方式。
- 默认继承配置的模型。每个子代理显式读取所需角色和报告约束；不能假定父会话已加载的 Skill 自动进入子代理。
- 检查 `WebSearch` / `WebFetch` 是否可用且获准。替代模型后端不保证这些工具仍可运行；失败时由有能力的主会话代查，或报告缺口。
- 此目录安装的是 Claude Code Skill；不把 Claude 网页对话的角色扮演视作独立子代理。

## DeepSeek Harness (DSH)

- 使用已注册、指向本地 `spawn` provider 的委派工具（常名 `subagent`）。这会创建新子会话；`fork` 继承父历史，不用于独立 A/B/C 初始化。
- 记录 `started subagent` 返回的 child ID，等待完成通知。使用本地 continuable child 的 `send_message` 继续；该调用只确认接收，不直接返回下一段发言。
- `list_agents` / `interrupt_agent` 可用于查状态和停止，以当前可见能力为准。外部 Codex/Claude/ACP/DSH SDK 委派后端可能只执行单个任务，不能假定支持 follow-up。
- 使用宿主提供的 `web_search` / `web_fetch`。取证依赖已配置可用的 search/fetch provider；仅有 DeepSeek 模型 API Key 不代表搜索 provider 可用。
- provider 选择不明确、未配置或调用失败时，保留错误与查询日志，报告缺口；不自行替换用户 provider。
- 模型与搜索凭据由 DSH 配置管理，本 Skill 不读取、分发或输出凭据。

## 官方依据

- [Codex Skill 与安装目录](https://learn.chatgpt.com/docs/build-skills)
- [Codex 子代理](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [Claude Code 子代理与续接](https://code.claude.com/docs/en/sub-agents)
- [DSH Skills 与发现目录](https://deepseek-harness.github.io/deepseek-harness/en/reference/subsystems/skills)
- [DSH 本地 Skill provider](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/skill-filesystem/README.md)
- [DSH 委派工具](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/subagent/tool-subagent/README.md)
- [DSH 子代理控制](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/subagent/tool-subagent-control/README.md)
- [DSH Web access](https://deepseek-harness.github.io/deepseek-harness/en/reference/subsystems/web)
