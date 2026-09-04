# game-replica

> An AI Agent Skill for source-based game replication.

`game-replica` 不是普通的 AI 游戏生成器。它面向已有游戏源码，帮助 Codex / Claude Code 按原框架做功能等价复刻、资源重制和运行时验证。

它默认把复刻结果放在原项目同级目录的 `XXX_replace` 中，原项目保持只读。

## What it does

- 读取已有游戏源码并分析结构、参数、资源和行为。
- 生成复刻计划，并按模块重写代码。
- 按原规格或用户风格要求重制资源。
- 备份生成图后再切图、裁切、分帧。
- 将成品替换到复刻项目 `XXX_replace` 中的对应路径。
- 最后做构建、参数、资源、输入、事件和运行时验证。

## Workflow

```text
01 source-analyzer
    ↓
02 code-replica
    ↓
03 asset-restyle
    ↓
04 replica-validator
```

### Workspace rule

```text
<parent>/
├── <original-folder>/
└── <original-folder>_replace/
```

所有修改都应发生在 `_replace` 工作区里，尽量保持与原项目一致的目录布局。

## Installation

复制整个仓库到 Codex skills 目录，或直接运行安装脚本：

```powershell
.\install.ps1
```

安装后可在 Codex 中这样调用：

```text
Use $game-replica to analyze and replicate this game project.
```

## Usage

1. 准备原始游戏项目源码。
2. 运行 `source-analyzer` 生成分析产物。
3. 在 `XXX_replace` 工作区中执行代码复刻。
4. 如需换皮，先生成、备份、切图，再替换到复刻项目对应路径。
5. 运行验证阶段，确认 `REPLICATION COMPLETE`。

## Asset pipeline

生成图的推荐顺序：

```text
Generate
    ↓
Backup raw generated files
    ↓
Cut / slice / crop
    ↓
Normalize size / alpha / format
    ↓
Replace in XXX_replace
```

## Project structure

```text
game-replica/
├── SKILL.md
├── agents/
├── references/
├── scripts/
├── skills/
├── doc/
└── install.ps1
```

## Supported workflows

- Source analysis
- Code replication
- Asset restyling
- Runtime validation

## Validation

The final validator checks:

- framework
- build
- parameters
- functions
- game logic
- input
- events
- assets
- animation
- runtime
- critical behavior

## Examples

Add your own before/after screenshots, GIFs, or case studies here when you have a real game project to showcase.

## Roadmap

- [x] Source analysis workflow
- [x] Code replication workflow
- [x] Asset restyling workflow
- [x] Validation workflow
- [ ] More framework-specific examples
- [ ] Demo cases
- [ ] Visual regression checks
- [ ] More automation helpers

## Legal / Usage Notice

This skill is intended for game source code, assets, and projects that you own or are explicitly allowed to modify, reproduce, or transform.

Do not use it to reproduce third-party games, assets, trademarks, or proprietary code without authorization.

## Related files

- [SKILL.md](SKILL.md)
- [skills/01-source-analyzer/SKILL.md](skills/01-source-analyzer/SKILL.md)
- [skills/02-code-replica/SKILL.md](skills/02-code-replica/SKILL.md)
- [skills/03-asset-restyle/SKILL.md](skills/03-asset-restyle/SKILL.md)
- [skills/04-replica-validator/SKILL.md](skills/04-replica-validator/SKILL.md)
