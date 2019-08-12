# encoding: utf-8

import gvsig
from gvsig import geom
from gvsig.geom import *
from org.gvsig.fmap.geom import GeometryLocator
from org.gvsig.fmap.geom import GeometryManager
from org.gvsig.topology.lib.spi import AbstractTopologyRuleAction
import sys

from gvsig import logger
from gvsig import LOGGER_WARN,LOGGER_INFO,LOGGER_ERROR

#from addons.TopologyRuleMustBeLargerThanClusterTolerance.mustBeLargerThanClusterToleranceFactory import MustBeLargerThanClusterToleranceRuleFactory
#from mustBeLargerThanClusterToleranceFactory import MustBeLargerThanClusterToleranceRuleFactory
from org.gvsig.topology.lib.api import ExecuteTopologyRuleActionException

#from mustBeLargerThanClusterToleranceRuleFactory import MustBeLargerThanClusterToleranceRuleFactory

class DeletePointsAction(AbstractTopologyRuleAction):

  def __init__(self):
    AbstractTopologyRuleAction.__init__(
      self,
      "MustBeLargerThanClusterTolerance", #MustBeLargerThanClusterToleranceRuleFactory.NAME,
      "DeletePointsAction",
      "Delete Points Action",
      ""#CAMBIAR
    )
  
  logger("1", LOGGER_INFO)
  def execute(self, rule, line, parameters):
    #TopologyRule rule, TopologyReportLine line, DynObject parameters
    try:

      dataSet = rule.getDataSet1()
      reference = line.getFeature1()
      feature = reference.getFeature()
      lineToFix = feature.getDefaultGeometry()
      tolerance = float(line.getData())
      #multiPoint = geom.createGeometryFromWKT(line.getData())
      #cloneGeometry = lineToFix.cloneGeometry()
      geoManager = GeometryLocator.getGeometryManager()
      subtype = lineToFix.getGeometryType().getSubType()
      fixedLine = geoManager.createLine(subtype)

      for i in range(0, lineToFix.getNumVertices()):
        vertex1 = lineToFix.getVertex(i)
        point = createPoint(D2, vertex1.getX(), vertex1.getY())
        if tolerance != 0:
          vertex1Tolerance = point.buffer(tolerance)
        else:
          vertex1Tolerance = point
        for j in range(0, lineToFix.getNumVertices()):
          vertex2 = lineToFix.getVertex(j)
          otherPoint = createPoint(D2, vertex2.getX(), vertex2.getY())
          if i==j:
            print "i, j", i, j
            continue
          else:
            print "i, j", i, j
            if not vertex1Tolerance.intersects(otherPoint):
              print "The distance is larger than the tolerance"
              if fixedLine.getNumVertices()==0:
                fixedLine.addVertex(lineToFix.getVertex(i))
              else:
                print "The fixedLine vertices number is different from 0"
              content = False
              for k in range(0, fixedLine.getNumVertices()):
                vertex = fixedLine.getVertex(k)
                if vertex2 == vertex:
                  content = True
                  print "Content is True"
                else:
                  print "Content is False"
              if content == False:
                print "if content == False"
                if j != lineToFix.getNumVertices()-1 and j>i:
                  fixedLine.addVertex(lineToFix.getVertex(j))
                  break
                else:
                  print "vertex not added"
              else:
                if j<i:
                  print "The vertex is already contained in the fixedLine"
                else:
                 break
            else:
              print "The distance is less than the tolerance"

      feature = feature.getEditable()
      feature.set("GEOMETRY", fixedLine)
      dataSet.update(feature)

    except:
      ex = sys.exc_info()[1]
      print "Error", ex.__class__.__name__, str(ex)
      #throw new ExecuteTopologyRuleActionException(ex);
      #raise ExecuteTopologyRuleActionException(ex)

def main(*args):

    c = DeletePointsAction()
    pass
