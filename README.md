# Visualized Academic Papers

论文精读网页合集。每篇论文一个网页：拆开方法，按原表比例重画结果，把论文的主张和我们的判断分开写。同一专题的论文另有一页横向对照。

在线浏览：https://gongshukai.github.io/VisualizedAcademicPapers/

## 已收录

下面的列表由 `tools/build.py` 根据 `catalog.json` 生成，不要手改。

<!-- catalog:start -->
### 力与触觉（生成模型 / 机器人 / 力与触觉）

[专题对照页](https://gongshukai.github.io/VisualizedAcademicPapers/topics/force-tactile/)

- [ForceVLA](https://gongshukai.github.io/VisualizedAcademicPapers/papers/forcevla/) · 2025-05 · arXiv [2505.22159](https://arxiv.org/abs/2505.22159) — π0 加力感知 MoE：6 维力/力矩在 VLM 之后融合，5 个真机接触任务平均成功率 60.5%，不接力的 π0 为 37.3%。
- [Tactile-VLA](https://gongshukai.github.io/VisualizedAcademicPapers/papers/tactile-vla/) · 2025-07 · arXiv [2507.09160](https://arxiv.org/abs/2507.09160) — 触觉 token 进 VLM 前缀，动作里带目标力，交给位置-力混合控制器；主打「轻一点」「用力」这类力度词的零样本泛化。
- [T-Rex](https://gongshukai.github.io/VisualizedAcademicPapers/papers/t-rex/) · 2026-06 · arXiv [2606.17055](https://arxiv.org/abs/2606.17055) — 去噪轨迹从 τ=0.4 劈开：动作专家每块跑前 6 步，只读触觉的小专家在块内每 4 步用最新触觉跑完后 4 步；100 小时触觉中训练，12 个灵巧手任务平均 65 分，最强基线 35。
- [N₀-TWAM](https://gongshukai.github.io/VisualizedAcademicPapers/papers/n0-twam/) · 2026-07 · arXiv [2607.23783](https://arxiv.org/abs/2607.23783) — 视频、触觉、动作三专家的非对称 MoT 世界动作模型：未来触觉和未来视频一起生成，当前触觉在力空间经交叉注意力读入；UniVTAC 84.5%，8 个真机任务平均 46.3%（π0.5 30.0%）。
- [N₀-VTLA](https://gongshukai.github.io/VisualizedAcademicPapers/papers/n0-vtla/) · 2026-07 · arXiv [2607.23782](https://arxiv.org/abs/2607.23782) — 触觉不进 VLM 前缀，先预测接下来一个动作块的触觉变化潜变量 z，再用 z 条件动作专家；三阶段接入 π0.5，20 个仿真任务 63.8%（π0.5 44.0%），另有离线 RL 方法 ALTER。
- [Motus2](https://gongshukai.github.io/VisualizedAcademicPapers/papers/motus2/) · 2026-08 · arXiv [2608.30237](https://arxiv.org/abs/2608.30237) — 一套权重分别当策略、模拟器、评估器的自进化世界模型；触觉是一个旁路专家，在动作块内每 0.2 s 修正一次动作。
- [ME-Dex 1.0](https://gongshukai.github.io/VisualizedAcademicPapers/papers/me-dex/) · 2026-09 · arXiv [2609.21449](https://arxiv.org/abs/2609.21449) — 视频、触觉、动作三专家联合去噪的世界动作模型，触觉作为要预测的未来观测；夹爪和灵巧手的触觉统一到规范手。

### Harness for Robotics（机器人 / 基础模型 / Harness）

[专题对照页](https://gongshukai.github.io/VisualizedAcademicPapers/topics/robot-harness/)

#### （1）Context Architecture

设计模型每次决策时看到什么、以什么形式看到：检索、视觉选择、时序对齐等。

- [ActiveVLA](https://gongshukai.github.io/VisualizedAcademicPapers/papers/activevla/) · 2026-01 · arXiv [2601.08325](https://arxiv.org/abs/2601.08325) — 相机不动，在重建点云上挑虚拟视点再缩视场角放大：BridgeVLA 骨干的精阶段改看球面上选出的 3 个视图和 4 倍放大图；RLBench 91.8%（BridgeVLA 88.2），推理时间约翻倍。
- [TIC-VLA](https://gongshukai.github.io/VisualizedAcademicPapers/papers/tic-vla/) · 2026-02 · arXiv [2602.02459](https://arxiv.org/abs/2602.02459) — 把慢 VLM 的 KV cache 连同推理延迟 Δt 和期间位移 Δp 一起喂给 10 Hz 导航动作专家，训练时注入延迟；DynaNav 85 条 SR 55.29（最强语言基线 32.94），不建模延迟时 47.06 → 30.59（均无 RL）。
- [RA-VLA](https://gongshukai.github.io/VisualizedAcademicPapers/papers/ra-vla/) · 2026-08 · arXiv [2608.25585](https://arxiv.org/abs/2608.25585) — GR00T N1.5 外挂示范检索：DTW 监督的检索器按动作阶段取片段，动作头每层拼一段并用 margin 损失逼它读；LIBERO 留出套件平均 0.3845（最强基线 0.2085），UR5e 0.5625（0.3542）。

#### （2）Persistent State / Memory

在多步任务中持续保存任务状态、空间状态和执行历史，让当前动作不只依赖当前观测。

- [MemoryVLA](https://gongshukai.github.io/VisualizedAcademicPapers/papers/memoryvla/) · 2025-08 · arXiv [2508.19236](https://arxiv.org/abs/2508.19236) — CogACT 式 VLA 的 VLM 与 DiT 动作头之间插一个感知-认知记忆库：每步存 256 个感知 token + 1 个认知 token，cross-attention 检索、门控融合，库满合并相邻最相似条目；真机 6 个时序任务平均 83，CogACT 57。
- [OptimusVLA](https://gongshukai.github.io/VisualizedAcademicPapers/papers/optimusvla/) · 2026-02 · arXiv [2602.20200](https://arxiv.org/abs/2602.20200) — 给 π0.5 外挂两块记忆，都接在 flow 的去噪起点上：检索同类示范轨迹的均值和方差代替高斯噪声，按相似度定噪声和步数；Mamba 读上一个动作块再加偏置。LIBERO 平均 98.6（π0.5 96.9），NFE 3.2 vs 10。
- [SOMA](https://gongshukai.github.io/VisualizedAcademicPapers/papers/soma/) · 2026-05 · arXiv [2605.22283](https://arxiv.org/abs/2605.22283) — 可动头部先扫一圈，用 YOLO-World、DINOv3、VGGT 把每个物体压成带 3D 框的记忆 token，门控 EMA 刷新、交叉注意力读进 DiT；5 个视野外真机任务各阶段平均成功率 28.3%，GR00T N1.5 约 18%。
- [HiMe](https://gongshukai.github.io/VisualizedAcademicPapers/papers/hime/) · 2026-07 · arXiv [2607.03449](https://arxiv.org/abs/2607.03449) — π0.5 执行、Qwen3-VL-8B 判子任务是否完成、GPT-4o 只在交接点增改删图文记忆的三层框架；WidowX 三个长程任务平均任务进度 90%，FIFO 式 Flat Memory 65%。

#### （3）结构化执行 Structured Execution

把复杂任务组织为「推理 → 意图/子任务 → 动作」的分层受控执行流程，通过明确的中间接口连接高层决策与低层控制。

- [ACoT-VLA](https://gongshukai.github.io/VisualizedAcademicPapers/papers/acot-vla/) · 2026-01 · arXiv [2601.11404](https://arxiv.org/abs/2601.11404) — 结构化执行：π0.5 先用 EAR 去噪出一段 15 点、步长 2 的粗参考轨迹，再用 IAR 从 VLM 的 KV 里抽隐式先验，动作头读两者生成动作；LIBERO 98.5（π0.5 96.9），LIBERO-Plus 微调设定 88.0（75.7）。
- [MotorMind](https://gongshukai.github.io/VisualizedAcademicPapers/papers/motormind/) · 2026-09 · arXiv [2609.38078](https://arxiv.org/abs/2609.38078) — 结构化执行：冻结的通用 VLM 分饰规划、执行、监控、验证、记忆，输出带数值的中层动作交给确定性控制器，监控异步并行；LIBERO-PRO 零样本 66.7% / 扰动 53.8%，但每回合约 223 秒。

#### （4）评估与反馈 Evaluation & Feedback

在执行前或执行后引入显式评价信号，根据结果修正计划、更新状态或适应策略，形成闭环。

- [TT-VLA](https://gongshukai.github.io/VisualizedAcademicPapers/papers/tt-vla/) · 2026-01 · arXiv [2601.06748](https://arxiv.org/abs/2601.06748) — 评估与反馈：VLAC 进度估计的差分做每步奖励，无价值函数的 PPO 每 8 步更新一次 LoRA，每回合重置；4 个 VLA、15 个未见任务上维度平均提升 0.8–3.8 个点。
- [τ₀-VLA](https://gongshukai.github.io/VisualizedAcademicPapers/papers/tau0-vla/) · 2026-08 · arXiv [2608.16885](https://arxiv.org/abs/2608.16885) — 评估与反馈：带执行记忆的高层在不确定时做子任务束搜索，世界模型想象后果、价值模型打分后再提交；分层 + 记忆让四个长程真机任务平均成功率 27.5% → 45.0%，搜索再加 2–3 次成功 / 10。
<!-- catalog:end -->

## 目录结构

```
index.html                  首页，由 tools/build.py 生成
catalog.json                唯一的清单：专题和论文的元数据
papers/<slug>/index.html    一篇论文的精读页，图放在同目录的 fig/
topics/<id>/index.html      专题对照页，手写
tools/build.py              生成首页和 README 列表，刷新各页导航条，检查断链
tools/home.template.html    首页模板
docs/page-spec.md           精读页怎么做：取材、结构、设计要求
```

`papers/` 下按论文平铺，不按专题分目录。这样一篇论文的网址不会因为调整专题而变化，一篇论文也可以同时属于多个专题。

## 新增一篇论文

1. 按 [docs/page-spec.md](docs/page-spec.md) 做页面，保存为 `papers/<slug>/index.html`，图放进 `papers/<slug>/fig/`。页面可以是完整的 HTML 文档，也可以是 claude.ai artifact 的正文片段（没有 `<!doctype>`），构建时会自动补成完整文档。
2. 在 `catalog.json` 的 `papers` 里加一条：

   | 字段 | 含义 |
   |---|---|
   | `slug` | 目录名，小写短横线，例如 `tactile-vla` |
   | `title` | 短名，用在导航和列表里 |
   | `full_title` | 论文完整标题 |
   | `arxiv` / `version` | arXiv 编号和精读时依据的版本 |
   | `date` | arXiv 首版年月，`YYYY-MM`，专题内按它排序 |
   | `org` | 机构 |
   | `topics` | 所属专题 id 列表，第一个决定导航条里列出哪组论文 |
   | `category` | 专题下的类别 id，只在所属专题定义了 `categories` 时填 |
   | `summary` | 一句话：做了什么、关键数字 |
   | `added` | 收录日期 |

   如果是新专题，在 `topics` 里加一条（`id`、`title`、`path`、`summary`、`page`），并写好 `topics/<id>/index.html`。专题可以再分类别：加 `categories` 列表，每项含 `id`、`title`、`short`（导航条里显示的短名）、`summary`，首页、README 和导航条会按列出的顺序分组显示。
3. 运行构建：

   ```sh
   python3 tools/build.py
   ```

   它会更新首页和上面的列表，给新页面加上导航条，并报告断掉的图片或链接。有问题时退出码为 1。
4. 本地预览：

   ```sh
   python3 -m http.server 8000
   ```

   打开 http://localhost:8000/ 。
5. 提交并推送，GitHub Pages 会在一两分钟内更新。

## GitHub Pages

仓库设置里 Settings → Pages → Build and deployment 选 **Deploy from a branch**，分支选 `main`，目录选 `/ (root)`。根目录的 `.nojekyll` 让 Pages 原样发布所有文件。
