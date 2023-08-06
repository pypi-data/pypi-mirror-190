<br />

<div align="center">
<img src="https://raw.githubusercontent.com/iamlemec/fastreg/master/content/fastreg_path.svg" alt="fastreg logo"></img>
</div>

<br />

Fast sparse regressions with advanced formula syntax. Good for high-dimensional fixed effects. Installation and usage are described below. Detailed documentation can be found [further down](#documentation).

**New**: generalized linear models and maximum likelihood estimation with JAX.

### Install


To install from PyPI with pip:
``` bash
pip install fastreg
```

To install directly from GitHub:

``` bash
pip install git+https://github.com/iamlemec/fastreg
```

Alternatively, you can clone this repository locally and run

``` bash
pip install -e .
```

Optionally, for the maximum likelihood routines, you'll need `jax` (and `jaxlib`) as well. See [here](https://github.com/google/jax) for detailed instructions.

### Usage

First import the necessary functions

``` python
import fastreg as fr
from fastreg import I, R, C
```

Create some testing data

``` python
data = fr.dataset(N=100_000, K1=10, K2=100, models=['linear', 'poisson'])
```

|     |     y0 |     y |     x1 |     x2 | id1   |   id2 |
|----:|-------:|------:|-------:|-------:|:------|------:|
|   0 |  0.140 | 3.450 | -0.260 |  0.958 | E     |    37 |
|   1 | -0.552 | 0.955 |  0.334 | -1.046 | I     |    65 |
|   2 | -0.683 | 1.517 |  0.067 | -0.631 | I     |    10 |
| ... |        |       |        |        |       |       |

We can construct formulas to define our specification. To make a real `Factor` on `x1`, use `R('x1')` or more conveniently `R.x1`. These can then be combined into `Term`s with `*` and then into `Formula`s with `+`. Regress `y0` on `1`, `x1`, and `x2` given `pandas` DataFrame `data`:

``` python
fr.ols(y=R.y0, x=I+R.x1+R.x2, data=data)
```

|    |   coeff |   stderr |   low95 |   high95 |   pvalue |
|:---|--------:|---------:|--------:|---------:|---------:|
| I  |   0.099 |    0.003 |   0.093 |    0.105 |    0.000 |
| x1 |   0.304 |    0.003 |   0.297 |    0.310 |    0.000 |
| x2 |   0.603 |    0.003 |   0.597 |    0.609 |    0.000 |

Regress `y` on `1`, `x1`, `x2`, categorical `id1`, and categorical `id2`:

``` python
fr.ols(y=R.y, x=I+R.x1+R.x2+C.id1+C.id2, data=data)
```

|       |   coeff |   stderr |   low95 |   high95 |   pvalue |
|:------|--------:|---------:|--------:|---------:|---------:|
| I     |   0.153 |    0.033 |   0.088 |    0.218 |    0.000 |
| x1    |   0.295 |    0.003 |   0.289 |    0.302 |    0.000 |
| x2    |   0.594 |    0.003 |   0.588 |    0.600 |    0.000 |
| id1=B |   0.072 |    0.014 |   0.044 |    0.099 |    0.000 |
| id1=C |   0.168 |    0.014 |   0.140 |    0.195 |    0.000 |
| ...   |         |          |         |          |          |

Regress `y` on `1`, `x1`, `x2`, and all combinations of categoricals `id1` and `id2` (Note that `*` is analogous to `:` in R-style syntax):

``` python
fr.ols(y=R.y, x=I+R.x1+R.x2+C.id1*C.id2, data=data)
```

|             |   coeff |   stderr |   low95 |   high95 |   pvalue |
|:------------|--------:|---------:|--------:|---------:|---------:|
| I           |   0.158 |    0.107 |  -0.051 |    0.368 |    0.138 |
| x1          |   0.295 |    0.003 |   0.289 |    0.301 |    0.000 |
| x2          |   0.593 |    0.003 |   0.587 |    0.599 |    0.000 |
| id1=A,id2=1 |  -0.068 |    0.144 |  -0.350 |    0.213 |    0.634 |
| id1=A,id2=2 |   0.060 |    0.155 |  -0.244 |    0.363 |    0.700 |
| ...         |         |          |         |          |          |

Instead of passing `y` and `x`, you can also pass an R-style formula string to `formula`, as in:

``` python
fr.ols(formula='y ~ 1 + x1 + x2 + C(id1):C(id2)', data=data)
```

There's even a third intermediate option using lists and tuples, which might be more useful when you are defining specifications programmatically:

``` python
fr.ols(y=R.y, x=[I, R.x1, R.x2, (C.id1, C.id2)], data=data)
```

Right now, categorical coding schemes other than treatment are not supported. You can pass a list of column names to `cluster` to cluster standard errors on those variables.

### Categorical coding

For categorical variables, one must avoid collinearity by either not including an intercept term or by dropping one value. The default for categorical variables is to drop the first value in alphabetical/numerical order. You can specify which value to drop by passing that as an argument to the specified variable. For instance, if one wanted to drop `B` from the factor `id1`, they would write `C.id1('B')` or equivalently `C('id1', 'B')`, or more verbosely `C('id1', drop='B')`. You can also tell it to not drop any values by passing `fr.NONE` and explicitly tell it to drop the first value with `fr.FIRST`.

In the case of interacted categorical variables, you would typically specify the dropped value for each factor and this will be inherited to the term level. For instance, if one wished to drop `id1 = B` and `id2 = 3` from the interaction of these two terms, they would write `C.id1('B')*C.id2(3)`. An alternative method would be to write `(C.id1*C.id2).drop('B', 3)`. When creating compound categorical terms, an attempt is made to find the correct drop strategy. In the case of ambiguity or when no information is given, the default is again `FIRST`. When interacting categorical and real variables, the default is `NONE`, as this source of collinearity is no longer an issue.

### High dimensional

Point estimates are obtained efficiently by using a sparse array representation of categorical variables. However, computing standard errors can be costly due to the need for large, dense matrix inversion. It is possible to make clever use of block diagonal properties to quickly compute standard errors for the case of a single (possibly interacted) categorical variable. In this case, we can recover the individual standard errors, but not the full covariance matrix. To employ this, pass a single `Term` (such as `C.id1` or `C.id1*C.id2`) with the `hdfe` flag, as in

``` python
fr.ols(y='y', x=I+R.x1+R.x2+C.id1, hdfe=C.id2, data=data)
```

You can also pass a term to the `absorb` flag to absorb those variables a la Stata's `areg`. In this case you do not recover the standard errors for the absorbed categorical, though it may be faster in the case of multiple high-dimensional regressors. This will automatically cluster standard errors on that term as well, as the errors will in fact be correlated, even if the original data was iid.

### Generalized linear models

We can do GLM now too! The syntax and usage is identical to that of `ols`. For instance, to run a properly specified Poisson regression using our test data:

``` python
fr.poisson(y=R.p, x=I+R.x1+R.x2+C.id1+C.id2, data=data)
```

|       |   coeff |   stderr |   low95 |   high95 |   pvalue |
|:------|--------:|---------:|--------:|---------:|---------:|
| I     |   0.322 |    0.011 |   0.300 |    0.344 |    0.000 |
| x1    |   0.294 |    0.001 |   0.293 |    0.296 |    0.000 |
| x2    |   0.597 |    0.001 |   0.596 |    0.599 |    0.000 |
| id1=B |   0.072 |    0.005 |   0.062 |    0.081 |    0.000 |
| id1=C |   0.178 |    0.005 |   0.169 |    0.187 |    0.000 |
| ...   |         |          |         |          |          |

You can use the `hdfe` flag here as well, for instance:

``` python
fr.poisson(y=R.p, x=I+R.x1+R.x2+C.id1, hdfe=C.id2, data=data)
```

Under the hood, this is all powered by a maximum likelihood estimation routine in `general.py` called `maxlike_panel`. Just give this a function that computes the mean log likelihood and it'll take care of the rest, computing standard errors from the inverse of the Fisher information matrix. This is then specialized into a generalized linear model routine called `glm`, which accepts a loss function along with data. I've provided implementations for `logit`, `poisson`, `negbin`, `zinf_poisson`, `zinf_negbin`, and `gols`.

### Custom factors

The algebraic system used to define specifications is highly customizable. First, there are the core factors `I` (identity), `R` (real), and `C` (categorical). Then there are the provided factors `D` (demean) and `B` (binned). You can also create your own custom column types. The simplest way is using the `factor` function decorator. For instance, we might want to standardize variables:

``` python
@fr.factor
def Z(x):
    return (x-np.mean(x))/np.std(x)
```

The we can using this in a regression with either `Z('x1')` or `Z.x1`, as in:

``` python
fr.ols(y=R.y0, x=I+Z.x1+Z.x2, data=data)
```

We may also want factors that use data from multiple columns. In this case we need to use `eval_args` to tell it what expressions to map, as it defaults to only the first argument (`0`). For example, to implement conditional demean (which is also included by default as `fr.D`), we would do:

``` python
@fr.factor(eval_args=(0, 1))
def CD(x, i):
    datf = pd.DataFrame({'vals': x, 'cond': i})
    cmean = datf.groupby('cond')['vals'].mean().rename('mean')
    datf = datf.join(cmean, on='cond')
    return datf['vals'] - datf['mean']
```
and then use it in a regression, though we can't use the convenience syntax with multiple arguments

``` python
fr.ols(y=R.y0, x=I+CD('x1','id1')+CD('x2','id2'), data=data)
```

The `factor` decorator also accepts a `categ` flag that you can set to `True` for categorical variables. Finally, it may be useful to inject functions into the evaluation namespace rather than create a whole new factor type. To do this, you can pass a `dict` to the `extern` flag and prefix the desired variable or function with `@`, as in:

``` python
extern = {'logit': lambda x: 1/(1+np.exp(-x))}
fr.ols(y='y0', x=I+R('@logit(x1)')+R.x2, data=data, extern=extern)
```

### Documentation

The core functionality of this library lies in creating well-structured data matrices (often called "design matrices") from actual data in the for of Pandas DataFrames and a regression specification, either Fastreg-style or R-style. For that, we have the following function defined in `formula.py`. You must always pass `data` as well as either `y`/`x` or `formula`.

```python
fastreg.design_matrices(
    y=None, x=None, formula=None, data=None, dropna=True, prune=True, validate=False,
    flatten=True, extern=None, warn=True
)
```
- **y**: specification for the outcome variable, a column name (`str`) or a single `Term`, which might be the combination of multiple `Factor`s
- **x**: specification for the input variables, a `Formula` or `list` of `Term`s
- **formula**: an R-style specification string, this will override any `y` or `x` given above
- **data**: a DataFrame with the underlying dataset
- **dropna**: drop any rows containing null data
- **prune**: prune categories that have no instances
- **validate**: return binary mask specifying which rows were dropped
- **flatten**: combine dense and sparse `x` variables into one matrix
- **extern**: a dictionary of functions for use in specification
- **warn**: output info on dropped rows or categories

This returns (data, name) pairs for both `y` and `x` variables. In addition, if you only want to deal with the `x` variables, you can use `design_matrix`, which has nearly identical syntax but does not accept the `y` argument. Next is the `ols` function defined in `linear.py` that handles regressions.

```python
fastreg.ols(
    y=None, x=None, formula=None, data=None, cluster=None, absorb=None, hdfe=None,
    stderr=True, output='table'
)
```
- **y**: specification for the outcome variable, a column name (`str`) or a single `Term`, which might be the combination of multiple `Factor`s
- **x**: specification for the input variables, a `Formula` or `list` of `Term`s
- **formula**: an R-style specification string, this will override any `y` or `x` given above
- **data**: a DataFrame with the underlying dataset
- **cluster**: cluster standard errors on the given `Term`
- **absorb**: regress on differences within groups specified by given `Term`
- **hdfe**: use block inversion to speed up standard error calculation for given `Term`
- **stderr**: standard error type, `True` for basic, and `hc0`-`hc3` for robust types
- **output**: control output, `table` gives DataFrame of estimates, `dict` gives much more info

Other estimators use syntax very similar to that of `ols`. This includes `glm` in `general.py`, which also accepts custom a `loss` functions. For instance, the built-in `poisson` uses a Poisson likelihood loss function (with an exponential link). Below only the arguments not common to `ols` are listed.

```python
fastreg.glm(
    y=None, x=None, formula=None, data=None, hdfe=None, loss=None, model=None,
    extra={}, raw={}, offset=None, epochs=None, display=True, per=None, stderr=True,
    output='table'
)
```
- **loss**: the loss (log likelihood) function to use for optimization, can be one of `'logit'`, `'poisson'`, `'negbin'`, `'normal'`, `'lognorm'`, `'lstsq'`, or a custom function that accepts `(params, data, yhat, y)`
- **model**: in lieu of a loss function, one can specify a model function mapping from `(params, data)` to an average log likelihood
- **extra**: a `dict` of extra parameter names mapping to initial values that can be accessed by the `loss` function
- **raw**: a `dict` of extra `Term` specifications that are evaluated and passed to the `loss` function as part of `data`
- **offset**: a `Term` to evaluate and add to the linear predictor (for instance, `R('log(t)')`)
- **epochs**: how many full iterations over the dataset to do during optimization
- **display**: whether to display updates on objective and parameter values during optimization
- **per**: how often to display updates during optimization
