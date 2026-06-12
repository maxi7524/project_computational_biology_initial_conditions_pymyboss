

# MaBoSS Model Input/Output Specification

## 1. Network Topology Formulation (`.bnd`)

### 1.1 Structural Syntax
Continuous-time Markovian Boolean models are declared using two tightly coupled text assets: the structural network layout (`.bnd`) and the configuration parameters (`.cfg`). The structural layout defines the graph topology, specifying all node names, upstream activation/inhibition links, and mathematical transition rate formulas referred to as logic rules. Each regulatory node is declared using an explicit grammar block format:

```bnd
Node Node_Name {
    logic = Logic_Expression;
    rate_up = Rate_Equation;
    rate_down = Rate_Equation;
}
```

### 1.2 Node Attributes and Core Properties

- **`Node_Name`**: Unique alphanumeric identifier string (may contain underscores).
- **`logic`**: A Boolean logic rule determining the target state transition. It operates using standard Boolean operators: AND (`&`), OR (`|`), and NOT (`!`).
- **`rate_up`**: The transition rate formula describing the probability per unit time for a state change from $0 \rightarrow 1$.
- **`rate_down`**: The transition rate formula describing the probability per unit time for a state change from $1 \rightarrow 0$.

### 1.3 Mathematical Framework
The temporal dynamics follow a continuous-time Markov process governed by transition rates. For a given node $i$, the transition probabilities within an infinitesimal interval $dt$ are governed by:

$$\omega_i^{\text{up}}(\mathbf{X}) = \gamma_i \cdot f_i(\mathbf{X})$$
$$\omega_i^{\text{down}}(\mathbf{X}) = \delta_i \cdot g_i(\mathbf{X})$$

Where $\gamma_i$ and $\delta_i$ are baseline kinetic rate constants or global variables (prefixed with `$`), and $f_i, g_i$ evaluate to numbers based on the logical configuration.

---

## 2. Configuration Parameters System (`.cfg`)

### 2.1 Structural Grammar Elements

The configuration asset controls boundary parameters, probability vectors, node initial states ($P(\text{node}=1)$), simulation constraints, maximum transition bounds, and output tracking flags.

- **Global Variable Definitions**: Used to parameterize kinetic rates.
```cfg
$Variable_Name = Numeric_Value;
```
- **Initial Conditions Allocation**: Defines individual node initial state probabilities $P(X_i = 1)$.
```cfg
[Node_Name].istate = Probability_Value;
```
Where $\text{Probability\_Value} \in [0.0, 1.0]$.
- **Internal Flags Declaration**: Isolates output metrics by hiding intermediate steps.
```cfg
Node_Name.is_internal = Boolean_Value;
```
Where $\text{Boolean\_Value} \in \{\text{TRUE}, \text{FALSE}\}$.

### 2.2 Core Simulation Engine Settings

The simulation configuration requires the declaration of execution bounds:

| Parameter Token | Data Type | Physical Description |
| :--- | :--- | :--- |
| `sample_count` | `int` | Number of stochastic trajectories (Monte Carlo runs) to compute. |
| `max_time` | `float` | Maximum simulation time window upper bound for each trajectory ($T_{\text{maboss}}$). |
| `time_tick` | `float` | Discrete evaluation resolution for saving trajectory probability arrays. |
| `thread_count` | `int` | Number of concurrent POSIX threads allocated to execute independent trajectories. |

