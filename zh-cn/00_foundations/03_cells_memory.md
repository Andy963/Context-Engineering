<!-- markdownlint-disable MD009 MD012 MD013 MD022 MD024 MD031 MD032 MD033 MD036 MD040 MD046 MD050 MD060 -->

# 细胞：引入记忆与状态

> "We are our memory, we are that chimerical museum of shifting shapes, that pile of broken mirrors." — Jorge Luis Borges

## 从分子到细胞

我们已经讨论了原子（单条指令）与分子（指令加示例）。现在我们进入细胞：带有记忆的上下文结构，能够跨多轮交互保持状态并累积信息。

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  CELL = [INSTRUCTIONS] + [EXAMPLES] + [MEMORY/STATE] + [CURRENT INPUT]      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

就像生物细胞在与环境交互时仍能维持内部状态一样，上下文细胞也能在多轮对话中保留信息，从而让交互连续、可控。

## 记忆问题

默认情况下，大语言模型没有跨请求的记忆。每次请求都是独立处理的：

```
┌───────────────────────┐      ┌───────────────────────┐
│ Request 1             │      │ Request 2             │
├───────────────────────┤      ├───────────────────────┤
│ "My name is Alex."    │      │ "What's my name?"     │
│                       │      │                       │
│                       │      │                       │
└───────────────────────┘      └───────────────────────┘
          │                              │
          ▼                              ▼
┌───────────────────────┐      ┌───────────────────────┐
│ Response 1            │      │ Response 2            │
├───────────────────────┤      ├───────────────────────┤
│ "Hello Alex, nice     │      │ "I don't have access  │
│  to meet you."        │      │  to previous          │
│                       │      │  conversations..."    │
└───────────────────────┘      └───────────────────────┘
```

没有记忆，大语言模型会忘记之前交互中的信息，导致体验割裂、令人沮丧。

## 细胞解法：对话记忆

最简单的细胞结构，就是把对话历史追加到上下文里：

```
┌───────────────────────────────────────────────────────────────────────┐
│                                                                       │
│  SYSTEM PROMPT: "You are a helpful assistant..."                      │
│                                                                       │
│  CONVERSATION HISTORY:                                                │
│  User: "My name is Alex."                                             │
│  Assistant: "Hello Alex, nice to meet you."                           │
│                                                                       │
│  CURRENT INPUT: "What's my name?"                                     │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

这样大语言模型就能访问先前内容，维持连续性。

## 记忆的标记预算问题

对话变长后，上下文窗口会逐渐被填满，因此需要记忆管理策略：

```
          [Context Window Tokens]
          ┌─────────────────────────────────────────────┐
          │                                             │
Turn 1    │ System Instructions       User Input 1      │
          │                                             │
          ├─────────────────────────────────────────────┤
          │                                             │
Turn 2    │ System    History 1       User Input 2      │
          │                                             │
          ├─────────────────────────────────────────────┤
          │                                             │
Turn 3    │ Sys  History 1  History 2  User Input 3     │
          │                                             │
          ├─────────────────────────────────────────────┤
          │                                             │
Turn 4    │ S  History 1-3             User Input 4     │
          │                                             │
          ├─────────────────────────────────────────────┤
          │                                             │
Turn 5    │ History 2-4                User Input 5     │
          │                                             │
          └─────────────────────────────────────────────┘
                                       ▲
                                       │
                        Eventually, something has to go
```

## Memory Management Strategies

Several strategies help optimize the use of limited context windows:

```
┌───────────────────────────────────────────────────────────────────┐
│ MEMORY MANAGEMENT STRATEGIES                                      │
├────────────────────┬──────────────────────────────────────────────┤
│ Windowing          │ Keep only the most recent N turns            │
├────────────────────┼──────────────────────────────────────────────┤
│ Summarization      │ Compress older turns into summaries          │
├────────────────────┼──────────────────────────────────────────────┤
│ Key-Value Storage  │ Extract and store important facts separately │
├────────────────────┼──────────────────────────────────────────────┤
│ Priority Pruning   │ Remove less important turns first            │
├────────────────────┼──────────────────────────────────────────────┤
│ Semantic Chunking  │ Group related exchanges together             │
└────────────────────┴──────────────────────────────────────────────┘
```

## Windowing: The Sliding Context

The simplest memory management approach keeps only the most recent conversation turns:

```
                    ┌───────────────────────────┐
Turn 1              │ System + Turn 1           │
                    └───────────────────────────┘
                              │
                              ▼
                    ┌───────────────────────────┐
Turn 2              │ System + Turn 1-2         │
                    └───────────────────────────┘
                              │
                              ▼
                    ┌───────────────────────────┐
Turn 3              │ System + Turn 1-3         │
                    └───────────────────────────┘
                              │
                              ▼
                    ┌───────────────────────────┐
Turn 4              │ System + Turn 2-4         │ ← Turn 1 dropped
                    └───────────────────────────┘
                              │
                              ▼
                    ┌───────────────────────────┐
Turn 5              │ System + Turn 3-5         │ ← Turn 2 dropped
                    └───────────────────────────┘
```

这种方法简单直接，但会丢失更早轮次的信息。

## 总结：压缩记忆

更复杂一些的做法，是把较早的对话轮次压缩成摘要：

```
                    ┌────────────────────────────────────────────┐
Turn 1-3            │ System + Turn 1-3                          │
                    └────────────────────────────────────────────┘
                                       │
                                       ▼
                    ┌────────────────────────────────────────────┐
Turn 4              │ System + Summary(Turn 1-2) + Turn 3-4      │
                    └────────────────────────────────────────────┘
                                       │
                                       ▼
                    ┌────────────────────────────────────────────┐
Turn 5              │ System + Summary(Turn 1-3) + Turn 4-5      │
                    └────────────────────────────────────────────┘
```

总结能保留关键信息，同时降低标记消耗。

## 键值记忆：结构化状态

如果想要更强的控制力，可以把关键事实抽取出来，用结构化格式存储：

```
┌─────────────────────────────────────────────────────────────────────┐
│ CONTEXT WINDOW                                                      │
│                                                                     │
│  SYSTEM PROMPT: "You are a helpful assistant..."                    │
│                                                                     │
│  MEMORY:                                                            │
│  {                                                                  │
│    "user_name": "Alex",                                             │
│    "favorite_color": "blue",                                        │
│    "location": "Toronto",                                           │
│    "last_topic": "vacation plans"                                   │
│  }                                                                  │
│                                                                     │
│  RECENT CONVERSATION:                                               │
│  User: "What activities would you recommend?"                       │
│  Assistant: "Given your location in Toronto and interest in..."     │
│                                                                     │
│  CURRENT INPUT: "How about something indoors? It's cold."           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

结构化的好处是：你可以精确控制“保留什么、丢弃什么”。

## 超越对话：有状态应用

细胞的价值远不止“对话连贯”。它们可以支撑有状态应用，使大语言模型能够：

1. 记住之前交互
2. 更新并维护变量
3. 跟踪多步骤流程的进度
4. 在已有输出基础上继续构建

例如，一个简单的“带状态计算器”：

```
┌─────────────────────────────────────────────────────────────────────┐
│ STATEFUL CALCULATOR                                                 │
│                                                                     │
│ SYSTEM: "You are a calculator assistant that maintains a running    │
│          total. Follow the user's math operations step by step."    │
│                                                                     │
│ STATE: { "current_value": 0 }                                       │
│                                                                     │
│ User: "Start with 5"                                                │
│ Assistant: "Starting with 5. Current value is 5."                   │
│ STATE: { "current_value": 5 }                                       │
│                                                                     │
│ User: "Multiply by 3"                                               │
│ Assistant: "5 × 3 = 15. Current value is 15."                       │
│ STATE: { "current_value": 15 }                                      │
│                                                                     │
│ User: "Add 7"                                                       │
│ Assistant: "15 + 7 = 22. Current value is 22."                      │
│ STATE: { "current_value": 22 }                                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

状态变量跨轮次持久化，从而支持连续计算。

## 长期记忆：超越上下文窗口

要实现真正的持久化记忆，需要引入外部存储：

```
┌──────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│   User Input                                                             │
│       │                                                                  │
│       ▼                                                                  │
│  ┌─────────────┐                                                         │
│  │ Extract     │                                                         │
│  │ Key Info    │                                                         │
│  └─────────────┘                                                         │
│       │                                                                  │
│       ▼                                                                  │
│  ┌─────────────┐      ┌────────────────────┐                             │
│  │ Update      │◄─────┤ External Memory    │                             │
│  │ Memory      │      │ (Vector DB,        │                             │
│  │             │─────►│  Document DB, etc) │                             │
│  └─────────────┘      └────────────────────┘                             │
│       │                        ▲                                         │
│       │                        │                                         │
│       ▼                        │                                         │
│  ┌─────────────┐      ┌────────────────────┐                             │
│  │ Construct   │      │ Retrieve Relevant  │                             │
│  │ Context     │◄─────┤ Memory             │                             │
│  │             │      │                    │                             │
│  └─────────────┘      └────────────────────┘                             │
│       │                                                                  │
│       ▼                                                                  │
│  ┌─────────────┐                                                         │
│  │             │                                                         │
│  │ LLM         │                                                         │
│  │             │                                                         │
│  └─────────────┘                                                         │
│       │                                                                  │
│       ▼                                                                  │
│   Response                                                               │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

这种架构使“近乎无限”的记忆成为可能，因为它能：
1. 从对话中抽取关键信息
2. 存入外部数据库
3. 在需要时检索相关记忆
4. 把检索结果注入提示

## 细胞实现：记忆管理器

下面给出一个示例类，用于实现基础的记忆管理：

```python
class ContextCell:
    """A context cell that maintains memory across interactions."""
    
    def __init__(self, system_prompt, max_turns=10, memory_strategy="window"):
        """
        Initialize the context cell.
        
        Args:
            system_prompt (str): The system instructions
            max_turns (int): Maximum conversation turns to keep
            memory_strategy (str): 'window', 'summarize', or 'key_value'
        """
        self.system_prompt = system_prompt
        self.max_turns = max_turns
        self.memory_strategy = memory_strategy
        self.conversation_history = []
        self.key_value_store = {}
        
    def add_exchange(self, user_input, assistant_response):
        """Add a conversation exchange to history."""
        self.conversation_history.append({
            "user": user_input,
            "assistant": assistant_response
        })
        
        # Apply memory management if needed
        if len(self.conversation_history) > self.max_turns:
            self._manage_memory()
    
    def extract_info(self, key, value):
        """Store important information in key-value store."""
        self.key_value_store[key] = value
    
    def _manage_memory(self):
        """Apply the selected memory management strategy."""
        if self.memory_strategy == "window":
            # Keep only the most recent turns
            self.conversation_history = self.conversation_history[-self.max_turns:]
        
        elif self.memory_strategy == "summarize":
            # Summarize older turns (would use an LLM in practice)
            to_summarize = self.conversation_history[:-self.max_turns + 1]
            summary = self._create_summary(to_summarize)
            
            # Replace old turns with summary
            self.conversation_history = [{"summary": summary}] + \
                                       self.conversation_history[-(self.max_turns-1):]
    
    def _create_summary(self, exchanges):
        """Create a summary of conversation exchanges."""
        # In practice, this would call an LLM to create the summary
        # For this example, we'll use a placeholder
        return f"Summary of {len(exchanges)} previous exchanges"
    
    def build_context(self, current_input):
        """Build the full context for the next LLM call."""
        context = f"{self.system_prompt}\n\n"
        
        # Add key-value memory if we have any
        if self.key_value_store:
            context += "MEMORY:\n"
            for key, value in self.key_value_store.items():
                context += f"{key}: {value}\n"
            context += "\n"
        
        # Add conversation history
        if self.conversation_history:
            context += "CONVERSATION HISTORY:\n"
            for exchange in self.conversation_history:
                if "summary" in exchange:
                    context += f"[Previous exchanges: {exchange['summary']}]\n\n"
                else:
                    context += f"User: {exchange['user']}\n"
                    context += f"Assistant: {exchange['assistant']}\n\n"
        
        # Add current input
        context += f"User: {current_input}\nAssistant:"
        
        return context
```

## 度量细胞的效率

和分子一样，细胞的效率度量也很关键：

```
┌─────────────────────────────────────────────────────────────────┐
│ MEMORY STRATEGY COMPARISON                                      │
├──────────────────┬──────────────┬─────────────┬─────────────────┤
│ Strategy         │ Token Usage  │ Information │ Implementation  │
│                  │              │ Retention   │ Complexity      │
├──────────────────┼──────────────┼─────────────┼─────────────────┤
│ No Memory        │ Lowest       │ None        │ Trivial         │
├──────────────────┼──────────────┼─────────────┼─────────────────┤
│ Full History     │ Highest      │ Complete    │ Trivial         │
├──────────────────┼──────────────┼─────────────┼─────────────────┤
│ Windowing        │ Controlled   │ Recent Only │ Easy            │
├──────────────────┼──────────────┼─────────────┼─────────────────┤
│ Summarization    │ Moderate     │ Good        │ Moderate        │
├──────────────────┼──────────────┼─────────────┼─────────────────┤
│ Key-Value Store  │ Low          │ Selective   │ Moderate        │
├──────────────────┼──────────────┼─────────────┼─────────────────┤
│ External Store   │ Very Low     │ Extensive   │ Complex         │
└──────────────────┴──────────────┴─────────────┴─────────────────┘
```

不同策略优化的目标不同。选择哪一种，取决于你的具体应用需求。

## 高级技巧：记忆编排

对于更复杂的应用，多个记忆系统可以协同工作：

```
┌─────────────────────────────────────────────────────────────────────┐
│                      MEMORY ORCHESTRATION                           │
│                                                                     │
│  ┌─────────────────┐    ┌─────────────────┐   ┌─────────────────┐   │
│  │                 │    │                 │   │                 │   │
│  │ Short-term      │    │ Working         │   │ Long-term       │   │
│  │ Memory          │    │ Memory          │   │ Memory          │   │
│  │                 │    │                 │   │                 │   │
│  │ • Recent turns  │    │ • Current task  │   │ • User profile  │   │
│  │ • Immediate     │    │ • Active        │   │ • Historical    │   │
│  │   context       │    │   variables     │   │   facts         │   │
│  │ • Last few      │    │ • Task progress │   │ • Learned       │   │
│  │   exchanges     │    │ • Mid-task      │   │   preferences   │   │
│  │                 │    │   state         │   │                 │   │
│  └─────────────────┘    └─────────────────┘   └─────────────────┘   │
│         ▲ ▼                   ▲ ▼                   ▲ ▼             │
│         │ │                   │ │                   │ │             │
│  ┌──────┘ └───────────────────┘ └───────────────────┘ └──────┐      │
│  │                                                           │      │
│  │                    Memory Manager                         │      │
│  │                                                           │      │
│  └───────────────────────────────┬───────────────────────────┘      │
│                                  │                                  │
│                                  ▼                                  │
│                        ┌─────────────────┐                          │
│                        │                 │                          │
│                        │   Context       │                          │
│                        │   Builder       │                          │
│                        │                 │                          │
│                        └─────────────────┘                          │
│                                  │                                  │
│                                  ▼                                  │
│                        ┌─────────────────┐                          │
│                        │                 │                          │
│                        │      LLM        │                          │
│                        │                 │                          │
│                        └─────────────────┘                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

这种架构模仿人类的记忆系统，包括：
- **短期记忆**：最近的对话轮次
- **工作记忆**：当前任务状态和变量
- **长期记忆**：持久化的用户信息和偏好

记忆管理器负责协调这些系统，并决定在每个上下文中包含哪些信息。

## 记忆与幻觉抑制

记忆细胞最有价值的收益之一，就是减少幻觉：

```
┌─────────────────────────────────────────────────────────────────────┐
│ HALLUCINATION REDUCTION STRATEGIES                                  │
├─────────────────────────────────────────────────────────────────────┤
│ 1. Explicitly store facts extracted from previous exchanges         │
│ 2. Tag information with source/certainty levels                     │
│ 3. Include relevant facts in context when similar topics arise      │
│ 4. Detect and correct contradictions between memory and responses   │
│ 5. Periodically verify important facts through user confirmation    │
└─────────────────────────────────────────────────────────────────────┘
```

当我们用记忆中一致的事实去“锚定”模型时，整体可靠性会显著提升。

## 超越文本：结构化状态

更高级的细胞会维护结构化状态，而不仅仅是文本历史：

```
┌─────────────────────────────────────────────────────────────────────┐
│ STRUCTURED STATE EXAMPLES                                           │
├─────────────────────────┬───────────────────────────────────────────┤
│ Progression State       │ {"step": 3, "completed_steps": [1, 2],    │
│                         │  "next_action": "validate_input"}         │
├─────────────────────────┼───────────────────────────────────────────┤
│ User Profile            │ {"name": "Alex", "preferences": {         │
│                         │  "communication_style": "concise",        │
│                         │  "expertise_level": "beginner"}}          │
├─────────────────────────┼───────────────────────────────────────────┤
│ Application State       │ {"current_view": "dashboard",             │
│                         │  "filters": ["active", "high_priority"],  │
│                         │  "sort_by": "deadline"}                   │
├─────────────────────────┼───────────────────────────────────────────┤
│ Environmental Context   │ {"location": "Toronto",                   │
│                         │  "weather": "snowing",                    │
│                         │  "time": "evening"}                       │
└─────────────────────────┴───────────────────────────────────────────┘
```

结构化方式能更精确地控制上下文，并支撑更复杂的应用。

## 记忆反馈闭环

更复杂的细胞会构建反馈闭环，让大语言模型参与自身记忆的管理：

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  User: "I'm planning a trip to Japan next month."                   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │ [INTERNAL MEMORY EXTRACTION]                                    ││
│  │ Important facts to remember:                                    ││
│  │ - User is planning a trip to Japan                              ││
│  │ - Trip is scheduled for next month                              ││
│  │ Confidence: High                                                ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                     │
│  Assistant: "That's exciting! Japan is beautiful. Are you           │
│  interested in cities like Tokyo and Kyoto, or more rural areas?"   │
│                                                                     │
│  User: "Definitely Tokyo, and maybe Osaka too."                     │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │ [INTERNAL MEMORY UPDATE]                                        ││
│  │ Updated facts:                                                  ││
│  │ - User is planning a trip to Japan next month                   ││
│  │ - User is interested in Tokyo and Osaka                         ││
│  │ - User may not be interested in rural areas (confidence: medium)││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

大语言模型自己抽取并更新“应该记住”的信息，从而形成一个自我改进的记忆系统。

## 关键要点

1. 记忆细胞提供跨多轮交互的状态持久化
2. 随着对话增长，**标记预算管理** 变得至关重要
3. 常见记忆策略包括窗口截断、总结压缩与键值存储
4. 外部记忆让上下文窗口之外的持久化存储成为可能
5. 结构化状态支撑超越对话的复杂应用
6. 记忆编排能把多种记忆系统组合到最优
7. 自我改进记忆让大语言模型参与自身记忆管理与改进

## 练习

1. 用窗口截断实现一个简单的对话记忆系统
2. 在同一段长对话上对比不同记忆策略
3. 构建一个从对话中抽取关键事实的键值存储
4. 试验让大语言模型对较早轮次进行总结压缩
5. 为一个特定应用领域设计结构化状态管理器

## 下一步

下一节我们将讨论器官：多智能体系统，让多个上下文细胞协同工作来解决复杂问题。

继续阅读下一节：

[04_organs_applications.md →](04_organs_applications.md)

---

## 深入：记忆抽象

记忆可以按抽象层次组织为多层：

```
┌────────────────────────────────────────────────────────────────────┐
│ MEMORY ABSTRACTION LAYERS                                          │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│   ┌─────────────────┐                                              │
│   │ Episodic Memory │  Specific conversation exchanges and events  │
│   └─────────────────┘                                              │
│           ▲                                                        │
│           │                                                        │
│   ┌─────────────────┐                                              │
│   │ Semantic Memory │  Facts, concepts, and structured knowledge   │
│   └─────────────────┘                                              │
│           ▲                                                        │
│           │                                                        │
│   ┌─────────────────┐                                              │
│   │ Conceptual      │  High-level patterns, preferences, goals     │
│   │ Memory          │                                              │
│   └─────────────────┘                                              │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

这种分层方式能在“具体细节”和“高层理解”之间取得平衡，让系统既不丢关键信息，也不被细节淹没。
