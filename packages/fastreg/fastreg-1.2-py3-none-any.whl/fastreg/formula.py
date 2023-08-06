##
## formula operations
##

import re
from functools import reduce
from operator import add

import numpy as np
import pandas as pd

from .meta import MetaFactor, MetaTerm, MetaFormula, MetaReal, MetaCateg, Drop, Column
from .tools import (
    categorize, hstack, chainer, decorator, func_disp, valid_rows, split_size,
    atleast_2d, fillna, all_valid, splice, factorize_2d, onehot_encode
)

##
## tools
##

def is_categorical(x, strict=False):
    agg = all if strict else any
    if isinstance(x, MetaFactor):
        return isinstance(x, MetaCateg)
    elif isinstance(x, MetaTerm):
        return agg([is_categorical(f) for f in x])
    elif isinstance(x, MetaFormula):
        return agg([is_categorical(t) for t in x])

def ensure_tuple(t):
    if type(t) is tuple:
        return t
    elif type(t) is list:
        return tuple(t)
    else:
        return t,

def robust_eval(data, expr, extern=None):
    # short circuit
    if expr is None:
        return None

    # extract values
    if type(expr) is str:
        vals = data.eval(expr, engine='python', local_dict=extern)
    elif callable(expr):
        vals = expr(data)
    else:
        vals = expr

    # ensure array
    if type(vals) is pd.Series:
        return vals.values
    elif type(vals) is np.ndarray:
        return vals
    else:
        return np.full(len(data), vals)

# this works with __add__ overload
def sum0(items):
    return reduce(add, items)

##
## categoricals
##

# make labels
def swizzle(ks, vs):
    return ','.join([f'{k}={v}' for k, v in zip(ks, vs)])

# ordinally encode interaction terms (tuple-like things)
# null data is returned with a -1 index if not dropna
def category_indices(vals, dropna=False, return_labels=False):
    # also accept single vectors
    vals = atleast_2d(vals)

    # track valid rows
    valid = valid_rows(vals)
    vals1 = vals[valid]

    # find unique rows
    uni_indx, uni_vals = factorize_2d(vals1)

    # patch in valid data
    if dropna or valid.all():
        uni_ind1 = uni_indx
    else:
        uni_ind1 = splice(valid, uni_indx, -1)

    # return requested
    if return_labels:
        return uni_ind1, uni_vals, valid
    else:
        return uni_ind1, valid

# splice out a category to -1 (in ordinal space)
def zero_category(vals, labs, lab0):
    try:
        idx0 = labs.index(lab0)
    except ValueError:
        raise Exception(f'drop label not found: {lab0}')

    # promote to zero index
    labs = labs.copy()
    labs = [labs.pop(idx0), *labs]

    # shift value indices
    vals = np.where(vals == idx0, -1, vals)
    vals = np.where(vals < idx0, vals+1, vals)

    return vals, labs

# encode categories as one-hot matrix or ordinals
def encode_categorical(vals, names, encoding='sparse', drop=Drop.FIRST):
    # reindex categoricals jointly
    cats_val, cats_lab, valid = category_indices(vals, return_labels=True)
    cats_lab = [swizzle(names, l) for l in cats_lab]

    # here 0 corresponds to dropped
    dtype = drop_type(drop)
    if dtype == Drop.VALUE:
        sdrop = swizzle(names, drop)
        cats_val, cats_lab = zero_category(cats_val, cats_lab, sdrop)
        drop_first = True
    else:
        drop_first = dtype == Drop.FIRST

    # handle drop first case (now -1 is dropped)
    if drop_first:
        cats_val -= 1
        cats_lab = cats_lab[1:]

    # implement final encoding
    if encoding == 'ordinal':
        cats_enc = cats_val
    elif encoding == 'sparse':
        cats_enc = onehot_encode(cats_val)

    return cats_enc, cats_lab, valid

# subset data allowing for missing chunks
def drop_invalid(valid, *mats, warn=False, name='data'):
    V, N = np.sum(valid), len(valid)
    if V == 0:
        raise Exception('all rows contain null data')
    elif V < N:
        if warn:
            print(f'dropping {N-V}/{N} null {name} rows')
        mats = [
            m[valid] if m is not None else None for m in mats
        ]
    return *mats,

def prune_sparse(labels, values, warn=True):
    # get active categories
    vcats = np.ravel((values!=0).sum(axis=0)) > 0
    P = np.sum(vcats)

    # get total categories
    Kt = [len(ls) for ls in labels.values()]
    K = sum(Kt)

    # bail if total
    if P == K:
        return labels, values
    if warn:
        print(f'pruning {K-P}/{K} unused categories')

    # split back into terms
    vcats = split_size(vcats, Kt)

    # modify data matrices
    values = values[:, vcats]
    labels = {
        t: [l for l, v in zip(ls, vs) if v]
        for (t, ls), vs in zip(labels.items(), vcats)
    }

    return labels, values

def prune_ordinal(labels, values, warn=True):
    # get active categories
    cvals, cinvs, cnums = zip(*[
        np.unique(cm, return_inverse=True, return_counts=True) for cm in values.T
    ])
    P = sum([len(cn) for cn in cnums])

    # get total categories
    Kt = [len(ls) for ls in labels.values()]
    K = sum(Kt)

    # bail if total
    if P >= K:
        return labels, values
    if warn:
        print(f'pruning {K-P}/{K} unused categories')

    # modify data matrices (tricky to exclude -1)
    values = np.vstack([ci+np.min(cv) for cv, ci in zip(cvals, cinvs)]).T
    labels = {
        t: [ls[v] for v in cv if v != -1]
        for (t, ls), cv in zip(labels.items(), cvals)
    }

    return labels, values

# remove unused categories (sparse `values` requires `labels`)
def prune_categories(labels, values, encoding='sparse', warn=True):
    if encoding == 'sparse':
        return prune_sparse(labels, values, warn=warn)
    elif encoding == 'ordinal':
        return prune_ordinal(labels, values, warn=warn)

def drop_type(d):
    return d if d in (Drop.FIRST, Drop.NONE) else Drop.VALUE

def drop_repr(d):
    t = drop_type(d)
    if t == Drop.VALUE:
        return ','.join([str(x) for x in d])
    else:
        _, s = str(t).split('.')
        return s

# aggregate drop values from list of Factors to Term
def consensus_drop(drops):
    if len(drops) == 0:
        return None
    udrop, *rdrop = set([drop_type(d) for d in drops])
    if len(rdrop) > 0:
        return Drop.FIRST
    elif udrop == Drop.VALUE:
        return tuple(drops)
    else:
        return udrop

##
## formula structure
##

class AccessorType(type):
    def __getattr__(cls, expr):
        return cls(expr)

class Factor(MetaFactor, metaclass=AccessorType):
    def __init__(self, expr, name=None):
        if type(expr) is str:
            self._expr = expr
            self._name = expr if name is None else name
        elif callable(expr):
            self._expr = expr
            self._name = name
        elif type(expr) is pd.Series:
            self._expr = expr.values
            self._name = expr.name
        else:
            self._expr = np.array(expr)
            self._name = name

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if isinstance(other, MetaFactor):
            return str(self) == str(other)
        else:
            return False

    def __repr__(self, **kwargs):
        return self._name

    def __add__(self, other):
        if isinstance(other, (MetaFactor, MetaTerm)):
            return Formula(self, other)
        elif isinstance(other, MetaFormula):
            return Formula(self, *other)
        else:
            raise TypeError(f'Not a valid addition: {other}')

    def __sub__(self, other):
        return Formula(self) - other

    def __mul__(self, other):
        if isinstance(other, MetaFactor):
            return Term(self, other)
        elif isinstance(other, MetaTerm):
            return Term(self, *other)
        elif isinstance(other, MetaFormula):
            return Formula(*[Term(self, *t) for t in other])
        else:
            raise TypeError(f'Not a valid multiplier: {other}')

    def __call__(self, *args, **kwargs):
        cls = type(self)
        return cls(self._expr, *args, **kwargs)

    def to_term(self, **kwargs):
        return Term(self, **kwargs)

    def name(self):
        return self._name

    def raw(self, data, extern=None):
        return robust_eval(data, self._expr, extern=extern)

    def eval(self, data, **kwargs):
        return self.to_term().eval(data, **kwargs)

class Term(MetaTerm):
    def __init__(self, *facts, drop=None):
        self._facts = facts
        if drop is None:
            if all(is_categorical(f) for f in facts):
                self._drop = consensus_drop([f._drop for f in facts])
            else:
                self._drop = Drop.NONE
        else:
            if drop_type(drop) == Drop.VALUE:
                self._drop = tuple(drop)
            else:
                self._drop = drop

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if isinstance(other, MetaTerm):
            return set(self) == set(other)
        elif isinstance(other, MetaFactor):
            return set(self) == {other}
        else:
            return False

    def __repr__(self):
        if len(self) == 0:
            return 'I'
        else:
            ds = f'|{drop_repr(self._drop)}' if self._drop != Drop.NONE else ''
            return '*'.join([f.__repr__(drop=False) for f in self]) + ds

    def __iter__(self):
        return iter(self._facts)

    def __len__(self):
        return len(self._facts)

    def __add__(self, other):
        if isinstance(other, (MetaFactor, MetaTerm)):
            return Formula(self, other)
        elif isinstance(other, MetaFormula):
            return Formula(self, *other)
        else:
            raise TypeError(f'Not a valid addition: {other}')

    def __sub__(self, other):
        return Formula(self) - other

    def __mul__(self, other):
        if isinstance(other, MetaFactor):
            return Term(*self, other)
        elif isinstance(other, MetaTerm):
            return Term(*self, *other)
        elif isinstance(other, MetaFormula):
            return Formula(*[Term(*self, *t) for t in other])
        else:
            raise TypeError(f'Not a valid multiplier: {other}')

    def name(self):
        return '*'.join([f.name() for f in self])

    def drop(self, *drop):
        if len(drop) == 1:
            drop0, = drop
            if drop_type(drop0) == Drop.VALUE:
                self._drop = drop
            else:
                self._drop = drop0
        else:
            self._drop = drop
        return self

    def raw(self, data, extern=None):
        return np.vstack([f.raw(data, extern=extern) for f in self]).T

    def eval(self, data, extern=None, encoding='sparse'):
        if encoding not in ('sparse', 'ordinal'):
            raise ValueError(f'Unknown encoding: {encoding}')

        # zero length is identity
        if len(self) == 0:
            N = len(data)
            return Column(
                'I', 'I', np.ones(N), np.ones(N, dtype=bool)
            )

        # separate pure real and categorical
        categ, reals = categorize(is_categorical, self)
        categ, reals = Term(*categ), Term(*reals)

        # error with mixed types + encoding='ordinal'
        if encoding == 'ordinal' and len(categ) > 0 and len(reals) > 0:
            raise ValueError('Cannot use encoding="ordinal" with mixed factor types')

        # handle categorical
        if len(categ) > 0:
            categ_raw = categ.raw(data, extern=extern)
            categ_nam = [c.name() for c in categ]
            categ_value, categ_label, categ_valid = encode_categorical(
                categ_raw, categ_nam, encoding=encoding, drop=self._drop
            )

        # handle reals
        if len(reals) > 0:
            reals_mat = reals.raw(data, extern=extern)
            reals_value = reals_mat.prod(axis=1)
            reals_label = reals.name()
            reals_valid = valid_rows(reals_value)

        # combine results
        name = self.name()
        if len(categ) == 0:
            return Column(name, reals_label, reals_value, reals_valid)
        elif len(reals) == 0:
            return Column(name, categ_label, categ_value, categ_valid)
        else:
            # filling nulls with 0 keeps sparse the same
            term_value = categ_value.multiply(fillna(reals_value, v=0)[:,None])
            term_label = [f'({l})*{reals_label}' for l in categ_label]
            term_valid = categ_valid & reals_valid
            return Column(name, term_label, term_value, term_valid)

class Formula(MetaFormula):
    def __init__(self, *terms):
        # order preserving unique
        self._terms = tuple(dict.fromkeys(
            t if isinstance(t, MetaTerm) else Term(t) for t in terms
        ))

    def __eq__(self, other):
        self_set = {frozenset(t) for t in self}
        if isinstance(other, MetaFormula):
            return self_set == {frozenset(t) for t in other}
        if isinstance(other, MetaTerm):
            return self_set == {frozenset(other)}
        elif isinstance(other, MetaFactor):
            return self_set == {frozenset({other})}
        else:
            return False

    def __repr__(self):
        if len(self) == 0:
            return 'O'
        else:
            return ' + '.join(str(t) for t in self)

    def __iter__(self):
        return iter(self._terms)

    def __len__(self):
        return len(self._terms)

    def __add__(self, other):
        if isinstance(other, (MetaFactor, MetaTerm)):
            return Formula(*self, other)
        elif isinstance(other, MetaFormula):
            return Formula(*self, *other)
        else:
            raise TypeError(f'Not a valid addition: {other}')

    def __sub__(self, other):
        if isinstance(other, MetaFactor):
            other = Term(other)
        if isinstance(other, MetaTerm):
            return Formula(*[
                t for t in self if t != other
            ])
        if isinstance(other, MetaFormula):
            return Formula(*[
                t for t in self if t not in other
            ])
        else:
            raise TypeError(f'Not a valid subtraction: {other}')

    def __mul__(self, other):
        if isinstance(other, MetaFactor):
            return Formula(*[Term(*t, other) for t in self])
        elif isinstance(other, MetaTerm):
            return Formula(*[Term(*t, *other) for t in self])
        elif isinstance(other, MetaFormula):
            return Formula(*chainer([
                [Term(*t1, *t2) for t1 in self] for t2 in other
            ]))
        else:
            raise TypeError(f'Not a valid multiplier: {other}')

    def raw(self, data, extern=None):
        return [t.raw(data, extern=extern) for t in self]

    def eval(self, data, extern=None, encoding='sparse', group=True, flatten=False):
        if encoding not in ('sparse', 'ordinal'):
            raise ValueError(f'Unknown encoding: {encoding}')

        # zero length is zero
        if len(self) == 0:
            N = len(data)
            labels, values, valid = 'O', np.zeros(N), np.ones(N, dtype=bool)
            if flatten:
                return labels, values, valid
            else:
                return (labels, None), (values, None), valid

        # get all term specs (type, labels, values, valid)
        columns = [t.eval(data, extern=extern, encoding=encoding) for t in self]
        valid = all_valid(*[c.valid for c in columns])

        # just return raw specs
        if not group and not flatten:
            specs = [(c.name, c.labels, c.values) for c in columns]
            return specs, valid

        # group by real/categorical
        if group or flatten:
            # combine labels and default values
            categ, reals = categorize(lambda c: type(c.labels) is list, columns)
            reals_label = [c.labels for c in reals]
            categ_label = {c.name: c.labels for c in categ}
            reals_value, categ_value = None, None

            # handle real terms
            if len(reals) > 0:
                reals_value = hstack([c.values[:,None] for c in reals])

            # handle categorical terms
            if len(categ) > 0:
                if encoding == 'ordinal':
                    categ_value = hstack([c.values[:,None] for c in categ])
                elif encoding == 'sparse':
                    categ_value = hstack([c.values for c in categ])

        # do a full flatten?
        if flatten:
            labels = reals_label + chainer(categ_label.values())
            values = hstack([reals_value, categ_value])
        else:
            labels = reals_label, categ_label
            values = reals_value, categ_value

        return labels, values, valid

##
## column types
##

class Real(MetaReal, Factor):
    def __repr__(self, **kwargs):
        return f'R({self.name()})'

class Categ(MetaCateg, Factor):
    def __init__(self, expr, drop=Drop.FIRST, **kwargs):
        super().__init__(expr, **kwargs)
        self._drop = drop

    def __repr__(self, drop=True, **kwargs):
        nm = self.name()
        if drop and self._drop != Drop.NONE:
            ds = drop_repr(self._drop)
            return f'C({nm}|{ds})'
        else:
            return f'C({nm})'

    def drop(self, drop):
        self._drop = drop
        return self

# custom columns — class interface
# raw (mandatory): an ndarray of the values
# name (recommended): what gets displayed in the regression table
# __repr__ (optional): what gets displayed on print [default to C/R(name)]

class Demean(Real):
    def __init__(self, expr, cond=None, name=None):
        args = '' if cond is None else f'|{cond}'
        name = expr if name is None else name
        super().__init__(expr, name=f'{name}-μ{args}')
        self._cond = cond

    def raw(self, data, extern=None):
        vals = super().raw(data, extern=extern)
        if self._cond is None:
            means = np.mean(vals)
        else:
            cond = robust_eval(data, self._cond, extern=extern)
            datf = pd.DataFrame({'vals': vals, 'cond': cond})
            cmean = datf.groupby('cond')['vals'].mean().rename('mean')
            datf = datf.join(cmean, on='cond')
            means = datf['mean'].values
        return vals - means

class Binned(Categ):
    def __init__(self, expr, bins=10, drop=Drop.FIRST, labels=False, name=None):
        nb = bins if type(bins) is int else len(bins)
        name = expr if name is None else name
        super().__init__(expr, drop=drop, name=f'{name}:bin{nb}')
        self._bins = bins
        self._labels = None if labels else False

    def raw(self, data, extern=None):
        vals = super().raw(data, extern=extern)
        bins = pd.cut(vals, self._bins, labels=self._labels)
        return bins

# shorthand for drop=NONE

class Categ0(Categ):
    def __init__(self, expr, *args, drop=None, **kwargs):
        super().__init__(expr, *args, drop=Drop.NONE, **kwargs)

class Binned0(Binned):
    def __init__(self, expr, *args, drop=None, **kwargs):
        super().__init__(expr, *args, drop=Drop.NONE, **kwargs)

# custom columns — functional interface

class Custom:
    def __init__(
        self, func, name=None, categ=False, base=Real, eval_args=0, frame=False
    ):
        self._base = Categ if categ else base
        self._func = func
        self._name = name if callable(name) else func_disp(func, name=name)
        self._eval = ensure_tuple(eval_args)
        self._frame = frame

    def __getattr__(self, key):
        if key.startswith('_'):
            return super().__getattr__(key)
        else:
            return self(key)

    def __call__(self, *args, **kwargs):
        if self._frame:
            evaler = lambda data: self._func(data, *args, **kwargs)
        else:
            def evaler(data):
                args1 = [
                    robust_eval(data, e) if i in self._eval else e
                    for i, e in enumerate(args)
                ]
                return self._func(*args1, **kwargs)
        name = self._name(*args, **kwargs)
        return self._base(evaler, name=name)

@decorator
def factor(func, *args, **kwargs):
    return Custom(func, *args, **kwargs)

# shortcuts
O = Formula()
I = Term()
R = Real
C = Categ
D = Demean
B = Binned
C0 = Categ0
B0 = Binned0

##
## conversion
##

# lookup table
FTYPES = {
    'C': Categ,
    'I': Real,
}

def parse_factor(fact):
    ret = re.match(r'(C|I)\(([^\)]+)\)', fact.code)
    if ret is not None:
        pre, name = ret.groups()
        return FTYPES[pre](name)
    else:
        return Real(fact.code)

def parse_term(term):
    return Term(*[parse_factor(f) for f in term.factors])

# this can only handle treatment coding, but that's required for sparsity
def parse_formula(form):
    from patsy.desc import ModelDesc

    # use patsy for formula parse
    desc = ModelDesc.from_formula(form)
    lhs, rhs = desc.lhs_termlist, desc.rhs_termlist

    # check for invalid y
    if len(lhs) > 1:
        raise Exception('Must have single factor y term')

    # convert to string lists
    y_terms = parse_factor(lhs[0].factors[0]) if len(lhs) > 0 else None
    x_terms = Formula(*[parse_term(t) for t in rhs])

    return y_terms, x_terms

def parse_item(i, convert=Real):
    if isinstance(i, MetaFactor):
        return i
    else:
        return convert(i)

def parse_tuple(t, convert=Real):
    if isinstance(t, MetaTerm):
        return t
    else:
        if type(t) not in (tuple, list):
            t = t,
        return Term(*[
            parse_item(i, convert=convert) for i in t
        ])

def parse_list(l, convert=Real):
    if isinstance(l, MetaFormula):
        return l
    else:
        if type(l) not in (tuple, list):
            l = l,
        return Formula(*[
            parse_tuple(t, convert=convert) for t in l
        ])

##
## design interface
##

def ensure_formula(y=None, x=None, formula=None):
    if formula is not None:
        y, x = parse_formula(formula)
    else:
        if isinstance(y, (MetaTerm, MetaFormula)):
            raise Exception(f'LHS variable must be a single factor. Instead got: y = {y}')
        else:
            y = parse_item(y) if y is not None else None
        x = parse_list(x)
    return y, x

def design_matrix(
    x=None, formula=None, data=None, encoding='sparse', dropna=True, prune=True,
    warn=True, extern=None, valid0=None, flatten=True, validate=False
):
    _, x = ensure_formula(x=x, formula=formula)

    # evaluate x variables
    (x_lab, c_lab), (x_vec, c_vec), val = x.eval(
        data, extern=extern, encoding=encoding, group=True
    )

    # aggregate valid info for data
    valid = all_valid(valid0, val)

    # drop null values if requested
    if dropna:
        x_vec, c_vec = drop_invalid(valid, x_vec, c_vec, warn=warn, name='x')

    # prune empty categories if requested
    if prune and c_vec is not None:
        c_lab, c_vec = prune_categories(c_lab, c_vec, encoding=encoding, warn=warn)

    # combine real and categorical?
    if flatten:
        lab = x_lab + chainer(c_lab.values())
        vec = hstack([x_vec, c_vec])
        ret = lab, vec
    else:
        ret = (x_lab, c_lab), (x_vec, c_vec)

    # return valid mask?
    if validate:
        return *ret, valid
    else:
        return ret

def design_matrices(
    y=None, x=None, formula=None, data=None, dropna=True, extern=None,
    valid0=None, validate=False, warn=True, **kwargs
):
    # parse into pythonic formula system
    y, x = ensure_formula(x=x, y=y, formula=formula)
    if y is None:
        raise Exception('Use design_matrix for formulas without an LHS')

    # get y data
    y_vec = y.raw(data, extern=extern)
    y_lab = y.name()
    y_val = valid_rows(y_vec)

    # get valid x data
    x_val0 = all_valid(valid0, y_val)
    x_lab, x_vec, valid = design_matrix(
        x=x, data=data, dropna=dropna, extern=extern, valid0=x_val0, warn=False,
        validate=True, **kwargs
    )

    # drop invalid y
    if dropna:
        y_vec, = drop_invalid(valid, y_vec, warn=warn, name='y')

    # return combined data
    ret = y_lab, y_vec, x_lab, x_vec
    if validate:
        return *ret, valid
    else:
        return ret
