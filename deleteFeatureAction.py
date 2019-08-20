# encoding: utf-8

import gvsig
from gvsig import geom
from gvsig.geom import *
from org.gvsig.topology.lib.spi import AbstractTopologyRuleAction
import sys

from gvsig import logger
from gvsig import LOGGER_WARN,LOGGER_INFO,LOGGER_ERROR

#from addons.TopologyRuleMustBeLargerThanClusterTolerance.mustBeLargerThanClusterToleranceFactory import MustBeLargerThanClusterToleranceRuleFactory
#from mustBeLargerThanClusterToleranceFactory import MustBeLargerThanClusterToleranceRuleFactory
from org.gvsig.topology.lib.api import ExecuteTopologyRuleActionException

#from mustBeLargerThanClusterToleranceRuleFactory import MustBeLargerThanClusterToleranceRuleFactory

class DeleteFeatureAction(AbstractTopologyRuleAction):

  def __init__(self):
    AbstractTopologyRuleAction.__init__(
      self,
      "MustBeLargerThanClusterTolerance", #MustBeLargerThanClusterToleranceRuleFactory.NAME,
      "DeleteFeatureAction",
      "Delete Feature Action",
      "This action will remove polygon and line features whose points collapse during the validate process bassed on the topology's tolerance. This action can be applied to one or more Must Be Larger Than Cluster Tolerance errors."
    )
  
  logger("1", LOGGER_INFO)
  def execute(self, rule, line, parameters):
    #TopologyRule rule, TopologyReportLine line, DynObject parameters
    try:

      dataSet = rule.getDataSet1()
      dataSet.delete(line.getFeature1())

    except:
      ex = sys.exc_info()[1]
      print "Error", ex.__class__.__name__, str(ex)
      #throw new ExecuteTopologyRuleActionException(ex);
      #raise ExecuteTopologyRuleActionException(ex)

def main(*args):

    c = DeleteFeatureAction()
    pass