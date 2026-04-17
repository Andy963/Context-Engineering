<!-- markdownlint-disable MD009 MD012 MD013 MD022 MD024 MD031 MD032 MD033 MD036 MD040 MD046 MD050 MD060 -->

# 原子（Atoms）：Prompting 的基本单元

> "If you wish to make an apple pie from scratch, you must first invent the universe." — Carl Sagan

## 原子：单条指令

在 context engineering 的旅程里，我们从最基础的单元开始：**atom**——一条给 LLM 的独立指令。

```
┌───────────────────────────────────────────────┐
│                                               │
│  "Write a poem about the ocean in 4 lines."   │
│                                               │
└───────────────────────────────────────────────┘
```

这就是最“纯”的 prompt engineering：一个人、一条指令、一次模型响应。简单、直接、原子化。

## 原子 Prompt 的结构

把一个有效的 atomic prompt 拆开来看：

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ATOMIC PROMPT = [TASK] + [CONSTRAINTS] + [OUTPUT FORMAT]   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

例如：

```
┌─────────────────────┬────────────────────────┬────────────────────┐
│        TASK         │      CONSTRAINTS       │   OUTPUT FORMAT    │
├─────────────────────┼────────────────────────┼────────────────────┤
│ "Write a poem       │ "about the ocean       │ "in 4 lines."      │
│  about space."      │  using only words      │                    │
│                     │  with 5 letters        │                    │
│                     │  or less."             │                    │
└─────────────────────┴────────────────────────┴────────────────────┘
```

## 原子的局限

atomic prompts 虽然是 LLM 交互的积木，但它们很快就会暴露出一些基本局限：

```
┌──────────────────────────────────────┐
│ LIMITATIONS OF ATOMIC PROMPTS        │
├──────────────────────────────────────┤
│ ✗ No memory across interactions      │
│ ✗ Limited demonstration capability   │
│ ✗ No complex reasoning scaffolds     │
│ ✗ Prone to ambiguity                 │
│ ✗ High variance in outputs           │
└──────────────────────────────────────┘
```

我们可以用一个简单实验做经验性度量：

```python
# A basic atomic prompt
atomic_prompt = "List 5 symptoms of diabetes."

# Send to LLM multiple times
responses = [llm.generate(atomic_prompt) for _ in range(5)]

# Measure variability
unique_symptoms = set()
for response in responses:
    symptoms = extract_symptoms(response)
    unique_symptoms.update(symptoms)

print(f"Found {len(unique_symptoms)} unique symptoms across 5 identical prompts")
# Typically outputs far more than just 5 unique symptoms
```

糖尿病常见的 5 个症状：

1. 多饮：经常口渴，喝水明显增多  
2. 多尿：排尿次数变多，尤其夜尿增多  
3. 多食：容易饥饿，吃得比平时多  
4. 体重下降：食量不一定减少，但体重却变轻  
5. 容易疲劳：常感到乏力、没精神  

如果你愿意，我也可以继续告诉你：
- 糖尿病的早期症状
- 1 型和 2 型糖尿病症状区别
- 什么时候该去医院检查

5 个糖尿病常见症状：

1. **频繁口渴**
2. **尿频**
3. **容易疲劳**
4. **体重不明原因下降**
5. **视力模糊**

如果你愿意，我也可以进一步告诉你：
- 这些症状为什么会出现
- 1 型和 2 型糖尿病症状有何区别
- 什么时候应该去做血糖检查

糖尿病常见的 5 个症状：

1. **经常口渴**
2. **排尿增多**
3. **容易感到疲劳**
4. **体重无明显原因下降**
5. **视力模糊**

如果你愿意，我也可以继续给你：
- 区分 **1 型 / 2 型糖尿病** 的常见表现
- 说明 **何时需要尽快就医**
- 列一个 **更完整的症状清单**

糖尿病常见的 5 个症状有：

1. **频繁口渴**
2. **尿频**
3. **容易感到疲劳**
4. **体重莫名下降**
5. **视力模糊**

如果你愿意，我也可以继续告诉你：
- 这些症状为什么会出现
- 糖尿病的早期表现
- 什么时候应该去做血糖检查

5 个常见的糖尿病症状：

1. 多尿  
2. 口渴明显增加  
3. 容易饥饿  
4. 体重不明原因下降  
5. 容易疲劳  

如果你愿意，我也可以继续补充：
- 早期症状
- 1 型和 2 型糖尿病症状区别
- 何时该去医院检查

以上5次测试使用的gpt-5.4 reasoning-efffort:high的情况测试的。

问题在哪里？当上下文极少时，模型很难保持一致性。

## 单原子基线：有用但有限

尽管有限，atomic prompts 依然是非常重要的基线（baseline）。它们帮助我们：

1. 度量 token 效率（额外开销最小）
2. 基准化比较回答质量
3. 为实验建立对照组（control）

```
                     [Response Quality]
                            ▲
                            │
                            │               ⭐ Context
                            │                 Engineering
                            │               
                            │           
                            │       ⭐ Advanced
                            │         Prompting
                            │
                            │   ⭐ Basic Prompting
                            │
                            │
                            └────────────────────────►
                                  [Complexity]
```

## 未明说的上下文：模型“默认知道”的东西

即使只给 atomic prompt，LLM 也会调用训练中习得的大量隐式上下文：

```
┌───────────────────────────────────────────────────────────────┐
│ IMPLICIT CONTEXT IN MODELS                                    │
├───────────────────────────────────────────────────────────────┤
│ ✓ Language rules and grammar                                  │
│ ✓ Common knowledge facts                                      │
│ ✓ Format conventions (lists, paragraphs, etc.)                │
│ ✓ Domain-specific knowledge (varies by model)                 │
│ ✓ Learned interaction patterns                                │
└───────────────────────────────────────────────────────────────┘
```

这些隐式知识让我们在“零上下文”时也能得到可用输出，但它不稳定，而且会随模型与版本变化。

## 幂律：Token-质量曲线

在许多任务上，我们会观察到一种“上下文 token 数量”和“输出质量”之间的幂律关系：

```
Quality
      ▲
      │                        •
      │                    •       •
      │                •               •
      │            •                       •
      │        •                               •
      │    •
      │•
      └───────────────────────────────────────────► Tokens
          [Poor Start]  [Maximum ROI]  [Diminishing Returns]
```

关键洞见在于：存在一个“最大 ROI 区间”，在这里增加少量 tokens 就能显著提升质量；也存在“边际递减区间”，在这里继续堆 tokens 反而可能带来性能下降或不稳定。

## [了解更多：Context Rot](https://research.trychroma.com/context-rot)

## 从原子到分子：为什么需要更多上下文

atom 的局限会自然把我们带到下一步：**molecules**——把指令与示例、补充上下文、结构化格式组合在一起的多段 prompts。

下面是这种转变的基本形态：

```
┌──────────────────────────┐         ┌──────────────────────────┐
│                          │         │ "Here's an example:      │
│ "Write a limerick about  │    →    │  There once was a...     │
│  a programmer."          │         │                          │
│                          │         │  Now write a limerick    │
└──────────────────────────┘         │  about a programmer."    │
                                     └──────────────────────────┘
    [Atomic Prompt]                       [Molecular Prompt]
```

当我们加入 examples 和结构时，就开始“有意塑形”上下文窗口——这正是走向 context engineering 的第一步。

## 度量原子效率：你的第一个练习

在继续之前，你可以做一个非常简单的练习：

1. 选择一个你常给 LLM 的基础任务
2. 写出三个不同版本的 atomic prompt
3. 度量 tokens 消耗与主观质量
4. 画出效率前沿（efficiency frontier）

```
┌─────────────────────────────────────────────────────────────┐
│ Task: Summarize a news article                              │
├─────────┬───────────────────────────────┬────────┬──────────┤
│ Version │ Prompt                        │ Tokens │ Quality  │
├─────────┼───────────────────────────────┼────────┼──────────┤
│ A       │ "Summarize this article."     │ 4      │ 2/10     │
├─────────┼───────────────────────────────┼────────┼──────────┤
│ B       │ "Provide a concise summary    │ 14     │ 6/10     │
│         │  of this article in 3         │        │          │
│         │  sentences."                  │        │          │
├─────────┼───────────────────────────────┼────────┼──────────┤
│ C       │ "Write a summary of the key   │ 27     │ 8/10     │
│         │  points in this article,      │        │          │
│         │  highlighting the main        │        │          │
│         │  people and events."          │        │          │
└─────────┴───────────────────────────────┴────────┴──────────┘
```

## 关键要点

1. **Atomic prompts** 是 LLM 交互的基本单元
2. 它们遵循基本结构：task + constraints + output format
3. 它们有天然限制：没有 memory、examples 与 reasoning scaffolds
4. 即使很简单的 atomic prompt 也会依赖模型的隐式知识
5. context tokens 与质量之间常呈幂律关系
6. 从 atoms 走向 molecules，是进入 context engineering 的第一步

## 下一步

下一节将介绍如何把 atoms 组合成 **molecules**——few-shot learning 模式，它能显著提升可靠性与可控性。

[继续阅读 02_molecules_context.md →](02_molecules_context.md)

---

## 深入：Prompt Templates

如果你想对 atomic prompts 做更多实验，这里有一些可以直接复用的模板：

```
# Basic instruction
{task}

# Persona-based
As a {persona}, {task}

# Format-specific
{task}
Format: {format_specification}

# Constraint-based
{task}
Constraints:
- {constraint_1}
- {constraint_2}
- {constraint_3}

# Step-by-step guided
{task}
Please follow these steps:
1. {step_1}
2. {step_2}
3. {step_3}
```

建议你把同一个任务套到不同模板上，实际测一下 token 数和输出质量的变化。
