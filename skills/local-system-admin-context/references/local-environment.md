# 本机环境

这台机器涉及软件安装、系统配置、桌面环境或工具链调整时，默认以这份记录为准。

## 基础环境

- 主机名：`davisarch`
- 用户名：`davisye`
- 发行版：`Arch Linux x86_64`
- 内核：`Linux 6.19.11-arch1-1`
- 图形会话：`Wayland`
- 窗口管理器 / 合成器：`niri 26.04`
- niri：`Mod+H/L` 在当前工作区聚焦左/右侧列，`Mod+Shift+H/L` 聚焦左/右显示器；`Mod+Ctrl+H/L` 将焦点窗口移动到左/右显示器，`Mod+Ctrl+J/K` 将焦点窗口移动到下/上工作区。
- 双屏常用布局：笔记本 `eDP-1` 保持 1920x1080、125% 缩放；外接 AOC `HDMI-A-1` 固定在左侧（`x=-1920`）、1920x1080@74.973 Hz、100% 缩放。对应配置在 `~/.config/niri/outputs.kdl`。
- Noctalia：Niri 登录时通过 `~/.config/niri/shell-switcher-startup.kdl` 启动 v5 原生 `noctalia`；`Mod+Space` 调用 v5 启动器 IPC，音量/麦克风静音/亮度硬件键通过 v5 IPC 显示 OSD。旧版 `noctalia-shell` / `noctalia-qs` 暂保留，待验证后再移除。
- 音频：PipeWire/WirePlumber + EasyEffects；应用通常先进入 `Easy Effects Sink`，再由 EasyEffects 输出到物理设备。EasyEffects 当前持久输出设备为 `Ryzen HD Audio Controller Headphones`，配置键位于 `~/.config/easyeffects/db/easyeffectsrc` 的 `outputDevice`。按应用保存的目标位于 `~/.local/state/wireplumber/stream-properties*`；未发现额外的用户 WirePlumber 路由规则。
- 显示管理器：`greetd` 已替代并移除 `GDM` / `ly`；通过 `noctalia-greeter-git` 启动 Noctalia Greeter，配置位于 `/etc/greetd/config.toml`，会话用户为 `greeter`
- 终端：`kitty 0.46.2`
- 登录 shell：`fish 4.5.0`
- kitty：未对 `Shift+Enter` 做额外重映射，避免干扰支持多行输入的 TUI（例如 Codex CLI）
- 文件系统：`ext4`
- 文本编辑器命令映射：`vi` 和 `vim` 默认映射到 `nvim`
- 凭据存储：用户级 `gnome-keyring` 已启用，供本机应用通过 Secret Service 使用
- VS Code：通过 `argv.json` 固定使用 `gnome-libsecret` 作为密码存储后端
- Zed：已设为 VS Code 键位；编辑字体 `FiraCode Nerd Font` 18px，1 秒延迟自动保存并在保存时格式化。用户配置位于 `~/.config/zed/settings.json`，命令行为 `zeditor`。
- v2rayA：通过 `/etc/systemd/system/v2raya.service.d/xray.conf` 固定使用 `xray` 核心，路径为 `/usr/sbin/xray`
- 通知守护进程：用户级 `mako.service` 已被 mask；Wayland 会话中不要默认按 `mako` 仍在接管通知来判断
- 本机通知：`send-notification` 通过用户级 `send-notification@.service` 按需投递 niri 桌面、邮件与 Telegram；默认目标和 Telegram 凭据保存在 GNOME Keyring，非敏感策略文件为 `~/.config/send-notifications/settings.conf`（0600）。邮件已验证，SMTP 实现归档在 `~/.local/libexec/send-notifications/send-mail`，由通知服务内部调用。
- Flameshot（Wayland/niri）：稳定组合为 `xdg-desktop-portal-wlr` 可用 + `~/.config/flameshot/flameshot.ini` 中 `useGrimAdapter=false`；在该机上 `useGrimAdapter=true` 会出现只显示左上角部分或 `QPainter not active` 异常
- Flameshot（降噪约定）：`showDesktopNotification=false`、`disabledTrayIcon=true`，并停用 `flameshot-daemon.service`（快捷键直接调用 `flameshot gui`，不依赖 daemon）
- X11/XWayland 缩放：用户级 `xsettingsd.service` 的配置为 `~/.config/xsettingsd/xsettingsd.conf`，全局 `Xft/DPI=122880`（120 DPI，即 125%）；它优先保证笔记本屏可读性，混合 DPI 下外接 100% 屏的 X11/XCB 应用会偏大，原生 Wayland 应用不受影响。
- Codex：`~/.codex/config.toml` 已配置 `context7` 远程 MCP，服务地址为 `https://mcp.context7.com/mcp`
- ChatGPT Linux 客户端：Noctalia 可搜索三个入口：`ChatGPT Davis`（默认 `~/.codex`）、`ChatGPT haoyue`（`~/.codex_xinta/.codex`）及 `ChatGPT xuanzhi`（`~/.codex_xuanzhi/.codex`）。后两者通过独立 Electron `--user-data-dir` 运行，避免不同登录账号被同一客户端进程接管；三个实际 Codex 根目录的 `sessions` 与 `.chatgpt-projects` 均链接到默认 `~/.codex`。xuanzhi 的 `session_index.jsonl` 也链接到默认索引，确保 `codey` 显示共享的最新本地历史；原索引保留为同目录备份。启动器位于 `~/.local/share/applications/`。
- Codex：全局 skill `~/.codex/skills/context7-docs` 已创建，用于规范 Context7 的库 ID 解析、版本选择和窄查询写法
- Codex：已全局安装官方 `gh-address-comments` 与 `gh-fix-ci` skills，分别用于处理 GitHub PR 评论和排查 GitHub Actions 检查失败
- Bun：`bun 1.3.14` 已安装；fish 的持久 PATH 包含 `~/.cache/.bun/bin`，全局 `@redocly/cli 2.40.0` 提供 `redocly` 与 `openapi`，用于 OpenAPI 3.1 契约校验
- DeepSeek Harness：用户级 `dsh-web.service` 启用后在 `127.0.0.1:3080` 提供 Web UI，工作目录为 `~/opt/dsh-deploy`。`~/.dsh/profiles/web` 的 Codex provider 由 `@deepseek-ai/dsh-subagent-codex` bundle 注册；本地 `cordis.patch.yml` 只能用 `id: subagent-codex` 覆盖其 `HOME=~/.codex_xinta`，不可再次 `insert` 同 ID。
- 用户级知识库挂载：`rclone-pan-webdav.service` 将 Cloudflare R2 bucket `kb:davis-kb` 挂到 `~/mnt/knowledge-base`，避免直接占用家目录下的 `~/knowledge-base`
- Neovim：`~/.local/share/nvim/mason` 里已安装的常用工具包括 `stylua`、`bash-language-server`、`shellcheck`、`shfmt`、`marksman`、`yaml-language-server`、`taplo`、`debugpy`、`delve`、`eslint-lsp`、`tailwindcss-language-server`、`emmet-language-server`、`json-lsp`、`dockerfile-language-server`、`docker-compose-language-service`
- MATLAB：`~/.local/bin/matlab` wrapper 已固定 `QT_QPA_PLATFORM=xcb` 并 `unset WAYLAND_DISPLAY`，用于在 Wayland(niri) 下确保账号登录窗口可启动（走 X11/xcb）
- 用户级 Xorg 启动脚本：`~/.local/bin/tty3-xorg-session` 可在真实 TTY（如 `tty3`）里通过 `startx` 拉起独立的 `X11` 桌面会话，默认支持本机已装的 `gnome`，若额外安装 `plasma-x11-session` 与 `kwin-x11` 也可起 `plasma`
- fish / tty3：`~/.config/fish/conf.d/tty3-auto-dm.fish` 仍保留旧的 Ly 兼容逻辑，但当前显示管理器由 systemd 的 `greetd.service` 接管；不要在 tty3 的 fish 中再次启动 Ly
- 用户级 v2rayN：`~/.config/systemd/user/v2rayn.service` 仅挂到 `graphical-session.target`，避免在 GNOME 初始化前抢先激活图形会话
- fish / thinkfan：`~/.config/fish/functions/game-on.fish` / `game-off.fish` 会联动 ThinkPad 游戏模式切换；`game-on` 会把 `~/.config/thinkfan/thinkfan-game.yaml` 安装到 `/etc/thinkfan.yaml` 并重启 `thinkfan.service`，`game-off` 会停止 `thinkfan.service` 并恢复 `level auto`
- 字体：用户级目录 `~/.local/share/fonts/fontawesome-7` 已安装 Font Awesome 7 Free/Brands（OTF）
- TI / CCS：当前用户目录下未保留 `Code Composer Studio`、`msp430ware` 或其他 `~/ti` 资源；不要默认按本机仍装有 TI 工具链处理

## 处理约定

- 优先给出兼容 `Wayland` 的方案，不默认按 `X11` 处理。
- 本机 `flameshot gui` 异常时，先区分快捷键问题与命令本身问题；命令本身异常时优先检查 `xdg-desktop-portal-wlr.service` 与 `useGrimAdapter`，再看缩放因素。
- 不默认假设安装了 `GNOME` 或 `KDE` 的专有工具。
- 涉及系统包管理时，优先按 `Arch Linux` 的方式处理，例如 `pacman`。
- 某些工具内启动的命令环境可能仍然是 `bash`，即使登录 shell 是 `fish`。
- fish：`~/.config/fish/conf.d/user.fish` 统一导出 `NO_PROXY/no_proxy`，默认绕过 `localhost` 与常见私有网段（`10/8`、`172.16/12`、`192.168/16`、`100.64/10`、`169.254/16`、`.local`）。
- 涉及本机应用的凭据安全存储时，优先复用 `gnome-keyring`，不要默认把敏感信息明文落到配置文件。

## 维护规则

- 这里只记录相对稳定的机器信息和长期约定。
- 不记录内存占用、磁盘使用量、运行时长、临时进程状态等会频繁变化的信息。
- 只要任务改变了本机的稳定软件或配置基线，结束前就要同步更新这份文件。
