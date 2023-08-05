# Bladed Next Gen Python Models API

`dnv_bladed_models=0.3.32`

A Python package to easily work with JSON input models for Bladed Next Generation.

Visit <https://bladednextgen.dnv.com/> for more information.

## Usage

Load a JSON model from file:

```python
import dnv_bladed_models as models

analysis = models.BladedAnalysis.from_file('/path/to/analysis.json')
```

Modify a model object in code:

```python
analysis.SteadyCalculation.TipSpeedRatioRange.Minimum = 4.
analysis.SteadyCalculation.TipSpeedRatioRange.Maximum = 10.
analysis.SteadyCalculation.TipSpeedRatioRange.Interval = 0.1
```

Work with a turbine assembly component in the Component Library, in code:

```python
blade: models.Blade = analysis.ComponentDefinitions['Blade']
```

Save a model to a JSON file:

```python
analysis.to_file('/path/to/file.json')
```

Create a new model object programmatically:

```python
beam = models.LidarBeam(
    MountingPosition=models.LidarMountingPosition(
        X=1,
        Y=2,
        Z=3
    )
)
```

Render a model as a JSON string:

```python
json_str = blade.to_json()
```

Load a model from a JSON string:

```python
blade = models.Blade.from_json(json_str)
```

