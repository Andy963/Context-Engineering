# Context Retrieval and Generation
## From Static Prompts to Dynamic Knowledge Orchestration

> **Module 01** | *Context Engineering Course: From Foundations to Frontier Systems*
> 
> Building on [Context Engineering Survey](https://arxiv.org/pdf/2507.13334) | Advancing Software 3.0 Paradigms

---

## 学习目标

完成本模块后，你将能够理解并实践以下内容：

- **高级 Prompt Engineering**：从基础提示词到复杂推理模板
- **外部知识整合**：RAG 基础与动态知识检索
- **动态上下文组装**：对多源信息进行实时组合
- **战略性上下文编排**：优化信息负载，以最大化模型效果

---

## 概念演进：从静态文本到智能知识编排

可以把上下文生成看作是我们向一个正在解决问题的人提供信息方式的演化——从递给他一份单独的文档，到为他整理一座研究图书馆，再到拥有一位智能研究助理，能够准确知道该收集哪些信息，以及应当如何呈现这些信息。

### 阶段 1：静态提示工程
```
"解决这个问题：[问题描述]"
```
**上下文**：就像给某人一张单独的说明书。简单直接，但受限于你能放进这一份文档中的内容。

### 阶段 2：增强型提示模式
```
"让我们一步一步思考：
1. 首先，理解问题……
2. 然后，考虑可能的方法……
3. 最后，实现解决方案……"
```
**上下文**：就像提供一种结构化的方法论。它更有效，因为它引导了思考过程，但仍然受制于静态内容的限制。

### 阶段 3：外部知识集成
```
[从知识库中检索到的相关信息]
"基于以下上下文：[外部知识]
现在解决：[问题]"
```
**上下文**：就像可以访问一座研究图书馆。它强大得多，因为它能够纳入超出工作记忆容量的专业化、最新的信息。

### 阶段 4：动态上下文组装
```
Context = Assemble(
    task_instructions + 
    relevant_retrieved_knowledge + 
    user_history + 
    domain_expertise + 
    real_time_data
)
```
**上下文**：就像拥有一位研究助理，能够从多个来源中收集恰到好处的信息，并针对你的具体任务以最优方式进行组织。

### 阶段 5：智能上下文编排
```
Adaptive Context System:
- 理解你的目标与约束
- 监控你的进展并自适应地调整信息流
- 从结果中学习，以改进未来的上下文组装
- 在相关性、完整性与认知负荷之间取得平衡
```
**上下文**：就像拥有一位 AI 研究伙伴，它不仅理解你需要知道什么，也理解你如何思考、如何学习，并持续优化信息环境，以实现最高效的效果。

---

## 数学基础

### 上下文形式化框架
基于我们的核心数学基础：
```
C = A(cinstr, cknow, ctools, cmem, cstate, cquery)
```

在本模块中，我们主要关注 **cknow**（外部知识）以及组装函数 **A**，具体来说：

```
cknow = R(cquery, K)
```

其中：
- **R** 是检索函数
- **cquery** 是用户当前的请求  
- **K** 是外部知识库

### 基于信息论的优化
最优检索函数的目标是最大化相关信息量：
```
R* = arg max_R I(Y*; cknow | cquery)
```

其中，**I(Y*; cknow | cquery)** 表示：在给定查询 **cquery** 的条件下，目标响应 **Y*** 与检索知识 **cknow** 之间的互信息。

**直观解释**：我们希望检索到那些最能告诉我们“正确答案应该是什么”的信息。这就像一位熟练的图书管理员：他不仅能找到与你主题相关的书，还能找到那些真正包含你所需关键洞见的书。

### 动态组装优化
```
A*(cinstr, cknow, cmem, cquery) = arg max_A P(Y* | A(...)) × Efficiency(A)
```

需要满足以下约束：
- `|A(...)| ≤ Lmax`（上下文窗口上限）
- `Quality(cknow) ≥ threshold`（信息质量阈值）
- `Relevance(cknow, cquery) ≥ min_relevance`（相关性阈值）

**直观解释**：组装函数就像一位总编辑，知道如何把不同的信息片段组合成一份连贯、高效的 briefing，在现实约束内尽可能提高获得高质量回答的概率。

---

## 可视化架构：上下文工程栈

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTEXT ASSEMBLY LAYER                  │
│  ┌─────────────────┬────────────────┬─────────────────────┐ │
│  │   INSTRUCTIONS  │    KNOWLEDGE   │      ORCHESTRATION  │ │
│  │                 │                │                     │ │
│  │  • Task specs   │  • Retrieved   │  • Assembly logic  │ │
│  │  • Constraints  │    documents   │  • Prioritization  │ │
│  │  • Examples     │  • Real-time   │  • Formatting      │ │
│  │  • Format rules │    data        │  • Length mgmt     │ │
│  └─────────────────┴────────────────┴─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              ▲
┌─────────────────────────────────────────────────────────────┐
│                   KNOWLEDGE RETRIEVAL LAYER                │
│  ┌─────────────────┬────────────────┬─────────────────────┐ │
│  │   QUERY PROC    │   RETRIEVAL    │    KNOWLEDGE BASES  │ │
│  │                 │                │                     │ │
│  │  • Query anal   │  • Vector      │  • Documents       │ │
│  │  • Intent extr  │    search      │  • Databases       │ │
│  │  • Expansion    │  • Semantic    │  • APIs            │ │
│  │  • Filtering    │    matching    │  • Real-time       │ │
│  └─────────────────┴────────────────┴─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              ▲
┌─────────────────────────────────────────────────────────────┐
│                    PROMPT ENGINEERING LAYER                │
│  ┌─────────────────┬────────────────┬─────────────────────┐ │
│  │  BASIC PROMPTS  │   TEMPLATES    │   REASONING CHAINS  │ │
│  │                 │                │                     │ │
│  │  • Direct inst │  • Reusable    │  • Chain-of-thought │ │
│  │  • Few-shot     │    patterns    │  • Tree-of-thought  │ │
│  │  • Zero-shot    │  • Domain      │  • Self-consistency │ │
│  │  • Role-based   │    specific    │  • Reflection       │ │
│  └─────────────────┴────────────────┴─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**通俗解释**：这个栈展示了上下文工程如何从基础提示逐步发展为复杂的信息编排系统。每一层都在增加新的能力：
- **底层**：核心提示工程——如何高效地与 LLM 进行沟通
- **中层**：知识检索——如何找到并访问相关的外部信息  
- **顶层**：上下文组装——如何把各类信息以最优方式组合起来

---

## Software 3.0 范式 1：Prompts（策略模板）

在上下文工程中，Prompt 不再只是简单的指令，而是演变为用于信息收集与推理的策略性模板。

### 高级推理模板
```markdown
# 思维链推理框架

## 上下文评估
你当前要处理的任务是 [specific_task]，它需要深入分析和逐步推理。
请考虑任务复杂度、可用信息以及推理要求。

## 信息清单
**可用上下文**: {context_summary}
**缺失信息**: {information_gaps}
**所需假设**: {necessary_assumptions}
**推理类型**: {演绎|归纳|溯因|类比}

## 结构化推理过程

### 第 1 步：问题拆解
将主要问题拆分为若干子问题：
1. {subquestion_1}
2. {subquestion_2}  
3. {subquestion_3}

### 第 2 步：证据分析
针对每个子问题，分析现有证据：
- **支持性证据**: [列出相关的支持信息]
- **矛盾证据**: [列出相冲突的信息]
- **证据质量**: [评估其可靠性与相关性]
- **证据缺口**: [识别缺失的关键信息]

### 第 3 步：推理链构建
在证据与结论之间建立逻辑连接：

前提 1: [带有证据支撑的陈述]
    ├─ 支撑细节 A
    ├─ 支撑细节 B
    └─ 置信水平: [高/中/低]

前提 2: [带有证据支撑的陈述] 
    ├─ 支撑细节 C
    ├─ 支撑细节 D
    └─ 置信水平: [高/中/低]

中间结论: [根据前提出得出的逻辑推断]
    └─ 推理说明: [解释其中的逻辑联系]


### 第 4 步：替代假设考察
还可能存在哪些其他解释或解决方案？
- **备选方案 1**: [不同的解释/做法]
  - 优势: [哪些因素支持这一方案]
  - 劣势: [哪些因素不支持这一方案]
- **备选方案 2**: [另一种解释/做法]
  - 优势: [支持因素]
  - 劣势: [限制因素]

### 第 5 步：综合与结论
**主要结论**: [主要答案/解决方案]
**置信水平**: [百分比或定性评估]
**关键推理**: [导出该结论的最关键逻辑步骤]
**局限性**: [哪些因素可能使该结论出错]
**下一步**: [哪些额外信息能够强化该结论]

## 质量检查
- [ ] 我是否回答了所有子问题？
- [ ] 我的逻辑连接是否清晰且有效？
- [ ] 我是否考虑了主要的替代解释？
- [ ] 我的置信度评估是否现实？
- [ ] 其他人是否能够跟随我的推理链？
```

**通俗解释**：这个模板把简单的“让我们一步一步思考”升级成了一套完整的推理方法。它就像有一位逻辑学高手在引导你的思考过程，确保你能考虑不同角度、明确展示逻辑连接，并检查自己推理的质量。

### 动态知识整合模板
```xml
<knowledge_integration_template>
  <intent>系统性地将外部知识与用户查询整合，以获得最佳响应</intent>
  
  <context_analysis>
    <user_query>
      <main_intent>{primary_user_goal}</main_intent>
      <sub_intents>
        <intent priority="high">{critical_sub_goal}</intent>
        <intent priority="medium">{important_sub_goal}</intent>
        <intent priority="low">{optional_sub_goal}</intent>
      </sub_intents>
      <complexity_level>{simple|moderate|complex|expert}</complexity_level>
      <domain_context>{specific_field_or_general}</domain_context>
    </user_query>
    
    <information_needs>
      <critical_info>为准确回答绝对必需的信息</critical_info>
      <supporting_info>能够提升回答质量的信息</supporting_info>
      <contextual_info>提供有帮助背景的信息</contextual_info>
    </information_needs>
  </context_analysis>
  
  <knowledge_retrieval_strategy>
    <search_approach>
      <primary_search>{most_likely_to_find_critical_info}</primary_search>
      <secondary_search>{backup_approach_for_comprehensive_coverage}</secondary_search>
      <tertiary_search>{specialized_or_edge_case_coverage}</tertiary_search>
    </search_approach>
    
    <quality_filters>
      <relevance_threshold>信息与查询意图需要匹配到什么程度</relevance_threshold>
      <credibility_threshold>最低来源可靠性标准</credibility_threshold>
      <recency_weight>近期信息与权威信息应如何权衡优先级</recency_weight>
    </quality_filters>
  </knowledge_retrieval_strategy>
  
  <context_assembly>
    <information_hierarchy>
      <tier_1>直接回答主要问题的核心事实</tier_1>
      <tier_2>支持性证据与解释</tier_2>
      <tier_3>背景上下文与相关信息</tier_3>
    </information_hierarchy>
    
    <assembly_constraints>
      <max_context_length>{token_limit_consideration}</max_context_length>
      <cognitive_load_limit>用户能够理解的信息复杂度上限</cognitive_load_limit>
      <coherence_requirement>信息应当如何在逻辑上连接</coherence_requirement>
    </assembly_constraints>
    
    <assembly_process>
      <step name="prioritize">按相关性与重要性对检索到的信息进行排序</step>
      <step name="filter">移除冗余、过时或低质量的信息</step>
      <step name="structure">为保证逻辑流畅与易于理解而组织信息</step>
      <step name="integrate">将信息编织成连贯叙述，以回应用户查询</step>
      <step name="validate">确保组装后的上下文能够支撑准确且有帮助的回答</step>
    </assembly_process>
  </context_assembly>
  
  <response_optimization>
    <tailoring>
      <user_expertise_level>适当调整技术深度</user_expertise_level>
      <communication_style>匹配用户偏好的交互方式</communication_style>
      <information_density>在全面性与清晰性之间取得平衡</information_density>
    </tailoring>
    
    <quality_assurance>
      <accuracy_check>核验信息正确性及其与上下文的一致性</accuracy_check>
      <completeness_check>确保覆盖用户所有关键需求</completeness_check>
      <coherence_check>确认逻辑流畅且表达清晰</coherence_check>
    </quality_assurance>
  </response_optimization>
</knowledge_integration_template>
```

**基础解释**：这个 XML 模板对“查找并整合外部知识”这一复杂过程进行了结构化。它就像一套研究方法，确保你不仅能找到相关信息，还能针对具体用户和任务，以最有效的方式组织并呈现这些信息。

---

## 软件 3.0 范式 2：编程（检索算法）

编程为智能上下文检索与组装提供了计算机制。

### 语义检索引擎

```python
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from abc import ABC, abstractmethod
import sqlite3
import json
from datetime import datetime, timedelta

@dataclass
class RetrievalCandidate:
    """A piece of information that could be relevant to the query"""
    content: str
    source: str
    relevance_score: float
    credibility_score: float
    recency_score: float
    content_type: str  # 'fact', 'procedure', 'example', 'definition'
    metadata: Dict
    
class KnowledgeRetriever(ABC):
    """Abstract base for different knowledge retrieval strategies"""
    
    @abstractmethod
    def retrieve(self, query: str, max_results: int = 10) -> List[RetrievalCandidate]:
        """Retrieve relevant knowledge for the given query"""
        pass
    
    @abstractmethod
    def update_relevance_feedback(self, query: str, candidate: RetrievalCandidate, 
                                 helpful: bool):
        """Learn from user feedback about retrieval quality"""
        pass

class SemanticVectorRetriever(KnowledgeRetriever):
    """Retrieval using semantic similarity via embeddings"""
    
    def __init__(self, embedding_model, vector_database):
        self.embedding_model = embedding_model
        self.vector_db = vector_database
        self.feedback_history = []
        
    def retrieve(self, query: str, max_results: int = 10) -> List[RetrievalCandidate]:
        """Retrieve semantically similar content"""
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query)
        
        # Search vector database
        raw_results = self.vector_db.similarity_search(
            query_embedding, 
            top_k=max_results * 2  # Get more candidates for filtering
        )
        
        # Convert to RetrievalCandidates with scoring
        candidates = []
        for result in raw_results:
            candidate = RetrievalCandidate(
                content=result.content,
                source=result.source,
                relevance_score=self._calculate_relevance_score(query, result),
                credibility_score=self._calculate_credibility_score(result),
                recency_score=self._calculate_recency_score(result),
                content_type=self._classify_content_type(result.content),
                metadata=result.metadata
            )
            candidates.append(candidate)
        
        # Apply learning from feedback history
        candidates = self._apply_feedback_learning(query, candidates)
        
        # Rank and filter
        ranked_candidates = self._rank_candidates(candidates)
        
        return ranked_candidates[:max_results]
    
    def _calculate_relevance_score(self, query: str, result) -> float:
        """Calculate how relevant the content is to the query"""
        
        # Base semantic similarity
        base_score = result.similarity_score
        
        # Adjust based on content type match
        content_type_bonus = self._get_content_type_bonus(query, result.content)
        
        # Adjust based on query specificity
        specificity_factor = self._calculate_query_specificity_factor(query, result)
        
        # Combine factors
        relevance_score = base_score * (1 + content_type_bonus) * specificity_factor
        
        return min(1.0, max(0.0, relevance_score))
    
    def _calculate_credibility_score(self, result) -> float:
        """Assess source credibility and information quality"""
        
        # Source authority (academic, government, established organization)
        source_authority = self._get_source_authority_score(result.source)
        
        # Content quality indicators (length, structure, citations)
        content_quality = self._assess_content_quality(result.content)
        
        # Cross-reference validation (how well it aligns with other sources)
        cross_reference_score = self._calculate_cross_reference_score(result)
        
        # Combine factors
        credibility = (source_authority * 0.4 + 
                      content_quality * 0.3 + 
                      cross_reference_score * 0.3)
        
        return credibility
    
    def _calculate_recency_score(self, result) -> float:
        """Score based on information recency (more recent = higher score)"""
        if 'date' not in result.metadata:
            return 0.5  # Neutral score for undated content
            
        content_date = datetime.fromisoformat(result.metadata['date'])
        days_old = (datetime.now() - content_date).days
        
        # Exponential decay: score decreases as content gets older
        # Half-life of 365 days (information relevance decreases by half each year)
        half_life = 365
        recency_score = 0.5 ** (days_old / half_life)
        
        return recency_score
    
    def _classify_content_type(self, content: str) -> str:
        """Classify content as fact, procedure, example, or definition"""
        
        # Simple heuristic classification (in practice, use ML classifier)
        content_lower = content.lower()
        
        if any(phrase in content_lower for phrase in ['step', 'first', 'then', 'finally', 'procedure']):
            return 'procedure'
        elif any(phrase in content_lower for phrase in ['for example', 'such as', 'instance']):
            return 'example'
        elif any(phrase in content_lower for phrase in ['is defined as', 'refers to', 'means']):
            return 'definition'
        else:
            return 'fact'
    
    def _rank_candidates(self, candidates: List[RetrievalCandidate]) -> List[RetrievalCandidate]:
        """Rank candidates using composite scoring"""
        
        for candidate in candidates:
            # Composite score balancing multiple factors
            candidate.composite_score = (
                candidate.relevance_score * 0.5 +      # Relevance is most important
                candidate.credibility_score * 0.3 +    # Credibility is very important  
                candidate.recency_score * 0.2          # Recency matters but less
            )
        
        # Sort by composite score
        ranked = sorted(candidates, key=lambda c: c.composite_score, reverse=True)
        
        return ranked
    
    def update_relevance_feedback(self, query: str, candidate: RetrievalCandidate, 
                                 helpful: bool):
        """Learn from feedback to improve future retrieval"""
        
        feedback_entry = {
            'query': query,
            'candidate_source': candidate.source,
            'candidate_type': candidate.content_type,
            'helpful': helpful,
            'timestamp': datetime.now().isoformat()
        }
        
        self.feedback_history.append(feedback_entry)
        
        # Update retrieval parameters based on feedback patterns
        self._update_retrieval_parameters()
    
    def _apply_feedback_learning(self, query: str, candidates: List[RetrievalCandidate]) -> List[RetrievalCandidate]:
        """Adjust candidate scores based on learned feedback patterns"""
        
        if not self.feedback_history:
            return candidates
        
        # Analyze feedback patterns
        feedback_patterns = self._analyze_feedback_patterns(query)
        
        # Adjust scores based on patterns
        for candidate in candidates:
            adjustment = self._calculate_feedback_adjustment(candidate, feedback_patterns)
            candidate.relevance_score = min(1.0, max(0.0, candidate.relevance_score + adjustment))
        
        return candidates
    
    def _analyze_feedback_patterns(self, query: str) -> Dict:
        """Analyze historical feedback to identify useful patterns"""
        
        patterns = {
            'helpful_sources': [],
            'helpful_content_types': [],
            'unhelpful_sources': [],
            'unhelpful_content_types': []
        }
        
        # Group feedback by helpfulness
        for feedback in self.feedback_history[-100:]:  # Recent feedback
            if self._is_similar_query(query, feedback['query']):
                if feedback['helpful']:
                    patterns['helpful_sources'].append(feedback['candidate_source'])
                    patterns['helpful_content_types'].append(feedback['candidate_type'])
                else:
                    patterns['unhelpful_sources'].append(feedback['candidate_source'])
                    patterns['unhelpful_content_types'].append(feedback['candidate_type'])
        
        return patterns

class HybridKnowledgeRetriever(KnowledgeRetriever):
    """Combines multiple retrieval strategies for comprehensive results"""
    
    def __init__(self, retrievers: List[KnowledgeRetriever], weights: List[float] = None):
        self.retrievers = retrievers
        self.weights = weights or [1.0] * len(retrievers)
        self.performance_history = {i: [] for i in range(len(retrievers))}
        
    def retrieve(self, query: str, max_results: int = 10) -> List[RetrievalCandidate]:
        """Retrieve from multiple sources and intelligently combine results"""
        
        all_candidates = []
        
        # Retrieve from each strategy
        for i, retriever in enumerate(self.retrievers):
            try:
                candidates = retriever.retrieve(query, max_results)
                
                # Weight candidates based on retriever performance
                weight = self.weights[i] * self._get_dynamic_weight(i, query)
                
                for candidate in candidates:
                    candidate.composite_score *= weight
                    candidate.metadata['retriever_id'] = i
                
                all_candidates.extend(candidates)
                
            except Exception as e:
                print(f"Retriever {i} failed: {e}")
                continue
        
        # Remove duplicates and merge similar content
        unique_candidates = self._deduplicate_candidates(all_candidates)
        
        # Rank final candidates
        final_candidates = self._rank_hybrid_candidates(unique_candidates)
        
        return final_candidates[:max_results]
    
    def _get_dynamic_weight(self, retriever_id: int, query: str) -> float:
        """Calculate dynamic weight based on retriever performance for similar queries"""
        
        if not self.performance_history[retriever_id]:
            return 1.0  # Default weight for new retrievers
        
        # Calculate recent performance average
        recent_performance = self.performance_history[retriever_id][-10:]  # Last 10 queries
        avg_performance = sum(recent_performance) / len(recent_performance)
        
        # Dynamic weight based on performance (better performers get higher weight)
        return max(0.1, min(2.0, avg_performance))
    
    def _deduplicate_candidates(self, candidates: List[RetrievalCandidate]) -> List[RetrievalCandidate]:
        """Remove duplicate and very similar candidates"""
        
        unique_candidates = []
        content_hashes = set()
        
        for candidate in sorted(candidates, key=lambda c: c.composite_score, reverse=True):
            # Simple deduplication based on content similarity
            content_hash = hash(candidate.content[:200])  # Hash first 200 chars
            
            if content_hash not in content_hashes:
                content_hashes.add(content_hash)
                unique_candidates.append(candidate)
        
        return unique_candidates
    
    def update_relevance_feedback(self, query: str, candidate: RetrievalCandidate, helpful: bool):
        """Update feedback for the specific retriever that provided this candidate"""
        
        retriever_id = candidate.metadata.get('retriever_id')
        if retriever_id is not None:
            # Update performance history
            performance_score = 1.0 if helpful else 0.0
            self.performance_history[retriever_id].append(performance_score)
            
            # Forward feedback to specific retriever
            self.retrievers[retriever_id].update_relevance_feedback(query, candidate, helpful)

class DynamicContextAssembler:
    """Assembles optimal context from retrieved knowledge and other sources"""
    
    def __init__(self, max_context_length: int = 4000):
        self.max_context_length = max_context_length
        self.assembly_history = []
        
    def assemble_context(self, query: str, retrieved_candidates: List[RetrievalCandidate],
                        instructions: str = "", user_context: str = "",
                        task_type: str = "general") -> str:
        """Dynamically assemble optimal context from available information"""
        
        # Analyze query to understand information needs
        info_needs = self._analyze_information_needs(query, task_type)
        
        # Select optimal subset of candidates
        selected_candidates = self._select_optimal_candidates(
            retrieved_candidates, info_needs, self.max_context_length
        )
        
        # Structure and format context
        assembled_context = self._structure_context(
            instructions, selected_candidates, user_context, query, info_needs
        )
        
        # Validate and optimize final context
        optimized_context = self._optimize_context(assembled_context, query)
        
        return optimized_context
    
    def _analyze_information_needs(self, query: str, task_type: str) -> Dict:
        """Analyze what types of information are needed for this query"""
        
        needs = {
            'definitions': 0.0,
            'facts': 0.0,
            'procedures': 0.0,
            'examples': 0.0,
            'background': 0.0
        }
        
        query_lower = query.lower()
        
        # Heuristic analysis of information needs
        if any(word in query_lower for word in ['what is', 'define', 'meaning', 'definition']):
            needs['definitions'] = 1.0
            needs['examples'] = 0.7
            
        elif any(word in query_lower for word in ['how to', 'steps', 'procedure', 'process']):
            needs['procedures'] = 1.0
            needs['examples'] = 0.8
            
        elif any(word in query_lower for word in ['why', 'explain', 'reason', 'cause']):
            needs['facts'] = 1.0
            needs['background'] = 0.8
            
        elif 'example' in query_lower:
            needs['examples'] = 1.0
            needs['procedures'] = 0.5
            
        else:
            # General query - balanced information needs
            for key in needs:
                needs[key] = 0.6
        
        # Adjust based on task type
        if task_type == "analytical":
            needs['facts'] *= 1.3
            needs['background'] *= 1.2
        elif task_type == "practical":
            needs['procedures'] *= 1.3
            needs['examples'] *= 1.2
        elif task_type == "creative":
            needs['examples'] *= 1.2
            needs['background'] *= 1.1
        
        return needs
    
    def _select_optimal_candidates(self, candidates: List[RetrievalCandidate],
                                  info_needs: Dict, max_length: int) -> List[RetrievalCandidate]:
        """Select optimal subset of candidates based on information needs and length constraints"""
        
        # Score candidates based on information needs alignment
        for candidate in candidates:
            content_type_score = info_needs.get(candidate.content_type, 0.5)
            candidate.need_alignment_score = (
                candidate.composite_score * 0.7 + 
                content_type_score * 0.3
            )
        
        # Use greedy knapsack-style selection
        selected = []
        total_length = 0
        remaining_candidates = sorted(candidates, key=lambda c: c.need_alignment_score, reverse=True)
        
        for candidate in remaining_candidates:
            candidate_length = len(candidate.content)
            
            if total_length + candidate_length <= max_length * 0.8:  # Reserve 20% for formatting
                selected.append(candidate)
                total_length += candidate_length
            elif len(selected) < 2:  # Ensure we have at least 2 candidates
                # Truncate content to fit
                available_space = max_length * 0.8 - total_length
                if available_space > 100:  # Only if we can fit meaningful content
                    truncated_candidate = RetrievalCandidate(
                        content=candidate.content[:int(available_space)],
                        source=candidate.source,
                        relevance_score=candidate.relevance_score,
                        credibility_score=candidate.credibility_score,
                        recency_score=candidate.recency_score,
                        content_type=candidate.content_type,
                        metadata=candidate.metadata
                    )
                    selected.append(truncated_candidate)
                    break
        
        return selected
    
    def _structure_context(self, instructions: str, candidates: List[RetrievalCandidate],
                          user_context: str, query: str, info_needs: Dict) -> str:
        """Structure the context for optimal comprehension and utility"""
        
        context_parts = []
        
        # Add instructions if provided
        if instructions.strip():
            context_parts.append(f"## Instructions\n{instructions}\n")
        
        # Add user context if provided
        if user_context.strip():
            context_parts.append(f"## Context\n{user_context}\n")
        
        # Group candidates by type for better organization
        candidates_by_type = {}
        for candidate in candidates:
            if candidate.content_type not in candidates_by_type:
                candidates_by_type[candidate.content_type] = []
            candidates_by_type[candidate.content_type].append(candidate)
        
        # Add retrieved information in logical order
        type_order = ['definitions', 'facts', 'procedures', 'examples']
        type_labels = {
            'definition': 'Key Definitions',
            'fact': 'Relevant Information', 
            'procedure': 'Procedures and Methods',
            'example': 'Examples and Case Studies'
        }
        
        context_parts.append("## Retrieved Knowledge\n")
        
        for content_type in type_order:
            if content_type in candidates_by_type:
                candidates_of_type = candidates_by_type[content_type]
                section_label = type_labels.get(content_type, content_type.title())
                
                context_parts.append(f"### {section_label}\n")
                
                for i, candidate in enumerate(candidates_of_type, 1):
                    source_note = f" (Source: {candidate.source})" if candidate.source else ""
                    context_parts.append(f"{i}. {candidate.content.strip()}{source_note}\n")
                
                context_parts.append("")  # Add spacing
        
        # Add the user's specific query
        context_parts.append(f"## Current Query\n{query}\n")
        
        return "\n".join(context_parts)
    
    def _optimize_context(self, context: str, query: str) -> str:
        """Final optimization of assembled context"""
        
        # Remove excessive whitespace
        optimized = "\n".join(line.strip() for line in context.split("\n"))
        
        # Remove duplicate information (simple approach)
        lines = optimized.split("\n")
        unique_lines = []
        seen_content = set()
        
        for line in lines:
            if line.strip():
                # Check for substantial duplicates (not just headers)
                line_content = line.lower().strip()
                if len(line_content) > 20:  # Only check substantial lines
                    if line_content not in seen_content:
                        seen_content.add(line_content)
                        unique_lines.append(line)
                else:
                    unique_lines.append(line)
            else:
                unique_lines.append(line)
        
        return "\n".join(unique_lines)

# Example usage demonstrating the complete retrieval and assembly pipeline
class ContextGenerationDemo:
    """Demonstration of complete context generation pipeline"""
    
    def __init__(self):
        # Initialize retrievers (mock implementations for demo)
        self.semantic_retriever = SemanticVectorRetriever(
            embedding_model=MockEmbeddingModel(),
            vector_database=MockVectorDatabase()
        )
        
        self.hybrid_retriever = HybridKnowledgeRetriever([
            self.semantic_retriever,
            # Add other retrievers as needed
        ])
        
        self.context_assembler = DynamicContextAssembler(max_context_length=4000)
    
    def generate_context(self, query: str, instructions: str = "", 
                        user_context: str = "", task_type: str = "general") -> str:
        """完整的上下文生成流水线"""
        
        print(f"正在为查询生成上下文：'{query}'")
        
        # 第 1 步：检索相关知识
        print("第 1 步：正在检索知识...")
        candidates = self.hybrid_retriever.retrieve(query, max_results=10)
        print(f"已检索到 {len(candidates)} 个候选结果")
        
        # 第 2 步：组装最优上下文
        print("第 2 步：正在组装上下文...")
        context = self.context_assembler.assemble_context(
            query, candidates, instructions, user_context, task_type
        )
        
        print(f"第 3 步：已生成上下文（{len(context)} 个字符）")
        
        return context

# Mock classes for demonstration
class MockEmbeddingModel:
    def encode(self, text: str) -> np.ndarray:
        # Simplified mock embedding
        return np.random.rand(384)

class MockVectorDatabase:
    def __init__(self):
        self.mock_results = [
            MockResult("Machine learning is a subset of artificial intelligence...", "wikipedia.org", 0.85),
            MockResult("To implement a neural network: 1. Define architecture...", "tutorial.com", 0.78),
            MockResult("For example, a simple classification model...", "examples.org", 0.72)
        ]
    
    def similarity_search(self, query_embedding: np.ndarray, top_k: int = 10):
        return self.mock_results[:top_k]

@dataclass 
class MockResult:
    content: str
    source: str
    similarity_score: float
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {"date": "2024-01-01"}
```

**基础解释**：这个检索系统就像拥有多位各具专长的研究助理，再加上一位知道如何把他们的发现整合成完美简报的总编辑。`HybridKnowledgeRetriever` 会从多个来源获取信息，`DynamicContextAssembler` 会以最优方式组织这些信息，而整个系统还会从反馈中学习，随着时间推移不断变得更好。

---

## 软件 3.0 范式 3：协议（自适应组装外壳）

协议提供了可自我修改的上下文生成模式，并会基于效果持续演化。

### 自适应上下文生成协议

```
/context.generate.adaptive{
    intent="通过学习使用模式并调整组装策略，动态生成最优上下文",
    
    input={
        user_query=<immediate_user_request>,
        task_context={
            domain=<subject_area_or_field>,
            complexity_level=<simple|moderate|complex|expert>,
            user_expertise=<novice|intermediate|advanced|expert>,
            time_constraints=<available_processing_time>,
            quality_requirements=<accuracy_completeness_specificity_needs>
        },
        available_sources={
            knowledge_bases=<accessible_information_repositories>,
            real_time_data=<current_information_streams>,
            user_history=<relevant_past_interactions>,
            domain_expertise=<specialized_knowledge_sources>
        }
    },
    
    process=[
        /analyze.information_needs{
            action="深度分析为了获得最佳响应所需的信息",
            method="结合学习机制的多维需求评估",
            analysis_dimensions=[
                {factual_requirements="需要哪些事实、数据或证据？"},
                {conceptual_requirements="需要哪些概念、定义或框架？"},
                {procedural_requirements="需要哪些流程、方法或步骤？"},
                {contextual_requirements="需要哪些背景或情境信息？"},
                {example_requirements="需要哪些示例、案例或演示？"}
            ],
            learning_integration="应用从相似成功查询上下文中学到的模式",
            output="带有优先级权重的完整信息需求规格"
        },
        
        /orchestrate.multi_source_retrieval{
            action="智能协调来自多个信息源的检索",
            method="结合战略性来源选择与结果融合的并行检索",
            retrieval_strategies=[
                {semantic_search="针对知识嵌入进行向量相似度匹配"},
                {keyword_expansion="使用领域特定术语扩展查询"},
                {contextual_filtering="根据用户上下文和专业水平过滤相关内容"},
                {temporal_prioritization="适当权衡近期信息与权威信息"},
                {cross_reference_validation="验证多个来源之间的一致性"}
            ],
            fusion_algorithm="通过去重和相关性排序对结果进行智能组合",
            output="按优先级排序的高质量候选信息集合"
        },
        
        /optimize.context_assembly{
            action="将检索到的信息组装为最优上下文结构",
            method="结合认知负荷管理的动态组装优化",
            assembly_strategies=[
                {information_hierarchy="按从最关键到最次要的顺序组织信息"},
                {cognitive_chunking="将相关信息分组以降低认知负荷"},
                {logical_flow="按自然推理过程组织信息"},
                {length_optimization="在上下文窗口限制内最大化信息价值"},
                {user_customization="根据用户专业水平和偏好调整呈现方式"}
            ],
            optimization_criteria=[
                {relevance_maximization="确保每一条信息都服务于用户目标"},
                {coherence_enhancement="在各信息片段之间建立逻辑连接"},
                {clarity_optimization="以合适的复杂度水平呈现信息"},
                {actionability_focus="突出能够帮助用户采取行动的信息"}
            ],
            output="为模型使用而准备好的最优结构化上下文"
        },
        
        /monitor.effectiveness{
            action="跟踪上下文生成效果并识别改进机会",
            method="结合学习机制的多指标效果评估",
            effectiveness_metrics=[
                {response_quality="生成的上下文在多大程度上支持高质量回答？"},
                {user_satisfaction="用户对基于该上下文生成的回答满意度如何？"},
                {task_completion="该上下文在多大程度上促进任务完成？"},
                {efficiency_measures="上下文生成速度与资源利用情况"},
                {learning_indicators="随时间推移性能改进的证据"}
            ],
            feedback_integration=[
                {explicit_feedback="用户对回答质量的直接评分与评论"},
                {implicit_feedback="反映满意/不满意的用户行为模式"},
                {outcome_tracking="涉及生成上下文任务的长期成功指标"},
                {comparative_analysis="与其他上下文生成方法的性能比较"}
            ],
            output="包含具体改进建议的综合效果评估"
        }
    ],
    
    output={
        generated_context={
            assembled_information=<optimally_structured_context_ready_for_model>,
            information_sources=<attribution_and_credibility_information>,
            assembly_rationale=<explanation_of_context_construction_decisions>,
            quality_indicators=<confidence_scores_and_completeness_measures>
        },
        
        optimization_metadata={
            retrieval_performance=<metrics_on_information_gathering_effectiveness>,
            assembly_efficiency=<metrics_on_context_construction_performance>,
            predicted_effectiveness=<estimated_quality_of_generated_context>,
            alternative_approaches=<other_context_generation_strategies_considered>
        },
        
        learning_updates={
            pattern_discoveries=<new_effective_patterns_identified>,
            strategy_refinements=<improvements_to_existing_approaches>,
            feedback_integration=<how_user_feedback_influenced_context_generation>,
            knowledge_base_updates=<improvements_to_underlying_information_sources>
        }
    },
    
    // 自我改进机制
    adaptation_triggers=[
        {condition="user_satisfaction < 0.7", action="analyze_context_assembly_weaknesses"},
        {condition="response_quality_decline_detected", action="audit_information_source_quality"},
        {condition="new_domain_patterns_identified", action="integrate_domain_specific_optimizations"},
        {condition="efficiency_below_threshold", action="optimize_retrieval_and_assembly_performance"}
    ],
    
    meta={
        context_generation_version="adaptive_v2.1",
        learning_integration_level="advanced",
        adaptation_frequency="continuous_with_batch_updates",
        quality_assurance="multi_dimensional_effectiveness_monitoring"
    }
}
```

**基础解释**：这个协议创建了一个能够自我改进的上下文生成系统。它就像一个研究团队，每次执行项目时都会更擅长查找和组织信息，并逐步学会针对不同类型的问题和不同用户，哪些信息最有价值。

---

## 集成与真实世界应用

### 案例研究：医疗诊断支持上下文生成

```python
def medical_diagnosis_context_example():
    """Demonstrate context generation for medical diagnosis support"""
    
    # Simulated medical query
    query = "Patient presents with chest pain, shortness of breath, and elevated troponin levels. What are the differential diagnoses and recommended diagnostic workup?"
    
    # Medical-specific context generation
    medical_context_generator = ContextGenerationDemo()
    
    # Generate specialized medical context
    context = medical_context_generator.generate_context(
        query=query,
        instructions="""
        You are providing medical decision support. Focus on:
        1. Evidence-based differential diagnoses
        2. Appropriate diagnostic workup recommendations  
        3. Risk stratification considerations
        4. Latest clinical guidelines and protocols
        
        Always emphasize the need for clinical judgment and direct patient evaluation.
        """,
        user_context="Emergency department setting, adult patient, no known allergies",
        task_type="analytical"
    )
    
    print("Medical Diagnosis Support Context:")
    print("=" * 50)
    print(context)
    
    return context
```

### 性能评估框架

```python
class ContextGenerationEvaluator:
    """Comprehensive evaluation of context generation effectiveness"""
    
    def __init__(self):
        self.evaluation_metrics = {
            'relevance': self._evaluate_relevance,
            'completeness': self._evaluate_completeness,
            'clarity': self._evaluate_clarity,
            'efficiency': self._evaluate_efficiency,
            'adaptability': self._evaluate_adaptability
        }
    
    def evaluate_context_generation(self, query: str, generated_context: str, 
                                   response_quality: float, user_feedback: Dict) -> Dict:
        """Comprehensive evaluation of context generation performance"""
        
        results = {}
        for metric_name, metric_function in self.evaluation_metrics.items():
            score = metric_function(query, generated_context, response_quality, user_feedback)
            results[metric_name] = score
        
        # Calculate overall effectiveness
        results['overall_effectiveness'] = self._calculate_overall_effectiveness(results)
        
        # Generate improvement recommendations
        results['improvement_recommendations'] = self._generate_improvement_recommendations(results)
        
        return results
    
    def _evaluate_relevance(self, query: str, context: str, response_quality: float, feedback: Dict) -> float:
        """Evaluate how relevant the generated context is to the query"""
        
        # Analyze semantic alignment between query and context
        query_terms = set(query.lower().split())
        context_terms = set(context.lower().split())
        
        term_overlap = len(query_terms.intersection(context_terms)) / len(query_terms.union(context_terms))
        
        # Factor in response quality as indicator of context relevance
        relevance_score = (term_overlap * 0.3 + response_quality * 0.7)
        
        return min(1.0, max(0.0, relevance_score))
    
    def _evaluate_completeness(self, query: str, context: str, response_quality: float, feedback: Dict) -> float:
        """Evaluate whether context contains all necessary information"""
        
        # Simple heuristic: longer contexts are generally more complete
        # But also consider user feedback about missing information
        
        context_length_score = min(1.0, len(context) / 2000)  # Normalize to reasonable length
        
        # Check feedback for missing information indicators
        missing_info_penalty = 0.0
        if feedback.get('missing_information', False):
            missing_info_penalty = 0.3
        
        completeness_score = max(0.0, context_length_score - missing_info_penalty)
        
        return completeness_score
    
    def _calculate_overall_effectiveness(self, metric_scores: Dict) -> float:
        """Calculate weighted overall effectiveness score"""
        
        weights = {
            'relevance': 0.30,
            'completeness': 0.25,
            'clarity': 0.20,
            'efficiency': 0.15,
            'adaptability': 0.10
        }
        
        overall = sum(metric_scores[metric] * weight 
                     for metric, weight in weights.items() 
                     if metric in metric_scores)
        
        return overall
```

**基础解释**：这个评估框架就像一套全面的质量控制系统，会从多个角度审视上下文生成过程，不只关注它是否奏效，还关注它的效果有多好，以及还能如何改进。

---

## 实践练习与下一步

### 练习 1：构建你自己的检索系统
**目标**：实现一个基础的语义检索系统

```python
# Your implementation template
class BasicRetriever:
    def __init__(self):
        # TODO: Initialize your retrieval system
        self.knowledge_base = {}
        self.embedding_cache = {}
    
    def add_document(self, doc_id: str, content: str):
        # TODO: Add document to knowledge base
        pass
    
    def retrieve(self, query: str, max_results: int = 5) -> List[str]:
        # TODO: Implement retrieval logic
        pass

# Test your retriever
retriever = BasicRetriever()
# Add some test documents
# Test retrieval with different queries
```

### 练习 2：上下文组装优化
**目标**：创建一个能够优化信息组织方式的上下文组装器

```python
class ContextOptimizer:
    def __init__(self, max_length: int = 2000):
        # TODO: Initialize context optimizer
        self.max_length = max_length
    
    def optimize_context(self, information_pieces: List[str], query: str) -> str:
        # TODO: Implement optimal context assembly
        pass
```

---

## 总结与下一步

**已掌握的核心概念**：
- 从静态提示词演进到动态上下文编排
- 基于信息论的知识检索优化
- 多源检索策略与结果融合
- 结合学习机制的自适应上下文组装
- 对上下文生成效果进行全面评估

**与 Software 3.0 的集成**：
- **Prompts**：用于推理与知识整合的战略模板
- **Programming**：复杂的检索与组装算法
- **Protocols**：可自我改进的上下文生成系统

**实现能力**：
- 使用嵌入与向量数据库进行语义检索
- 结合认知负荷优化的动态上下文组装
- 多源信息融合与去重
- 效果评估与持续改进系统

**Research Grounding**：直接实现上下文生成研究（§4.1），并在自适应组装、多源融合与自我改进上下文编排方面进行了新的扩展。

**Next Module**：[01_prompt_engineering.md](01_prompt_engineering.md) - 深入学习高级提示技术，在上下文生成基础之上掌握 LLM 沟通的艺术与科学。

---

*本模块为智能上下文工程建立了基础，将简单的 “prompt” 概念转化为一个用于动态知识编排与最优信息组装的复杂系统。*
