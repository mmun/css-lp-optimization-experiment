from __future__ import print_function
from pyscipopt import Model
import sys
import pprint
pp = pprint.PrettyPrinter(indent=2)

# Constants
# =========
#
# n = number of decls = number of potential new rules
#
# d_ij = rule  i contains decl j
#
# cost(rule' i) = 5
# cost(decl i) = len(decl i's source)
#
# Variables
# =========
#
# D_ij    (Boolean) rule' i contains decl j
# X_i     (Boolean) rule' i contains at least one decl
# A_ij    (Boolean) rule' i is a subset of rule j
#
# Constraints
# ===========
#
# d_ij =  Max   A_ik D_kj
#        k=1..n
#
# X_i  =  Max   D_ij
#        j=1..n
#
# Objective
# =========
#
# Minimize:
#
#  Sum   cost(rule' i) * X_i   +    Sum   cost(decl j) * D_ij
# i=1..n                           i=1..n
#                                  j=1..n

rules = {
  ".button": [
    "background-color: #ed2651;",
    "border: 0;",
    "border-radius: 2px;",
    "box-sizing: border-box;",
    "color: white;",
    "height: 24px;",
    "line-height: 24px;",
    "overflow: hidden;",
    "padding: 0 16px;",
  ],

  ".button--size-small": [
    "height: 16px;",
    "line-height: 16px;",
    "padding: 0px 8px;",
  ],

  ".button--inverse": [
    "background-color: white;",
    "color: #2e184a;",
  ],

  ".button__icon--animate": [
    "animation: 3s ease-in 1s icon-animation;",
  ],

  ".button__icon": [
    "width: 16px;",
    "margin-right: 8px;",
    "overflow: hidden;",
    "height: 16px;",
  ],
}

###############
# Data Munging
###############

rule_string_lookup = []
decl_string_lookup = []
decl_to_rules = []

for rule_string, decl_strings in rules.iteritems():
  rule = len(rule_string_lookup)
  rule_string_lookup.append(rule_string)

  for decl_string in decl_strings:
    if decl_string in decl_string_lookup:
      decl = decl_string_lookup.index(decl_string)
      decl_to_rules[decl].append(rule)
    else:
      decl_string_lookup.append(decl_string)
      decl_to_rules.append([rule])

############
# Constants
############

m = len(rule_string_lookup)
n = len(decl_string_lookup)

d = [[0 for j in xrange(n)] for i in xrange(m)]

for decl, rules in enumerate(decl_to_rules):
  for rule in rules:
    d[rule][decl] = 1

def cost_rule(i):
  return 5

def cost_decl(i):
  return len(decl_string_lookup[i])

############
# Variables
############

model = Model("CSS Class Optimizer")

def bool_var(name):
  return model.addVar(name, vtype="B")

X = [bool_var("X[{0}]".format(i)) for i in xrange(n)]
D = [[bool_var("D[{0}][{1}]".format(i, j)) for j in xrange(n)] for i in xrange(n)]
A = [[bool_var("A[{0}][{1}]".format(i, j)) for j in xrange(n)] for i in xrange(m)]

##############
# Constraints
##############

for i in xrange(m):
  for j in xrange(n):
    cons = 0
    
    for k in xrange(n):
      cons += A[i][k] * D[k][j]

    model.addCons(d[i][j] == cons)

for i in xrange(n):
  for j in xrange(n):
    model.addCons(X[i] >= D[i][j])

############
# Objective
############

objective = 0

for i in xrange(n):
  objective += cost_rule(i) * X[i]

for i in xrange(n):
  for j in xrange(n):
    objective += cost_decl(j) * D[i][j]

####################
# Run the optimizer
####################

model.setObjective(objective)
model.optimize()

###############
# Print result
###############

print("")
print("")

def new_rule_name(rule):
  i = rule/26
  j = rule%26

  if i == 0:
    return "." + chr(97+j)
  else:
    return "." + chr(96+i) + chr(97+j)

new_rule_to_decls = {}

for i in xrange(n):
  if model.getVal(X[i]) == 1:
    decls = []

    for j in xrange(n):
      if model.getVal(D[i][j]) == 1:
        decls.append(j)

    new_rule_to_decls[i] = decls

for new_rule, decls in new_rule_to_decls.iteritems():
  print("{0} {{".format(new_rule_name(new_rule)))
  for decl in decls:
    print("  {0}".format(decl_string_lookup[decl]))
  print("}")

print("")
print("")

for i in xrange(m):
  new_rule_names = []

  for j in xrange(n):
    if model.getVal(A[i][j]) == 1:
      new_rule_names.append(new_rule_name(j))

  print("{0} = {1}".format(rule_string_lookup[i], ', '.join(new_rule_names)))

print("")
print("")
