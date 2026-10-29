# 验证记录

日期：2026-10-29。安装目录和工具语义已对照各宿主官方文档；出处见 [宿主适配](../skills/cicero-machine/references/runtime-adapters.md)。

## 自动检查

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

结果：Skill Creator 的 quick_validate 检查通过；仓库校验通过；安装器 **9 项测试通过**。检查 Skill frontmatter、四份参考文件、相对链接、许可和 UI 元数据；安装器测试覆盖三宿主路径、DSH_HOME、自定义项目路径、完整复制、重复安装、dry-run、冲突预检、替换备份、发布失败恢复、符号链接拒绝和源/目标嵌套保护。测试写入隔离临时目录，未向本机三个宿主实际安装。

## 验收边界

本次环境没有 Codex CLI、Claude Code CLI 或 DSH 可执行程序及其模型/搜索凭据。目录安装测试和官方接口核查不等于三平台模型调用均已端到端通过。

在各自已配置的宿主内执行：

1. 列出并读取 cicero-machine，核对加载路径。
2. 发起一场三轮辩论，确认 A/B/C 为真实不同 agent ID、后续轮复用角色。
3. 确认 B 看到 A 同轮发言，每轮 C 审计；最终给八部分报告。
4. 检查检索调用、S 编号、真实 URL 与原文支持关系。
5. 检查停止后没有新派发；恢复时仅使用可用上下文或公开检查点。
6. 无搜索/子代理时报告缺口；不得自动冒充完整运行。

仓库的安装器不安装或配置上述宿主。搜索 provider 的费用、权限和可用性取决于宿主配置。
