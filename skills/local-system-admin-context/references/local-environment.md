# 本机环境

这台机器涉及软件安装、系统配置、桌面环境或工具链调整时，默认以这份记录为准。

## 基础环境

- 主机名：`davisarch`
- 用户名：`davisye`
- 发行版：`Arch Linux x86_64`
- 内核：`Linux 6.19.9-arch1-1`
- 图形会话：`Wayland`
- 窗口管理器 / 合成器：`niri 25.11`
- 终端：`kitty 0.46.2`
- 登录 shell：`fish 4.5.0`
- 文件系统：`ext4`
- 文本编辑器命令映射：`vi` 和 `vim` 默认映射到 `nvim`
- 凭据存储：用户级 `gnome-keyring` 已启用，供本机应用通过 Secret Service 使用
- VS Code：通过 `argv.json` 固定使用 `gnome-libsecret` 作为密码存储后端
- v2rayA：通过 `/etc/systemd/system/v2raya.service.d/xray.conf` 固定使用 `xray` 核心，路径为 `/usr/sbin/xray`
- 通知守护进程：用户级 `mako.service` 已被 mask；Wayland 会话中不要默认按 `mako` 仍在接管通知来判断
- Codex：`~/.codex/config.toml` 已配置 `context7` 远程 MCP，服务地址为 `https://mcp.context7.com/mcp`
- Codex：全局 skill `~/.codex/skills/context7-docs` 已创建，用于规范 Context7 的库 ID 解析、版本选择和窄查询写法
- Codex：已全局安装官方 `gh-address-comments` 与 `gh-fix-ci` skills，分别用于处理 GitHub PR 评论和排查 GitHub Actions 检查失败

## 处理约定

- 优先给出兼容 `Wayland` 的方案，不默认按 `X11` 处理。
- 不默认假设安装了 `GNOME` 或 `KDE` 的专有工具。
- 涉及系统包管理时，优先按 `Arch Linux` 的方式处理，例如 `pacman`。
- 某些工具内启动的命令环境可能仍然是 `bash`，即使登录 shell 是 `fish`。
- 涉及本机应用的凭据安全存储时，优先复用 `gnome-keyring`，不要默认把敏感信息明文落到配置文件。

## 维护规则

- 这里只记录相对稳定的机器信息和长期约定。
- 不记录内存占用、磁盘使用量、运行时长、临时进程状态等会频繁变化的信息。
- 只要任务改变了本机的稳定软件或配置基线，结束前就要同步更新这份文件。
