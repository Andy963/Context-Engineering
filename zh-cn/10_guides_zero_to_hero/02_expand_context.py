#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Context Expansion Techniques: From Prompts to Layered Context
=============================================================

This guide presents hands-on strategies for evolving basic prompts into layered, information-rich
contexts that enhance LLM performance. The focus is on practical context engineering: how to
strategically add and structure context layers, and systematically measure the effects on both
token usage and output quality.

Key concepts covered:
1. Transforming minimal prompts into expanded, context-rich structures
2. Principles of context layering and compositional prompt engineering
3. Quantitative measurement of token usage as context grows
4. Qualitative assessment of model output improvements
5. Iterative approaches to context refinement and optimization

Usage:
    python 02_expand_context.py

Notes:
    - Each section is modular: experiment by editing and running different context layers.
    - Track how additional context alters both cost (token count) and performance (output quality).
    - This file is intentionally a .py script (not a notebook). All narrative is preserved as
      comments/docstrings so the file compiles and can run end-to-end.
"""

from __future__ import annotations

import os
import time
from typing import Any, Dict, List, Optional, Tuple

# Optional dependencies. Keep imports resilient so the file runs even if some are missing.
try:
    import dotenv  # type: ignore
except Exception:
    dotenv = None  # type: ignore

try:
    import numpy as np  # type: ignore
except Exception:
    np = None  # type: ignore

try:
    import matplotlib.pyplot as plt  # type: ignore
except Exception:
    plt = None  # type: ignore

try:
    import tiktoken  # type: ignore
except Exception:
    tiktoken = None  # type: ignore


# --------------------------------------------------------------------------------------
# Setup and Prerequisites
# --------------------------------------------------------------------------------------
# This guide supports OpenAI and Groq via an OpenAI-compatible client.
#
# Environment variables (choose one):
#   - OPENAI_API_KEY=...
#   - GROQ_API_KEY=...
#
# Optional:
#   - LLM_PROVIDER=openai | groq   (default: auto-detect)
#   - LLM_MODEL=...                (default: provider-specific)
#
# Groq uses an OpenAI-compatible API base URL:
#   https://api.groq.com/openai/v1
# --------------------------------------------------------------------------------------

if dotenv is not None:
    dotenv.load_dotenv()

DEFAULT_OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DEFAULT_GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")

LLM_PROVIDER = (os.getenv("LLM_PROVIDER") or "").strip().lower()
OPENAI_API_KEY = (os.getenv("OPENAI_API_KEY") or "").strip()
GROQ_API_KEY = (os.getenv("GROQ_API_KEY") or "").strip()
LLM_MODEL = (os.getenv("LLM_MODEL") or "").strip()

GROQ_BASE_URL = "https://api.groq.com/openai/v1"


def _select_provider_and_model() -> Tuple[str, str]:
    """
    Decide provider/model without forcing the user to edit code.
    Priority:
      1) explicit LLM_PROVIDER + LLM_MODEL
      2) explicit LLM_PROVIDER with default model
      3) auto-detect key presence: OpenAI > Groq
    """
    if LLM_PROVIDER in {"openai", "groq"}:
        if LLM_MODEL:
            return LLM_PROVIDER, LLM_MODEL
        return LLM_PROVIDER, (DEFAULT_OPENAI_MODEL if LLM_PROVIDER == "openai" else DEFAULT_GROQ_MODEL)

    # auto-detect
    if OPENAI_API_KEY:
        return "openai", (LLM_MODEL or DEFAULT_OPENAI_MODEL)
    if GROQ_API_KEY:
        return "groq", (LLM_MODEL or DEFAULT_GROQ_MODEL)

    # no keys found
    return "none", (LLM_MODEL or DEFAULT_OPENAI_MODEL)


PROVIDER, MODEL = _select_provider_and_model()


def _build_client() -> Optional[Any]:
    """
    Build an OpenAI-compatible client.
    Uses openai>=1.x SDK if installed.
    """
    if PROVIDER == "none":
        return None

    try:
        from openai import OpenAI  # type: ignore
    except Exception:
        return None

    if PROVIDER == "openai":
        return OpenAI(api_key=OPENAI_API_KEY)

    # PROVIDER == "groq"
    return OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)


CLIENT = _build_client()


def _build_tokenizer(model_name: str) -> Optional[Any]:
    """
    Token counting is best-effort.
    - If tiktoken is unavailable, fallback to a rough heuristic.
    - If model is unknown to tiktoken, fallback to cl100k_base when available.
    """
    if tiktoken is None:
        return None
    try:
        return tiktoken.encoding_for_model(model_name)
    except Exception:
        try:
            return tiktoken.get_encoding("cl100k_base")
        except Exception:
            return None


TOKENIZER = _build_tokenizer(MODEL)


def count_tokens(text: str) -> int:
    """Count tokens in a string using the available tokenizer (best-effort)."""
    if TOKENIZER is not None:
        try:
            return len(TOKENIZER.encode(text))
        except Exception:
            pass
    # Fallback approximation (intentionally simple)
    return int(len(text.split()) * 1.3)


def measure_latency(func, *args, **kwargs) -> Tuple[Any, float]:
    """Measure execution time of a function."""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return result, end_time - start_time


# --------------------------------------------------------------------------------------
# 1. Understanding Context Expansion
# --------------------------------------------------------------------------------------
# In the previous guide (01_min_prompt), we explored the basics of atomic prompts.
# Now we'll see how to strategically expand these atoms into molecules (richer context structures).
# We'll measure:
#   - prompt tokens
#   - response tokens
#   - token efficiency (response/prompt)
#   - latency
#   - latency per 1k prompt tokens
# --------------------------------------------------------------------------------------


def calculate_metrics(prompt: str, response: str, latency: float) -> Dict[str, float]:
    """Calculate key metrics for a prompt-response pair."""
    prompt_tokens = count_tokens(prompt)
    response_tokens = count_tokens(response)

    token_efficiency = response_tokens / prompt_tokens if prompt_tokens > 0 else 0.0
    latency_per_1k = (latency / prompt_tokens) * 1000 if prompt_tokens > 0 else 0.0

    return {
        "prompt_tokens": float(prompt_tokens),
        "response_tokens": float(response_tokens),
        "token_efficiency": float(token_efficiency),
        "latency": float(latency),
        "latency_per_1k": float(latency_per_1k),
    }


def generate_response(prompt: str, temperature: float = 0.7, max_tokens: int = 500) -> Tuple[str, float]:
    """
    Generate a response from the LLM and measure latency.

    If no client/provider is configured, returns a deterministic placeholder response
    so the rest of the guide can still run (metrics/plots).
    """
    if CLIENT is None:
        placeholder = (
            "LLM is not configured (missing client or API key). "
            "Set OPENAI_API_KEY or GROQ_API_KEY to generate real outputs."
        )
        return placeholder, 0.0

    def _call() -> str:
        resp = CLIENT.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content

    response_text, latency = measure_latency(_call)
    return response_text, latency


# --------------------------------------------------------------------------------------
# 2. Experiment: Context Expansion Techniques
# --------------------------------------------------------------------------------------
# We'll test different ways to expand a base prompt:
#   - role assignment
#   - few-shot examples
#   - constraints
#   - audience specification
#   - comprehensive (combining multiple layers)
# --------------------------------------------------------------------------------------


def run_experiments() -> Tuple[Dict[str, Dict[str, float]], Dict[str, str], Dict[str, str]]:
    # Base prompt (atom)
    base_prompt = "Write a paragraph about climate change."

    # Expanded prompt variations (molecules)
    expanded_prompts: Dict[str, str] = {
        "base": base_prompt,
        "with_role": (
            "You are an environmental scientist with expertise in climate systems.\n"
            "Write a paragraph about climate change."
        ),
        "with_examples": (
            "Write a paragraph about climate change.\n\n"
            "Example 1:\n"
            "Climate change refers to long-term shifts in temperatures and weather patterns. "
            "Human activities have been the main driver of climate change since the 1800s, "
            "primarily due to the burning of fossil fuels like coal, oil, and gas, which produces "
            "heat-trapping gases.\n\n"
            "Example 2:\n"
            "Global climate change is evident in the increasing frequency of extreme weather events, "
            "rising sea levels, and shifting wildlife populations. Scientific consensus points to "
            "human activity as the primary cause."
        ),
        "with_constraints": (
            "Write a paragraph about climate change.\n"
            "- Include at least one scientific fact with numbers\n"
            "- Mention both causes and effects\n"
            "- End with a call to action\n"
            "- Keep the tone informative but accessible"
        ),
        "with_audience": (
            "Write a paragraph about climate change for high school students who are\n"
            "just beginning to learn about environmental science. Use clear explanations\n"
            "and relatable examples."
        ),
        "comprehensive": (
            "You are an environmental scientist with expertise in climate systems.\n\n"
            "Write a paragraph about climate change for high school students who are\n"
            "just beginning to learn about environmental science. Use clear explanations\n"
            "and relatable examples.\n\n"
            "Guidelines:\n"
            "- Include at least one scientific fact with numbers\n"
            "- Mention both causes and effects\n"
            "- End with a call to action\n"
            "- Keep the tone informative but accessible\n\n"
            "Example of tone and structure:\n"
            "\"Ocean acidification occurs when seawater absorbs CO2 from the atmosphere, causing pH levels to drop. "
            "Since the Industrial Revolution, ocean pH has decreased by 0.1 units, representing a 30% increase in acidity. "
            "This affects marine life, particularly shellfish and coral reefs, as it impairs their ability to form shells and skeletons. "
            "Scientists predict that if emissions continue at current rates, ocean acidity could increase by 150% by 2100, devastating marine ecosystems. "
            "By reducing our carbon footprint through simple actions like using public transportation, we can help protect these vital ocean habitats.\""
        ),
    }

    results: Dict[str, Dict[str, float]] = {}
    responses: Dict[str, str] = {}

    print(f"\nModel: {MODEL}")
    print("Running context expansion experiments...\n")

    for name, prompt in expanded_prompts.items():
        print(f"--- Testing: {name} ---")
        response, latency = generate_response(prompt)
        responses[name] = response
        metrics = calculate_metrics(prompt, response, latency)
        results[name] = metrics
        print(f"Prompt tokens:    {int(metrics['prompt_tokens'])}")
        print(f"Response tokens:  {int(metrics['response_tokens'])}")
        print(f"Latency:         {metrics['latency']:.2f}s")
        print("-" * 40)

    return results, responses, expanded_prompts


# --------------------------------------------------------------------------------------
# 3. Visualizing and Analyzing Results
# --------------------------------------------------------------------------------------
# If matplotlib is installed, we plot:
#   - Token usage (prompt/response)
#   - Token efficiency
#   - Latency
#   - Latency per 1k tokens
# --------------------------------------------------------------------------------------


def plot_results(results: Dict[str, Dict[str, float]]) -> None:
    if plt is None:
        print("\nmatplotlib not installed. Skipping plots.\n")
        return

    prompt_types = list(results.keys())
    prompt_tokens = [results[k]["prompt_tokens"] for k in prompt_types]
    response_tokens = [results[k]["response_tokens"] for k in prompt_types]
    latencies = [results[k]["latency"] for k in prompt_types]
    token_efficiency = [results[k]["token_efficiency"] for k in prompt_types]
    latency_per_1k = [results[k]["latency_per_1k"] for k in prompt_types]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Token usage
    axes[0, 0].bar(prompt_types, prompt_tokens, label="Prompt Tokens", alpha=0.7)
    axes[0, 0].bar(prompt_types, response_tokens, bottom=prompt_tokens, label="Response Tokens", alpha=0.7)
    axes[0, 0].set_title("Token Usage by Prompt Type")
    axes[0, 0].set_ylabel("Tokens")
    axes[0, 0].legend()
    plt.setp(axes[0, 0].get_xticklabels(), rotation=45, ha="right")

    # Token efficiency
    axes[0, 1].bar(prompt_types, token_efficiency, alpha=0.7)
    axes[0, 1].set_title("Token Efficiency (Response/Prompt)")
    axes[0, 1].set_ylabel("Efficiency Ratio")
    plt.setp(axes[0, 1].get_xticklabels(), rotation=45, ha="right")

    # Latency
    axes[1, 0].bar(prompt_types, latencies, alpha=0.7)
    axes[1, 0].set_title("Response Latency")
    axes[1, 0].set_ylabel("Seconds")
    plt.setp(axes[1, 0].get_xticklabels(), rotation=45, ha="right")

    # Latency per 1k
    axes[1, 1].bar(prompt_types, latency_per_1k, alpha=0.7)
    axes[1, 1].set_title("Latency per 1k Prompt Tokens")
    axes[1, 1].set_ylabel("Seconds per 1k")
    plt.setp(axes[1, 1].get_xticklabels(), rotation=45, ha="right")

    plt.tight_layout()
    plt.show()


# --------------------------------------------------------------------------------------
# 4. Qualitative Analysis
# --------------------------------------------------------------------------------------
# We print the full responses so you can compare output quality across prompts.
# --------------------------------------------------------------------------------------


def print_responses(responses: Dict[str, str]) -> None:
    print("\nQualitative Analysis (Responses)\n" + "=" * 80)
    for name, response in responses.items():
        print(f"\n=== Response for '{name}' prompt ===\n")
        print(response)
        print("\n" + "=" * 80)


# --------------------------------------------------------------------------------------
# 5. Context Expansion Patterns
# --------------------------------------------------------------------------------------
# Based on our experiments, we can identify several effective context expansion patterns:
#   1) Role Assignment
#   2) Few-shot Examples
#   3) Constraint Definition
#   4) Audience Specification
#   5) Comprehensive Context (combining multiple elements)
# --------------------------------------------------------------------------------------


def create_expanded_context(
    base_prompt: str,
    role: Optional[str] = None,
    examples: Optional[List[str]] = None,
    constraints: Optional[List[str]] = None,
    audience: Optional[str] = None,
    tone: Optional[str] = None,
    output_format: Optional[str] = None,
) -> str:
    """
    Create an expanded context from a base prompt with optional components.

    Args:
        base_prompt: The core instruction or question
        role: Who the model should act as
        examples: List of example outputs to guide the model
        constraints: List of requirements or boundaries
        audience: Who the output is intended for
        tone: Desired tone of the response
        output_format: Specific format requirements

    Returns:
        Expanded context as a string
    """
    context_parts: List[str] = []

    if role:
        context_parts.append(f"You are {role}.")

    context_parts.append(base_prompt)

    if audience:
        context_parts.append(f"Your response should be suitable for {audience}.")

    if tone:
        context_parts.append(f"Use a {tone} tone in your response.")

    if output_format:
        context_parts.append(f"Format your response as {output_format}.")

    if constraints:
        context_parts.append("Requirements:")
        for c in constraints:
            context_parts.append(f"- {c}")

    if examples:
        context_parts.append("Examples:")
        for i, ex in enumerate(examples, 1):
            context_parts.append(f"Example {i}:\n{ex}")

    return "\n\n".join(context_parts)


def demo_template() -> None:
    new_base_prompt = "Explain how photosynthesis works."

    new_expanded_context = create_expanded_context(
        base_prompt=new_base_prompt,
        role="a biology teacher with 15 years of experience",
        audience="middle school students",
        tone="enthusiastic and educational",
        constraints=[
            "Use a plant-to-factory analogy",
            "Mention the role of chlorophyll",
            "Explain the importance for Earth's ecosystem",
            "Keep it under 200 words",
        ],
        examples=[
            (
                "Photosynthesis is like a tiny factory inside plants. Just as a factory needs raw materials, "
                "energy, and workers to make products, plants need carbon dioxide, water, sunlight, and "
                "chlorophyll to make glucose (sugar) and oxygen. The sunlight is the energy source, "
                "chlorophyll molecules are the workers that capture this energy, while carbon dioxide and "
                "water are the raw materials. The factory's products are glucose, which the plant uses for "
                "growth and energy storage, and oxygen, which is released into the air for animals like us "
                "to breathe. This process is essential for life on Earth because it provides the oxygen we "
                "need and removes carbon dioxide from the atmosphere."
            )
        ],
    )

    print("\nTemplate-generated expanded context:\n" + "-" * 80)
    print(new_expanded_context)
    print("-" * 80)
    print(f"Token count (best-effort): {count_tokens(new_expanded_context)}")

    response, latency = generate_response(new_expanded_context)
    metrics = calculate_metrics(new_expanded_context, response, latency)

    print("\nResponse:\n" + "-" * 80)
    print(response)
    print("-" * 80)
    print(f"Response tokens (best-effort): {int(metrics['response_tokens'])}")
    print(f"Latency: {metrics['latency']:.2f}s")


# --------------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------------


def main() -> None:
    if PROVIDER == "none":
        print(
            "No LLM provider configured.\n"
            "Set OPENAI_API_KEY or GROQ_API_KEY (or set LLM_PROVIDER=openai|groq).\n"
            "This script will still run with placeholder responses.\n"
        )
    else:
        if CLIENT is None:
            print(
                "Provider was selected but the OpenAI-compatible SDK client could not be created.\n"
                "Install the OpenAI Python SDK: pip install openai\n"
                "Then re-run.\n"
            )

    results, responses, _prompts = run_experiments()
    plot_results(results)
    print_responses(responses)
    demo_template()


if __name__ == "__main__":
    main()

"""
Model: gpt-5.4
Running context expansion experiments...

--- Testing: base ---
Prompt tokens:    7
Response tokens:  133
Latency:         3.60s
----------------------------------------
--- Testing: with_role ---
Prompt tokens:    18
Response tokens:  157
Latency:         6.59s
----------------------------------------
--- Testing: with_examples ---
Prompt tokens:    102
Response tokens:  120
Latency:         3.54s
----------------------------------------
--- Testing: with_constraints ---
Prompt tokens:    39
Response tokens:  174
Latency:         4.17s
----------------------------------------
--- Testing: with_audience ---
Prompt tokens:    30
Response tokens:  159
Latency:         3.77s
----------------------------------------
--- Testing: comprehensive ---
Prompt tokens:    202
Response tokens:  206
Latency:         6.93s
----------------------------------------

Qualitative Analysis (Responses)
================================================================================

=== Response for 'base' prompt ===

Climate change refers to long-term shifts in Earth’s temperatures and weather patterns,
largely caused today by human activities such as burning fossil fuels, cutting down forests,
and industrial agriculture. These actions increase the amount of greenhouse gases like carbon
dioxide and methane in the atmosphere, which trap heat and warm the planet.

As a result, the world is experiencing rising temperatures, melting glaciers, stronger storms,
more frequent heatwaves, droughts, and rising sea levels. Climate change also threatens
ecosystems, food supplies, water resources, and human health.

Addressing it requires reducing emissions, investing in clean energy, protecting natural
habitats, and working together globally to create a more sustainable future.

中文：
气候变化是指地球气温和天气模式的长期变化，而当今这种变化主要由人类活动造成，
例如燃烧化石燃料、砍伐森林和工业化农业。这些行为会增加大气中二氧化碳、
甲烷等温室气体的含量，这些气体会困住热量并使地球升温。

因此，全球正在经历气温上升、冰川融化、更强的风暴、更频繁的热浪、干旱以及
海平面上升。气候变化还威胁着生态系统、粮食供应、水资源和人类健康。

要应对这一问题，需要减少排放、投资清洁能源、保护自然栖息地，并在全球范围内
协作，建设一个更可持续的未来。

评价：
这是最基础的一版，没有额外的角色、受众或语气控制。回复整体中性、概括性强，
覆盖了定义、成因、影响和应对方式，算是比较标准的百科式回答。但也正因为没有
额外约束，它没有明显的风格特征，面向谁说、用什么口吻说都不突出。

================================================================================

=== Response for 'with_role' prompt ===

Climate change refers to long-term shifts in Earth’s temperature, precipitation, and weather
patterns, driven largely today by human activities such as burning fossil fuels, deforestation,
and industrial agriculture. These activities release greenhouse gases like carbon dioxide and
methane, which trap heat in the atmosphere and cause global temperatures to rise.

As a result, the world is experiencing more frequent and intense heatwaves, stronger storms,
melting glaciers, rising sea levels, ocean acidification, and disruptions to ecosystems and
agriculture. Climate change also affects human health, water resources, and food security,
with the greatest impacts often falling on vulnerable communities that have contributed the
least to the problem.

Addressing climate change requires both mitigation, by reducing greenhouse gas emissions,
and adaptation, by preparing societies and ecosystems for the changes already underway.

中文：
气候变化是指地球温度、降水和天气模式的长期变化，而如今这种变化主要由人类活动
驱动，例如燃烧化石燃料、森林砍伐和工业化农业。这些活动会释放二氧化碳、
甲烷等温室气体，它们将热量困在大气中并导致全球气温上升。

因此，全球正在经历更频繁、更强烈的热浪、更猛烈的风暴、冰川融化、海平面上升、
海洋酸化，以及生态系统和农业受到扰动。气候变化还会影响人类健康、水资源和
粮食安全，而影响最严重的往往是那些对问题贡献最少的脆弱群体。

应对气候变化既需要通过减少温室气体排放来缓解问题，也需要通过让社会和生态系统
为已经发生的变化做好准备来适应现实。

评价：
`role` 的效果是明显的。这一版更像“环境科学工作者”的表达方式：术语更完整，
不仅提到 temperature，还加入了 precipitation、ocean acidification、food security、
mitigation 和 adaptation，专业密度明显更高。代价是可读性略低于基础版，
更适合已经有一点背景知识的读者。

================================================================================

=== Response for 'with_examples' prompt ===

Climate change is the long-term alteration of Earth’s temperature, weather patterns, and
ecosystems, largely driven by human activities such as burning fossil fuels, deforestation,
and industrial processes. These actions release greenhouse gases like carbon dioxide and
methane into the atmosphere, trapping heat and causing global temperatures to rise.

As a result, the planet is experiencing more frequent and intense heatwaves, storms, droughts,
melting glaciers, rising sea levels, and disruptions to plant and animal life.

Addressing climate change requires reducing emissions, transitioning to cleaner energy sources,
and adopting sustainable practices to protect the environment for future generations.

中文：
气候变化是指地球温度、天气模式和生态系统的长期改变，这种改变主要由人类活动
推动，例如燃烧化石燃料、森林砍伐和工业过程。这些行为会向大气中释放二氧化碳、
甲烷等温室气体，从而困住热量并导致全球气温上升。

因此，地球正在经历更频繁、更强烈的热浪、风暴、干旱、冰川融化、海平面上升，
以及动植物生存环境受到干扰。

要应对气候变化，需要减少排放、转向更清洁的能源来源，并采用可持续做法，
为后代保护环境。

评价：
`examples` 的效果也比较明显。相比基础版，这一版的句式和结构更收敛，读起来更像
“教材标准答案”，说明示例确实把输出拉向了给定范式。不过它也更保守，信息点没有
`with_role` 那么丰富，属于稳定性更强、但探索性更弱的一类结果。

================================================================================

=== Response for 'with_constraints' prompt ===

Climate change is the long-term warming of Earth’s climate, driven mainly by human activities
such as burning coal, oil, and gas, which release heat-trapping greenhouse gases like carbon
dioxide into the atmosphere.

A key scientific fact is that global average temperatures have risen by about 1.1°C since
the late 1800s, and atmospheric carbon dioxide levels have increased to over 420 parts per
million, far above preindustrial levels of about 280 ppm.

These changes are contributing to more frequent heat waves, stronger storms, melting glaciers,
rising sea levels, and disruptions to ecosystems, agriculture, and human health around the
world. While the problem is serious, its worst impacts can still be reduced if governments,
businesses, and individuals act quickly to cut emissions, expand clean energy, and protect
natural systems, so now is the time to support meaningful climate action.

中文：
气候变化是地球气候的长期变暖，主要由人类活动驱动，例如燃烧煤、石油和天然气，
这些行为会向大气中释放二氧化碳等会困住热量的温室气体。

一个关键科学事实是，自 19 世纪末以来，全球平均气温已经上升了约 1.1°C，
而大气中的二氧化碳浓度也已增加到每百万超过 420 份，远高于工业化前
大约 280 ppm 的水平。

这些变化正在导致全球范围内更频繁的热浪、更强的风暴、冰川融化、海平面上升，
以及生态系统、农业和人类健康受到扰动。虽然问题很严重，但如果政府、企业和个人
迅速行动起来减少排放、扩展清洁能源并保护自然系统，最严重的影响仍然可以被减轻，
所以现在正是支持真正气候行动的时候。

评价：
`constraints` 的效果最容易验证，因为几乎每条约束都能在输出里对上。它确实加入了
带数字的科学事实，同时同时写到了 causes 和 effects，最后也有明确的 call to action。
这说明“显式要求”在这里比抽象风格提示更稳定、更可检验，是最有评估价值的一组。

================================================================================

=== Response for 'with_audience' prompt ===

Climate change is the long-term warming of Earth caused mainly by human activities like
burning coal, oil, and gas for energy. These activities release gases such as carbon dioxide
into the atmosphere, where they act like a thickening blanket that traps heat from the sun.

As a result, average temperatures rise, which can lead to stronger heat waves, melting ice,
rising sea levels, and more extreme weather like heavy storms or droughts. You can think of
it like adding extra layers to a greenhouse that make it harder for heat to escape.

Climate change also affects everyday life by influencing food production, water supplies,
and the places plants and animals can live. Understanding it is important because the choices
people make, such as saving energy, using cleaner transportation, and protecting forests,
can help reduce its impact.

中文：
气候变化是地球长期变暖的现象，主要由人类活动引起，例如为了获取能源而燃烧煤、
石油和天然气。这些活动会向大气中释放二氧化碳等气体，这些气体就像一层
越来越厚的毯子，把来自太阳的热量困住。

结果就是平均气温上升，从而带来更强的热浪、冰层融化、海平面上升，以及
更极端的天气，例如强风暴或干旱。你可以把它想象成温室外又多加了几层覆盖物，
让热量更难散出去。

气候变化还会通过影响粮食生产、水资源供应以及动植物能够生存的地方，改变人们的
日常生活。理解这一问题很重要，因为人们做出的选择，例如节约能源、使用更清洁的
交通方式和保护森林，都能帮助减轻它的影响。

评价：
`audience` 的效果也比较明显。这一版明显更面向初学者，使用了“毯子”“温室多加几层”
这类易懂类比，句子更口语化，解释也更循序渐进。专业精确度略低一点，但对高中生
这种目标受众来说反而更合适，说明受众设定确实影响了表达层级。

================================================================================

=== Response for 'comprehensive' prompt ===

Climate change is the long-term warming of Earth caused mainly by human activities such as
burning coal, oil, and gas, which release carbon dioxide and other heat-trapping gases into
the atmosphere.

Since the late 1800s, Earth’s average temperature has risen by about 1.2°C (2.2°F), and even
that small-sounding change can have big effects, like stronger heat waves, melting glaciers,
rising sea levels, and more intense storms and droughts. You can think of greenhouse gases
like an extra blanket around the planet: a little helps keep Earth warm enough for life,
but too much traps excess heat.

Climate change also affects people directly by making some places harder to farm, increasing
wildfire risk, and threatening homes near coasts with flooding. The good news is that solutions
already exist, such as using renewable energy, wasting less electricity, and driving less
when possible. By learning more, speaking up, and making everyday choices that reduce pollution,
you can help build a healthier future for our planet.

中文：
气候变化是地球长期变暖的现象，主要由人类活动造成，例如燃烧煤、石油和天然气，
这些行为会向大气中释放二氧化碳和其他会困住热量的气体。

自 19 世纪末以来，地球平均气温已经上升了约 1.2°C（2.2°F），而这个听起来
不算大的变化，却足以带来巨大的影响，例如更强的热浪、冰川融化、海平面上升，
以及更猛烈的风暴和干旱。你可以把温室气体想象成包裹地球的一层额外毯子：
少量有助于让地球保持适合生命存在的温度，但过多就会困住多余热量。

气候变化还会直接影响人类生活，比如让某些地区更难耕种、增加野火风险，并让沿海
地区的房屋面临洪水威胁。好消息是，解决方案已经存在，例如使用可再生能源、
减少电力浪费，以及在可能时少开车。通过学习更多知识、积极发声，并在日常生活中
做出减少污染的选择，你可以帮助我们的星球建立一个更健康的未来。

评价：
这一版综合了 `role + audience + constraints + example tone`，整体上是最完整的一版。
可以看出它既保留了数字事实，又用了“额外毯子”这种面向学生的解释方式，最后还有
行动号召，说明多层上下文确实产生了叠加效果。不过它也最容易变长、最贵，且不同
控制信号之间如果冲突，后续会更难判断究竟是哪一层在起主要作用。

================================================================================

Template-generated expanded context:
--------------------------------------------------------------------------------
You are a biology teacher with 15 years of experience.

Explain how photosynthesis works.

Your response should be suitable for middle school students.

Use a enthusiastic and educational tone in your response.

Requirements:

- Use a plant-to-factory analogy

- Mention the role of chlorophyll

- Explain the importance for Earth's ecosystem

- Keep it under 200 words

Examples:

Example 1:
Photosynthesis is like a tiny factory inside plants. Just as a factory needs raw materials, energy, and workers to make products, plants need carbon dioxide, water, sunlight, and chlorophyll to make glucose (sugar) and oxygen. The sunlight is the energy source, chlorophyll molecules are the workers that capture this energy, while carbon dioxide and water are the raw materials. The factory's products are glucose, which the plant uses for growth and energy storage, and oxygen, which is released into the air for animals like us to breathe. This process is essential for life on Earth because it provides the oxygen we need and removes carbon dioxide from the atmosphere.
--------------------------------------------------------------------------------
Token count (best-effort): 216

Response:
--------------------------------------------------------------------------------
Photosynthesis is like a busy factory inside a plant’s leaves!

In this factory, the raw materials are **water** (from the roots) and **carbon dioxide** (from the air). The energy source is **sunlight**. A special green chemical called **chlorophyll** acts like the factory’s solar panels, capturing light energy.

Using that energy, the plant’s factory turns water and carbon dioxide into **glucose**, a type of sugar the plant uses for food and growth. As a bonus, the factory also produces **oxygen**, which is released into the air.

So the basic idea is:

**sunlight + water + carbon dioxide → glucose + oxygen**

This process is super important for Earth’s ecosystem. Plants are the base of many food chains, so photosynthesis helps feed living things. It also puts oxygen into the atmosphere for animals and humans to breathe, while removing some carbon dioxide from the air.

Pretty amazing, right? Plants aren’t just living things—they’re like solar-powered food factories that help keep our whole planet alive!
--------------------------------------------------------------------------------
Response tokens (best-effort): 214
Latency: 5.73s
"""
