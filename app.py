#!/usr/bin/env python3
import os

import aws_cdk as cdk

from my_cdk_sample.my_cdk_sample_stack import MyCdkSampleStack


app = cdk.App()
stack = MyCdkSampleStack(app, "MyCdkSampleStack")
Tags.of(stack).add("service", "cdk_sample")
app.synth()
