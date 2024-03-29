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
from mustBeLargerThanClusterToleranceRule import MustBeLargerThanClusterToleranceRule


class MustBeLargerThanClusterToleranceLineRuleFactory(AbstractTopologyRuleFactory):
  #NAME = "MustBeLargerThanClusterToleranceLine"
    
  def __init__(self):
    AbstractTopologyRuleFactory.__init__(
      self,
      "MustBeLargerThanClusterToleranceLine",
      "Must Be Larger Than Cluster Tolerance", 
      "Requires that a feature does not collapse during a validate process and applies to all line and polygon features. In other words, the vertices of each feature of these types of geometries must be spaced a distance greater than the tolerance established by the user in the topological plan rule. Vertices that fall within the tolerance are defined as coincident and are snnaped together. Thiss rule is mandatory for all topology.", 
      ListBuilder().add(Geometry.TYPES.LINE).add(Geometry.TYPES.MULTILINE).asList()
      )
  def createRule(self, plan, dataSet1, dataSet2, tolerance):
    #TopologyPlan plan, String dataSet1, String dataSet2, double tolerance
    rule = MustBeLargerThanClusterToleranceRule(plan, self, tolerance, dataSet1)
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