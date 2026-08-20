# davis-llm-skill

面向 **OpenAI Codex** 和 **DeepSeek Harness (DSH)** 的可版本化 skill 仓库。

默认英文说明见：[README.md](./README.md)

所有 skill 统一部署到全局 hub `~/.agents/skills`：DSH 直接读取该目录，三个 Codex
环境（`~/.codex/skills`、`~/.codex_xinta/.codex/skills`、`~/.codex_xuanzhi/.codex/skills`）
通过符号链接指向它。

## 仓库包含什么

- `skills/`：兼容 Codex 的 skill（SKILL.md + 支撑文件）
- `shared/`：可复用的共享工作流源（core.md + meta.json）
- `scripts/`：导入、安装、同步工具

## 当前包含的 skill（33 个）

`anachb`、`apple-mail`、`attack-tree-construction`、`audio-transcription`、
`browser-act`、`chrome-cdp-browser-control`、`cloudflare`、`commit`、
`context7-docs`、`frontend-design`、`gh-address-comments`、`gh-fix-ci`、`ghidra`、
`github`、`google-workspace`、`librarian`、`local-system-admin-context`、
`native-web-search`、`oebb-scotty`、`openscad`、`pi-share`、`ppt-creator`、
`pptx`、`project-skill-bootstrap`、`send-notifications`、`sentry`、
`skill-repo-manager`、`skillsmp-search`、`summarize`、`tmux`、
`update-changelog`、`uv`、`web-browser`

## 仓库模型

1. 把可复用的工作流语义放在 `shared/<skill-name>/`（core.md + meta.json）
2. 把部署用的 SKILL.md 放在 `skills/<skill-name>/`
3. 用 `scripts/sync_all.sh` 同步进全局 hub

## 目录结构

```text
skills/     Codex skill 目录（SKILL.md + 支撑文件）
shared/     共享工作流源文件
scripts/    导入、安装、同步工具
```

## 同步到 hub

把全部 skill 同步到全局 hub `~/.agents/skills`：

```bash
./scripts/sync_all.sh
```

把单个（或全部）skill 同步到 `~/.codex/skills`（指向 hub 的符号链接）：

```bash
./scripts/sync_codex_skill.sh <skill-name>
./scripts/sync_codex_skill.sh --all
```

确认 diff 后强制覆盖部署副本：

```bash
./scripts/sync_codex_skill.sh --all --force
```

## 导入新 skill

把 hub 里存在但仓库还没有的 skill 拉进仓库：

```bash
./scripts/import_from_codex.sh
```

然后检查 `shared/<skill-name>/meta.json`，提交即可（不再维护多平台 adapter）。

## 在新机器上安装

```bash
./scripts/install_codex_skills.sh
```

## 说明

- `local-system-admin-context` 带有机器相关内容，迁移到其他机器前应先审查其
  `references/local-environment.md` baseline
- 19 个 skill（anachb … web-browser）在 hub 中是指向上游 `mitsuhiko/agent-stuff`
  checkout 的符号链接，本仓库保留其导入快照

## 许可证

这个仓库包含部分从 `openai/skills` 和 `mitsuhiko/agent-stuff` 复制过来的文件。
再次分发修改版本前，应保留其 license 文件并检查上游许可要求。
