#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import print_function

header = """#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#"""

# Code generator for shared params (shared.py). Run under this folder with:
# python _shared_params_code_gen.py > shared.py


def _gen_param_header(name, doc, defaultValueStr):
    """
    Generates the header part for shared variables

    :param name: param name
    :param doc: param doc
    """
    template = '''class Has$Name(Params):
    """
    Mixin for param $name: $doc.
    """

    # a placeholder to make it appear in the generated doc
    $name = Param(Params._dummy(), "$name", "$doc")

    def __init__(self):
        super(Has$Name, self).__init__()
        #: param for $doc
        self.$name = Param(self, "$name", "$doc")'''
    if defaultValueStr is not None:
        template += '''
        self._setDefault($name=$defaultValueStr)'''

    Name = name[0].upper() + name[1:]
    return template \
        .replace("$name", name) \
        .replace("$Name", Name) \
        .replace("$doc", doc) \
        .replace("$defaultValueStr", str(defaultValueStr))


def _gen_param_code(name, doc, defaultValueStr):
    """
    Generates Python code for a shared param class.

    :param name: param name
    :param doc: param doc
    :param defaultValueStr: string representation of the default value
    :return: code string
    """
    # TODO: How to correctly inherit instance attributes?
    template = '''
    def set$Name(self, value):
        """
        Sets the value of :py:attr:`$name`.
        """
        self._paramMap[self.$name] = value
        return self

    def get$Name(self):
        """
        Gets the value of $name or its default value.
        """
        return self.getOrDefault(self.$name)'''

    Name = name[0].upper() + name[1:]
    return template \
        .replace("$name", name) \
        .replace("$Name", Name) \
        .replace("$doc", doc) \
        .replace("$defaultValueStr", str(defaultValueStr))

if __name__ == "__main__":
    print(header)
    print("\n# DO NOT MODIFY THIS FILE! It was generated by _shared_params_code_gen.py.\n")
    print("from pyspark.ml.param import Param, Params\n\n")
    shared = [
        ("maxIter", "max number of iterations (>= 0)", None),
        ("regParam", "regularization parameter (>= 0)", None),
        ("featuresCol", "features column name", "'features'"),
        ("labelCol", "label column name", "'label'"),
        ("predictionCol", "prediction column name", "'prediction'"),
        ("probabilityCol", "Column name for predicted class conditional probabilities. " +
         "Note: Not all models output well-calibrated probability estimates! These probabilities " +
         "should be treated as confidences, not precise probabilities.", "'probability'"),
        ("rawPredictionCol", "raw prediction (a.k.a. confidence) column name", "'rawPrediction'"),
        ("inputCol", "input column name", None),
        ("inputCols", "input column names", None),
        ("outputCol", "output column name", None),
        ("numFeatures", "number of features", None),
        ("checkpointInterval", "checkpoint interval (>= 1)", None),
        ("seed", "random seed", "hash(type(self).__name__)"),
        ("tol", "the convergence tolerance for iterative algorithms", None),
        ("stepSize", "Step size to be used for each iteration of optimization.", None)]
    code = []
    for name, doc, defaultValueStr in shared:
        param_code = _gen_param_header(name, doc, defaultValueStr)
        code.append(param_code + "\n" + _gen_param_code(name, doc, defaultValueStr))

    decisionTreeParams = [
        ("maxDepth", "Maximum depth of the tree. (>= 0) E.g., depth 0 means 1 leaf node; " +
         "depth 1 means 1 internal node + 2 leaf nodes."),
        ("maxBins", "Max number of bins for" +
         " discretizing continuous features.  Must be >=2 and >= number of categories for any" +
         " categorical feature."),
        ("minInstancesPerNode", "Minimum number of instances each child must have after split. " +
         "If a split causes the left or right child to have fewer than minInstancesPerNode, the " +
         "split will be discarded as invalid. Should be >= 1."),
        ("minInfoGain", "Minimum information gain for a split to be considered at a tree node."),
        ("maxMemoryInMB", "Maximum memory in MB allocated to histogram aggregation."),
        ("cacheNodeIds", "If false, the algorithm will pass trees to executors to match " +
         "instances with nodes. If true, the algorithm will cache node IDs for each instance. " +
         "Caching can speed up training of deeper trees.")]

    decisionTreeCode = '''class DecisionTreeParams(Params):
    """
    Mixin for Decision Tree parameters.
    """

    # a placeholder to make it appear in the generated doc
    $dummyPlaceHolders

    def __init__(self):
        super(DecisionTreeParams, self).__init__()
        $realParams'''
    dtParamMethods = ""
    dummyPlaceholders = ""
    realParams = ""
    paramTemplate = """$name = Param($owner, "$name", "$doc")"""
    for name, doc in decisionTreeParams:
        variable = paramTemplate.replace("$name", name).replace("$doc", doc)
        dummyPlaceholders += variable.replace("$owner", "Params._dummy()") + "\n    "
        realParams += "#: param for " + doc + "\n        "
        realParams += "self." + variable.replace("$owner", "self") + "\n        "
        dtParamMethods += _gen_param_code(name, doc, None) + "\n"
    code.append(decisionTreeCode.replace("$dummyPlaceHolders", dummyPlaceholders)
                .replace("$realParams", realParams) + dtParamMethods)
    print("\n\n\n".join(code))
