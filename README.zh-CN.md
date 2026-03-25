# davis-llm-skill

面向 OpenAI Codex、GitHub Copilot CLI 和 VS Code Copilot 的可版本化 skill 仓库。

默认英文说明见：[README.md](./README.md)

这个仓库的目标是把可复用的 skill 工作流集中维护，再映射成不同客户端能理解的格式。

## 仓库包含什么

- `skills/`：兼容 Codex 的 skill
- `shared/`：可复用的共享工作流源
- `adapters/`：面向 Copilot CLI 和 VS Code Copilot 的适配文件
- `scripts/`：生成、同步、安装相关脚本

## 当前包含的 skill

- `context7-docs`
- `gh-address-comments`
- `gh-fix-ci`
- `local-system-admin-context`
- `project-skill-bootstrap`
- `skillsmp-search`
- `skill-repo-manager`

## 仓库模型

这个仓库采用 shared-first 的维护方式：

1. 把可复用的工作流语义放在 `shared/<skill-name>/`
2. 把 Codex 部署文件放在 `skills/<skill-name>/`
3. 在 `adapters/copilot-cli/<skill-name>/` 里生成或维护 Copilot CLI 文件
4. 在 `adapters/vscode-copilot/<skill-name>/` 里生成或维护 VS Code Copilot 文件
5. 先 review 变更，再把 Codex skill 同步到 `~/.codex/skills/`

这样做的目的，是避免把某一个客户端的文件格式错误地当成所有平台的唯一源。

## 目录结构

```text
skills/                    Codex skill 目录
shared/                    共享工作流源文件
adapters/copilot-cli/      AGENTS.md 和 Copilot CLI instructions
adapters/vscode-copilot/   VS Code Copilot instructions 和 prompt files
scripts/                   生成、安装、同步工具
```

## 生成适配文件

从共享 skill 源重新生成 adapter 文件：

```bash
python scripts/generate_adapters.py --all
```

只生成单个 skill：

```bash
python scripts/generate_adapters.py context7-docs
```

生成器会读取 `shared/<skill-name>/meta.json` 里的结构化元数据。

## 同步到 Codex

把单个 skill 同步到 `~/.codex/skills`：

```bash
./scripts/sync_codex_skill.sh context7-docs
```

同步全部已跟踪的 skill：

```bash
./scripts/sync_codex_skill.sh --all
```

在确认 diff 后强制覆盖部署副本：

```bash
./scripts/sync_codex_skill.sh --all --force
```

## 在新机器上安装

克隆或更新仓库后，把全部 Codex skill 同步到本机：

```bash
./scripts/install_codex_skills.sh
```

也可以传入自定义仓库地址和安装目录：

```bash
./scripts/install_codex_skills.sh https://github.com/DavisYe/davis-llm-skill.git ~/project/davis-llm-skill
```

## 安装 VS Code Copilot 文件到项目

把某个 skill 的 VS Code Copilot adapter 拷贝到目标项目：

```bash
./scripts/install_vscode_copilot_adapter.sh context7-docs ~/project/my-app
```

如果目标项目已经存在 `.github` 指令文件，并且你希望以本仓库版本为准：

```bash
./scripts/install_vscode_copilot_adapter.sh context7-docs ~/project/my-app --force
```

## 跨平台说明

- Codex 消费 `skills/<name>/`
- Copilot CLI 消费 `AGENTS.md` 等指令型文件
- VS Code Copilot 消费 `.github/copilot-instructions.md`、作用域 instruction 文件和 prompt files
- `local-system-admin-context` 带有机器相关内容，迁移到其他机器前应先审查其 baseline 数据

## 贡献流程

1. 如果 skill 有可复用语义，先修改共享源
2. 如果 adapter 文案发生变化，更新 `shared/<skill-name>/meta.json`
3. 运行 `python scripts/generate_adapters.py --all` 重新生成 adapter
4. 如有需要，再更新 Codex 专属文件
5. 运行 `./scripts/sync_codex_skill.sh --all` 同步到本地 Codex
6. 提交并推送

## CI

GitHub Actions 会重新运行生成器，并通过 diff 检查生成后的 adapter 文件是否过期。

## 许可证

这个仓库包含部分从 `openai/skills` 复制过来的文件。再次分发修改版本前，应保留其 license 文件并检查上游许可要求。
