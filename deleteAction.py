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

class DeleteAction(AbstractTopologyRuleAction):

  def __init__(self):
    AbstractTopologyRuleAction.__init__(
      self,
      "MustBeLargerThanClusterTolerance", #MustBeLargerThanClusterToleranceRuleFactory.NAME,
      "DeleteAction",
      "Delete Action",
      ""#CAMBIAR
    )
  
  logger("1", LOGGER_INFO)
  def execute(self, rule, line, parameters):
    #TopologyRule rule, TopologyReportLine line, DynObject parameters
    try:

      dataSet = rule.getDataSet1()
      reference = line.getFeature1()
      feature = reference.getFeature()
      geometry = feature.getDefaultGeometry()
      multiPoint = geom.createGeometryFromWKT(line.getData())
      cloneGeometry = geometry.cloneGeometry()

      for i in range(0, multiPoint.getPrimitivesNumber()):
        point = multiPoint.getPrimitiveAt(i)
        for j in range(0, geometry.getNumVertices()):
          vertex = geometry.getVertex(j)
          if point == vertex:
            cloneGeometry.removeVertex(j)
          else:
            pass

      feature = feature.getEditable()
      feature.set("GEOMETRY", cloneGeometry)
      dataSet.update(feature)

    except:
      ex = sys.exc_info()[1]
      print "Error", ex.__class__.__name__, str(ex)
      #throw new ExecuteTopologyRuleActionException(ex);
      #raise ExecuteTopologyRuleActionException(ex)

def main(*args):

    c = DeleteAction()
    pass
