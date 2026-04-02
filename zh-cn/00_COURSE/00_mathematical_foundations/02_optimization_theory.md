<!-- markdownlint-disable MD013 MD025 MD033 MD046 MD050 -->

# 优化理论：寻找最优的上下文组装方式

## 从“够用”到“数学最优”

> **Module 00.2** | *Context Engineering Course: From Foundations to Frontier Systems*
>
> *"Optimization is the art of finding the best solution among all possible solutions" — Stephen Boyd*

---

## 从手工调参到数学优化

你已经学会把上下文形式化为 `C = A(c₁, c₂, ..., c₆)`。现在关键问题来了：**怎样找到尽可能最优的组装函数 `A`？**

### 通用的优化挑战

先看几个熟悉的优化场景：

**GPS 导航**：在数百万条可能路径里找到最快路线

```text
Minimize: Total_Travel_Time(route)
Subject to: Valid_roads, Traffic_conditions, Vehicle_constraints

```

**配方优化**：调整配料与比例以得到“最满意”的结果

```text
Maximize: Taste_satisfaction(ingredients, proportions)
Subject to: Available_ingredients, Dietary_restrictions, Budget_limits

```

**Context Engineering**：寻找最优的组装策略

```text
Maximize: Context_Quality(A, c₁, c₂, ..., c₆)
Subject to: Token_limits, Quality_thresholds, Computational_constraints

```

**共同模式**：在每个场景中，我们都要在大量候选里找到“最好”的选择，并同时满足清晰的目标函数与现实世界的约束。

---

## 上下文优化的数学框架

### 基本优化问题

```text
F* = arg max F(A, c₁, c₂, ..., c₆)
     A∈𝒜

Where:
F* = Optimal assembly function
F(·) = Objective function measuring context quality
A = Assembly function we're optimizing
𝒜 = Set of all possible assembly functions
cᵢ = Context components

```

### 优化地形的直观理解

```text
    Context Quality
         ↑
    1.0  │     🏔️ Global Maximum
         │    ╱ ╲    (Optimal assembly)
    0.8  │   ╱   ╲
         │  ╱     ╲  🏔️ Local Maximum
    0.6  │ ╱       ╲╱ ╲  (Good but not optimal)
         │╱            ╲  🏔️
    0.4  │              ╲╱ ╲
         │                  ╲
    0.2  │                   ╲
         └─────────────────────────────────────────►
         0                   Assembly Strategy Space

Goal: Navigate this landscape to find the highest peak (best strategy)

```

**从零解释**：你可以把优化理解为“爬山”：高度代表质量，我们想找到最高峰，但地形里充满了局部山峰与谷地。数学优化提供了系统化的方法，让我们能更高效地在这片地形中导航并逼近最优解。

---

## Software 3.0 范式 1：Prompts（优化策略模板）

Prompts 提供可复用的结构化框架，用来以更稳定、可复制的方式处理上下文优化问题。

### 目标函数设计模板

<pre>
```markdown
# Context Optimization Objective Design Framework

## Problem Definition
**Goal**: Define what "optimal context" means for your specific use case
**Approach**: Systematic decomposition of quality into measurable components

## Objective Function Structure
Maximize: Quality(C) = Σᵢ wᵢ · Quality_Componentᵢ(C)

### Quality Component Analysis

#### 1. Relevance Component (w₁ = 0.4)
**Definition**: How well does the context address the user's query?
**Measurement Approach**:
- Semantic similarity between context and query
- Coverage of query requirements
- Information density relevant to query

**Mathematical Formulation**:
```
Relevance(C, q) = Σⱼ Similarity(contextⱼ, q) × Importance(contextⱼ)
```

**Optimization Questions**:
- Which components contribute most to query relevance?
- How can we maximize relevant information within token constraints?
- What trade-offs exist between breadth and depth of relevant information?

#### 2. Completeness Component (w₂ = 0.3)
**Definition**: Does the context provide all necessary information for effective response?
**Measurement Approach**:
- Coverage of required information categories
- Presence of essential background context
- Availability of supporting details

**Mathematical Formulation**:
```
Completeness(C) = Required_Information_Present(C) / Total_Required_Information
```

**Optimization Questions**:
- What information is absolutely essential vs. nice-to-have?
- How do we balance comprehensive coverage with token efficiency?
- What dependencies exist between different information components?

#### 3. Consistency Component (w₃ = 0.2)
**Definition**: Are all context components internally consistent and non-contradictory?
**Measurement Approach**:
- Detection of contradictory statements
- Logical coherence across components
- Alignment between instructions and knowledge

**Mathematical Formulation**:
```
Consistency(C) = 1 - Contradiction_Count(C) / Total_Statements(C)
```

**Optimization Questions**:
- How do we detect and resolve information conflicts?
- What hierarchies exist for resolving contradictory information?
- How do we maintain consistency while incorporating diverse sources?

#### 4. Efficiency Component (w₄ = 0.1)
**Definition**: How effectively does the context use available token budget?
**Measurement Approach**:
- Information density per token
- Redundancy elimination
- Token utilization effectiveness

**Mathematical Formulation**:
```
Efficiency(C) = Information_Value(C) / Token_Count(C)
```

**Optimization Questions**:
- Where can we eliminate redundancy without losing information?
- How do we prioritize high-value information within constraints?
- What compression techniques maintain quality while reducing tokens?

## Constraint Definition Framework

### Hard Constraints (Must be satisfied)
```
Token_Count(C) ≤ L_max
Quality_Threshold(C) ≥ Q_min
Safety_Requirements(C) = True
```

### Soft Constraints (Preferences with flexibility)
```
Preferred_Token_Usage ≈ 0.8 × L_max
Preferred_Response_Time ≤ T_target
Preferred_Complexity_Level ∈ [Simple, Moderate, Advanced]
```

## Weight Determination Strategy

### Context-Adaptive Weighting
```
IF query_type == "analytical":
    w₁ = 0.5, w₂ = 0.3, w₃ = 0.15, w₄ = 0.05
ELIF query_type == "creative":
    w₁ = 0.3, w₂ = 0.2, w₃ = 0.1, w₄ = 0.4
ELIF query_type == "factual":
    w₁ = 0.4, w₂ = 0.4, w₃ = 0.15, w₄ = 0.05
```

### User-Preference Adaptation
```
weights = base_weights + α × user_preference_vector + β × performance_feedback
```

## Optimization Strategy Selection

### Simple Optimization (Single objective, few constraints)
**Method**: Grid search or simple hill climbing
**When to Use**: Clear single objective, limited complexity
**Example**: Optimizing token allocation for maximum relevance

### Multi-Objective Optimization (Multiple competing objectives)
**Method**: Pareto optimization or weighted sum approach
**When to Use**: Trade-offs between quality dimensions
**Example**: Balancing relevance vs. completeness vs. efficiency

### Constrained Optimization (Complex constraints)
**Method**: Lagrangian optimization or penalty methods
**When to Use**: Multiple hard constraints must be satisfied
**Example**: Meeting token limits while achieving quality thresholds

### Dynamic Optimization (Changing conditions)
**Method**: Adaptive algorithms with real-time adjustment
**When to Use**: Context requirements change during optimization
**Example**: Optimizing based on user feedback during interaction
```
</pre>

**从零解释**：这个模板像“工程师设计桥梁”一样引导你设计优化问题：你需要明确成功的定义、必须遵守的约束，以及你愿意接受哪些权衡。

### 多目标优化策略模板

```xml
<multi_objective_optimization_template>
  <scenario>Context optimization with competing objectives</scenario>

  <objective_definition>
    <primary_objectives>
      <objective name="relevance" weight="variable" priority="high">
        <description>Maximize semantic relevance to user query</description>
        <measurement>Cosine similarity between context embeddings and query embedding</measurement>
        <optimization_direction>maximize</optimization_direction>
      </objective>

      <objective name="completeness" weight="variable" priority="high">
        <description>Ensure comprehensive information coverage</description>
        <measurement>Percentage of required information categories covered</measurement>
        <optimization_direction>maximize</optimization_direction>
      </objective>

      <objective name="efficiency" weight="variable" priority="medium">
        <description>Optimize information density per token</description>
        <measurement>Information value divided by token count</measurement>
        <optimization_direction>maximize</optimization_direction>
      </objective>
    </primary_objectives>

    <secondary_objectives>
      <objective name="diversity" weight="0.1" priority="low">
        <description>Include diverse perspectives and approaches</description>
        <measurement>Semantic diversity score across context components</measurement>
        <optimization_direction>maximize</optimization_direction>
      </objective>

      <objective name="freshness" weight="0.1" priority="low">
        <description>Prioritize recent and current information</description>
        <measurement>Time-weighted average of information recency</measurement>
        <optimization_direction>maximize</optimization_direction>
      </objective>
    </secondary_objectives>
  </objective_definition>

  <optimization_approaches>
    <pareto_optimization>
      <description>Find solutions that cannot be improved in one objective without degrading another</description>
      <when_to_use>When no clear priority ranking exists between objectives</when_to_use>
      <implementation>Generate Pareto frontier and let user choose preferred trade-off</implementation>
    </pareto_optimization>

    <weighted_sum_optimization>
      <description>Combine objectives using weighted linear combination</description>
      <when_to_use>When relative importance of objectives can be quantified</when_to_use>
      <implementation>Optimize single composite objective: Σ wᵢ × objectiveᵢ</implementation>
    </weighted_sum_optimization>

    <lexicographic_optimization>
      <description>Optimize objectives in strict priority order</description>
      <when_to_use>When clear hierarchy exists between objectives</when_to_use>
      <implementation>Optimize highest priority first, then next priority within acceptable range</implementation>
    </lexicographic_optimization>

    <epsilon_constraint>
      <description>Optimize primary objective while constraining others to acceptable levels</description>
      <when_to_use>When one objective is clearly most important</when_to_use>
      <implementation>Maximize primary objective subject to secondary objectives ≥ thresholds</implementation>
    </epsilon_constraint>
  </optimization_approaches>

  <trade_off_analysis_framework>
    <trade_off type="relevance_vs_completeness">
      <scenario>High relevance might mean narrow focus, reducing completeness</scenario>
      <resolution_strategy>Use hierarchical information organization: core relevance + supplementary completeness</resolution_strategy>
    </trade_off>

    <trade_off type="completeness_vs_efficiency">
      <scenario>Complete information coverage might exceed token budgets</scenario>
      <resolution_strategy>Use intelligent summarization and priority-based selection</resolution_strategy>
    </trade_off>

    <trade_off type="consistency_vs_diversity">
      <scenario>Diverse perspectives might introduce apparent contradictions</scenario>
      <resolution_strategy>Clearly label perspective sources and provide synthesis framework</resolution_strategy>
    </trade_off>
  </trade_off_analysis_framework>

  <dynamic_weight_adjustment>
    <user_feedback_integration>
      <positive_feedback>Increase weights for objectives that contributed to successful outcomes</positive_feedback>
      <negative_feedback>Adjust weights to address areas where user expressed dissatisfaction</negative_feedback>
      <implicit_feedback>Monitor user behavior patterns to infer objective preferences</implicit_feedback>
    </user_feedback_integration>

    <context_adaptation>
      <query_complexity>Increase completeness weight for complex queries</query_complexity>
      <time_pressure>Increase efficiency weight when user indicates urgency</time_pressure>
      <domain_specificity>Increase relevance weight for highly specialized domains</domain_specificity>
    </context_adaptation>
  </dynamic_weight_adjustment>
</multi_objective_optimization_template>

```

**从零解释**：这个 XML 模板用于处理“想要多个目标、但目标之间会冲突”的场景——例如既要全面覆盖、又要足够简洁。它提供了系统化的方法来管理这些权衡，类似项目经理在质量、时间、预算之间做平衡。

### 约束处理策略模板

```yaml
# Constraint Handling Strategy Template

constraint_optimization_framework:

  constraint_types:
    hard_constraints:
      description: "Constraints that absolutely must be satisfied"
      violation_consequence: "Solution is invalid/unusable"
      examples:
        - token_budget: "Total tokens ≤ maximum context window"
        - safety_requirements: "No harmful or inappropriate content"
        - format_requirements: "Output must match required structure"
        - computational_limits: "Processing time ≤ acceptable threshold"

    soft_constraints:
      description: "Preferences that should be satisfied when possible"
      violation_consequence: "Solution quality degrades but remains usable"
      examples:
        - preferred_length: "Target 80% of maximum token budget"
        - response_time: "Prefer faster assembly when possible"
        - writing_style: "Match user's preferred communication style"
        - complexity_level: "Adjust to user's expertise level"

    adaptive_constraints:
      description: "Constraints that change based on context and performance"
      violation_consequence: "Dynamic adjustment based on conditions"
      examples:
        - quality_threshold: "Minimum quality adjusts based on query complexity"
        - efficiency_requirement: "Stricter efficiency under resource pressure"
        - completeness_standard: "Higher completeness for critical decisions"

  constraint_satisfaction_strategies:
    penalty_method:
      description: "Add penalty terms to objective function for constraint violations"
      mathematical_form: "Minimize f(x) + Σ penalty_weights × violation_amounts"
      when_to_use: "When constraints can be violated temporarily during optimization"
      advantages: ["Simple to implement", "Handles soft constraints naturally"]
      disadvantages: ["May not guarantee hard constraint satisfaction"]

    barrier_method:
      description: "Create barriers that prevent violation of constraints"
      mathematical_form: "Minimize f(x) + Σ barrier_functions(constraints)"
      when_to_use: "When hard constraints must never be violated"
      advantages: ["Guarantees constraint satisfaction", "Efficient for simple constraints"]
      disadvantages: ["Can be unstable near constraint boundaries"]

    lagrangian_method:
      description: "Use Lagrange multipliers to incorporate constraints"
      mathematical_form: "Optimize L(x,λ) = f(x) + Σ λᵢ × constraint_violations"
      when_to_use: "When constraints are differentiable and well-behaved"
      advantages: ["Theoretically elegant", "Provides sensitivity analysis"]
      disadvantages: ["Requires mathematical sophistication", "May have convergence issues"]

    projection_method:
      description: "Project solutions back into feasible region after each step"
      mathematical_form: "x_new = project_to_feasible_region(x_optimized)"
      when_to_use: "When feasible region has simple geometric structure"
      advantages: ["Always maintains feasibility", "Simple conceptually"]
      disadvantages: ["Projection may be computationally expensive"]

  constraint_prioritization:
    critical_constraints:
      priority: 1
      handling: "Must be satisfied exactly - optimization fails if violated"
      examples: ["Safety requirements", "Legal compliance", "Technical feasibility"]

    important_constraints:
      priority: 2
      handling: "Strong preference for satisfaction - significant penalty if violated"
      examples: ["Token budget limits", "Quality thresholds", "Performance requirements"]

    preferred_constraints:
      priority: 3
      handling: "Mild preference for satisfaction - small penalty if violated"
      examples: ["Style preferences", "Efficiency targets", "Convenience factors"]

  dynamic_constraint_adaptation:
    performance_based_adjustment:
      description: "Adjust constraints based on observed performance"
      mechanism: "Tighten constraints when performance is good, relax when struggling"
      example: "If consistently exceeding quality targets, increase efficiency requirements"

    context_based_adjustment:
      description: "Modify constraints based on current context characteristics"
      mechanism: "Different constraint sets for different types of queries/users"
      example: "Stricter completeness requirements for medical/legal queries"

    user_feedback_adjustment:
      description: "Adapt constraints based on user satisfaction and feedback"
      mechanism: "Learn user preferences and adjust constraint priorities accordingly"
      example: "User values speed over completeness → relax completeness constraints"

  constraint_conflict_resolution:
    conflict_detection:
      method: "Analyze constraint combinations for mathematical inconsistencies"
      indicators: ["No feasible solution exists", "Contradictory requirements", "Impossible combinations"]

    resolution_strategies:
      constraint_relaxation:
        description: "Temporarily relax lower-priority constraints"
        process: "Identify minimum relaxation needed to restore feasibility"

      constraint_reformulation:
        description: "Rewrite constraints in compatible forms"
        process: "Transform constraints to eliminate contradictions while preserving intent"

      priority_override:
        description: "Allow higher-priority constraints to override lower-priority ones"
        process: "Establish clear hierarchy and resolution rules"

      user_consultation:
        description: "Request user guidance when automatic resolution is unclear"
        process: "Present trade-offs and allow user to choose resolution approach"

  implementation_guidelines:
    constraint_validation:
      - "Validate all constraints before beginning optimization"
      - "Check for mathematical consistency and feasibility"
      - "Ensure constraint functions are well-defined and computable"

    monitoring_and_adjustment:
      - "Continuously monitor constraint satisfaction during optimization"
      - "Log constraint violations and their impacts on solution quality"
      - "Adjust constraint handling strategies based on empirical performance"

    user_communication:
      - "Clearly communicate which constraints are hard vs. soft"
      - "Explain trade-offs when constraints conflict"
      - "Provide transparency about constraint handling decisions"

```

**从零解释**：这个 YAML 模板提供了一套系统化的“约束处理”方法，就像在复杂项目里用清晰规则管理相互竞争的需求。它帮助你区分哪些是可协商的、哪些是不可妥协的，并以系统化方式处理冲突。

---

## Software 3.0 范式 2：Programming（优化算法）

Programming 提供把优化策略系统化落地的“计算引擎”，让系统能够自动搜索并逼近最优解，而不是依赖手工调参。

### 基于梯度的优化实现

```python
import numpy as np
from typing import Dict, List, Tuple, Callable, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
import warnings

@dataclass
class OptimizationResult:
    """Results from context optimization process"""
    optimal_assembly: Dict
    final_quality_score: float
    optimization_history: List[Dict]
    convergence_info: Dict
    constraint_satisfaction: Dict

class ContextOptimizer(ABC):
    """Abstract base class for context optimization algorithms"""

    @abstractmethod
    def optimize(self, initial_assembly: Dict, objective_function: Callable,
                constraints: List[Callable]) -> OptimizationResult:
        """Optimize context assembly configuration"""
        pass

class GradientBasedOptimizer(ContextOptimizer):
    """Gradient-based optimization for context assembly parameters"""

    def __init__(self, learning_rate: float = 0.01, max_iterations: int = 1000,
                 convergence_threshold: float = 1e-6):
        self.learning_rate = learning_rate
        self.max_iterations = max_iterations
        self.convergence_threshold = convergence_threshold
        self.optimization_history = []

    def optimize(self, initial_assembly: Dict, objective_function: Callable,
                constraints: List[Callable] = None) -> OptimizationResult:
        """
        Optimize context assembly using gradient-based methods

        Args:
            initial_assembly: Starting point for optimization
            objective_function: Function to maximize (context quality)
            constraints: List of constraint functions

        Returns:
            OptimizationResult with optimal configuration and metadata
        """

        # Convert assembly dict to parameter vector for optimization
        params, param_mapping = self._assembly_to_params(initial_assembly)

        # Initialize optimization tracking
        self.optimization_history = []
        best_params = params.copy()
        best_score = objective_function(self._params_to_assembly(params, param_mapping))

        for iteration in range(self.max_iterations):
            # Calculate numerical gradient
            gradient = self._compute_numerical_gradient(
                params, objective_function, param_mapping
            )

            # Apply constraints through projected gradient
            if constraints:
                gradient = self._project_gradient(params, gradient, constraints, param_mapping)

            # Update parameters
            old_params = params.copy()
            params = params + self.learning_rate * gradient

            # Ensure parameter bounds are respected
            params = self._enforce_parameter_bounds(params)

            # Evaluate new configuration
            current_assembly = self._params_to_assembly(params, param_mapping)
            current_score = objective_function(current_assembly)

            # Track progress
            iteration_info = {
                'iteration': iteration,
                'score': current_score,
                'gradient_norm': np.linalg.norm(gradient),
                'parameter_change': np.linalg.norm(params - old_params),
                'assembly_config': current_assembly.copy()
            }
            self.optimization_history.append(iteration_info)

            # Update best solution if improved
            if current_score > best_score:
                best_score = current_score
                best_params = params.copy()

            # Check convergence
            if iteration_info['parameter_change'] < self.convergence_threshold:
                break

            # Adaptive learning rate
            if iteration > 10:
                recent_improvements = [
                    self.optimization_history[i]['score'] - self.optimization_history[i-1]['score']
                    for i in range(max(0, iteration-10), iteration)
                ]
                avg_improvement = np.mean(recent_improvements)

                if avg_improvement < 0:  # Getting worse
                    self.learning_rate *= 0.9
                elif avg_improvement > self.convergence_threshold:  # Good progress
                    self.learning_rate *= 1.05

        # Prepare results
        optimal_assembly = self._params_to_assembly(best_params, param_mapping)

        convergence_info = {
            'converged': iteration < self.max_iterations - 1,
            'final_iteration': iteration,
            'final_gradient_norm': np.linalg.norm(gradient),
            'improvement_from_start': best_score - self.optimization_history[0]['score']
        }

        constraint_satisfaction = self._check_constraint_satisfaction(
            optimal_assembly, constraints
        ) if constraints else {'all_satisfied': True}

        return OptimizationResult(
            optimal_assembly=optimal_assembly,
            final_quality_score=best_score,
            optimization_history=self.optimization_history,
            convergence_info=convergence_info,
            constraint_satisfaction=constraint_satisfaction
        )

    def _assembly_to_params(self, assembly: Dict) -> Tuple[np.ndarray, Dict]:
        """Convert assembly configuration to parameter vector"""

        # Extract optimizable parameters
        params = []
        param_mapping = {'indices': {}, 'types': {}}

        current_idx = 0

        # Component weights
        if 'component_weights' in assembly:
            weights = assembly['component_weights']
            for comp_name, weight in weights.items():
                param_mapping['indices'][f'weight_{comp_name}'] = current_idx
                param_mapping['types'][f'weight_{comp_name}'] = 'weight'
                params.append(weight)
                current_idx += 1

        # Token allocations
        if 'token_allocations' in assembly:
            allocations = assembly['token_allocations']
            for comp_name, allocation in allocations.items():
                param_mapping['indices'][f'tokens_{comp_name}'] = current_idx
                param_mapping['types'][f'tokens_{comp_name}'] = 'allocation'
                params.append(allocation)
                current_idx += 1

        # Assembly strategy parameters
        if 'strategy_params' in assembly:
            strategy_params = assembly['strategy_params']
            for param_name, value in strategy_params.items():
                param_mapping['indices'][f'strategy_{param_name}'] = current_idx
                param_mapping['types'][f'strategy_{param_name}'] = 'strategy'
                params.append(value)
                current_idx += 1

        return np.array(params), param_mapping

    def _params_to_assembly(self, params: np.ndarray, param_mapping: Dict) -> Dict:
        """Convert parameter vector back to assembly configuration"""

        assembly = {
            'component_weights': {},
            'token_allocations': {},
            'strategy_params': {}
        }

        for param_name, idx in param_mapping['indices'].items():
            param_type = param_mapping['types'][param_name]
            value = params[idx]

            if param_type == 'weight':
                comp_name = param_name.replace('weight_', '')
                assembly['component_weights'][comp_name] = value
            elif param_type == 'allocation':
                comp_name = param_name.replace('tokens_', '')
                assembly['token_allocations'][comp_name] = max(0, int(value))
            elif param_type == 'strategy':
                strategy_name = param_name.replace('strategy_', '')
                assembly['strategy_params'][strategy_name] = value

        return assembly

    def _compute_numerical_gradient(self, params: np.ndarray,
                                  objective_function: Callable,
                                  param_mapping: Dict, epsilon: float = 1e-8) -> np.ndarray:
        """Compute numerical gradient using finite differences"""

        gradient = np.zeros_like(params)

        for i in range(len(params)):
            # Forward difference
            params_plus = params.copy()
            params_plus[i] += epsilon
            assembly_plus = self._params_to_assembly(params_plus, param_mapping)

            params_minus = params.copy()
            params_minus[i] -= epsilon
            assembly_minus = self._params_to_assembly(params_minus, param_mapping)

            # Calculate numerical derivative
            try:
                f_plus = objective_function(assembly_plus)
                f_minus = objective_function(assembly_minus)
                gradient[i] = (f_plus - f_minus) / (2 * epsilon)
            except Exception:
                # If function evaluation fails, set gradient to zero
                gradient[i] = 0.0

        return gradient

    def _project_gradient(self, params: np.ndarray, gradient: np.ndarray,
                         constraints: List[Callable], param_mapping: Dict) -> np.ndarray:
        """Project gradient to respect constraints"""

        projected_gradient = gradient.copy()

        # Check if current point satisfies constraints
        current_assembly = self._params_to_assembly(params, param_mapping)

        for constraint in constraints:
            if constraint(current_assembly) < 0:  # Constraint violated
                # Compute constraint gradient
                constraint_grad = self._compute_numerical_gradient(
                    params, lambda assembly: constraint(assembly), param_mapping
                )

                # Project gradient away from constraint boundary
                if np.dot(gradient, constraint_grad) < 0:
                    # Gradient points into infeasible region, project it
                    constraint_grad_norm = np.linalg.norm(constraint_grad)
                    if constraint_grad_norm > 1e-10:
                        constraint_grad_unit = constraint_grad / constraint_grad_norm
                        projection = np.dot(gradient, constraint_grad_unit) * constraint_grad_unit
                        projected_gradient = gradient - projection

        return projected_gradient

    def _enforce_parameter_bounds(self, params: np.ndarray) -> np.ndarray:
        """Enforce parameter bounds (weights between 0 and 1, allocations non-negative)"""

        bounded_params = params.copy()

        # Simple bounds: weights should be non-negative, allocations should be non-negative
        bounded_params = np.maximum(bounded_params, 0.0)

        # Additional bound: weights should not exceed 1.0 (though they can sum to > 1)
        # This prevents individual weights from becoming unreasonably large
        bounded_params = np.minimum(bounded_params, 10.0)

        return bounded_params

    def _check_constraint_satisfaction(self, assembly: Dict,
                                     constraints: List[Callable]) -> Dict:
        """Check if final solution satisfies all constraints"""

        satisfaction_info = {
            'all_satisfied': True,
            'individual_constraints': [],
            'violation_summary': {}
        }

        for i, constraint in enumerate(constraints):
            try:
                violation = constraint(assembly)
                satisfied = violation >= 0

                satisfaction_info['individual_constraints'].append({
                    'constraint_index': i,
                    'satisfied': satisfied,
                    'violation_amount': violation if not satisfied else 0.0
                })

                if not satisfied:
                    satisfaction_info['all_satisfied'] = False
                    satisfaction_info['violation_summary'][f'constraint_{i}'] = abs(violation)

            except Exception as e:
                satisfaction_info['individual_constraints'].append({
                    'constraint_index': i,
                    'satisfied': False,
                    'error': str(e)
                })
                satisfaction_info['all_satisfied'] = False

        return satisfaction_info

```

class MultiObjectiveOptimizer(ContextOptimizer):
    """Multi-objective optimization for context assembly"""

    def __init__(self, population_size: int = 50, max_generations: int = 100,
                 mutation_rate: float = 0.1, crossover_rate: float = 0.8):
        self.population_size = population_size
        self.max_generations = max_generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate

    def optimize(self, initial_assembly: Dict, objective_functions: List[Callable],
                constraints: List[Callable] = None) -> OptimizationResult:
        """
        Multi-objective optimization using evolutionary approach

        Args:
            initial_assembly: Starting point for optimization
            objective_functions: List of objective functions to optimize
            constraints: List of constraint functions

        Returns:
            OptimizationResult with Pareto-optimal solutions
        """

        # Initialize population around starting point
        population = self._initialize_population(initial_assembly)

        optimization_history = []
        pareto_front = []

        for generation in range(self.max_generations):
            # Evaluate population
            population_scores = []
            for individual in population:
                scores = [obj_func(individual) for obj_func in objective_functions]
                population_scores.append(scores)

            # Find Pareto front
            current_pareto_front = self._find_pareto_front(population, population_scores)

            # Update best Pareto front found so far
            if not pareto_front or self._pareto_front_improved(current_pareto_front, pareto_front):
                pareto_front = current_pareto_front.copy()

            # Record generation statistics
            generation_info = {
                'generation': generation,
                'pareto_front_size': len(current_pareto_front),
                'best_scores': [max(scores[i] for scores in population_scores)
                              for i in range(len(objective_functions))],
                'population_diversity': self._calculate_diversity(population)
            }
            optimization_history.append(generation_info)

            # Create next generation
            if generation < self.max_generations - 1:
                population = self._create_next_generation(population, population_scores)

        # Select single best solution from Pareto front for return
        # (In practice, might return entire Pareto front)
        best_solution = self._select_best_from_pareto_front(
            pareto_front, objective_functions
        )

        return OptimizationResult(
            optimal_assembly=best_solution,
            final_quality_score=sum(obj_func(best_solution) for obj_func in objective_functions),
            optimization_history=optimization_history,
            convergence_info={'pareto_front_size': len(pareto_front)},
            constraint_satisfaction={'all_satisfied': True}  # Simplified
        )

    def _initialize_population(self, base_assembly: Dict) -> List[Dict]:
        """Initialize population of assembly configurations"""
        population = []

        for _ in range(self.population_size):
            individual = self._mutate_assembly(base_assembly, mutation_strength=0.3)
            population.append(individual)

        return population

    def _find_pareto_front(self, population: List[Dict],
                          scores: List[List[float]]) -> List[Dict]:
        """Find Pareto-optimal solutions in current population"""
        pareto_front = []

        for i, (individual, score) in enumerate(zip(population, scores)):
            is_dominated = False

            for j, other_score in enumerate(scores):
                if i != j and self._dominates(other_score, score):
                    is_dominated = True
                    break

            if not is_dominated:
                pareto_front.append(individual)

        return pareto_front

    def _dominates(self, score_a: List[float], score_b: List[float]) -> bool:
        """Check if solution A dominates solution B (A is better in all objectives)"""
        return all(a >= b for a, b in zip(score_a, score_b)) and \
               any(a > b for a, b in zip(score_a, score_b))

    def _mutate_assembly(self, assembly: Dict, mutation_strength: float = 0.1) -> Dict:
        """Create mutated version of assembly configuration"""
        mutated = assembly.copy()

        # Mutate component weights
        if 'component_weights' in mutated:
            for comp_name in mutated['component_weights']:
                if np.random.random() < self.mutation_rate:
                    current_weight = mutated['component_weights'][comp_name]
                    mutation = np.random.normal(0, mutation_strength)
                    mutated['component_weights'][comp_name] = max(0, current_weight + mutation)

        # Mutate token allocations
        if 'token_allocations' in mutated:
            for comp_name in mutated['token_allocations']:
                if np.random.random() < self.mutation_rate:
                    current_allocation = mutated['token_allocations'][comp_name]
                    mutation = int(np.random.normal(0, mutation_strength * 100))
                    mutated['token_allocations'][comp_name] = max(0, current_allocation + mutation)

        return mutated

class BayesianOptimizer(ContextOptimizer):
    """Bayesian optimization for expensive context assembly evaluation"""

    def __init__(self, max_iterations: int = 50, exploration_factor: float = 2.0):
        self.max_iterations = max_iterations
        self.exploration_factor = exploration_factor
        self.evaluation_history = []

    def optimize(self, initial_assembly: Dict, objective_function: Callable,
                constraints: List[Callable] = None) -> OptimizationResult:
        """
        Bayesian optimization using Gaussian process surrogate model

        This approach is particularly useful when objective function evaluation
        is expensive (e.g., requires running full LLM inference)
        """

        # Sample initial points
        sample_points = self._generate_initial_samples(initial_assembly, n_samples=10)

        optimization_history = []
        best_assembly = initial_assembly
        best_score = objective_function(initial_assembly)

        for iteration in range(self.max_iterations):
            # Evaluate all sample points
            for assembly in sample_points:
                score = objective_function(assembly)
                self.evaluation_history.append((assembly, score))

                if score > best_score:
                    best_score = score
                    best_assembly = assembly

            # Fit Gaussian process to evaluation history
            gp_model = self._fit_gaussian_process()

            # Find next point to evaluate using acquisition function
            next_assembly = self._optimize_acquisition_function(gp_model, initial_assembly)
            sample_points = [next_assembly]

            # Record iteration progress
            iteration_info = {
                'iteration': iteration,
                'best_score': best_score,
                'evaluations_so_far': len(self.evaluation_history),
                'gp_confidence': self._assess_gp_confidence(gp_model)
            }
            optimization_history.append(iteration_info)

        return OptimizationResult(
            optimal_assembly=best_assembly,
            final_quality_score=best_score,
            optimization_history=optimization_history,
            convergence_info={'total_evaluations': len(self.evaluation_history)},
            constraint_satisfaction={'all_satisfied': True}  # Simplified
        )

# Complete context optimization system integrating multiple algorithms

class AdaptiveContextOptimizer:
    """Adaptive optimization system that selects best algorithm for the problem"""

    def __init__(self):
        self.optimizers = {
            'gradient': GradientBasedOptimizer(),
            'multi_objective': MultiObjectiveOptimizer(),
            'bayesian': BayesianOptimizer()
        }
        self.performance_history = {}

    def optimize(self, assembly_config: Dict, optimization_problem: Dict) -> OptimizationResult:
        """
        Automatically select and apply best optimization approach

        Args:
            assembly_config: Initial assembly configuration
            optimization_problem: Problem definition with objectives and constraints
        """

        # Analyze problem characteristics
        problem_type = self._analyze_problem_type(optimization_problem)

        # Select appropriate optimizer
        optimizer_name = self._select_optimizer(problem_type)
        optimizer = self.optimizers[optimizer_name]

        # Execute optimization
        result = optimizer.optimize(
            assembly_config,
            optimization_problem.get('objective_function'),
            optimization_problem.get('constraints', [])
        )

        # Record performance for future selection
        self._record_performance(optimizer_name, problem_type, result)

        return result

    def _analyze_problem_type(self, optimization_problem: Dict) -> Dict:
        """Analyze characteristics of optimization problem"""

        characteristics = {
            'num_objectives': len(optimization_problem.get('objective_functions', [1])),
            'num_constraints': len(optimization_problem.get('constraints', [])),
            'problem_complexity': self._assess_complexity(optimization_problem),
            'evaluation_cost': optimization_problem.get('evaluation_cost', 'medium')
        }

        return characteristics

    def _select_optimizer(self, problem_characteristics: Dict) -> str:
        """Select best optimizer based on problem characteristics"""

        if problem_characteristics['num_objectives'] > 1:
            return 'multi_objective'
        elif problem_characteristics['evaluation_cost'] == 'high':
            return 'bayesian'
        else:
            return 'gradient'

**从零解释**：这个编程框架提供了多种优化算法，就像“不同工作用不同工具”：平滑问题用梯度法更高效，多目标问题用进化方法更稳健，而每次评估代价很高时，贝叶斯优化更节省采样次数。

---

## Software 3.0 范式 3：Protocols（自适应优化演化）

Protocols 提供“可自我改进”的优化系统：它会学习哪些方法在什么问题上最有效，并持续精炼自身的优化策略。

### 自适应优化学习 Protocol

```text

/optimize.context.adaptive{
    intent="Continuously improve context optimization through learning and adaptation",

    input={
        optimization_problem={
            assembly_configuration=<current_context_assembly_setup>,
            objective_functions=<quality_metrics_to_optimize>,
            constraints=<hard_and_soft_limitations>,
            problem_characteristics=<complexity_evaluation_cost_time_pressure>
        },

        historical_performance={
            past_optimizations=<previous_optimization_attempts_and_results>,
            algorithm_effectiveness=<which_approaches_worked_best_when>,
            problem_pattern_recognition=<identified_patterns_in_optimization_success>,
            user_satisfaction_feedback=<quality_assessments_from_actual_use>
        },

        adaptation_context={
            current_resources=<available_computational_budget>,
            time_constraints=<optimization_time_limitations>,
            quality_requirements=<minimum_acceptable_performance>,
            exploration_vs_exploitation=<balance_between_trying_new_vs_using_proven>
        }
    },

    process=[
        /analyze.optimization.landscape{
            action="Systematically analyze the optimization problem structure and characteristics",
            method="Multi-dimensional problem analysis with pattern recognition",
            analysis_dimensions=[
                {problem_structure="Analyze objective function properties: smooth vs. discontinuous, local vs. global"},
                {constraint_complexity="Evaluate constraint interactions and feasibility regions"},
                {parameter_sensitivity="Assess how sensitive objectives are to parameter changes"},
                {optimization_history="Review past performance on similar problems"}
            ],
            pattern_recognition=[
                {smooth_landscapes="Identify when gradient-based methods are likely to succeed"},
                {multi_modal_landscapes="Detect problems requiring global optimization approaches"},
                {expensive_evaluations="Recognize when surrogate-model approaches are beneficial"},
                {multi_objective_trade_offs="Identify competing objectives requiring Pareto optimization"}
            ],
            output="Comprehensive problem characterization with optimization strategy recommendations"
        },

        /select.optimization.strategy{
            action="Choose optimal optimization approach based on problem analysis and historical performance",
            method="Adaptive strategy selection with performance-based learning",
            strategy_selection_criteria=[
                {problem_match="Match current problem characteristics to historical successful patterns"},
                {resource_efficiency="Consider computational budget and time constraints"},
                {success_probability="Estimate likelihood of successful optimization with each approach"},
                {exploration_value="Balance proven approaches with potentially better new methods"}
            ],
            available_strategies=[
                {gradient_based="Fast convergence for smooth, differentiable problems"},
                {evolutionary_algorithms="Robust global optimization for complex landscapes"},
                {bayesian_optimization="Sample-efficient optimization for expensive evaluations"},
                {hybrid_approaches="Combinations of methods for multi-stage optimization"},
                {adaptive_methods="Self-tuning algorithms that adjust during optimization"}
            ],
            output="Selected optimization strategy with confidence assessment and backup plans"
        },

        /execute.adaptive.optimization{
            action="Implement selected optimization strategy with real-time monitoring and adjustment",
            method="Dynamic optimization execution with performance feedback integration",
            execution_monitoring=[
                {convergence_tracking="Monitor optimization progress and convergence indicators"},
                {constraint_satisfaction="Ensure all constraints remain satisfied during optimization"},
                {quality_improvement="Track objective function improvements over iterations"},
                {resource_utilization="Monitor computational resource usage and efficiency"}
            ],
            adaptive_adjustments=[
                {strategy_modification="Adjust optimization parameters based on observed performance"},
                {algorithm_switching="Change algorithms if current approach shows poor progress"},
                {constraint_relaxation="Temporarily relax constraints if no feasible solution exists"},
                {multi_restart="Launch multiple optimization runs with different initializations"}
            ],
            output="Optimized context assembly with performance metrics and adaptation history"
        },

        /validate.optimization.quality{
            action="Comprehensively assess optimization results and validate solution quality",
            method="Multi-dimensional quality assessment with robustness testing",
            validation_dimensions=[
                {objective_achievement="Measure how well final solution achieves optimization objectives"},
                {constraint_compliance="Verify all constraints are satisfied in final solution"},
                {stability_analysis="Test solution robustness to small parameter perturbations"},
                {generalization_assessment="Evaluate how well solution performs on similar problems"}
            ],
            quality_metrics=[
                {improvement_over_baseline="Compare optimized solution to initial configuration"},
                {pareto_optimality="Assess trade-offs achieved in multi-objective optimization"},
                {convergence_quality="Evaluate whether optimization converged to good solution"},
                {computational_efficiency="Measure optimization cost relative to improvement achieved"}
            ],
            output="Comprehensive quality assessment with confidence intervals and recommendations"
        },

        /learn.optimization.patterns{
            action="Extract insights and patterns from optimization experience for future improvement",
            method="Pattern recognition and knowledge extraction from optimization history",
            learning_mechanisms=[
                {success_pattern_identification="Identify characteristics of successful optimizations"},
                {failure_mode_analysis="Understand why certain approaches failed or underperformed"},
                {algorithm_performance_modeling="Build models predicting algorithm effectiveness"},
                {problem_type_categorization="Develop taxonomy of optimization problems and solutions"}
            ],
            knowledge_integration=[
                {strategy_refinement="Improve optimization strategy selection rules"},
                {parameter_tuning="Learn better default parameters for different algorithms"},
                {hybrid_method_development="Create new optimization approaches combining successful elements"},
                {meta_optimization="Optimize the optimization process itself"}
            ],
            output="Updated optimization knowledge base with improved strategy selection and execution"
        }
    ],

    output={
        optimization_results={
            optimal_assembly=<best_context_assembly_configuration_found>,
            quality_metrics=<achieved_values_for_all_optimization_objectives>,
            optimization_metadata=<algorithm_used_iterations_convergence_info>,
            confidence_assessment=<reliability_and_robustness_of_solution>
        },

        learning_outcomes={
            strategy_effectiveness=<performance_of_chosen_optimization_approach>,
            pattern_insights=<new_patterns_discovered_about_optimization_problems>,
            knowledge_updates=<improvements_made_to_optimization_knowledge_base>,
            future_recommendations=<suggested_approaches_for_similar_problems>
        },

        adaptive_improvements={
            algorithm_refinements=<modifications_made_to_optimization_algorithms>,
            strategy_evolution=<how_optimization_strategy_selection_improved>,
            meta_learning_gains=<learning_about_learning_optimization_effectiveness>,
            system_adaptation=<overall_system_improvements_from_this_optimization>
        }
    },

    meta={
        optimization_approach=<specific_algorithm_and_configuration_used>,
        adaptation_level=<degree_of_system_learning_and_modification>,
        knowledge_integration=<how_new_insights_were_incorporated>,
        future_evolution=<predicted_improvements_for_next_optimizations>
    },

    // Self-evolution mechanisms for optimization improvement
    optimization_evolution=[
        {trigger="poor_convergence_detected",
         action="experiment_with_alternative_algorithms_and_hybrid_approaches"},
        {trigger="new_problem_type_encountered",
         action="develop_specialized_optimization_strategies_for_novel_characteristics"},
        {trigger="computational_efficiency_below_threshold",
         action="optimize_algorithm_implementations_and_parameter_selection"},
        {trigger="user_satisfaction_below_expectations",
         action="refine_objective_functions_and_incorporate_user_preference_learning"}
    ]
}

```

**从零解释**：这个 protocol 构建了一套“会学习的优化系统”，它会像经验丰富的工匠一样逐渐形成对“不同问题该用什么技术更有效”的直觉，并基于历史效果持续改进自己的方法。

---

## 研究连接与未来方向

### 与 Context Engineering Survey 的连接

本优化理论模块直接实现并扩展了 [Context Engineering Survey](https://arxiv.org/pdf/2507.13334) 中的关键概念：

**Context Optimization Foundations (§4.2 & §4.3)**：

- 通过数学形式化实现上下文处理优化的系统化方法
- 通过多目标优化框架扩展上下文管理技术
- 通过自适应算法选择应对计算复杂度挑战

**Scaling Law Applications (§7.1)**：

- 展示用于应对 O(n²) 计算挑战的上下文优化理论基础
- 通过参数优化实现 compositional understanding 框架
- 为资源约束下的上下文质量优化提供数学依据

**Production Deployment Challenges (§7.3)**：

- 通过高效优化算法满足可扩展性要求
- 通过资源优化策略管理计算预算
- 为生产环境中的实时上下文优化提供框架

### 超越现有研究的新增贡献

**Mathematical Optimization Framework for Context Engineering**：survey 覆盖了大量上下文技术，但我们提出的系统化数学优化路径 `F* = arg max F(A, c₁, ..., c₆)` 更强调“组装过程的严谨优化基础”，从而支持自动发现最优策略。

**Multi-Paradigm Optimization Integration**：把梯度法、进化算法与贝叶斯优化统一整合，并针对 context assembly 做特化，使优化策略更全面，也更贴合 context engineering 的问题特征。

**Adaptive Algorithm Selection**：根据问题特征与历史表现自动选择最佳算法的自学习优化系统，属于面向 context engineering 的 meta-optimization 前沿方向。

**Real-time Optimization Protocols**：把优化融入可学习、可演化的自适应 protocol，使系统从“静态优化”走向“动态、自我改进”的上下文优化体系。

### 未来研究方向

**Quantum-Inspired Optimization**：探索受量子退火与量子算法启发的优化方法，通过“叠加”同时探索多条优化路径，可能更高效地穿越复杂的 context assembly 优化地形。

**Neuromorphic Optimization**：借鉴生物神经网络的连续激活与突触可塑性，构建更自然、更自适应的优化过程，模拟生物系统优化信息处理的方式。

**Distributed Context Optimization**：研究可跨分布式 context engineering 系统协同的优化框架，使多个系统能够共享优化洞见与策略，形成协作式优化。

**Meta-Context Optimization**：研究能够推理并优化“自身优化过程”的系统，形成递归式改进闭环，使优化算法能够演化其数学基础与策略选择机制。

**Human-AI Collaborative Optimization**：发展将人类直觉与偏好纳入数学优化过程的框架，构建同时利用人类洞见与计算能力的混合优化系统。

**Temporal Optimization Dynamics**：研究时间依赖的优化问题：组装策略与质量指标随时间演化，需要能适配时序变化与用户需求的动态优化框架。

**Uncertainty-Aware Optimization**：研究不确定性下的优化：上下文组件、用户偏好与环境条件存在不确定性，需要鲁棒优化方法在信息不完备时仍能保持有效性。

**Multi-Scale Optimization**：研究可同时在多个尺度（组件级、组装级、系统级）优化 context assembly 的框架，并在所有尺度上保持一致性与效率。

---

## 实践练习与项目

### 练习 1：单目标优化实现

**目标**：用基于梯度的方法实现 token 分配优化

```python

# Your implementation template

class TokenAllocationOptimizer:
    def __init__(self, max_tokens: int):
        self.max_tokens = max_tokens

    def optimize_allocation(self, components: List[str],
                          relevance_scores: List[float]) -> Dict[str, int]:
        # TODO: Implement optimization to maximize relevance within token budget
        pass

    def objective_function(self, allocation: Dict[str, int],
                          relevance_scores: List[float]) -> float:
        # TODO: Calculate quality score for given allocation
        pass

# Test your optimizer

optimizer = TokenAllocationOptimizer(max_tokens=1000)

# Add test cases here

```

### 练习 2：多目标优化挑战

**目标**：在 context assembly 中平衡 relevance、completeness 与 efficiency

```python

class MultiObjectiveContextOptimizer:
    def __init__(self):
        # TODO: Initialize multi-objective optimization
        pass

    def optimize(self, context_components: Dict,
                objectives: List[Callable]) -> Dict:
        # TODO: Find Pareto-optimal solutions
        pass

    def visualize_pareto_front(self, solutions: List[Dict]):
        # TODO: Visualize trade-offs between objectives
        pass

# Test with competing objectives

optimizer = MultiObjectiveContextOptimizer()

```

### 练习 3：自适应优化系统

**目标**：构建能从经验中学习的优化系统

```python

class AdaptiveLearningOptimizer:
    def __init__(self):
        # TODO: Initialize learning mechanisms
        self.optimization_history = []
        self.algorithm_performance = {}

    def optimize_with_learning(self, problem: Dict) -> Dict:
        # TODO: Select algorithm based on problem characteristics and history
        # TODO: Execute optimization and record results
        # TODO: Update learning models
        pass

    def learn_from_feedback(self, optimization_result: Dict,
                          user_satisfaction: float):
        # TODO: Incorporate user feedback into learning
        pass

# Test adaptive learning

adaptive_optimizer = AdaptiveLearningOptimizer()

```

---

## 总结与下一步

### 已掌握的关键概念

**Mathematical Optimization Framework**：

- 目标函数形式：`F* = arg max F(A, c₁, c₂, ..., c₆)`
- 约束处理与多目标优化
- 基于问题特征的算法选择

**Three Paradigm Integration**：

- **Prompts**：用于优化问题建模的策略模板
- **Programming**：用于系统化优化的计算算法
- **Protocols**：可学习“最优优化策略”的自适应系统

**Advanced Optimization Techniques**：

- 面向平滑问题的基于梯度优化
- 面向多目标优化的进化算法
- 面向高代价评估的贝叶斯优化
- 自适应算法选择与 meta-optimization

### 已获得的实践掌握

现在你可以：

1. 用数学框架为 context assembly **建立优化问题**
2. **实现优化算法** 并针对 context engineering 的特征做适配
3. 处理竞争质量维度之间的 **多目标权衡**
4. 构建能够学习最优优化策略的 **自适应系统**
5. 基于问题特征与约束 **选择合适的算法**

### 与课程后续的衔接

这套优化基础将支撑：

- **Information Theory**（Module 03）：最优信息选择与相关性最大化
- **Bayesian Inference**（Module 04）：不确定性下的概率优化
- **Advanced Applications**：真实系统中的系统化优化实践

你在此掌握的数学优化精度，为“寻找真正最优的 context assembly 策略”提供了计算层面的基础，从而不必依赖启发式规则或反复试错。

**下一模块**：[03_information_theory.md](03_information_theory.md) ——我们将学习如何量化并优化 context 组件中的信息含量、相关性与互信息。

---

## 快速参考：优化方法

|Problem Type|Best Algorithm|When to Use|Key Advantages|
|--------------|----------------|-------------|----------------|
|**Single Objective, Smooth**|Gradient Descent|Differentiable objectives|Fast convergence|
|**Multi-Objective**|Evolutionary/Pareto|Competing objectives|Finds trade-off solutions|
|**Expensive Evaluation**|Bayesian Optimization|Costly function calls|Sample efficient|
|**Constrained**|Lagrangian Methods|Hard constraints|Theoretical guarantees|
|**Unknown Problem Type**|Adaptive Selection|Unclear characteristics|Learns best approach|

这套优化能力将 context engineering 从“手工调参”推进为“系统化、数学化的优化工程”，并让系统能够自动发现更好的组装策略。
