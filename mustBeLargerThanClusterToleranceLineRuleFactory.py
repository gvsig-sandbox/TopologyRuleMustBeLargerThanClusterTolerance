# encoding: utf-8

import gvsig
from gvsig import uselib

uselib.use_plugin("org.gvsig.topology.app.mainplugin")

from org.gvsig.fmap.geom import Geometry
from org.gvsig.tools.util import ListBuilder
from org.gvsig.topology.lib.api import TopologyLocator
from org.gvsig.topology.lib.api import TopologyManager
from org.gvsig.topology.lib.spi import AbstractTopologyRuleFactory
from org.gvsig.topology.lib.api import TopologyPlan
from org.gvsig.topology.lib.api import TopologyRule

from gvsig import logger
from gvsig import LOGGER_WARN,LOGGER_INFO,LOGGER_ERROR

from org.gvsig.topology.lib.api import TopologyLocator
from mustBeLargerThanClusterToleranceLineRule import MustBeLargerThanClusterToleranceLineRule


class MustBeLargerThanClusterToleranceLineRuleFactory(AbstractTopologyRuleFactory):
  #NAME = "MustBeLargerThanClusterToleranceLine"
    
  def __init__(self):
    AbstractTopologyRuleFactory.__init__(
      self,
      "MustBeLargerThanClusterToleranceLine",
      "Must Be Larger Than Cluster Tolerance", 
      "Requires that ...", 
      ListBuilder().add(Geometry.TYPES.LINE).add(Geometry.TYPES.MULTILINE).asList()
      )
  def createRule(self, plan, dataSet1, dataSet2, tolerance):
    #TopologyPlan plan, String dataSet1, String dataSet2, double tolerance
    rule = MustBeLargerThanClusterToleranceLineRule(plan, self, tolerance, dataSet1)
    return rule

def selfRegister():
    try:
      manager = TopologyLocator.getTopologyManager()
      manager.addRuleFactories(MustBeLargerThanClusterToleranceLineRuleFactory())
      print "added rule"
    except Exception as ex:
      logger("Can't register topology rule from MustBeLargerThanClusterToleranceLineRuleFactory."+str(ex), LOGGER_WARN)

def main(*args):
  print "* Executing MustBeLargerThanClusterToleranceLineRuleFactory main."
  selfRegister()
  pass