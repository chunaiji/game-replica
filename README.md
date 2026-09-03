# game-replica

`game-replica` 是一个 Codex Skill，用于在拥有源码和复刻权限的前提下，对游戏项目执行源码分析、功能等价重写、资源风格重制和最终验证。

复刻输出默认放在原项目同级目录：

```text
原项目: D:\games\demo
复刻项目: D:\games\demo_replace
```

Skill 会把原项目作为只读分析输入，代码和资源改动都应发生在 `_replace` 项目中，并尽量保持原项目文件布局一致。

## 安装

将整个 `game-replica` 文件夹复制到 Codex skills 目录：

```powershell
Copy-Item -Recurse . "$env:USERPROFILE\.codex\skills\game-replica"
```

或在项目根目录直接运行：

```powershell
.\install.ps1
```

安装后可在 Codex 中这样调用：

```text
Use $game-replica to analyze and replicate this game project.
```

## 目录

```text
game-replica/
├── SKILL.md
├── agents/openai.yaml
├── skills/
├── references/
└── scripts/
```

详细流程见 `SKILL.md`。
