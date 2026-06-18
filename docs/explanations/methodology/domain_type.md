
# Domain type

``` {contents} Local Contents
:depth: 2
:local:


```

## Problem Statement

The component is responsible for defining the spatial domain for the model. The simulation boundaries are determined based on Visium spatial data using a conversion factor between the number of pixels and the actual distance in micrometers ($ \mu m $).

---

## Foundations & Assumptions

### Biological Point of View

Within the designated physical space, the microenvironment computational grid steps are defined every $ 20,\mu m $ ($ \Delta x = \Delta y = \Delta z = 20,\mu m $), along with the initial coordinates of the cells. The grid step of $ 20,\mu m $ stems from mass transport constraints and the average cell size, and has been adopted based on the literature [Insert link to PhysiCell documentation].

* **Spatial/Temporal Scale Constraints**: Grid step $ \Delta x = 20,\mu m $.
* **Phenotypic Variation**: Cell positions reproduce the geometry of the input tissue.

### Mathematical Formulation

Let $ d_{px} $ denote the spot diameter in full-resolution pixels, extracted from `scalefactors['spot_diameter_fullres']`. Since the standard Visium spot diameter is $ 55.0,\mu m $, the pixel-to-micrometer conversion factor $ S_{px \to \mu m} $ is given by:

$$S_{px \to \mu m} = \frac{55.0}{d_{px}}$$

The physical coordinates $ x_i, y_i $ for each point $ i $ are directly computed as:

$$x_i = x_{i, px} \cdot S_{px \to \mu m}$$

$$y_i = y_{i, px} \cdot S_{px \to \mu m}$$

The boundaries of the computational domain $ \Omega $, accounting for a safety margin $ \delta $ (padding), are defined as follows:

$$x_{min} = \min_{i} (x_i) - \delta, \quad x_{max} = \max_{i} (x_i) + \delta$$

$$y_{min} = \min_{i} (y_i) - \delta, \quad y_{max} = \max_{i} (y_i) + \delta$$

$$z_{min} = -\frac{\Delta z}{2}, \quad z_{max} = \frac{\Delta z}{2}$$

---

## Implemented Strategies

### Strategy 1: Default Spatial Scaling Strategy

#### Idea

Automatic scaling of the domain based on a technological invariant (spot diameter), which makes the model independent of the input histological image resolution.

#### Detailed Algorithmic Implementation

1. **Configuration Read**: Retrieve the grid step values ($ \Delta x, \Delta y, \Delta z $) and the margin $ \delta $ from the `config` dictionary.
2. **Scale Computation**: Retrieve the `spot_diameter_fullres` value from the first available key in `mdata.mod['rna'].uns['spatial']` and determine $ S_{px \to \mu m} $.
3. **Scaling and Boundary Transformation**: Convert the extreme coordinates from `obsm['spatial']` to micrometers and add the margins $ \delta $.
4. **Metadata Persistence**: Save the computed factor and boundaries into the `domain_type_metadata_dict` dictionary inside `.uns` for subsequent reuse during cell positioning.
5. **Object Construction**: Generate and return an instance of the `DomainType` class.

