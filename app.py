#!/usr/bin/env python3

import aws_cdk as cdk
from aws_cdk import Aspects, Tags
import jsii

from my_cdk_sample.my_cdk_sample_stack import MyCdkSampleStack


@jsii.implements(cdk.IAspect)
class ResourceTags:
    def visit(self, node):
        Tags.of(node).add("resource", node.path)


app = cdk.App()
stack = MyCdkSampleStack(app, "MyCdkSampleStack")
Tags.of(stack).add("service", "cdk_sample")
Aspects.of(stack).add(ResourceTags())
app.synth()
